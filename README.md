# zmqpc
Simple and fast IPC (Inter-Process Communication) between Python processes using ZMQ.


```python
import time
from zmqpc import Events

pub = Events()
sub = Events()

# Events typically need some time to discover each other.
time.sleep(0.1)

# set up our subscriber to call 'fn' every time it receives a message with topic 'your_topic'
def fn(data):
    fn.data = data
    fn.data = None
sub.connect(fn, 'your_topic')

pub.publish('your_topic', 'your_data')

# give our sockets time to receive the data
time.sleep(0.1)
assert fn.data == 'your_data'
```
