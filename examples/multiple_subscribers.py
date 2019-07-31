'''
Example of sending simple strings using args and kwargs.
'''
import time
from zmqpc import Events
from resources import logging_config

pub = Events()
sub1 = Events()
sub2 = Events()
sub3 = Events()
sub4 = Events()
sub5 = Events()

def on_message(*args, **kwargs):
    print(f'args: {args}\tkwargs: {kwargs}')
sub1.connect(on_message, 'apple')
sub2.connect(on_message, 'apple')
sub3.connect(on_message, 'apple')
sub4.connect(on_message, 'apple')
sub5.connect(on_message, 'apple')

for i in range(0, 10):
    pub.publish('apple', 'pub1')
