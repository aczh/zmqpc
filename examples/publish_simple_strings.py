'''
Example of sending simple strings using args and kwargs.
'''
import time
from zmqpc import Events

pub = Events()
sub = Events()

def on_message(*args, **kwargs):
    print(f'args: {args}\tkwargs: {kwargs}')
sub.connect(on_message, 'apple')

for i in range(0, 10):
    pub.publish('apple', 'arg1', 'arg2', kwarg1='kwarg1', kwarg2='kwarg2')
