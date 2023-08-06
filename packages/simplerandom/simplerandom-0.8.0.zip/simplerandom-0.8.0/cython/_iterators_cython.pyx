
cdef extern from "types.h":
    ctypedef int uint64_t
    ctypedef int uint32_t
    ctypedef int uint8_t


cdef class RandomCongIterator(object):
    '''Congruential random number generator

    This is a congruential generator with the widely used
    69069 multiplier: x[n]=69069x[n-1]+1234567. It has
    period 2**32.
    
    The leading half of its 32 bits seem to pass tests,
    but bits in the last half are too regular. It fails
    tests for which those bits play a significant role.
    Cong+Fib will also have too much regularity in
    trailing bits, as each does. But keep in mind that
    it is a rare application for which the trailing
    bits play a significant role. Cong is one of the
    most widely used generators of the last 30 years,
    as it was the system generator for VAX and was
    incorporated in several popular software packages,
    all seemingly without complaint.
    '''

    cdef public uint32_t cong

    def __init__(self, seed = None):
        if seed==None:
            seed = 12344
        self.cong = int(seed)

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        self.cong = 69069 * self.cong + 1234567
        return self.cong

    def __iter__(self):
        return self

    def getstate(self):
        return (self.cong, )

    def setstate(self, state):
        self.cong = int(state[0])


cdef class RandomCong2Iterator(object):
    '''Congruential random number generator

    Very similar to RandomCongIterator, but with different
    added constant and different default seed.
    '''

    cdef public uint32_t cong

    def __init__(self, seed = None):
        if seed==None:
            seed = 123456789
        self.cong = int(seed)

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        self.cong = 69069 * self.cong + 12345
        return self.cong

    def __iter__(self):
        return self

    def getstate(self):
        return (self.cong, )

    def setstate(self, state):
        self.cong = int(state[0])


cdef class RandomSHR3Iterator(object):
    '''3-shift-register random number generator

    SHR3 is a 3-shift-register generator with period
    2**32-1. It uses y[n]=y[n-1](I+L^17)(I+R^13)(I+L^5),
    with the y's viewed as binary vectors, L the 32x32
    binary matrix that shifts a vector left 1, and R its
    transpose.

    SHR3 seems to pass all except those related to the
    binary rank test, since 32 successive values, as
    binary vectors, must be linearly independent, while
    32 successive truly random 32-bit integers, viewed
    as binary vectors, will be linearly independent only
    about 29% of the time.
    '''

    cdef public uint32_t shr3_j

    def __init__(self, seed = None):
        if seed==None or seed==0:
            seed = 34223
        self.shr3_j = int(seed)

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        cdef uint32_t shr3_j
        shr3_j = self.shr3_j
        shr3_j ^= shr3_j << 17
        shr3_j ^= shr3_j >> 13
        shr3_j ^= shr3_j << 5
        self.shr3_j = shr3_j
        return shr3_j

    def __iter__(self):
        return self

    def getstate(self):
        return (self.shr3_j, )

    def setstate(self, state):
        self.shr3_j = int(state[0])


cdef class RandomSHR3_2Iterator(object):
    '''3-shift-register random number generator
    
    This differs from the SHR3 generator in the default seed
    value, and the values of the three shift operations.
    '''

    cdef public uint32_t shr3_j

    def __init__(self, seed = None):
        if seed==None or seed==0:
            seed = 362436000
        self.shr3_j = int(seed)

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        cdef uint32_t shr3_j
        shr3_j = self.shr3_j
        shr3_j ^= shr3_j << 13
        shr3_j ^= shr3_j >> 17
        shr3_j ^= shr3_j << 5
        self.shr3_j = shr3_j
        return shr3_j

    def __iter__(self):
        return self

    def getstate(self):
        return (self.shr3_j, )

    def setstate(self, state):
        self.shr3_j = int(state[0])


