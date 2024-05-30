from nicegui import ui,app
from fastapi.responses import RedirectResponse
from entities import Diagram, Node, Edge
import asyncio 
from context import Context, get_task_id
import logging
log = logging.getLogger(__name__)




@ui.page('/')
def main_page() -> None:


    


    # f_map = {'A':do_a_thing,'B':do_b_thing}

    m=ui.mermaid('')
    m.run_method('initialize')


    with Diagram(current_type='flowchart',direction='TD') as diag:

        @ui.refreshable
        def make_panel(info_string):
            ui.label(info_string)

        a = Node(text="My Node", identifier="A",shape='circle',on_click=lambda: make_panel.refresh("This data relates to node A"))
        b = Node(text="Another Node", identifier="B",shape='stadium',on_click=lambda: make_panel.refresh("This data relates to node B and is much longer - to the point hwere it becomes dull"))
        c = Node(text="Another Node", identifier="C",shape='rounded_rectangle')
        d = Node(text="The End", identifier="D",shape='circle')
        Edge(src=a,tgt=b, thickness='dotted', length=1,label="Oooops",head='arrow')
        Edge(src=a,tgt=c, thickness='thin', length=3,head='circle',tail='circle',label=None)
        Edge(src=c,tgt=d, thickness='thick', label="Alt", head='point')
        Edge(src=b,tgt=d, head=None,thickness='invisible',length=3)


        with ui.row().style('width: 60%'):
            m.run_method('update',str(diag))
            make_panel("Info goes here")


ui.run(storage_secret = 'This is a very secret thing')


