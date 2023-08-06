import unittest

from pykka import Actor

class MethodCallTest(unittest.TestCase):
    def setUp(self):
        class ActorWithMethods(Actor):
            foo = 'bar'
            def functional_hello(self, s):
                return 'Hello, %s!' % s
            def set_foo(self, s):
                self.foo = s
        self.actor = ActorWithMethods.start()

    def tearDown(self):
        self.actor.stop()

    def test_functional_method_call_returns_correct_value(self):
        self.assertEqual('Hello, world!',
            self.actor.functional_hello('world').get())
        self.assertEqual('Hello, moon!',
            self.actor.functional_hello('moon').get())

    def test_side_effect_of_method_is_observable(self):
        self.assertEqual('bar', self.actor.foo.get())
        self.actor.set_foo('baz')
        self.assertEqual('baz', self.actor.foo.get())

    def test_calling_unknown_method_raises_attribute_error(self):
        try:
            self.actor.unknown_method()
            self.fail('Should raise AttributeError')
        except AttributeError as e:
            self.assertEquals("proxy for 'ActorWithMethods' object " +
                "has no attribute 'unknown_method'", str(e))


class MethodAddedAtRuntimeTest(unittest.TestCase):
    def setUp(self):
        class ActorExtendableAtRuntime(Actor):
            def add_method(self, name):
                setattr(self, name, lambda: 'returned by ' + name)
        self.actor = ActorExtendableAtRuntime().start()

    def tearDown(self):
        self.actor.stop()

    def test_can_call_method_that_was_added_at_runtime(self):
        self.actor.add_method('foo')
        self.assertEqual('returned by foo', self.actor.foo().get())
