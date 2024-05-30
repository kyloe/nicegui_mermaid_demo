from shapes import Shape, Arrow
from typing_extensions import Self
from nicegui import app, ui
from context import Context, get_task_id
import logging
log = logging.getLogger(__name__)

class Child():
    '''
    Top level abstract class to hold common functionality
    '''
    def __init__(self):
        pass

    def get_shim(self,target,**kwargs):
        sub_class_name = f"{Context.get_current_type().capitalize()}{target}"
        # Dynamically build sub class ref to avoid pages of if/elif 
        module = __import__(__name__)
        sub_class = getattr(module,sub_class_name)
        s = sub_class(**self._kwargs)
        Diagram._add_child(s)
        if 'on_click' in self._kwargs:
            Diagram._add_click(self._kwargs['identifier'],self._kwargs['on_click'])
        return s

    @classmethod
    def get_template(cls,template_name):
        return cls.templates[template_name]

class Node(Child):
    ''' 
    A box containing information on the diagram
    '''
    
    def __init__(self,**kwargs):
        super().__init__()
        self._kwargs = kwargs
        self._shim = self.get_shim(self.__class__.__name__,**self._kwargs)

    def __str__(self):
        return self._shim.__str__()

class Edge(Child):
    '''
    A line joining two nodes
    '''
    def __init__(self,**kwargs):
        super().__init__()
        self._kwargs = kwargs
        self._shim = self.get_shim(self.__class__.__name__,**self._kwargs)

    def __str__(self):
        return self._shim.__str__()


class FlowchartNode(Node):
    '''
    Node functions tailored for the 'flowchart' mermaid diagram type
    '''
    templates = {
        'node':"\t{identifier}{shape_opener}{text}{shape_closer}\n",
        'click':"click {identifier} call _mermaidClickHandler()\n"
        }

    def __init__(self,**kwargs):
        self._kwargs = kwargs
        # Do not call super.__init__() as this would recurse
        if 'identifier' not in self._kwargs and ' ' in self._kwargs['text']:
            raise Exception("Invalid ID used:",self._kwargs['text'])
            self._kwargs['identifier'] = self._kwargs['text']
        self._kwargs['shape_opener'] = Shape(self._kwargs['shape']).get_opener()
        self._kwargs['shape_closer'] = Shape(self._kwargs['shape']).get_closer()

    def __str__(self):
        return self.get_template('node').format(**self._kwargs)

    def _get_click_command(self):
        if 'on_click' in self._kwargs:
            return self.get_template('click').format(**self._kwargs)
        return ''


class FlowchartEdge(Edge):
    '''
    Node functions tailored for the 'flowchart' mermaid diagram type
    '''
    templates = {
        'edge' : "{str(self._src)} {self._arrow} {str(self._tgt)};\n"
        }

    def __init__(self,**kwargs):
        if 'src' not in kwargs or 'tgt' not in kwargs:
            raise Exception(f"Both src and tgt must be defined src:{src} tgt:{tgt}")
        self._arrow = Arrow(**kwargs)
        self._src = kwargs['src']
        self._tgt = kwargs['tgt']

    def __str__(self):
        return f"  {str(self._src)} {self._arrow} {str(self._tgt)};\n"


class Diagram():
    '''
    The embodiement of a single diagram
    Nodes and edges must be defined in the context of the 
    diagram for them to be rendered as part of the diagram
    '''

    templates = {
        'diagram_header':"{current_type} {direction}\n"
    }

    _children = {}

    def __init__(self,**kwargs):
        self._kwargs = kwargs


    def __enter__(self) -> Self:
        Context.set_current_type(self._kwargs['current_type'])
        task_id = get_task_id()
        if task_id not in self.__class__._children:
            self.__class__._children[task_id] = []
        if '_click_map' not in app.storage.client:
            app.storage.client['_click_map'] = {}
        self.__class__._dump_click_map()

        # Insert a handler function to caprture any click and emit an
        # event to trigger the nicegui 'ui.on()' call at th server
        # the Node id is passed to allow the appropraite function to be 
        # dispatched at the server

        ui.add_head_html('''
            <script>
                var _mermaidClickHandler = function (e) {
                        emitEvent("mermaidNodeEvent",e);
                        };

                function func(a) {
                     console.log(a)
                };
                    
            </script>
            ''')


        # Catch all click events here

        ui.on('mermaidNodeEvent',lambda e: click_dispatcher(e))

        # uses the function map to trigger the appropriate
        # function for the nodeId clicked

        def click_dispatcher(e):
            print('Get click for ',e.args)
            app.storage.client['_click_map'][e.args]()

        return self

    def __exit__(self,*_):
        Context.set_current_type(None)
        task_id = get_task_id()
        if task_id in self.__class__._children:
            del(self.__class__._children[task_id])

    def __str__(self):
        return self._render()

    def _render(self):
        current_type = Context.get_current_type()

        diagram_header_str = self.get_template('diagram_header').format(**self._kwargs)
        # render all childred
        nodes_str = ''
        edges_str = ''
        click_str = ''

        for child in self.__class__._children[get_task_id()]:
            if isinstance(child,Node):
                nodes_str += str(child) 

        for child in self.__class__._children[get_task_id()]:
            if isinstance(child,Edge):
                edges_str += str(child)
        
        for child in self.__class__._children[get_task_id()]:
            if isinstance(child,Node):
                click_str += child._get_click_command()

        return diagram_header_str+nodes_str+edges_str+click_str

    @classmethod
    def get_template(cls,template_name) -> str:
        return cls.templates[template_name]

    @classmethod
    def _add_child(cls,child) -> None:
        task_id = get_task_id()
        Diagram._children[task_id].append(child)
        return None

    @classmethod
    def _add_click(cls,identifier,f) -> None:
        print("Adding click",get_task_id())
        cls._dump_click_map()
        app.storage.client['_click_map'][identifier] = f
        return None

    @classmethod
    def _dump_click_map(cls):
        print('Map',app.storage.client)
