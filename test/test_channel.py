import unittest
from unittest import TestCase

from ecspo import Channel, RecursiveConnection


class TestChannel(TestCase):
    def setUp(self):
        self.channel = Channel()

    def test_call(self):
        """
        Ensure the __call__ method adds all recievers.
        """
        self.channel(sum)
        self.channel(map)
        self.assertListEqual([sum, map], self.channel.recievers)

    def test_iter(self):
        """
        Ensure the __iter__ method returns all recievers.  
        """
        self.channel(sum)
        self.channel(map)
        self.assertTupleEqual((sum, map), tuple(self.channel))

    def test_connect(self):
        self.channel.connect(sum)
        self.channel.connect(map)
        self.assertListEqual([sum, map], self.channel.recievers)

    def test_emit(self):
        """
        Ensure the channel.emit method functions correctly and detects improper use.
        """
        signal = dict()
        channel = Channel()
        self.channel(channel)
        channel(lambda signal: signal.update({"recieved": True}))

        with self.subTest("Ensure response propagation."):
            self.channel.emit(signal)
            self.assertTrue(signal.get("recieved"))

        channel(self.channel)
        with self.subTest("Ensure recursive subscription is detected."):
            with self.assertRaises(RecursiveConnection):
                self.channel.emit(signal)
            

if __name__ == "__main__":
    unittest.main()
