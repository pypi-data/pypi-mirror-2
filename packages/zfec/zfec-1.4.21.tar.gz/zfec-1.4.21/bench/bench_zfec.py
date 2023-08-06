from zfec import easyfec, Encoder, filefec
from pyutil import mathutil

import os, sys

from pyutil import benchutil

FNAME="benchrandom.data"

def _make_new_rand_file(size):
    open(FNAME, "wb").write(os.urandom(size))

def donothing(results, reslenthing):
    pass

K=3
M=10

d = ""
ds = []
easyfecenc = None
fecenc = None
def _make_new_rand_data(size, k, m):
    global d, easyfecenc, fecenc
    d = os.urandom(size)
    del ds[:]
    ds.extend([None]*k)
    blocksize = mathutil.div_ceil(size, k)
    for i in range(k):
        ds[i] = d[i*blocksize:(i+1)*blocksize]
    ds[-1] = ds[-1] + "\x00" * (len(ds[-2]) - len(ds[-1]))
    easyfecenc = easyfec.Encoder(k, m)
    fecenc = Encoder(k, m)

import sha
hashers = [ sha.new() for i in range(M) ]
def hashem(results, reslenthing):
    for i, result in enumerate(results):
        hashers[i].update(result)

def _encode_file(N):
    filefec.encode_file(open(FNAME, "rb"), donothing, K, M)

def _encode_file_stringy(N):
    filefec.encode_file_stringy(open(FNAME, "rb"), donothing, K, M)

def _encode_file_stringy_easyfec(N):
    filefec.encode_file_stringy_easyfec(open(FNAME, "rb"), donothing, K, M)

def _encode_file_not_really(N):
    filefec.encode_file_not_really(open(FNAME, "rb"), donothing, K, M)

def _encode_file_not_really_and_hash(N):
    filefec.encode_file_not_really_and_hash(open(FNAME, "rb"), donothing, K, M)

def _encode_file_and_hash(N):
    filefec.encode_file(open(FNAME, "rb"), hashem, K, M)

def _encode_data_not_really(N):
    i = 0
    for c in d:
        i += 1
    assert len(d) == N == i
    pass

def _encode_data_easyfec(N):
    easyfecenc.encode(d)

def _encode_data_fec(N):
    fecenc.encode(ds)

def bench(k, m):
    # for f in [_encode_file_stringy_easyfec, _encode_file_stringy, _encode_file, _encode_file_not_really,]:
    # for f in [_encode_file,]:
    # for f in [_encode_file_not_really, _encode_file_not_really_and_hash, _encode_file, _encode_file_and_hash,]:
    # for f in [_encode_data_not_really, _encode_data_easyfec, _encode_data_fec,]:
    print "measuring encoding of data with K=%d, M=%d, reporting results in nanoseconds per byte after encoding 4 MB..." % (k, m)
    for f in [_encode_data_fec,]:
        def _init_func(size):
            return _make_new_rand_data(size, k, m)
        for BSIZE in [2**22]:
            benchutil.rep_bench(f, n=BSIZE, initfunc=_init_func, MAXREPS=64, MAXTIME=None, UNITS_PER_SECOND=1000000000)
            benchutil.print_bench_footer(UNITS_PER_SECOND=1000000000)

k = K
m = M
for arg in sys.argv:
    if arg.startswith('--k='):
        k = int(arg[len('--k='):])
    if arg.startswith('--m='):
        m = int(arg[len('--m='):])

bench(k, m)
