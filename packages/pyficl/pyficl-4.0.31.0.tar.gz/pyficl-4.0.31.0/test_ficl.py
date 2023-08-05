import pyficl
import array
import unittest

class TestPyFICL(unittest.TestCase):

    def setUp(self):
        self.s = pyficl.System()
        di = self.s.getDictionary()
        di.setPrimitive("dosomething", lambda vm: vm.evaluate("947"))

    def test_simple(self):
        vm = self.s.createVm()
        stk = vm.getDataStack()
        self.assertEqual(stk.depth(), 0)
        stk.push(77)
        self.assertEqual(stk.depth(), 1)
        self.assertEqual(stk.pop(), 77)

    def test_float(self):
        vm = self.s.createVm()
        stk = vm.getFloatStack()
        stk.pushFloat(3.0)
        stk.pushFloat(11.0)
        vm.evaluate("f+")
        self.assertEqual(stk.popFloat(), 14.0)

    def test_range(self):
        vm = self.s.createVm()
        stk = vm.getDataStack()
        minint = -(2**31)
        maxint = (2**31) - 1
        for v in [ minint, -1, 0, 1, maxint ]:
            vm.evaluate(str(v))
            self.assertEqual(stk.pop(), v)

    def test_str(self):
        vm = self.s.createVm()
        stk = vm.getDataStack()
        for s in ['', 'x', 'Hello', chr(0), chr(0) * 100]:
            stk.reset()
            stk.pushStr(s)
            vm.evaluate(': expands 0 ?do count swap loop drop ; expands')
            self.assertEqual(list(stk), [ord(c) for c in s][::-1])
        stk.reset()
        stk.pushStr("foo")
        self.assertEqual(stk.popStr(), "foo")

        for i in range(1000):
            stk.push(i)
            vm.evaluate("decimal s>d <# #s #>")
            self.assertEqual(stk.popStr(), str(i))

    def test_buffer(self):
        vm = self.s.createVm()
        stk = vm.getDataStack()
        txt = "BUFFERS ARE WORKING"
        a = array.array('B', txt)
        stk.pushBuffer(a)
        self.assertEqual(stk.popStr(), txt)

    def test_callback(self):
        def square(vm):
            stk = vm.getDataStack()
            stk.push(stk.pop() ** 2)

        vm = self.s.createVm()
        stk = vm.getDataStack()
        self.assertEqual(stk.depth(), 0)
        di = self.s.getDictionary()
        di.setPrimitive("square", square)
        for i in range(10):
            stk.push(i)
            vm.evaluate("square")
            self.assertEqual(stk.pop(), i * i)

    def test_callback_lambda(self):
        vm = self.s.createVm()
        stk = vm.getDataStack()
        vm.evaluate("dosomething")
        self.assertEqual(stk.pop(), 947)

    def ztest_error(self):
        vm = self.s.createVm()
        vm.evaluate("947 0 / . cr")

if __name__ == '__main__':
    unittest.main()

