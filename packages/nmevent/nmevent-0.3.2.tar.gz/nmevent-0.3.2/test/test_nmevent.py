# -*- coding: utf8 -*-

import unittest
import doctest
import sys
# sys.path.append(sys.path[0] + '/../nmevent')
sys.path.insert(1, sys.path[0] + '/../nmevent')

import nmevent

suite = unittest.TestSuite()
suite.addTests(doctest.DocFileSuite('../doc/index.rst', globs = {'nmevent': nmevent}))
suite.addTests(doctest.DocTestSuite(nmevent, {'nmevent': nmevent}))

def case(clss):
	suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(clss))
	return clss

def create_class(events = [], methods = [], attrs = {}):
	class Clss(object):
		def __init__(self):
			self.counter = 0
			for name, clss in attrs.items():
				setattr(self, name, clss())
	for event in events:
		setattr(Clss, event, nmevent.Event())
	for method in methods:
		def meth(self, *args, **keywords):
			self.counter += 1
		meth.__name__ = method
		setattr(Clss, method, meth)
	return Clss

def function_observer_a(sender, *args, **keywords):
	pass

def function_observer_b(sender, *args, **keywords):
	pass

def function_bad_observer():
	pass

class Subject(object):
	def __init__(self):
		self.event_a = nmevent.Event()
		self.event_b = nmevent.Event()

	def fire_a(self):
		self.event_a(self)

	def fire_b(self):
		self.event_b(self)

class Observer(object):
	def __init__(self):
		self.event_caught = False
		self.event_count = 0

	def handler(self, sender, *args, **keywords):
		self.event_caught = True
		self.event_count += 1

class CallableObserver(object):
	def __init__(self):
		self.event_caught = False
		self.event_count = 0
	
	def __call__(self, *args, **keywords):
		self.event_caught = True
		self.event_count += 1

@case
class WeakRefCallbackTest(unittest.TestCase):
	def setUp(self):
		class Clss(object):
			def __init__(self):
				self.foo_counter = 0
				self.bar_counter = 0
			def foo(self):
				self.foo_counter += 1
			def bar(self):
				self.bar_counter += 1
		self.Clss = Clss
		self.obj1 = self.Clss()
		self.obj2 = self.Clss()
		self.r1_foo = nmevent.WeakRefCallback(self.obj1.foo)
		self.r1_bar = nmevent.WeakRefCallback(self.obj1.bar)
		self.r2_foo = nmevent.WeakRefCallback(self.obj2.foo)
		self.r2_bar = nmevent.WeakRefCallback(self.obj2.bar)
	
	def test_method(self):
		self.assertEqual(self.obj1.foo_counter, 0)
		self.r1_foo()
		self.assertEqual(self.obj1.foo_counter, 1)
		del self.obj1
		self.r1_foo()
	
	def test_is_alive(self):
		self.assertTrue(self.r1_foo.is_alive)
		del self.obj1
		self.assertFalse(self.r1_foo.is_alive)
	
	def test_hash(self):
		self.assertEqual(hash(self.r1_foo),
			hash(nmevent.WeakRefCallback(self.obj1.foo)))
		self.assertNotEqual(hash(self.r1_foo), hash(self.r1_bar))
		self.assertNotEqual(hash(self.r1_foo), hash(self.r2_foo))

