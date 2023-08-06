"""
Simple random

Unit Tests
"""

import random
import unittest

import simplerandom.iterators as sri
#import simplerandom.iterators._iterators_py as sri


class Marsaglia1999Tests(unittest.TestCase):
    """Tests as in Marsaglia 1999 post
    
    The Marsaglia 1999 post didn't explicitly set seed values for each RNG,
    but relied on the seed values that were side-effects of previous RNG
    executions. But we want to run each test as a stand-alone unit. So we
    have obtained the seed values from the C execution, and set them
    explicitly in each test here. The exception is LFIB4 followed by SWB--
    it would be painful to set the SWB seed table explicitly.
    """

    def test_lfib4_swb_million(self):
        # Set up KISS RNG to initialise seeds for LFIB4 and SWB RNGs.
        random_kiss = sri.RandomKISSIterator(12345, 65435, 12345, 34221)
        t = [ random_kiss.next() for i in range(256) ]

        # Test LFIB4
        lfib4 = sri.RandomLFIB4Iterator(t)
        for i in range(1000000):
            k = lfib4.next()
        self.assertEqual(k, 3673084687)

        # Test SWB
        swb = sri.RandomSWBIterator(lfib4.t)
        swb.c = lfib4.c
        for i in range(1000000):
            k = swb.next()
        self.assertEqual(k, 319777393)

    def test_kiss_million(self):
        random_kiss = sri.RandomKISSIterator(2247183469, 99545079, 3269400377, 3950144837)
        for i in range(1000000):
            k = random_kiss.next()
        self.assertEqual(k, 2100035942)

    def test_cong_million(self):
        cong = sri.RandomCongIterator(2051391225)
        for i in range(1000000):
            k = cong.next()
        self.assertEqual(k, 2416584377)

    def test_shr3_million(self):
        shr3 = sri.RandomSHR3Iterator(3360276411)
        for i in range(1000000):
            k = shr3.next()
        self.assertEqual(k, 1153302609)

    def test_mwc_million(self):
        mwc = sri.RandomMWCIterator(2374144069, 1046675282)
        for i in range(1000000):
            k = mwc.next()
        self.assertEqual(k, 904977562)

    def test_fib_million(self):
        fib = sri.RandomFibIterator(9983651,95746118)
        for i in range(1000000):
            k = fib.next()
        self.assertEqual(k, 3519793928)


class CongTest(unittest.TestCase):
    RNG_CLASS = sri.RandomCongIterator
    RNG_SEEDS = 1
    RNG_BITS = 32
    RNG_RANGE = (1 << RNG_BITS)


    def test_seed(self):
        # Make some random seed values
        seeds = [ random.randrange(self.RNG_RANGE) for _i in range(self.RNG_SEEDS) ]

        # Make the RNG instance
        rng = self.RNG_CLASS(*seeds)
        # Record its initial state
        state_from_init = rng.getstate()
        # Use the RNG to make some random numbers
        num_next_calls = random.randrange(3, 10)
        data_from_init = tuple([ rng.next() for _i in range(num_next_calls) ])
        # Get its state again
        state_after_data_from_init = rng.getstate()

        # Use the seed function to set its state to the same as before
        rng.seed(*seeds)
        # Get its state again. It should be the same as before.
        state_from_seed = rng.getstate()
        self.assertEqual(state_from_init, state_from_seed)
        # Get random numbers again. They should be the same as before.
        data_from_seed = tuple([ rng.next() for _i in range(num_next_calls) ])
        self.assertEqual(data_from_init, data_from_seed)
        # Get its state again. It should be the same as before.
        state_after_data_from_seed = rng.getstate()
        self.assertEqual(state_after_data_from_init, state_after_data_from_seed)


class SHR3Test(CongTest):
    RNG_CLASS = sri.RandomSHR3Iterator


class MWCTest(CongTest):
    RNG_CLASS = sri.RandomMWCIterator
    RNG_SEEDS = 2


class KISS2Test(CongTest):
    RNG_CLASS = sri.RandomKISS2Iterator
    RNG_SEEDS = 4
    MILLION_RESULT = 1010846401

    def test_million(self):
        rng = self.RNG_CLASS()
        for i in range(1000000):
            k = rng.next()
        self.assertEqual(k, self.MILLION_RESULT)


class MWC64Test(KISS2Test):
    RNG_CLASS = sri.RandomMWC64Iterator
    RNG_SEEDS = 2
    MILLION_RESULT = 3377343606

    def test_seed_with_MSbit_set(self):
        """Test MWC64 with MS-bit of mwc_c seed set.
        
        This caused an exception an earlier version of the Cython code (0.7.0)
        when built with Cython 0.14.
        """
        mwc64 = sri.RandomMWC64Iterator(2**31, 1)
        mwc64.next()


class KISSTest(CongTest):
    RNG_CLASS = sri.RandomKISSIterator
    RNG_SEEDS = 4


class FibTest(CongTest):
    RNG_CLASS = sri.RandomFibIterator
    RNG_SEEDS = 2


def runtests():
    unittest.main()


if __name__ == '__main__':
    runtests()

