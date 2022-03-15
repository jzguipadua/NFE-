
from random import random


thousands = {
    1000000:'M',
    1000:'K',
    100:'H',
    1:'0'
    

}
def round_thousands(x,y=thousands):
    for key in y:
        if x/key < 1:
            pass
        else:
            return f'{round(x/key)}.{y[key]}'
        