@case
class CallbackStoreTest(unittest.TestCase):
	def test_interface(self):
		store = nmevent.CallbackStore()
		observer = Observer()

		try:
			store += observer.handler
		except TypeError:
			self.fail("The \"+=\" operator is not supported.")

		try:
			store -= observer.handler
		except TypeError:
			self.fail("The \"-=\" operator is not supported.")

		try:
			observer.handler in store
		except TypeError:
			self.fail("The \"in\" operator is not supported.")

		try:
			for callback in store:
				pass
		except TypeError:
			self.fail("Iteration is not supported.")

		try:
			len(store)
		except TypeError:
			self.fail("\"len\" operator is not supported.")
	
	def test_adding(self):
		observers = [Observer(), Observer(), Observer(), ]
		store = nmevent.CallbackStore()

		self.assertEqual(len(store), 0)
		self.assertEqual(store.count(), 0)
		store += observers[0]
		self.assertEqual(len(store), 1)
		self.assertEqual(store.count(), 1)
		store += observers[0]
		self.assertEqual(len(store), 1)
		self.assertEqual(store.count(), 1)
		store += observers[1]
		self.assertEqual(len(store), 2)
		self.assertEqual(store.count(), 2)
		store += observers[2]
		self.assertEqual(len(store), 3)
		self.assertEqual(store.count(), 3)

		store = nmevent.CallbackStore()
		for x in range(100):
			observer = Observer()
			self.assertFalse(observer.handler in store)
			self.assertFalse(store.contains(observer.handler))
			store += observer.handler
			self.assertTrue(observer.handler in store)
			self.assertTrue(store.contains(observer.handler))
			self.assertEqual(len(store), x + 1)
			self.assertEqual(store.count(), x + 1)
	
	def test_removing(self):
		observers = [Observer(), Observer(), Observer(), ]
		store = nmevent.CallbackStore()

		for observer in observers:
			store += observer.handler
		for observer in observers:
			self.assertTrue(observer.handler in store)

		store -= observers[0].handler
		self.assertFalse(observers[0].handler in store)
		self.assertTrue(observers[1].handler in store)
		self.assertTrue(observers[2].handler in store)

		store -= observers[1].handler
		self.assertFalse(observers[0].handler in store)
		self.assertFalse(observers[1].handler in store)
		self.assertTrue(observers[2].handler in store)

		store -= observers[2].handler
		self.assertFalse(observers[0].handler in store)
		self.assertFalse(observers[1].handler in store)
		self.assertFalse(observers[2].handler in store)

		self.assertEqual(len(store), 0)
		self.assertEqual(store.count(), 0)
	
	def test_clearing(self):
		store = nmevent.CallbackStore()

		for x in range(100):
			observer = Observer()
			store += observer.handler

		self.assertEqual(len(store), 100)
		self.assertEqual(store.count(), 100)
		
		store.clear()
		
		self.assertEqual(len(store), 0)
		self.assertEqual(store.count(), 0)
		
		observer = Observer()
		
		store += observer.handler
		
		self.assertNotEqual(len(store), 0)
		self.assertNotEqual(store.count(), 0)
		self.assertTrue(observer.handler in store)
		
		store.clear()
		
		self.assertEqual(len(store), 0)
		self.assertEqual(store.count(), 0)
		self.assertFalse(observer.handler in store)

@case
class EventTest(unittest.TestCase):
	def test_interface(self):
		event = nmevent.Event()
		observer = Observer()
		try:
			event += observer.handler
			event(self)
			event -= observer.handler
			if observer.handler in event:
				pass
		except:
			self.fail("One of the event operations threw exception.")

	def test_adding(self):
		event = nmevent.Event()
		observers = [Observer(), Observer(), Observer()]
		
		for observer in observers:
			self.assertFalse(observer.handler in event)

		event += observers[0].handler
		self.assertTrue(observers[0].handler in event)
		self.assertFalse(observers[1].handler in event)
		self.assertFalse(observers[2].handler in event)

		event += observers[1].handler
		self.assertTrue(observers[0].handler in event)
		self.assertTrue(observers[1].handler in event)
		self.assertFalse(observers[2].handler in event)

		event += observers[2].handler
		self.assertTrue(observers[0].handler in event)
		self.assertTrue(observers[1].handler in event)
		self.assertTrue(observers[2].handler in event)
	
	def test_removing(self):
		event = nmevent.Event()
		observers = [Observer(), Observer(), Observer()]
		for observer in observers:
			self.assertFalse(observer.handler in observers)
		for observer in observers:
			event += observer.handler
		for observer in observers:
			self.assertTrue(observer.handler in event)
		for observer in observers:
			event -= observer.handler
			self.assertFalse(observer.handler in event)

	def test_fire(self):
		event = nmevent.Event()
		observers = [Observer(), Observer(), Observer()]

		event(self)
		for observer in observers:
			self.assertEqual(observer.event_count, 0)

		event += observers[0].handler
		event(self)
		self.assertEqual(observers[0].event_count, 1)
		self.assertEqual(observers[1].event_count, 0)
		self.assertEqual(observers[2].event_count, 0)

		event += observers[1].handler
		event(self)
		self.assertEqual(observers[0].event_count, 2)
		self.assertEqual(observers[1].event_count, 1)
		self.assertEqual(observers[2].event_count, 0)

		event -= observers[0].handler
		event(self)
		self.assertEqual(observers[0].event_count, 2)
		self.assertEqual(observers[1].event_count, 2)
		self.assertEqual(observers[2].event_count, 0)
	
	def test_descriptor(self):
		event1 = nmevent.Event()
		event2 = nmevent.Event()
		class TestClass(object):
			pass
		TestClass.event1 = event1
		TestClass.event2 = event2
		test1 = TestClass()
		test2 = TestClass()
		self.assertFalse(event1 is TestClass.event1)
		self.assertFalse(TestClass.event1 is test1.event1)
		self.assertFalse(test1.event1 is test2.event1)
		self.assertFalse(test1.event1 is test1.event2)
		self.assertFalse(test1.event1.im_event is test1.event2.im_event)

		self.assertTrue(isinstance(test1.event1, nmevent.InstanceEvent))

		observer1 = Observer()
		observer2 = Observer()

		test1.event1 += observer1.handler
		test1.event2 += observer2.handler
		test1.event1()
		self.assertEqual(observer1.event_count, 1)
		self.assertEqual(observer2.event_count, 0)
		test2.event1()
		self.assertEqual(observer1.event_count, 1)
		self.assertEqual(observer2.event_count, 0)
		test1.event2()
		self.assertEqual(observer1.event_count, 1)
		self.assertEqual(observer2.event_count, 1)
	
	def test_descriptor_get(self):
		class TestClass(object):
			event = nmevent.Event()
		self.assertTrue(isinstance(TestClass.__dict__['event'], nmevent.Event))
		self.assertTrue(isinstance(TestClass.event, nmevent.InstanceEvent))
		self.assertFalse(TestClass.event.is_bound)

		test1 = TestClass()
		test2 = TestClass()
		self.assertTrue(isinstance(test1.event, nmevent.InstanceEvent))
		self.assertTrue(test1.event.is_bound)
		self.assertFalse(test1.event is test2.event)
		self.assertTrue(test1.event.im_event is test2.event.im_event)
		self.assertTrue(test1.event.handlers is test1.event.handlers)
		self.assertFalse(test1.event.handlers is test2.event.handlers)
	
	def test_descriptor_set(self):
		event = nmevent.Event()
		class TestClass(object):
			pass
		TestClass.event = event
		def test():
			TestClass.event = "any value"
		#self.assertRaises(AttributeError, test)
		self.assertTrue(TestClass.__dict__['event'] is event)
	
	def test_descriptor_delete(self):
		class TestClass(object):
			event = nmevent.Event()
		inst = TestClass()
		def test():
			del inst.event
		self.assertRaises(AttributeError, test)
		self.assertTrue(isinstance(inst.event, nmevent.InstanceEvent))

