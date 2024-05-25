from nicegui import ui
from fastapi.responses import RedirectResponse

node_shapes = {
    'rectangle':('[',']'),
    'rounded_rectangle':('(',')'),
    'circle':('((','))'),
    'stadium':('([','])'),
    'subroutine':('[[',']]'),
    'cylinder':('[(',')]'),
    'flag':('>',']'),
    'hex':('{{','}}'),
    'rhombus':('{','}'),
    'parallelogram':('[/','/]'),
    'parallelogram_alt':('[\\','\\]'),
    'trapezoid':('/','\\'),
    'trapezoid_alt':('\\','/')
}



class Shape():
    
    def __init__(self,shape_name='rectangle'):
        self._shape = node_shapes[shape_name]
    
    def get_opener(self):
        return self._shape[0]
    
    def get_closer(self):
        return self._shape[1]


class Node():
    
    def __init__(self,identifier=None,text="NODE",shape="rectangle", on_click=None):
        if identifier is None and ' ' in text:
            raise Exception("Invalid ID used:",text)
        self._identifier = text if not identifier else identifier
        self._text = text
        self._shape = Shape(shape_name = shape)
        self._on_click = on_click

    def __str__(self):
        node_entry = f"{self._identifier}{self._shape.get_opener()}{self._text}{self._shape.get_closer()} "
        click_command = f"click {self._identifier} \"/click/{self._on_click}\""
        return node_entry

    def click_def(self):
        return f"click {self._identifier} call {self._on_click}()\n" if self._on_click else ''

class Edge():

    def __init__(self,src=None,style="-->",tgt=None):
        if src == None or tgt == None:
            raise Exception(f"Both src and tgt must be defined src:{src} tgt:{tgt}")
        self._style = style
        self._src = src
        self._tgt = tgt
    
    def __str__(self):
        return f"  {self._src} {self._style} {self._tgt};\n"

class Diagram():
    
    def __init__(self,style='graph',direction='LR', theme=None):
        self._style = style
        self._direction = direction
        self._edges = []
        self._nodes = []
        self._theme = theme

    def _render_config(self):
        return f"{'' if self._theme is None else self._theme}\n{self._style} {self._direction};"

    def _render_edges(self):
        s = ''
        for child in self._edges:
            s = s+str(child)
        return s

    def _render_nodes(self):
        s = ''
        for child in self._nodes:
            s = s+child.click_def()
        return s


    def __str__(self):
        return f"{self._render_config()}\n{self._render_edges()}\n{self._render_nodes()}"

    def add(self,item):

        def add_item(i):
            if type(i) is Edge:
                self._edges.append(i)
            elif type(i) is Node:
                self._nodes.append(i)
            else:
                raise Exception(f"Tried to store an unsuitable object {type(i)}")

        if type(item) is list:
            for item_i in item:
                add_item(item_i)
        else:
            add_item(item)





@ui.page('/')
def main_page() -> None:

    ui.add_head_html('''
    <script>
        var _mermaidClickHandler = function (e) {
                console.log(e);
                var nodeId = e.split('-')[1]
                emitEvent("mermaidNodeEvent",nodeId);
                }
            
    </script>
    ''')


    ui.on("mermaidNodeEvent",lambda e: (ui.notify(e.args)))
    

    diag = Diagram(theme="---\ntitle: Homely page\n---\n")
    a = Node(text="Albert",on_click='doit')
    b = Node(text="Boo", shape='hex', on_click='was_clicked')
    c = Node(text="Clipper")
    d = Node(text="Donkey", shape='circle')
    e = Node(identifier="XX",text="Edgeware Road Tube Station", shape='stadium')
    z = Edge(src=a,tgt=b)
    y = Edge(src=a,tgt=c)
    x = Edge(src=a,tgt=d)
    w = Edge(src=d,tgt=e)
    v = Edge(src=a,tgt=e)
    diag.add([v,w,x,y,z,b])
    print(str(diag))
    m=ui.mermaid('').style('width: 180vh; height: 80vh; background-color: #999999')
    #ui.run_javascript(f'console.log(Object.getOwnPropertyNames(getElement({m.id})))')
    #ui.run_javascript(f'getElement({m.id}).initialize()')
    m.run_method('initialize')
    m.run_method('update',
'''
classDiagram
  class aaa
  class qqq
  callback qqq  "_mermaidClickHandler"
  callback aaa  "_mermaidClickHandler"''')

@ui.page('/click/{click_function}')
def click_handler(click_function: str):
    print(click_function)
    return RedirectResponse('/')

ui.run()








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
