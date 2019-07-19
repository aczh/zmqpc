'''
Example of publishing more kwargs than callback receives.
'''
import time
from zmqpc import Events

pub = Events()
sub = Events()

def on_message(arg1, arg2, kwarg1=None):
    print(arg1)
    print(arg2)
    print(kwarg1)

sub.connect(on_message, 'apple')

for i in range(0, 10):
    pub.publish('apple', 'arg1-aaaa', 'arg2-bbbb', kwarg1='kwarg1-cccc', kwarg2='kwarg2-dddd')