cdef class RandomMWCIterator(object):
    '''"Multiply-with-carry" random number generator

    This uses two MWC generators to generate high and
    low 16-bit parts, which are then combined to make a
    32-bit value.

    The MWC generator concatenates two 16-bit multiply-
    with-carry generators:

        x[n]=36969x[n-1]+carry,
        y[n]=18000y[n-1]+carry mod 2**16,

    It has a period about 2**60 and seems to pass all
    tests of randomness. A favorite stand-alone generator,
    and faster than KISS, which contains it.
    '''

    cdef public uint32_t mwc_z
    cdef public uint32_t mwc_w

    def __init__(self, seed_z = None, seed_w = None):
        if seed_z==None:
            seed_z = 12344
        if seed_w==None:
            seed_w = 65437
        self.mwc_z = int(seed_z)
        self.mwc_w = int(seed_w)

    def seed(self, seed_z = None, seed_w = None):
        self.__init__(seed_z, seed_w)

    def __next__(self):
        cdef uint32_t mwc
        self.mwc_z = 36969u * (self.mwc_z & 0xFFFF) + (self.mwc_z >> 16)
        self.mwc_w = 18000u * (self.mwc_w & 0xFFFF) + (self.mwc_w >> 16)
        mwc = (self.mwc_z << 16) + self.mwc_w
        return mwc

    property mwc:
        def __get__(self):
            cdef uint32_t mwc
            mwc = (self.mwc_z << 16) + self.mwc_w
            return mwc

    def __iter__(self):
        return self

    def getstate(self):
        return (self.mwc_z, self.mwc_w)

    def setstate(self, state):
        self.mwc_z = int(state[0])
        self.mwc_w = int(state[1])


cdef class RandomMWC64Iterator(object):
    '''"Multiply-with-carry" random number generator

    This uses a single MWC generator with 64 bits to
    generate a 32-bit value. The seed should be a 64-bit
    value.
    '''

    cdef public uint64_t mwc_z

    def __init__(self, seed = None):
        if seed==None:
            seed = 32875058889374645
        self.mwc_z = int(seed)

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        cdef uint32_t mwc
        self.mwc_z = 698769069u * (self.mwc_z & 0xFFFFFFFF) + (self.mwc_z >> 32)
        mwc = self.mwc_z & 0xFFFFFFFF
        return mwc

    property mwc:
        def __get__(self):
            cdef uint32_t mwc
            mwc = self.mwc_z & 0xFFFFFFFF
            return mwc

    def __iter__(self):
        return self

    def getstate(self):
        return (self.mwc_z, )

    def setstate(self, state):
        self.mwc_z = int(state[0])


cdef class RandomKISSIterator(object):
    '''"Keep It Simple Stupid" random number generator
    
    It combines the RandomMWC, RandomCong, RandomSHR3
    generators. Period is about 2**123. It is one of
    Marsaglia's favourite generators.
    '''

    cdef public uint32_t cong
    cdef public uint32_t shr3_j
    cdef public uint32_t mwc_z
    cdef public uint32_t mwc_w

    def __init__(self, seed_mwc_z = None, seed_mwc_w = None, seed_cong = None, seed_shr3 = None):
        # Initialise MWC RNG
        if seed_mwc_z==None:
            seed_mwc_z = 12344
        if seed_mwc_w==None:
            seed_mwc_w = 65437
        self.mwc_z = int(seed_mwc_z)
        self.mwc_w = int(seed_mwc_w)
        # Initialise Cong RNG
        if seed_cong==None:
            seed_cong = 12344
        self.cong = int(seed_cong)
        # Initialise SHR3 RNG
        if seed_shr3==None or seed_shr3==0:
            seed_shr3 = 34223
        self.shr3_j = int(seed_shr3)

    def seed(self, seed_mwc_z = None, seed_mwc_w = None, seed_cong = None, seed_shr3 = None):
        self.__init__(seed_mwc_z, seed_mwc_w, seed_cong, seed_shr3)

    def __next__(self):
        cdef uint32_t mwc
        cdef uint32_t shr3_j

        self.mwc_z = 36969u * (self.mwc_z & 0xFFFF) + (self.mwc_z >> 16)
        self.mwc_w = 18000u * (self.mwc_w & 0xFFFF) + (self.mwc_w >> 16)
        mwc = (self.mwc_z << 16) + self.mwc_w

        self.cong = 69069 * self.cong + 1234567

        # Update SHR3 RNG
        shr3_j = self.shr3_j
        shr3_j ^= shr3_j << 17
        shr3_j ^= shr3_j >> 13
        shr3_j ^= shr3_j << 5
        self.shr3_j = shr3_j

        return (mwc ^ self.cong) + shr3_j

    property mwc:
        def __get__(self):
            cdef uint32_t mwc
            mwc = (self.mwc_z << 16) + self.mwc_w
            return mwc

    def getstate(self):
        return ((self.mwc_z, self.mwc_w), (self.cong,), (self.shr3_j,))

    def setstate(self, state):
        (mwc_state, cong_state, shr3_state) = state
        self.mwc_z = int(mwc_state[0])
        self.mwc_w = int(mwc_state[1])
        self.cong = int(cong_state[0])
        self.shr3_j = int(shr3_state[0])


