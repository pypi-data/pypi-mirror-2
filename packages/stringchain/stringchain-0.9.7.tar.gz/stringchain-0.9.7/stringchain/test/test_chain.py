import unittest
from stringchain.stringchain import StringChain as BufClass
# from stringchain.bench.bench import Dequey as BufClass
# from stringchain.bench.bench import Stringy as BufClass
# from stringchain.bench.bench import StringIOy as BufClass
# from stringchain.bench.bench import SimplerStringChain as BufClass

class T(unittest.TestCase):
    def test_al(self):
        c = BufClass()
        c.append("ab")
        self.failUnlessEqual(len(c), 2)
        c.append("")
        self.failUnlessEqual(len(c), 2)
        c.append("c")
        self.failUnlessEqual(len(c), 3)

    def test_str(self):
        c = BufClass()
        c.append("ab")
        c.append("c")
        self.failUnlessEqual(str(c), "abc")

    def test_trim(self):
        c = BufClass()
        c.append("ab")
        c.append("c")
        c.trim(1)
        self.failUnlessEqual(str(c.copy()), "bc")
        c.trim(1)
        self.failUnlessEqual(str(c.copy()), "c")
        c.trim(1)
        self.failUnlessEqual(str(c.copy()), "")
        c.append("ab")
        c.append("c")
        c.trim(2)
        self.failUnlessEqual(str(c.copy()), "c")
        c.trim(1)
        self.failUnlessEqual(str(c.copy()), "")
        c.append("a")
        c.append("bc")
        c.trim(2)
        self.failUnlessEqual(str(c.copy()), "c")
        c.trim(1)
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        c.trim(4) # We just silently trim all.
        self.failUnlessEqual(str(c.copy()), "")

    def test_popleft_new_stringchain(self):
        c = BufClass()
        c.append("ab")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "a")
        self.failUnlessEqual(str(c.copy()), "b")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "b")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "a")
        self.failUnlessEqual(str(c.copy()), "bc")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "b")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft_new_stringchain(2)
        self.failUnlessEqual(str(s), "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("ab")
        c.append("c")
        s = c.popleft_new_stringchain(2)
        self.failUnlessEqual(str(s), "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("a")
        c.append("bc")
        s = c.popleft_new_stringchain(2)
        self.failUnlessEqual(str(s), "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft_new_stringchain(1)
        self.failUnlessEqual(str(s), "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft_new_stringchain(4) # We just silently pop them all.
        self.failUnlessEqual(str(s), "abc")
        self.failUnlessEqual(str(c.copy()), "")

    def test_popleft(self):
        c = BufClass()
        c.append("ab")
        s = c.popleft(1)
        self.failUnlessEqual(s, "a")
        self.failUnlessEqual(str(c.copy()), "b")
        s = c.popleft(1)
        self.failUnlessEqual(s, "b")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft(1)
        self.failUnlessEqual(s, "a")
        self.failUnlessEqual(str(c.copy()), "bc")
        s = c.popleft(1)
        self.failUnlessEqual(s, "b")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft(1)
        self.failUnlessEqual(s, "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft(2)
        self.failUnlessEqual(s, "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft(1)
        self.failUnlessEqual(s, "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("ab")
        c.append("c")
        s = c.popleft(2)
        self.failUnlessEqual(s, "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft(1)
        self.failUnlessEqual(s, "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("a")
        c.append("bc")
        s = c.popleft(2)
        self.failUnlessEqual(s, "ab")
        self.failUnlessEqual(str(c.copy()), "c")
        s = c.popleft(1)
        self.failUnlessEqual(s, "c")
        self.failUnlessEqual(str(c.copy()), "")

        c.append("abc")
        s = c.popleft(4) # We just silently pop them all.
        self.failUnlessEqual(s, "abc")
        self.failUnlessEqual(str(c.copy()), "")

    def test_tailignored(self):
        c1 = BufClass()
        c1.append("abcde")
        c2 = c1.popleft_new_stringchain(2)
        assert str(c2.copy()) == "ab", (str(c2.copy()),)
        c2.append("f")
        self.failUnlessEqual(str(c2.copy()), "abf")

    def test_appendleft(self):
        c1 = BufClass()
        c1.append("abcd")
        c1.appendleft("ef")
        self.failUnlessEqual(str(c1.copy()), "efabcd")
        s = c1.popleft(1)
        self.failUnlessEqual(s, "e")
        s = c1.popleft(2)
        self.failUnlessEqual(s, "fa")
        s = c1.popleft(3)
        self.failUnlessEqual(s, "bcd")

        c1 = BufClass()
        c1.append("abcd")
        c1.popleft(1)
        c1.appendleft("ef")
        self.failUnlessEqual(str(c1.copy()), "efbcd")
        s = c1.popleft(1)
        self.failUnlessEqual(s, "e")
        s = c1.popleft(2)
        self.failUnlessEqual(s, "fb")
        s = c1.popleft(3)
        self.failUnlessEqual(s, "cd")

    def test_clear(self):
        c1 = BufClass()
        c1.append("abcd")
        c1.clear()
        self.failUnlessEqual(str(c1.copy()), '')