@case
class InstanceEventTest(unittest.TestCase):
	def setUp(self):
		self.event = nmevent.Event()
		class TestClass(object):
			pass
		self.test_class = TestClass
		self.instance = TestClass()
		self.unbound = nmevent.InstanceEvent(self.event, TestClass)
		self.bound = nmevent.InstanceEvent(self.event, TestClass, self.instance)
	
	def test_call_unbound(self):
		def test():
			self.unbound()
		self.assertRaises(TypeError, test)

		try:
			self.unbound(self.instance)
		except TypeError:
			self.fail("Cannot call unbound event with instance.")

		def test():
			self.unbound("not a TestClass")
		self.assertRaises(TypeError, test)

	def test_call_bound(self):
		try:
			self.bound()
		except TypeError:
			self.fail("Cannot call bound event without instance.")

@case
class PropertyTest(unittest.TestCase):
	def setUp(self):
		class TestClass(object):
			def get_x(self):
				return self._x
			def set_x(self, value):
				self._x = value
			def __init__(self):
				self._x = None
			x = nmevent.Property(get_x, set_x)
			x_changed = nmevent.Event()
			x.changed = x_changed
			no_rw = nmevent.Property()
		self.test_class = TestClass
		self.instance = TestClass()
	
	def tearDown(self):
		self.test_class = None
		self.instance = None
	
	def test_get_set(self):
		try:
			self.instance.x = 13
		except AttributeError:
			self.fail("Setter threw error.")

		self.assertEqual(self.instance.x, 13)

		def test():
			self.instance.no_rw = 13
		self.assertRaises(AttributeError, test)
	
	def test_changed_event(self):
		observer = Observer()
		self.instance.x_changed += observer.handler
		self.instance.x = 1
		self.instance.x = 2
		self.instance.x = 3
		self.assertEqual(observer.event_count, 3)

@case
class WithEventsTest(unittest.TestCase):
	def test_class(self):
		@nmevent.with_events
		class C(object):
			@property
			def x(self):
				return self._x

			@property
			def y(self):
				return self._y

			def foo(self):
				pass

		self.assertTrue(hasattr(C, 'x_changed'))
		self.assertTrue(hasattr(C, 'y_changed'))
		self.assertTrue(isinstance(C.x_changed, nmevent.InstanceEvent))
		self.assertTrue(isinstance(C.y_changed, nmevent.InstanceEvent))

		self.assertFalse(hasattr(C, 'foo_changed'))

	def test_instance(self):
		@nmevent.with_events
		class C(object):
			@property
			def x(self):
				return None

			@x.setter
			def x(self, value):
				self.x_changed()

		c = C()
		
		self.assertTrue(hasattr(c, 'x_changed'))
		self.assertTrue(isinstance(c.x_changed, nmevent.InstanceEvent))

		observer = Observer()
		c.x_changed += observer.handler
		c.x = 10

		self.assertEqual(observer.event_count, 1)
	
	def test_with_nmproperty(self):
		@nmevent.with_events
		class C(object):
			@nmevent.nmproperty
			def x(self):
				return self._x
			
			@x.setter
			def x(self, value):
				self._x = value
			
			def __init__(self):
				self._x = None
		
		observer = Observer()
		
		c = C()
		self.assertTrue(hasattr(c, "x_changed"))
		self.assertTrue(isinstance(c.x_changed, nmevent.InstanceEvent))
		
		c.x_changed += observer.handler
		self.assertTrue(observer.handler in c.x_changed)
		
		c.x = 1
		c.x = 2
		self.assertEqual(observer.event_count, 2)