cdef class RandomKISS2Iterator(object):
    '''"Keep It Simple Stupid" random number generator
    
    It combines the RandomMWC64, RandomCong2, RandomSHR3_2
    generators. Period is about 2**123.

    This is a slightly updated KISS generator design, from
    a newsgroup post in 2003:

    http://groups.google.com/group/comp.soft-sys.math.mathematica/msg/95a94c3b2aa5f077

    The Cong and SHR3 component generators are changed
    slightly. The MWC component uses a single 64-bit
    calculation, instead of two 32-bit calculations that
    are combined.
    '''

    cdef public uint32_t cong
    cdef public uint32_t shr3_j
    cdef public uint64_t mwc_z

    def __init__(self, seed_mwc = None, seed_cong = None, seed_shr3 = None):
        # Initialise MWC RNG
        if seed_mwc==None:
            seed_mwc = 32875058889374645
        self.mwc_z = int(seed_mwc)
        # Initialise Cong RNG
        if seed_cong==None:
            seed_cong = 123456789
        self.cong = int(seed_cong)
        # Initialise SHR3 RNG
        if seed_shr3==None or seed_shr3==0:
            seed_shr3 = 362436000
        self.shr3_j = int(seed_shr3)

    def seed(self, seed_mwc_z = None, seed_mwc_w = None, seed_cong = None, seed_shr3 = None):
        self.__init__(seed_mwc_z, seed_mwc_w, seed_cong, seed_shr3)

    def __next__(self):
        cdef uint32_t mwc
        cdef uint32_t shr3_j

        self.mwc_z = 698769069u * (self.mwc_z & 0xFFFFFFFF) + (self.mwc_z >> 32)
        mwc = self.mwc_z & 0xFFFFFFFF

        self.cong = 69069 * self.cong + 12345

        # Update SHR3 RNG
        shr3_j = self.shr3_j
        shr3_j ^= shr3_j << 13
        shr3_j ^= shr3_j >> 17
        shr3_j ^= shr3_j << 5
        self.shr3_j = shr3_j

        return mwc + self.cong + shr3_j

    property mwc:
        def __get__(self):
            cdef uint32_t mwc
            mwc = self.mwc_z & 0xFFFFFFFF
            return mwc

    def getstate(self):
        return ((self.mwc_z,), (self.cong,), (self.shr3_j,))

    def setstate(self, state):
        (mwc_state, cong_state, shr3_state) = state
        self.mwc_z = int(mwc_state[0])
        self.cong = int(cong_state[0])
        self.shr3_j = int(shr3_state[0])


def _fib_adjust_seed(seed):
    if not seed % 2:
        seed += 1
    if seed % 8 == 1:
        seed += 2
    return seed

cdef class _RandomFibIterator(object):
    '''Classical Fibonacci sequence

    x[n]=x[n-1]+x[n-2],but taken modulo 2**32. Its
    period is 3 * (2**31) if one of its two seeds is
    odd and not 1 mod 8.
    
    It has little worth as a RNG by itself, since it
    fails several tests. But it provides a simple and
    fast component for use in combination generators.
    '''

    cdef public uint32_t a
    cdef public uint32_t b

    def __init__(self, seed_a = None, seed_b = None):
        if seed_a==None:
            seed_a = 1468761293
        if seed_b==None:
            seed_b = 3460192787
        self.a = int(seed_a)
        self.b = int(seed_b)
        if self._adjust_seed(self.a) != self.a:
            self.b = self._adjust_seed(self.b)

    _adjust_seed = staticmethod(_fib_adjust_seed)

    def seed(self, seed_a = None, seed_b = None):
        self.__init__(seed_a, seed_b)

    def __next__(self):
        cdef uint32_t new_a
        cdef uint32_t new_b

        new_a = self.b
        new_b = self.a + self.b
        (self.a, self.b) = (new_a, new_b)
        return new_a

    def __iter__(self):
        return self

    def getstate(self):
        return (self.a, self.b)

    def setstate(self, state):
        self.a = int(state[0])
        self.b = int(state[1])


