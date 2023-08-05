# $Id: priqueue.py 3124 2010-03-19 18:16:29Z nikolay $
# Copyright: Enfold Systems, LLC

# A simple priority queue implementation using a list *and* a dict.
# The list remains sorted via the bisect module.  The list keeps both the
# value and the key.
# The LGPL "PQueue" module would be better than this and has a similar
# interface
from bisect import insort, bisect

class PQueue:
    def __init__(self):
        self.dict = dict()
        self.queue=[]

    def __setitem__(self, key, value):
        if self.dict.has_key(key):
            del self[key]
        self.dict[key] = value
        insort(self.queue, (value,key))

    def __delitem__(self,key):
        item=self.dict[key], key
        del self.dict[key]
        del self.queue[bisect(self.queue,item)-1]

    def insert(self,priority,data):
        self[data] = priority

    def peek(self):
        return self.queue[0]

    def pop(self):
        value,key = self.queue.pop(0)
        del self.dict[key]
        return value,key