@case
class WithPropertiesTest(unittest.TestCase):
	def test_multiple_properties(self):
		@nmevent.with_properties
		class A(object):
			foo = nmevent.Property()
			bar = nmevent.Property()
			x = nmevent.Property()
			y = nmevent.Property()

		a = A()
		val = object()
		a.foo = val
		self.assertTrue(a.foo is val)
		self.assertFalse(a.bar is val)
		
		a.bar = object()
		self.assertTrue(a.bar is a._bar)
		self.assertTrue(a.foo is a._foo)
	
	def test_with_events(self):
		@nmevent.with_events
		@nmevent.with_properties
		class A(object):
			foo = nmevent.Property()
			bar = nmevent.Property()
		
		a = A()
		b = A()
		a.foo = object()
		self.assertTrue(a.foo is not a.bar)
		self.assertTrue(a.foo is not b.foo)
		
		observer_a = Observer()
		observer_b = Observer()
		a.foo_changed += observer_a.handler
		a.bar_changed += observer_b.handler
		a.foo = 1
		a.foo = 2
		a.foo = 3
		self.assertEqual(observer_a.event_count, 3)
		self.assertEqual(observer_b.event_count, 0)

@case
class DiscoverHandlersTest(unittest.TestCase):
	def test_simple(self):
		subject = create_class(['event_a', 'event_b', ])()
		observer = create_class([], ['on_event_a', 'on_event_b', ])()
		
		connections = list(nmevent.discover_handlers(observer, subject, "on_"))
		
		self.assertEqual(len(connections), 2)
		self.assertTrue(isinstance(connections[0][0], nmevent.InstanceEvent))
		self.assertEqual(connections[0][1], observer.on_event_a)
		self.assertTrue(isinstance(connections[1][0], nmevent.InstanceEvent))
		self.assertEqual(connections[1][1], observer.on_event_b)
	
	def test_nested(self):
		subject = create_class(['some_event'], [], {
			'attr1': create_class([], [], {
				'attr2': create_class(['some_event', ])
			}),
		})()
		observer = create_class([], ['on_attr1__attr2__some_event', ])()
		
		connections = list(nmevent.discover_handlers(observer, subject, "on_"))
		
		self.assertEqual(len(connections), 1)
		self.assertEqual(connections[0][1], observer.on_attr1__attr2__some_event)

@case
class AdaptTest(unittest.TestCase):
	def test_simple(self):
		observer = create_class([], ['on_some_event', ])()
		subject = create_class(['some_event', ])()
		nmevent.adapt(observer, subject, "on_")
		self.assertEqual(observer.counter, 0)
		subject.some_event()
		self.assertEqual(observer.counter, 1)
		subject.some_event()
		self.assertEqual(observer.counter, 2)
	
	def test_nested(self):
		subject = create_class(['some_event'], [], {
			'attr1': create_class([], [], {
				'attr2': create_class(['some_event', ])
			}),
		})()
		observer = create_class([], ['on_attr1__attr2__some_event', ])()
		nmevent.adapt(observer, subject, "on_")
		
		self.assertEqual(observer.counter, 0)
		subject.attr1.attr2.some_event()
		subject.some_event()
		self.assertEqual(observer.counter, 1)
	
	def test_disconnect(self):
		subject = create_class(['some_event', 'other_event', ], [], {
			'attr1': create_class([], [], {
				'attr2': create_class(['some_event', ])
			}),
		})()
		observer = create_class([], [
			'on_some_event',
			'on_other_event',
			'on_attr1__attr2__some_event', ])()
		nmevent.adapt(observer, subject, "on_")
		self.assertTrue(
			observer.on_attr1__attr2__some_event in subject.attr1.attr2.some_event)
		self.assertTrue(
			observer.on_some_event in subject.some_event)
		self.assertTrue(
			observer.on_other_event in subject.other_event)
		nmevent.adapt(observer, subject, "on_", True)
		self.assertFalse(
			observer.on_attr1__attr2__some_event in subject.attr1.attr2.some_event)
		self.assertFalse(
			observer.on_some_event in subject.some_event)
		self.assertFalse(
			observer.on_other_event in subject.other_event)

def run():
	runner = unittest.TextTestRunner()
	runner.run(suite)
	# unittest.main()

if __name__ == "__main__":
	run()

