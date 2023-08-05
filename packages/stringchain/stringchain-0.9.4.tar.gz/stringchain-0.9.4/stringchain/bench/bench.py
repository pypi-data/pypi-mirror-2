from pyutil import benchutil, randutil
import copy, random
from stringchain.stringchain import StringChain

from cStringIO import StringIO

class StringIOy(object):
    def __init__(self):
        self.s = StringIO()

    def __len__(self):
        return self.s.tell()

    def append(self, s):
        self.s.write(s)

    def trim(self, l):
        v = self.s.getvalue()
        self.s = StringIO()
        self.s.write(v[l:])

    def popleft_new_stringchain(self, l):
        n = self.__class__()
        self.s.seek(0)
        n.s.write(self.s.read(l))
        rem = self.s.read()
        self.s = StringIO()
        self.s.write(rem)
        return n

    def popleft(self, l):
        self.s.seek(0)
        res = self.s.read(l)
        rem = self.s.read()
        self.s = StringIO()
        self.s.write(rem)
        return res

    def __str__(self):
        return self.s.getvalue()

    def copy(self):
        n = self.__class__()
        n.s = StringIO()
        x = self.s.tell()
        self.s.seek(0)
        n.s.write(self.s.read())
        self.s.seek(x)
        return n

class Stringy(object):
    def __init__(self):
        self.s = ''

    def __len__(self):
        return len(self.s)

    def append(self, s):
        self.s += s

    def trim(self, l):
        self.s = self.s[l:]

    def popleft_new_stringchain(self, l):
        n = self.__class__()
        n.s = self.s[:l]
        self.s = self.s[l:]
        return n

    def popleft(self, l):
        res = self.s[:l]
        self.s = self.s[l:]
        return res

    def __str__(self):
        return self.s

    def copy(self):
        n = self.__class__()
        n.s = self.s
        return n

class SimplerStringChain(object):
    def __init__(self):
        self.ss = []
        self.len = 0

    def __len__(self):
        return self.len

    def append(self, s):
        self.ss.append(s)
        self.len += len(s)

    def _collapse(self):
        s = ''.join(self.ss)
        del self.ss[:]
        self.ss.append(s)

    def trim(self, l):
        self._collapse()
        self.ss[0] = self.ss[0][l:]
        self.len = len(self.ss[0])

    def popleft_new_stringchain(self, l):
        self._collapse()
        n = self.__class__()
        n.ss.append(self.ss[0][:l])
        self.ss[0] = self.ss[0][l:]
        self.len = len(self.ss[0])
        return n

    def popleft(self, l):
        self._collapse()
        res = self.ss[0][:l]
        self.ss[0] = self.ss[0][l:]
        self.len = len(self.ss[0])
        return res

    def __str__(self):
        self._collapse()
        return self.ss[0]

    def copy(self):
        n = self.__class__()
        n.ss = copy.copy(self.ss)
        n.len = self.len
        return n


class B(object):
    def __init__(self, impl):
        self.impl = impl

    def init(self, N, randstr=randutil.insecurerandstr, rr=random.randrange):
        random.seed(76)
        self.l = []
        self.r = []
        self.a = self.impl()
        for i in range(0, N, 4096):
            self.l.append(randstr(4096))

    def init_loaded(self, N):
        self.init(N)
        for s in self.l:
            self.a.append(s)

    def _accumulate_then_one_gulp(self, N):
        for s in self.l:
            self.a.append(s)
        s = str(self.a)
        return s

    def _many_gulps_sc(self, N):
        while len(self.a):
            s = str(self.a.popleft_new_stringchain(4000))

    def _many_gulps_str(self, N):
        while len(self.a):
            s = self.a.popleft(4000)

    def _alternate_sc(self, N):
        acc=True
        i = 0
        while (i < len(self.l)) or (len(self.a) > 0):
            if (acc) or (i == len(self.l)):
                acc = False
                str(self.a.popleft_new_stringchain(3000))
            else:
                acc = True
                self.a.append(self.l[i])
                i += 1

    def _alternate_str(self, N):
        acc=True
        i = 0
        while (i < len(self.l)) or (len(self.a) > 0):
            if (acc) or (i == len(self.l)):
                acc = False
                self.a.popleft(3000)
            else:
                acc = True
                self.a.append(self.l[i])
                i += 1

def quick_bench(profile=False):
    for impl in [Stringy, StringChain]:
        print "impl: ", impl.__name__
        b = B(impl)
        for (task, initfunc) in [
            (b._accumulate_then_one_gulp, b.init),
            (b._many_gulps_str, b.init_loaded),
            (b._alternate_str, b.init),
            ]:
            print "task: ", task.__name__
            for BSIZE in [1*10**4, 5*10**4, 1*10**5, 5*10**5]:
                benchutil.rep_bench(task, BSIZE, initfunc=initfunc, MAXTIME=0.5, MAXREPS=20, profile=profile)

def slow_bench():
    for impl in [StringChain, SimplerStringChain, StringIOy,Stringy]:
        print "impl: ", impl.__name__
        b = B(impl)
        for (task, initfunc) in [
            (b._accumulate_then_one_gulp, b.init),
            (b._many_gulps_sc, b.init_loaded),
            (b._many_gulps_str, b.init_loaded),
            (b._alternate_sc, b.init),
            (b._alternate_str, b.init),
            ]:
            print "task: ", task.__name__
            for BSIZE in [1*10**4, 5*10**4, 1*10**5, 5*10**5, 1*10**6, 5*10**6]:
                benchutil.rep_bench(task, BSIZE, initfunc=initfunc)

if __name__ == "__main__":
    # for line_profiler.py
    quick_bench(False)
