'''
Example of sending simple strings using args and kwargs.
'''
import time
from zmqpc import Events

pub1 = Events()
pub2 = Events()
pub3 = Events()
pub4 = Events()
pub5 = Events()
sub = Events()

def on_message(*args, **kwargs):
    print(f'args: {args}\tkwargs: {kwargs}')
sub.connect(on_message, 'apple')

for i in range(0, 10):
    pub1.publish('apple', 'pub1')
    pub2.publish('apple', 'pub2')
    pub3.publish('apple', 'pub3')
    pub4.publish('apple', 'pub4')
    pub5.publish('apple', 'pub5')
