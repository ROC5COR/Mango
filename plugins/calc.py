import os
import sys
from . import calclib
def instance():
    return Calc()

class Calc(object):
    def __init__(self):

        hola = 2

    def go(self):
        try:
            while True:
                try:
                    expr = input('[CALC] > ').strip()
                    if expr:
                        expr = calclib.tokenize(expr)
                        expr = calclib.implicit_multiplication(expr)
                        expr = calclib.to_rpn(expr)
                        res = calclib.eval_rpn(expr)
                        print('%g' % res)
                except ValueError as ex:
                    print('error:', ex)
        except EOFError:
            print('\ncaught EOF')
        except KeyboardInterrupt:
            print('\ninterrupted')
