"""
Simple random

Unit Tests
"""

import unittest

import simplerandom.iterators as sri
#import simplerandom.iterators._iterators_py as sri


class MarsagliaTests(unittest.TestCase):
    def runTest(self):
        # Set up KISS RNG to initialise seeds for LFIB4 and SWB RNGs.
        random_kiss = sri.RandomKISSIterator(12345, 65435, 12345, 34221)
        t = [ random_kiss.next() for i in range(256) ]

        # Test LFIB4
        lfib4 = sri.RandomLFIB4Iterator(t)
        for i in range(1000000):
            k = lfib4.next()
        self.assertEqual(k, 1064612766, "LFIB4 test returned %d instead of expected value" % k)

        # Test SWB
        swb = sri.RandomSWBIterator(lfib4.t)
        swb.c = lfib4.c
        for i in range(1000000):
            k = swb.next()
        self.assertEqual(k, 627749721, "SWB test returned %d instead of expected value" % k)

        # Test KISS. We already set this up at the start.
        for i in range(1000000):
            k = random_kiss.next()
        self.assertEqual(k, 1372460312, "KISS test returned %d instead of expected value" % k)

        # Test Cong
        cong = sri.RandomCongIterator(random_kiss.cong)
        for i in range(1000000):
            k = cong.next()
        self.assertEqual(k, 1529210297, "Cong test returned %d instead of expected value" % k)

        # Test SHR3
        shr3 = sri.RandomSHR3Iterator(random_kiss.shr3_j)
        for i in range(1000000):
            k = shr3.next()
        self.assertEqual(k, 2642725982, "SHR3 test returned %d instead of expected value" % k)

        # Test MWC
        mwc = sri.RandomMWCIterator(random_kiss.mwc_z, random_kiss.mwc_w)
        for i in range(1000000):
            k = mwc.next()
        self.assertEqual(k, 904977562, "MWC test returned %d instead of expected value" % k)

        # Test Fib
        fib = sri._RandomFibIterator(9983651,95746118)
        for i in range(1000000):
            k = fib.next()
        self.assertEqual(k, 3519793928, "Fib test returned %d instead of expected value" % k)


class KISS2Test(unittest.TestCase):
    def runTest(self):
        kiss2 = sri.RandomKISS2Iterator()
        for i in range(1000000):
            k = kiss2.next()
        self.assertEqual(k, 1010846401, "KISS2 test returned %d instead of expected value" % k)


class MWC64Test(unittest.TestCase):
    def test_seed_with_MSbit_set(self):
        # This causes an error in the Cython module, when built with Cython 0.14.
        mwc64 = sri.RandomMWC64Iterator(2**63)
        k = mwc64.next()
        self.assertEqual(k, 2147483648)


def runtests():
    unittest.main()


if __name__ == '__main__':
    runtests()
