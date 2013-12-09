#!/usr/bin/env python2.7
"""Test linkedlist queue."""

import unittest

from fawnlog.linkedlist_queue import LinkedListQueue

class TestLinkedlistQueue(unittest.TestCase):
    """Test linkedlist queue functionality."""

    def test_enqueue(self):
        queue = LinkedListQueue([1, 2, 3, 4])
        for i in xrange(6):
            queue.enqueue(i)
        self.assertEqual(queue.length, 10)
        self.assertEqual(len(queue.to_list()), 10)

    def test_dequeue(self):
        queue = LinkedListQueue([0, 1, 2, 3, 4])
        for i in xrange(5):
            data = queue.dequeue()
            self.assertEqual(data, i)

    def test_dequeue_empty(self):
        """Test dequeue an empty queue"""

        queue = LinkedListQueue()
        with self.assertRaises(RuntimeError):
            queue.dequeue()

    def test_remove(self):
        queue = LinkedListQueue([0, 1, 2])
        node = queue.enqueue(3)
        queue.enqueue(4)
        queue.enqueue(5)
        queue.remove(node)
        self.assertEqual(queue.length, 5)
        self.assertEqual(len(queue.to_list()), 5)
        
    def test_remove_head(self):
        """Special case for remove, the node is the head"""

        queue = LinkedListQueue()
        head = queue.enqueue(1)
        queue.remove(head)
        self.assertEqual(queue.empty(), True)
        self.assertEqual(queue.head, None)
        self.assertEqual(queue.tail, None)

        head = queue.enqueue(1)
        queue.enqueue(2)
        queue.remove(head)
        self.assertEqual(len(queue.to_list()), 1)

    def test_remove_tail(self):
        """Special case for remove, the node is the tail"""

        queue = LinkedListQueue([0, 1, 2, 3])
        tail = queue.enqueue(4)
        queue.remove(tail)
        self.assertEqual(len(queue.to_list()), 4)
        self.assertEqual(queue.tail.data, 3)

if __name__ == "__main__":
    unittest.main()
