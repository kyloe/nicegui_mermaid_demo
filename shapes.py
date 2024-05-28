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
    'dotted':
        {
            'pre':'-.',
            'post':'.-'
        }
    }
arrow_head = {'point':'>','circle':'o','cross':'x'}
arrow_tail = {'circle':'o'}



class Shape():
    
    def __init__(self,shape_name='rectangle'):
        if shape_name not in node_shapes:
            raise Exception(f"Invalid shape requested: {shape_name}.")
        self._shape = node_shapes[shape_name]
    
    def get_opener(self) -> str:
        return self._shape[0]
    
    def get_closer(self) -> str:
        return self._shape[1]


class Arrow():
    def __init__(self,thickness='thin',length=2,head='point',tail=None,label=None):
        pre_bar = ''.join([arrow_thickness[thickness]['pre']]*length)
        post_bar = ''.join([arrow_thickness[thickness]['post']]*length)
        bar = pre_bar + label + post_bar if label else pre_bar
        t = arrow_tail[tail] if tail in arrow_tail else ''
        h = arrow_head[head] if head in arrow_head else ''
        self._arrow = t+bar+h

    def __str__(self):
        return self._arrow