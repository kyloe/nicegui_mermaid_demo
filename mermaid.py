from nicegui import ui
from fastapi.responses import RedirectResponse
from typing_extensions import Self
from shapes import Shape, Arrow
import asyncio 
 
def get_task_id() -> int:
    """Return the ID of the current asyncio task."""
    try:
        return id(asyncio.current_task())
    except RuntimeError:
        return 0


class Child():
    def __init__(self):
        pass
    def get_class_name(self):
        return self.__class__.__name__

class Node(Child):
    
    def __init__(self,**kwargs):
        super().__init__()
        self._kwargs = kwargs
        sub_class_name = f"{Diagram.get_current_type().capitalize()}Node"
        # Dynamically build sub class ref to avoid pages of if/elif 
        module = __import__(__name__)
        sub_class = getattr(module,sub_class_name)
        s = sub_class(**self._kwargs)
        Diagram._add_child(s)
        self._specialism = s

    def __str__(self):
        return self._specialism.__str__()


    # def click_def(self):
    #     return f"click {self._identifier} href \"javascript:_mermaidClickHandler(\'X-{self._identifier}-X\')\"\n" if self._clickable else ''


class GraphNode(Node):
    def __init__(self,**kwargs):
        self._kwargs = kwargs
        # Do not call super.__init__() as this would recurse
        if 'identifier' not in self._kwargs and ' ' in self._kwargs['text']:
            raise Exception("Invalid ID used:",self._kwargs['text'])
            self._kwargs['identifier'] = self._kwargs['text']
        self._kwargs['shape_opener'] = Shape(self._kwargs['shape']).get_opener()
        self._kwargs['shape_closer'] = Shape(self._kwargs['shape']).get_closer()

    def __str__(self):
        node_entry = Diagram.get_template('node').format(**self._kwargs)
        return node_entry

class Edge(Child):

    def __init__(self,src=None,tgt=None,**kwargs):
        super().__init__()
        if src == None or tgt == None:
            raise Exception(f"Both src and tgt must be defined src:{src} tgt:{tgt}")
        self._arrow = Arrow(**kwargs)
        self._src = src
        self._tgt = tgt
        Diagram._add_child(self)

    def __str__(self):
        return f"  {str(self._src)} {self._arrow} {str(self._tgt)};\n"

class Diagram():
    _current_type = {}
    _map = {
        'graph':{
            'arrows': {},
            'render_maps': {
                'diagram_header': "{current_type} {direction}\n",
                'node':"\t{identifier}{shape_opener}{text}{shape_closer}\n"
                }
            }
        }
    
    _children = {}

    def __init__(self,**kwargs):
        self._kwargs = kwargs


    def __enter__(self) -> Self:
        self.set_current_type(self._kwargs['current_type'])
        return self

    def __exit__(self,*_):
        self.set_current_type(None)

    def __str__(self):
        return self._render()

    def _render(self):
        current_type = self.__class__.get_current_type()
        # render all childred
        nodes_str = ''
        edges_str = ''
        for child in self.__class__._children[get_task_id()]:
            if isinstance(child,Node):
                nodes_str += str(child) 

        for child in self.__class__._children[get_task_id()]:
            if isinstance(child,Edge):
                edges_str += str(child)
            
        diagram_header_str = self.__class__._map[self._kwargs['current_type']]['render_maps']['diagram_header'].format(**self._kwargs)

        return diagram_header_str+nodes_str+edges_str

    @classmethod
    def get_template(self,template_name) -> str:
        task_id = get_task_id()
        ct = Diagram._current_type[task_id]

        return Diagram._map[ct]['render_maps'][template_name]

    @classmethod
    def _add_child(cls,child) -> None:
        task_id = get_task_id()
        Diagram._children[task_id].append(child)
        
        return None

    @classmethod
    def set_current_type(cls,current_type):
        task_id = get_task_id()
        cls._current_type[task_id] =  current_type
        if task_id not in cls._children:
            cls._children[task_id] = []

    @classmethod
    def get_current_type(cls):
        task_id = get_task_id()
        return cls._current_type[task_id]









@ui.page('/')
def main_page() -> None:
    with Diagram(current_type='graph',direction='TD') as diag:
        a = Node(text="My Node", identifier="A",shape='circle')
        b = Node(text="Another Node", identifier="B",shape='stadium')
        c = Node(text="Another Node", identifier="C",shape='stadium')
        d = Node(text="The End", identifier="D",shape='circle')
        Edge(src=a,tgt=b, thickness='dotted', label="Oooops",head='cross')
        Edge(src=a,tgt=c, thickness='thin', label="Alternative")
        Edge(src=c,tgt=d, thickness='thick', label="Alt")
        Edge(src=b,tgt=d, thickness='thin', label="Bong")

        ui.mermaid(str(diag))

ui.run()


    
#     m.run_method('update',
# '''
# flowchart
#     A --> B;
#     B --> C;

# click A href "javascript:_mermaidClickHandler('A-A-A')"

# ''')



# callback qqq  "_mermaidClickHandler"
# callback aaa  "_mermaidClickHandler"




# m = ui.mermaid("""
# ---
# title: Hello world
# config:
#     securityLevel: "loose"
#     theme: base
#     themeVariables:   

#       primaryColor: "#AAAA66"
#       primaryTextColor: "#444444"
#       primaryBorderColor: "#7C0000"
# ---
# flowchart
#     aaaa --> bbbb --> cccc
#     click aaaa href "javascript:alert('hi');"

# """)

# m.

ui.run()



# @ui.page('/')
# def main_page() -> None:

#     def action(identifier):
#         ui.notify(identifier)
#         if identifier == 'Boo':
#             b.update("Hurrah!")


#     ui.add_head_html('''
#     <script>
#         var _mermaidClickHandler = function (e) {
#                 console.log(e);
#                 var nodeId = e.split('-')[1]
#                 emitEvent("mermaidNodeEvent",nodeId);
#                 }
            
#     </script>
#     ''')


#     ui.on("mermaidNodeEvent",lambda e: (action(e.args)))
    

#     diag = Diagram(theme="---\ntitle: Homely page\n---\n")
#     a = Node(text="Albert",clickable=True)
#     b = Node(text="Boo", shape='hex', clickable=True)
#     c = Node(text="Clipper")
#     d = Node(text="Donkey", shape='circle')
#     e = Node(identifier="XX",text="Edgeware Road Tube Station", shape='stadium')
#     z = Edge(src=a,tgt=b)
#     y = Edge(src=a,tgt=c)
#     x = Edge(src=a,tgt=d)
#     w = Edge(src=d,tgt=e)
#     v = Edge(src=a,tgt=e)
#     diag.add([v,w,x,y,z,b])
#     print(str(diag))
#     m=ui.mermaid('').style('width: 180vh; height: 80vh; background-color: #999999')
#     m.run_method('initialize')
#     m.run_method('update',str(diag))

