'''
Example of publishing more args than callback receives.
'''
import time
from zmqpc import Events
from resources import logging_config

pub = Events()
sub = Events()

def on_message(arg1, kwarg1=None, kwarg2=None):
    print(arg1)
    print(kwarg1)
    print(kwarg2)

sub.connect(on_message, 'apple')

for i in range(0, 10):
    pub.publish('apple', 'arg1-aaaa', 'arg2-bbbb', kwarg1='kwarg1-cccc', kwarg2='kwarg2-dddd')
