"""LinkedListQueue.

Special purpose Queue implemented based on doubly linked list,
Support standard enqueue, dequeue, and remove a node in the middle.

"""

class Empty(RuntimeError):
    """The LinkedListQueue is empty"""

class Node(object):
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

    def __str__(self):
        pass

class LinkedListQueue(object):
    """Special purpose Queue implemented based on doubly linked list,
       Support standard enqueue, dequeue,
       and remove a node in the middle"""

    def __init__(self, iteration=None):
        self.head = None
        self.tail = None
        self.length = 0
        if iteration is not None:
            for i in iteration:
                self.enqueue(i)

    def empty(self):
        return self.length == 0

    def enqueue(self, data):
        """Return the enqueued object"""

        new_tail = Node(data)
        if self.tail is None:
            self.tail = new_tail
            self.head = new_tail
        else:
            self.tail.next = new_tail
            new_tail.prev = self.tail
            self.tail = new_tail
        self.length += 1
        return new_tail

    def dequeue(self):
        if self.head is None:
            raise Empty()
        node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self.length -= 1
        return node.data

    def remove(self, node):
        """Remove node from the LinkedListQueue"""
        # FIXME: what if the node is not in the queue anymore
        if node is None:
            return
        if node == self.head:
            self.dequeue()
            return
        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev
        if node == self.tail:
            self.tail = self.tail.prev
        self.length -= 1

    def peek(self):
        if self.head is None:
            return None
        return self.head.data

    def to_list(self):
        r = []
        p = self.head
        while p is not None:
            r.append(p.data)
            p = p.next
        return r

    def __str__(self):
        l = self.to_list()
        return ''.join([str(x) + " " for x in l])
