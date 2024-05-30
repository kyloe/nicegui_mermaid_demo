import logging
log = logging.getLogger(__name__)


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

arrow_thickness = {
    'thin':
        {
            'pre':'-',
            'post':'-'
        },
    'thick':
        {
            'pre':'=',
            'post':'='
        },
    'invisible':
        {
            'pre':'~',
            'post':'~'
        },
    'dotted':
        {
            'pre':'-.',
            'post':'.-'
        }
    }
arrow_head = {'point':'>','circle':'o','cross':'x'}
arrow_tail = {'point':'<','circle':'o','cross':'x'}



class Shape():
    
    def __init__(self,shape_name='rectangle'):
        if shape_name not in node_shapes:
            log.warning(f"{shape_name} is not a recognised shape: substitued 'stadium'")
            shape_name = 'stadium'
        self._shape = node_shapes[shape_name]
    
    def get_opener(self) -> str:
        return self._shape[0]
    
    def get_closer(self) -> str:
        return self._shape[1]

class Arrow():
    def __init__(self,**kwargs):
        self._thickness = kwargs.get('thickness','thin')
        self._head = kwargs.get('head',None)
        self._tail = kwargs.get('tail',None)
        self._label = kwargs.get('label',None)
        self._length = kwargs.get('length',2)

        pre_bar = ''.join([arrow_thickness[self._thickness]['pre']]*self._length)
        post_bar = ''.join([arrow_thickness[self._thickness]['post']]*self._length)
        bar = pre_bar + self._label + post_bar if self._label else pre_bar
        if 'point' in [self._tail,self._head]:
            log.warning(f"Crosses and circles ignored when arrow heads are used")
        t = arrow_tail[self._tail] if self._tail in arrow_tail else ''
        h = arrow_head[self._head] if self._head in arrow_head else ''
        self._arrow = t+bar+h

    def __str__(self):
        return self._arrow