cdef class RandomLFIB4Iterator(object):
    '''"Lagged Fibonacci 4-lag" random number generator

    LFIB4 is an extension of what Marsaglia has previously
    defined as a lagged Fibonacci generator:

        x[n]=x[n-r] op x[n-s]

    with the x's in a finite set over which there is a
    binary operation op, such as +,- on integers mod 2**32,
    * on odd such integers, exclusive-or(xor) on binary
    vectors. Except for those using multiplication, lagged
    Fibonacci generators fail various tests of randomness,
    unless the lags are very long. (See SWB).

    To see if more than two lags would serve to overcome
    the problems of 2-lag generators using +,- or xor,
    Marsaglia developed the 4-lag generator LFIB4 using
    addition:

        x[n]=x[n-256]+x[n-179]+x[n-119]+x[n-55] mod 2**32

    Its period is 2**31*(2**256-1), about 2**287,
    and it seems to pass all tests---in particular,
    those of the kind for which 2-lag generators using
    +,-,xor seem to fail.

    For even more confidence in its suitability, LFIB4
    can be combined with KISS, with a resulting period
    of about 2**410.
    '''

    cdef uint32_t tt[256]
    cdef public uint8_t c

    def __init__(self, seed = None):
        cdef int i
        if not seed:
            random_kiss = RandomKISSIterator(12345, 65435, 12345, 34221)
            for i in range(256):
                self.tt[i] = next(random_kiss)
        else:
            if len(seed) != 256:
                raise Exception("seed length must be 256")
            seed_iter = iter(seed)
            for i in range(256):
                self.tt[i] = next(seed_iter)
        self.c = 0

    def seed(self, seed = None):
        self.__init__(seed)

    def __next__(self):
        cdef uint32_t new_value
        self.c += 1

        new_value = (self.tt[self.c] +
                     self.tt[(self.c + 58) % 256] +
                     self.tt[(self.c + 119) % 256] +
                     self.tt[(self.c + 178) % 256])

        self.tt[self.c] = new_value

        return new_value

    def __iter__(self):
        return self

    def getstate(self):
#        return tuple( self.tt[(i + self.c) % 256] for i in range(256) )
        return tuple([ self.tt[(i + self.c) % 256] for i in range(256) ])

    def setstate(self, state):
        cdef int i
        if len(state) != 256:
            raise Exception("state length must be 256")
#        self.tt = list(int(val) & 0xFFFFFFFF for val in state)
#        self.tt = [ int(val) & 0xFFFFFFFF for val in state ]
        for i in range(256):
            self.tt[i] = state[i]
        self.c = 0

    property t:
        def __get__(self):
            cdef int i
            return tuple([ self.tt[i] for i in range(256) ])

        def __set__(self, value):
            cdef int i
            for i in range(256):
                self.tt[i] = value[i]


cdef class RandomSWBIterator(RandomLFIB4Iterator):
    '''"Subtract-With-Borrow" random number generator
    
    SWB is a subtract-with-borrow generator that Marsaglia
    developed to give a simple method for producing
    extremely long periods:
    x[n]=x[n-222]-x[n-237]- borrow mod 2**32.
    The 'borrow' is 0, or set to 1 if computing x[n-1]
    caused overflow in 32-bit integer arithmetic. This
    generator has a very long period, 2**7098(2**480-1),
    about 2**7578.

    It seems to pass all tests of randomness, except
    for the Birthday Spacings test, which it fails
    badly, as do all lagged Fibonacci generators using
    +,- or xor. Marsaglia suggests combining SWB with
    KISS, MWC, SHR3, or Cong. KISS+SWB has period
    >2**7700 and is highly recommended.

    Subtract-with-borrow has the same local behaviour
    as lagged Fibonacci using +,-,xor---the borrow
    merely provides a much longer period.

    SWB fails the birthday spacings test, as do all
    lagged Fibonacci and other generators that merely
    combine two previous values by means of =,- or xor.
    Those failures are for a particular case: m=512
    birthdays in a year of n=2**24 days. There are
    choices of m and n for which lags >1000 will also
    fail the test. A reasonable precaution is to always
    combine a 2-lag Fibonacci or SWB generator with
    another kind of generator, unless the generator uses
    *, for which a very satisfactory sequence of odd
    32-bit integers results.
    '''

    cdef public uint8_t borrow

    def __init__(self, seed = None):
        RandomLFIB4Iterator.__init__(self, seed)
        self.borrow = 0

    def __next__(self):
        cdef uint32_t x
        cdef uint32_t y

        self.c += 1

        x = self.tt[(self.c + 34) % 256]
        y = (self.tt[(self.c + 19) % 256] + self.borrow)
        new_value = x - y

        self.tt[self.c] = new_value

        self.borrow = 1 if (x < y) else 0

        return new_value

    def getstate(self):
        t_tuple = RandomLFIB4Iterator.getstate(self)
        return (t_tuple, self.borrow)

    def setstate(self, state):
        (t_tuple, borrow) = state
        RandomLFIB4Iterator.setstate(self, t_tuple)
        self.borrow = 1 if borrow else 0


