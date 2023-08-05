import pickle
import sqlalchemy.orm.attributes as attributes
from sqlalchemy.orm.collections import collection
from sqlalchemy.orm.interfaces import AttributeExtension
from sqlalchemy import exc as sa_exc
from sqlalchemy.test import *
from sqlalchemy.test.testing import eq_, ne_, assert_raises
from test.orm import _base
from sqlalchemy.test.util import gc_collect
from sqlalchemy.util import cmp, jython

# global for pickling tests
MyTest = None
MyTest2 = None


class AttributesTest(_base.ORMTest):
    def setup(self):
        global MyTest, MyTest2
        class MyTest(object): pass
        class MyTest2(object): pass

    def teardown(self):
        global MyTest, MyTest2
        MyTest, MyTest2 = None, None

    def test_basic(self):
        class User(object):pass

        attributes.register_class(User)
        attributes.register_attribute(User, 'user_id', uselist=False, useobject=False)
        attributes.register_attribute(User, 'user_name', uselist=False, useobject=False)
        attributes.register_attribute(User, 'email_address', uselist=False, useobject=False)

        u = User()
        u.user_id = 7
        u.user_name = 'john'
        u.email_address = 'lala@123.com'

        self.assert_(u.user_id == 7 and u.user_name == 'john' and u.email_address == 'lala@123.com')
        attributes.instance_state(u).commit_all(attributes.instance_dict(u))
        self.assert_(u.user_id == 7 and u.user_name == 'john' and u.email_address == 'lala@123.com')

        u.user_name = 'heythere'
        u.email_address = 'foo@bar.com'
        self.assert_(u.user_id == 7 and u.user_name == 'heythere' and u.email_address == 'foo@bar.com')

    def test_pickleness(self):
        attributes.register_class(MyTest)
        attributes.register_class(MyTest2)
        attributes.register_attribute(MyTest, 'user_id', uselist=False, useobject=False)
        attributes.register_attribute(MyTest, 'user_name', uselist=False, useobject=False)
        attributes.register_attribute(MyTest, 'email_address', uselist=False, useobject=False)
        attributes.register_attribute(MyTest, 'some_mutable_data', mutable_scalars=True, copy_function=list, compare_function=cmp, uselist=False, useobject=False)
        attributes.register_attribute(MyTest2, 'a', uselist=False, useobject=False)
        attributes.register_attribute(MyTest2, 'b', uselist=False, useobject=False)
        # shouldnt be pickling callables at the class level
        def somecallable(*args, **kw):
            return None
        attributes.register_attribute(MyTest, "mt2", uselist = True, trackparent=True, callable_=somecallable, useobject=True)

        o = MyTest()
        o.mt2.append(MyTest2())
        o.user_id=7
        o.some_mutable_data = [1,2,3]
        o.mt2[0].a = 'abcde'
        pk_o = pickle.dumps(o)

        o2 = pickle.loads(pk_o)
        pk_o2 = pickle.dumps(o2)

        # so... pickle is creating a new 'mt2' string after a roundtrip here,
        # so we'll brute-force set it to be id-equal to the original string
        if False:
            o_mt2_str = [ k for k in o.__dict__ if k == 'mt2'][0]
            o2_mt2_str = [ k for k in o2.__dict__ if k == 'mt2'][0]
            self.assert_(o_mt2_str == o2_mt2_str)
            self.assert_(o_mt2_str is not o2_mt2_str)
            # change the id of o2.__dict__['mt2']
            former = o2.__dict__['mt2']
            del o2.__dict__['mt2']
            o2.__dict__[o_mt2_str] = former

            # Relies on dict ordering
            if not jython:
                self.assert_(pk_o == pk_o2)

        # the above is kind of distrurbing, so let's do it again a little
        # differently.  the string-id in serialization thing is just an
        # artifact of pickling that comes up in the first round-trip.
        # a -> b differs in pickle memoization of 'mt2', but b -> c will
        # serialize identically.

        o3 = pickle.loads(pk_o2)
        pk_o3 = pickle.dumps(o3)
        o4 = pickle.loads(pk_o3)
        pk_o4 = pickle.dumps(o4)

        # Relies on dict ordering
        if not jython:
            self.assert_(pk_o3 == pk_o4)

        # and lastly make sure we still have our data after all that.
        # identical serialzation is great, *if* it's complete :)
        self.assert_(o4.user_id == 7)
        self.assert_(o4.user_name is None)
        self.assert_(o4.email_address is None)
        self.assert_(o4.some_mutable_data == [1,2,3])
        self.assert_(len(o4.mt2) == 1)
        self.assert_(o4.mt2[0].a == 'abcde')
        self.assert_(o4.mt2[0].b is None)
    
    def test_state_gc(self):
        """test that InstanceState always has a dict, even after host object gc'ed."""
        
        class Foo(object):
            pass
        
        attributes.register_class(Foo)
        f = Foo()
        state = attributes.instance_state(f)
        f.bar = "foo"
        assert state.dict == {'bar':'foo', state.manager.STATE_ATTR:state}
        del f
        gc_collect()
        assert state.obj() is None
        assert state.dict == {}
        
    def test_deferred(self):
        class Foo(object):pass

        data = {'a':'this is a', 'b':12}
        def loader(state, keys):
            for k in keys:
                state.dict[k] = data[k]
            return attributes.ATTR_WAS_SET

        attributes.register_class(Foo)
        manager = attributes.manager_of_class(Foo)
        manager.deferred_scalar_loader = loader
        attributes.register_attribute(Foo, 'a', uselist=False, useobject=False)
        attributes.register_attribute(Foo, 'b', uselist=False, useobject=False)

        f = Foo()
        attributes.instance_state(f).expire_attributes(attributes.instance_dict(f), None)
        eq_(f.a, "this is a")
        eq_(f.b, 12)

        f.a = "this is some new a"
        attributes.instance_state(f).expire_attributes(attributes.instance_dict(f), None)
        eq_(f.a, "this is a")
        eq_(f.b, 12)

        attributes.instance_state(f).expire_attributes(attributes.instance_dict(f), None)
        f.a = "this is another new a"
        eq_(f.a, "this is another new a")
        eq_(f.b, 12)

        attributes.instance_state(f).expire_attributes(attributes.instance_dict(f), None)
        eq_(f.a, "this is a")
        eq_(f.b, 12)

        del f.a
        eq_(f.a, None)
        eq_(f.b, 12)

        attributes.instance_state(f).commit_all(attributes.instance_dict(f))
        eq_(f.a, None)
        eq_(f.b, 12)

    def test_deferred_pickleable(self):
        data = {'a':'this is a', 'b':12}
        def loader(state, keys):
            for k in keys:
                state.dict[k] = data[k]
            return attributes.ATTR_WAS_SET

        attributes.register_class(MyTest)
        manager = attributes.manager_of_class(MyTest)
        manager.deferred_scalar_loader=loader
        attributes.register_attribute(MyTest, 'a', uselist=False, useobject=False)
        attributes.register_attribute(MyTest, 'b', uselist=False, useobject=False)

        m = MyTest()
        attributes.instance_state(m).expire_attributes(attributes.instance_dict(m), None)
        assert 'a' not in m.__dict__
        m2 = pickle.loads(pickle.dumps(m))
        assert 'a' not in m2.__dict__
        eq_(m2.a, "this is a")
        eq_(m2.b, 12)

    def test_list(self):
        class User(object):pass
        class Address(object):pass

        attributes.register_class(User)
        attributes.register_class(Address)
        attributes.register_attribute(User, 'user_id', uselist=False, useobject=False)
        attributes.register_attribute(User, 'user_name', uselist=False, useobject=False)
        attributes.register_attribute(User, 'addresses', uselist = True, useobject=True)
        attributes.register_attribute(Address, 'address_id', uselist=False, useobject=False)
        attributes.register_attribute(Address, 'email_address', uselist=False, useobject=False)

        u = User()
        u.user_id = 7
        u.user_name = 'john'
        u.addresses = []
        a = Address()
        a.address_id = 10
        a.email_address = 'lala@123.com'
        u.addresses.append(a)

        self.assert_(u.user_id == 7 and u.user_name == 'john' and u.addresses[0].email_address == 'lala@123.com')
        u, attributes.instance_state(a).commit_all(attributes.instance_dict(a))
        self.assert_(u.user_id == 7 and u.user_name == 'john' and u.addresses[0].email_address == 'lala@123.com')

        u.user_name = 'heythere'
        a = Address()
        a.address_id = 11
        a.email_address = 'foo@bar.com'
        u.addresses.append(a)
        self.assert_(u.user_id == 7 and u.user_name == 'heythere' and u.addresses[0].email_address == 'lala@123.com' and u.addresses[1].email_address == 'foo@bar.com')
    
    def test_extension_commit_attr(self):
        """test that an extension which commits attribute history
        maintains the end-result history.
        
        This won't work in conjunction with some unitofwork extensions.
        
        """
        
        class Foo(_base.ComparableEntity):
            pass
        class Bar(_base.ComparableEntity):
            pass
        
        class ReceiveEvents(AttributeExtension):
            def __init__(self, key):
                self.key = key
                
            def append(self, state, child, initiator):
                if commit:
                    state.commit_all(state.dict)
                return child

            def remove(self, state, child, initiator):
                if commit:
                    state.commit_all(state.dict)
                return child

            def set(self, state, child, oldchild, initiator):
                if commit:
                    state.commit_all(state.dict)
                return child

        attributes.register_class(Foo)
        attributes.register_class(Bar)

        b1, b2, b3, b4 = Bar(id='b1'), Bar(id='b2'), Bar(id='b3'), Bar(id='b4')
        
        def loadcollection(**kw):
            if kw.get('passive') is attributes.PASSIVE_NO_FETCH:
                return attributes.PASSIVE_NO_RESULT
            return [b1, b2]
        
        def loadscalar(**kw):
            if kw.get('passive') is attributes.PASSIVE_NO_FETCH:
                return attributes.PASSIVE_NO_RESULT
            return b2
            
        attributes.register_attribute(Foo, 'bars', 
                               uselist=True, 
                               useobject=True, 
                               callable_=lambda o:loadcollection,
                               extension=[ReceiveEvents('bars')])
                               
        attributes.register_attribute(Foo, 'bar', 
                              uselist=False, 
                              useobject=True, 
                              callable_=lambda o:loadscalar,
                              extension=[ReceiveEvents('bar')])
                              
        attributes.register_attribute(Foo, 'scalar', 
                            uselist=False, 
                            useobject=False, extension=[ReceiveEvents('scalar')])
        
            
        def create_hist():
            def hist(key, shouldmatch, fn, *arg):
                attributes.instance_state(f1).commit_all(attributes.instance_dict(f1))
                fn(*arg)
                histories.append((shouldmatch, attributes.get_history(f1, key)))

            f1 = Foo()
            hist('bars', True, f1.bars.append, b3)
            hist('bars', True, f1.bars.append, b4)
            hist('bars', False, f1.bars.remove, b2)
            hist('bar', True, setattr, f1, 'bar', b3)
            hist('bar', True, setattr, f1, 'bar', None)
            hist('bar', True, setattr, f1, 'bar', b4)
            hist('scalar', True, setattr, f1, 'scalar', 5)
            hist('scalar', True, setattr, f1, 'scalar', None)
            hist('scalar', True, setattr, f1, 'scalar', 4)
        
        histories = []
        commit = False
        create_hist()
        without_commit = list(histories)
        histories[:] = []
        commit = True
        create_hist()
        with_commit = histories
        for without, with_ in zip(without_commit, with_commit):
            shouldmatch, woc = without
            shouldmatch, wic = with_
            if shouldmatch:
                eq_(woc, wic)
            else:
                ne_(woc, wic)
        
    def test_extension_lazyload_assertion(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        class ReceiveEvents(AttributeExtension):
            def append(self, state, child, initiator):
                state.obj().bars
                return child

            def remove(self, state, child, initiator):
                state.obj().bars
                return child

            def set(self, state, child, oldchild, initiator):
                return child

        attributes.register_class(Foo)
        attributes.register_class(Bar)

        bar1, bar2, bar3 = [Bar(id=1), Bar(id=2), Bar(id=3)]
        def func1(**kw):
            if kw.get('passive') is attributes.PASSIVE_NO_FETCH:
                return attributes.PASSIVE_NO_RESULT
            
            return [bar1, bar2, bar3]

        attributes.register_attribute(Foo, 'bars', uselist=True, callable_=lambda o:func1, useobject=True, extension=[ReceiveEvents()])
        attributes.register_attribute(Bar, 'foos', uselist=True, useobject=True, extension=[attributes.GenericBackrefExtension('bars')])

        x = Foo()
        assert_raises(AssertionError, Bar(id=4).foos.append, x)
        
        x.bars
        b = Bar(id=4)
        b.foos.append(x)
        attributes.instance_state(x).expire_attributes(attributes.instance_dict(x), ['bars'])
        assert_raises(AssertionError, b.foos.remove, x)
        
        
    def test_scalar_listener(self):
        # listeners on ScalarAttributeImpl and MutableScalarAttributeImpl aren't used normally.
        # test that they work for the benefit of user extensions
        class Foo(object):
            pass
        
        results = []
        class ReceiveEvents(AttributeExtension):
            def append(self, state, child, initiator):
                assert False

            def remove(self, state, child, initiator):
                results.append(("remove", state.obj(), child))

            def set(self, state, child, oldchild, initiator):
                results.append(("set", state.obj(), child, oldchild))
                return child
        
        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'x', uselist=False, mutable_scalars=False, useobject=False, extension=ReceiveEvents())
        attributes.register_attribute(Foo, 'y', uselist=False, mutable_scalars=True, useobject=False, copy_function=lambda x:x, extension=ReceiveEvents())
        
        f = Foo()
        f.x = 5
        f.x = 17
        del f.x
        f.y = [1,2,3]
        f.y = [4,5,6]
        del f.y
        
        eq_(results, [
            ('set', f, 5, None),
            ('set', f, 17, 5),
            ('remove', f, 17),
            ('set', f, [1,2,3], None),
            ('set', f, [4,5,6], [1,2,3]),
            ('remove', f, [4,5,6])
        ])
        
        
    def test_lazytrackparent(self):
        """test that the "hasparent" flag works properly 
           when lazy loaders and backrefs are used
           
        """

        class Post(object):pass
        class Blog(object):pass
        attributes.register_class(Post)
        attributes.register_class(Blog)

        # set up instrumented attributes with backrefs
        attributes.register_attribute(Post, 'blog', uselist=False,
                                        extension=attributes.GenericBackrefExtension('posts'),
                                        trackparent=True, useobject=True)
        attributes.register_attribute(Blog, 'posts', uselist=True,
                                        extension=attributes.GenericBackrefExtension('blog'),
                                        trackparent=True, useobject=True)

        # create objects as if they'd been freshly loaded from the database (without history)
        b = Blog()
        p1 = Post()
        attributes.instance_state(b).set_callable(attributes.instance_dict(b), 
                                                    'posts', lambda **kw:[p1])
        attributes.instance_state(p1).set_callable(attributes.instance_dict(p1), 
                                                    'blog', lambda **kw:b)
        p1, attributes.instance_state(b).commit_all(attributes.instance_dict(b))

        # no orphans (called before the lazy loaders fire off)
        assert attributes.has_parent(Blog, p1, 'posts', optimistic=True)
        assert attributes.has_parent(Post, b, 'blog', optimistic=True)

        # assert connections
        assert p1.blog is b
        assert p1 in b.posts

        # manual connections
        b2 = Blog()
        p2 = Post()
        b2.posts.append(p2)
        assert attributes.has_parent(Blog, p2, 'posts')
        assert attributes.has_parent(Post, b2, 'blog')

    def test_inheritance(self):
        """tests that attributes are polymorphic"""
        class Foo(object):pass
        class Bar(Foo):pass


        attributes.register_class(Foo)
        attributes.register_class(Bar)

        def func1(**kw):
            return "this is the foo attr"
        def func2(**kw):
            return "this is the bar attr"
        def func3(**kw):
            return "this is the shared attr"
        attributes.register_attribute(Foo, 'element', uselist=False, 
                                            callable_=lambda o:func1, useobject=True)
        attributes.register_attribute(Foo, 'element2', uselist=False, 
                                            callable_=lambda o:func3, useobject=True)
        attributes.register_attribute(Bar, 'element', uselist=False, 
                                            callable_=lambda o:func2, useobject=True)

        x = Foo()
        y = Bar()
        assert x.element == 'this is the foo attr'
        assert y.element == 'this is the bar attr'
        assert x.element2 == 'this is the shared attr'
        assert y.element2 == 'this is the shared attr'

    def test_no_double_state(self):
        states = set()
        class Foo(object):
            def __init__(self):
                states.add(attributes.instance_state(self))
        class Bar(Foo):
            def __init__(self):
                states.add(attributes.instance_state(self))
                Foo.__init__(self)


        attributes.register_class(Foo)
        attributes.register_class(Bar)

        b = Bar()
        eq_(len(states), 1)
        eq_(list(states)[0].obj(), b)


    def test_inheritance2(self):
        """test that the attribute manager can properly traverse the managed attributes of an object,
        if the object is of a descendant class with managed attributes in the parent class"""
        class Foo(object):pass
        class Bar(Foo):pass

        class Element(object):
            _state = True

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'element', uselist=False, useobject=True)
        el = Element()
        x = Bar()
        x.element = el
        eq_(attributes.get_state_history(attributes.instance_state(x), 'element'), ([el], (), ()))
        attributes.instance_state(x).commit_all(attributes.instance_dict(x))

        (added, unchanged, deleted) = attributes.get_state_history(attributes.instance_state(x), 'element')
        assert added == ()
        assert unchanged == [el]

    def test_lazyhistory(self):
        """tests that history functions work with lazy-loading attributes"""

        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_class(Bar)

        bar1, bar2, bar3, bar4 = [Bar(id=1), Bar(id=2), Bar(id=3), Bar(id=4)]
        def func1(**kw):
            return "this is func 1"
        def func2(**kw):
            return [bar1, bar2, bar3]

        attributes.register_attribute(Foo, 'col1', uselist=False, callable_=lambda o:func1, useobject=True)
        attributes.register_attribute(Foo, 'col2', uselist=True, callable_=lambda o:func2, useobject=True)
        attributes.register_attribute(Bar, 'id', uselist=False, useobject=True)

        x = Foo()
        attributes.instance_state(x).commit_all(attributes.instance_dict(x))
        x.col2.append(bar4)
        eq_(attributes.get_state_history(attributes.instance_state(x), 'col2'), ([bar4], [bar1, bar2, bar3], []))

    def test_parenttrack(self):
        class Foo(object):pass
        class Bar(object):pass

        attributes.register_class(Foo)
        attributes.register_class(Bar)

        attributes.register_attribute(Foo, 'element', uselist=False, trackparent=True, useobject=True)
        attributes.register_attribute(Bar, 'element', uselist=False, trackparent=True, useobject=True)

        f1 = Foo()
        f2 = Foo()
        b1 = Bar()
        b2 = Bar()

        f1.element = b1
        b2.element = f2

        assert attributes.has_parent(Foo, b1, 'element')
        assert not attributes.has_parent(Foo, b2, 'element')
        assert not attributes.has_parent(Foo, f2, 'element')
        assert attributes.has_parent(Bar, f2, 'element')

        b2.element = None
        assert not attributes.has_parent(Bar, f2, 'element')

        # test that double assignment doesn't accidentally reset the 'parent' flag.
        b3 = Bar()
        f4 = Foo()
        b3.element = f4
        assert attributes.has_parent(Bar, f4, 'element')
        b3.element = f4
        assert attributes.has_parent(Bar, f4, 'element')

    def test_mutablescalars(self):
        """test detection of changes on mutable scalar items"""
        class Foo(object):pass

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'element', uselist=False, copy_function=lambda x:[y for y in x], mutable_scalars=True, useobject=False)
        x = Foo()
        x.element = ['one', 'two', 'three']
        attributes.instance_state(x).commit_all(attributes.instance_dict(x))
        x.element[1] = 'five'
        assert attributes.instance_state(x).modified

        attributes.unregister_class(Foo)

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'element', uselist=False, useobject=False)
        x = Foo()
        x.element = ['one', 'two', 'three']
        attributes.instance_state(x).commit_all(attributes.instance_dict(x))
        x.element[1] = 'five'
        assert not attributes.instance_state(x).modified

    def test_descriptorattributes(self):
        """changeset: 1633 broke ability to use ORM to map classes with unusual
        descriptor attributes (for example, classes that inherit from ones
        implementing zope.interface.Interface).
        This is a simple regression test to prevent that defect.
        """
        class des(object):
            def __get__(self, instance, owner):
                raise AttributeError('fake attribute')

        class Foo(object):
            A = des()

        attributes.register_class(Foo)
        attributes.unregister_class(Foo)

    def test_collectionclasses(self):

        class Foo(object):pass
        attributes.register_class(Foo)

        attributes.register_attribute(Foo, "collection", uselist=True, typecallable=set, useobject=True)
        assert attributes.manager_of_class(Foo).is_instrumented("collection")
        assert isinstance(Foo().collection, set)

        attributes.unregister_attribute(Foo, "collection")
        assert not attributes.manager_of_class(Foo).is_instrumented("collection")
        
        try:
            attributes.register_attribute(Foo, "collection", uselist=True, typecallable=dict, useobject=True)
            assert False
        except sa_exc.ArgumentError, e:
            assert str(e) == "Type InstrumentedDict must elect an appender method to be a collection class"

        class MyDict(dict):
            @collection.appender
            def append(self, item):
                self[item.foo] = item
            @collection.remover
            def remove(self, item):
                del self[item.foo]
        attributes.register_attribute(Foo, "collection", uselist=True, typecallable=MyDict, useobject=True)
        assert isinstance(Foo().collection, MyDict)

        attributes.unregister_attribute(Foo, "collection")

        class MyColl(object):pass
        try:
            attributes.register_attribute(Foo, "collection", uselist=True, typecallable=MyColl, useobject=True)
            assert False
        except sa_exc.ArgumentError, e:
            assert str(e) == "Type MyColl must elect an appender method to be a collection class"

        class MyColl(object):
            @collection.iterator
            def __iter__(self):
                return iter([])
            @collection.appender
            def append(self, item):
                pass
            @collection.remover
            def remove(self, item):
                pass
        attributes.register_attribute(Foo, "collection", uselist=True, typecallable=MyColl, useobject=True)
        try:
            Foo().collection
            assert True
        except sa_exc.ArgumentError, e:
            assert False

class UtilTest(_base.ORMTest):
    def test_helpers(self):
        class Foo(object):
            pass

        class Bar(object):
            pass
        
        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, "coll", uselist=True, useobject=True)
    
        f1 = Foo()
        b1 = Bar()
        b2 = Bar()
        coll = attributes.init_collection(f1, "coll")
        assert coll.data is f1.coll
        assert attributes.get_attribute(f1, "coll") is f1.coll
        attributes.set_attribute(f1, "coll", [b1])
        assert f1.coll == [b1]
        eq_(attributes.get_history(f1, "coll"), ([b1], [], []))
        attributes.set_committed_value(f1, "coll", [b2])
        eq_(attributes.get_history(f1, "coll"), ((), [b2], ()))
        
        attributes.del_attribute(f1, "coll")
        assert "coll" not in f1.__dict__

class BackrefTest(_base.ORMTest):

    def test_manytomany(self):
        class Student(object):pass
        class Course(object):pass

        attributes.register_class(Student)
        attributes.register_class(Course)
        attributes.register_attribute(Student, 'courses', uselist=True, extension=attributes.GenericBackrefExtension('students'), useobject=True)
        attributes.register_attribute(Course, 'students', uselist=True, extension=attributes.GenericBackrefExtension('courses'), useobject=True)

        s = Student()
        c = Course()
        s.courses.append(c)
        self.assert_(c.students == [s])
        s.courses.remove(c)
        self.assert_(c.students == [])

        (s1, s2, s3) = (Student(), Student(), Student())

        c.students = [s1, s2, s3]
        self.assert_(s2.courses == [c])
        self.assert_(s1.courses == [c])
        s1.courses.remove(c)
        self.assert_(c.students == [s2,s3])

    def test_onetomany(self):
        class Post(object):pass
        class Blog(object):pass

        attributes.register_class(Post)
        attributes.register_class(Blog)
        attributes.register_attribute(Post, 'blog', uselist=False, extension=attributes.GenericBackrefExtension('posts'), trackparent=True, useobject=True)
        attributes.register_attribute(Blog, 'posts', uselist=True, extension=attributes.GenericBackrefExtension('blog'), trackparent=True, useobject=True)
        b = Blog()
        (p1, p2, p3) = (Post(), Post(), Post())
        b.posts.append(p1)
        b.posts.append(p2)
        b.posts.append(p3)
        self.assert_(b.posts == [p1, p2, p3])
        self.assert_(p2.blog is b)

        p3.blog = None
        self.assert_(b.posts == [p1, p2])
        p4 = Post()
        p4.blog = b
        self.assert_(b.posts == [p1, p2, p4])

        p4.blog = b
        p4.blog = b
        self.assert_(b.posts == [p1, p2, p4])

        # assert no failure removing None
        p5 = Post()
        p5.blog = None
        del p5.blog

    def test_onetoone(self):
        class Port(object):pass
        class Jack(object):pass
        attributes.register_class(Port)
        attributes.register_class(Jack)
        attributes.register_attribute(Port, 'jack', uselist=False, extension=attributes.GenericBackrefExtension('port'), useobject=True)
        attributes.register_attribute(Jack, 'port', uselist=False, extension=attributes.GenericBackrefExtension('jack'), useobject=True)
        p = Port()
        j = Jack()
        p.jack = j
        self.assert_(j.port is p)
        self.assert_(p.jack is not None)

        j.port = None
        self.assert_(p.jack is None)

class PendingBackrefTest(_base.ORMTest):
    def setup(self):
        global Post, Blog, called, lazy_load

        class Post(object):
            def __init__(self, name):
                self.name = name
            __hash__ = None
            def __eq__(self, other):
                return other is not None and other.name == self.name

        class Blog(object):
            def __init__(self, name):
                self.name = name
            __hash__ = None
            def __eq__(self, other):
                return other is not None and other.name == self.name

        called = [0]

        lazy_load = []
        def lazy_posts(instance):
            def load(**kw):
                if kw['passive'] is not attributes.PASSIVE_NO_FETCH:
                    called[0] += 1
                    return lazy_load
                else:
                    return attributes.PASSIVE_NO_RESULT
            return load

        attributes.register_class(Post)
        attributes.register_class(Blog)
        attributes.register_attribute(Post, 'blog', uselist=False, extension=attributes.GenericBackrefExtension('posts'), trackparent=True, useobject=True)
        attributes.register_attribute(Blog, 'posts', uselist=True, extension=attributes.GenericBackrefExtension('blog'), callable_=lazy_posts, trackparent=True, useobject=True)

    def test_lazy_add(self):
        global lazy_load

        p1, p2, p3 = Post("post 1"), Post("post 2"), Post("post 3")
        lazy_load = [p1, p2, p3]

        b = Blog("blog 1")
        p = Post("post 4")
        
        p.blog = b
        p = Post("post 5")
        p.blog = b
        # setting blog doesnt call 'posts' callable
        assert called[0] == 0

        # calling backref calls the callable, populates extra posts
        assert b.posts == [p1, p2, p3, Post("post 4"), Post("post 5")]
        assert called[0] == 1
    
    def test_lazy_history(self):
        global lazy_load

        p1, p2, p3 = Post("post 1"), Post("post 2"), Post("post 3")
        lazy_load = [p1, p2, p3]
        
        b = Blog("blog 1")
        p = Post("post 4")
        p.blog = b
        
        p4 = Post("post 5")
        p4.blog = b
        assert called[0] == 0
        eq_(attributes.instance_state(b).get_history('posts'), ([p, p4], [p1, p2, p3], []))
        assert called[0] == 1

    def test_lazy_remove(self):
        global lazy_load
        called[0] = 0
        lazy_load = []

        b = Blog("blog 1")
        p = Post("post 1")
        p.blog = b
        assert called[0] == 0

        lazy_load = [p]

        p.blog = None
        p2 = Post("post 2")
        p2.blog = b
        assert called[0] == 0
        assert b.posts == [p2]
        assert called[0] == 1

    def test_normal_load(self):
        global lazy_load
        lazy_load = (p1, p2, p3) = [Post("post 1"), Post("post 2"), Post("post 3")]
        called[0] = 0

        b = Blog("blog 1")

        # assign without using backref system
        p2.__dict__['blog'] = b

        assert b.posts == [Post("post 1"), Post("post 2"), Post("post 3")]
        assert called[0] == 1
        p2.blog = None
        p4 = Post("post 4")
        p4.blog = b
        assert b.posts == [Post("post 1"), Post("post 3"), Post("post 4")]
        assert called[0] == 1

        called[0] = 0
        lazy_load = (p1, p2, p3) = [Post("post 1"), Post("post 2"), Post("post 3")]

    def test_commit_removes_pending(self):
        global lazy_load
        lazy_load = (p1, ) = [Post("post 1"), ]
        called[0] = 0

        b = Blog("blog 1")
        p1.blog = b
        attributes.instance_state(b).commit_all(attributes.instance_dict(b))
        attributes.instance_state(p1).commit_all(attributes.instance_dict(p1))
        assert b.posts == [Post("post 1")]

class HistoryTest(_base.ORMTest):

    def test_get_committed_value(self):
        class Foo(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=False, useobject=False)

        f = Foo()
        eq_(Foo.someattr.impl.get_committed_value(attributes.instance_state(f), attributes.instance_dict(f)), None)

        f.someattr = 3
        eq_(Foo.someattr.impl.get_committed_value(attributes.instance_state(f), attributes.instance_dict(f)), None)

        f = Foo()
        f.someattr = 3
        eq_(Foo.someattr.impl.get_committed_value(attributes.instance_state(f), attributes.instance_dict(f)), None)
        
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(Foo.someattr.impl.get_committed_value(attributes.instance_state(f), attributes.instance_dict(f)), 3)

    def test_scalar(self):
        class Foo(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=False, useobject=False)

        # case 1.  new object
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), (), ()))

        f.someattr = "hi"
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['hi'], (), ()))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['hi'], ()))

        f.someattr = 'there'

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['there'], (), ['hi']))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['there'], ()))

        del f.someattr
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), (), ['there']))

        # case 2.  object with direct dictionary settings (similar to a load operation)
        f = Foo()
        f.__dict__['someattr'] = 'new'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['new'], ()))

        f.someattr = 'old'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['old'], (), ['new']))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['old'], ()))

        # setting None on uninitialized is currently a change for a scalar attribute
        # no lazyload occurs so this allows overwrite operation to proceed
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), (), ()))
        f.someattr = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([None], (), ()))

        f = Foo()
        f.__dict__['someattr'] = 'new'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['new'], ()))
        f.someattr = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([None], (), ['new']))

        # set same value twice
        f = Foo()
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        f.someattr = 'one'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['one'], (), ()))
        f.someattr = 'two'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['two'], (), ()))
        
        
    def test_mutable_scalar(self):
        class Foo(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=False, useobject=False, mutable_scalars=True, copy_function=dict)

        # case 1.  new object
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), (), ()))

        f.someattr = {'foo':'hi'}
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([{'foo':'hi'}], (), ()))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [{'foo':'hi'}], ()))
        eq_(attributes.instance_state(f).committed_state['someattr'], {'foo':'hi'})

        f.someattr['foo'] = 'there'
        eq_(attributes.instance_state(f).committed_state['someattr'], {'foo':'hi'})

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([{'foo':'there'}], (), [{'foo':'hi'}]))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [{'foo':'there'}], ()))

        # case 2.  object with direct dictionary settings (similar to a load operation)
        f = Foo()
        f.__dict__['someattr'] = {'foo':'new'}
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [{'foo':'new'}], ()))

        f.someattr = {'foo':'old'}
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([{'foo':'old'}], (), [{'foo':'new'}]))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [{'foo':'old'}], ()))


    def test_use_object(self):
        class Foo(_base.BasicEntity):
            pass

        class Bar(_base.BasicEntity):
            _state = None
            def __nonzero__(self):
                assert False

        hi = Bar(name='hi')
        there = Bar(name='there')
        new = Bar(name='new')
        old = Bar(name='old')

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=False, useobject=True)

        # case 1.  new object
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [None], ()))

        f.someattr = hi
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], (), ()))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi], ()))

        f.someattr = there

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([there], (), [hi]))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [there], ()))

        del f.someattr
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([None], (), [there]))

        # case 2.  object with direct dictionary settings (similar to a load operation)
        f = Foo()
        f.__dict__['someattr'] = 'new'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['new'], ()))

        f.someattr = old
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([old], (), ['new']))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [old], ()))

        # setting None on uninitialized is currently not a change for an object attribute
        # (this is different than scalar attribute).  a lazyload has occured so if its
        # None, its really None
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [None], ()))
        f.someattr = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [None], ()))

        f = Foo()
        f.__dict__['someattr'] = 'new'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), ['new'], ()))
        f.someattr = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([None], (), ['new']))

        # set same value twice
        f = Foo()
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        f.someattr = 'one'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['one'], (), ()))
        f.someattr = 'two'
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), (['two'], (), ()))

    def test_object_collections_set(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            def __nonzero__(self):
                assert False

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=True, useobject=True)

        hi = Bar(name='hi')
        there = Bar(name='there')
        old = Bar(name='old')
        new = Bar(name='new')

        # case 1.  new object
        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [], ()))

        f.someattr = [hi]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], [], []))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi], ()))

        f.someattr = [there]

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([there], [], [hi]))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [there], ()))

        f.someattr = [hi]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], [], [there]))

        f.someattr = [old, new]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([old, new], [], [there]))

        # case 2.  object with direct settings (similar to a load operation)
        f = Foo()
        collection = attributes.init_collection(f, 'someattr')
        collection.append_without_event(new)
        attributes.instance_state(f).commit_all(attributes.instance_dict(f))
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [new], ()))

        f.someattr = [old]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([old], [], [new]))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [old], ()))

    def test_dict_collections(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        from sqlalchemy.orm.collections import attribute_mapped_collection

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=True, useobject=True, typecallable=attribute_mapped_collection('name'))

        hi = Bar(name='hi')
        there = Bar(name='there')
        old = Bar(name='old')
        new = Bar(name='new')

        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [], ()))

        f.someattr['hi'] = hi
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], [], []))

        f.someattr['there'] = there
        eq_(tuple([set(x) for x in attributes.get_state_history(attributes.instance_state(f), 'someattr')]), (set([hi, there]), set(), set()))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(tuple([set(x) for x in attributes.get_state_history(attributes.instance_state(f), 'someattr')]), (set(), set([hi, there]), set()))

    def test_object_collections_mutate(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'someattr', uselist=True, useobject=True)
        attributes.register_attribute(Foo, 'id', uselist=False, useobject=False)

        hi = Bar(name='hi')
        there = Bar(name='there')
        old = Bar(name='old')
        new = Bar(name='new')

        # case 1.  new object
        f = Foo(id=1)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [], ()))

        f.someattr.append(hi)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], [], []))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi], ()))

        f.someattr.append(there)

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([there], [hi], []))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])

        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi, there], ()))

        f.someattr.remove(there)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([], [hi], [there]))

        f.someattr.append(old)
        f.someattr.append(new)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([old, new], [hi], [there]))
        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi, old, new], ()))

        f.someattr.pop(0)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([], [old, new], [hi]))

        # case 2.  object with direct settings (similar to a load operation)
        f = Foo()
        f.__dict__['id'] = 1
        collection = attributes.init_collection(f, 'someattr')
        collection.append_without_event(new)
        attributes.instance_state(f).commit_all(attributes.instance_dict(f))
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [new], ()))

        f.someattr.append(old)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([old], [new], []))

        attributes.instance_state(f).commit(attributes.instance_dict(f), ['someattr'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [new, old], ()))

        f = Foo()
        collection = attributes.init_collection(f, 'someattr')
        collection.append_without_event(new)
        attributes.instance_state(f).commit_all(attributes.instance_dict(f))
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [new], ()))

        f.id = 1
        f.someattr.remove(new)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([], [], [new]))

        # case 3.  mixing appends with sets
        f = Foo()
        f.someattr.append(hi)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi], [], []))
        f.someattr.append(there)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi, there], [], []))
        f.someattr = [there]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([there], [], []))

        # case 4.  ensure duplicates show up, order is maintained
        f = Foo()
        f.someattr.append(hi)
        f.someattr.append(there)
        f.someattr.append(hi)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([hi, there, hi], [], []))

        attributes.instance_state(f).commit_all(attributes.instance_dict(f))
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ((), [hi, there, hi], ()))
        
        f.someattr = []
        eq_(attributes.get_state_history(attributes.instance_state(f), 'someattr'), ([], [], [hi, there, hi]))
        
    def test_collections_via_backref(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'bars', uselist=True, extension=attributes.GenericBackrefExtension('foo'), trackparent=True, useobject=True)
        attributes.register_attribute(Bar, 'foo', uselist=False, extension=attributes.GenericBackrefExtension('bars'), trackparent=True, useobject=True)

        f1 = Foo()
        b1 = Bar()
        eq_(attributes.get_state_history(attributes.instance_state(f1), 'bars'), ((), [], ()))
        eq_(attributes.get_state_history(attributes.instance_state(b1), 'foo'), ((), [None], ()))

        #b1.foo = f1
        f1.bars.append(b1)
        eq_(attributes.get_state_history(attributes.instance_state(f1), 'bars'), ([b1], [], []))
        eq_(attributes.get_state_history(attributes.instance_state(b1), 'foo'), ([f1], (), ()))

        b2 = Bar()
        f1.bars.append(b2)
        eq_(attributes.get_state_history(attributes.instance_state(f1), 'bars'), ([b1, b2], [], []))
        eq_(attributes.get_state_history(attributes.instance_state(b1), 'foo'), ([f1], (), ()))
        eq_(attributes.get_state_history(attributes.instance_state(b2), 'foo'), ([f1], (), ()))

    def test_lazy_backref_collections(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        lazy_load = []
        def lazyload(instance):
            def load(**kw):
                return lazy_load
            return load

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'bars', uselist=True, extension=attributes.GenericBackrefExtension('foo'), trackparent=True, callable_=lazyload, useobject=True)
        attributes.register_attribute(Bar, 'foo', uselist=False, extension=attributes.GenericBackrefExtension('bars'), trackparent=True, useobject=True)

        bar1, bar2, bar3, bar4 = [Bar(id=1), Bar(id=2), Bar(id=3), Bar(id=4)]
        lazy_load = [bar1, bar2, bar3]

        f = Foo()
        bar4 = Bar()
        bar4.foo = f
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([bar4], [bar1, bar2, bar3], []))

        lazy_load = None
        f = Foo()
        bar4 = Bar()
        bar4.foo = f
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([bar4], [], []))

        lazy_load = [bar1, bar2, bar3]
        attributes.instance_state(f).expire_attributes(attributes.instance_dict(f), ['bars'])
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ((), [bar1, bar2, bar3], ()))

    def test_collections_via_lazyload(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        lazy_load = []
        def lazyload(instance):
            def load(**kw):
                return lazy_load
            return load

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'bars', uselist=True, callable_=lazyload, trackparent=True, useobject=True)

        bar1, bar2, bar3, bar4 = [Bar(id=1), Bar(id=2), Bar(id=3), Bar(id=4)]
        lazy_load = [bar1, bar2, bar3]

        f = Foo()
        f.bars = []
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([], [], [bar1, bar2, bar3]))

        f = Foo()
        f.bars.append(bar4)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([bar4], [bar1, bar2, bar3], []) )

        f = Foo()
        f.bars.remove(bar2)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([], [bar1, bar3], [bar2]))
        f.bars.append(bar4)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([bar4], [bar1, bar3], [bar2]))

        f = Foo()
        del f.bars[1]
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([], [bar1, bar3], [bar2]))

        lazy_load = None
        f = Foo()
        f.bars.append(bar2)
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bars'), ([bar2], [], []))

    def test_scalar_via_lazyload(self):
        class Foo(_base.BasicEntity):
            pass

        lazy_load = None
        def lazyload(instance):
            def load(**kw):
                return lazy_load
            return load

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'bar', uselist=False, callable_=lazyload, useobject=False)
        lazy_load = "hi"

        # with scalar non-object and active_history=False, the lazy callable is only executed on gets, not history
        # operations

        f = Foo()
        eq_(f.bar, "hi")
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), ["hi"], ()))

        f = Foo()
        f.bar = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), ()))

        f = Foo()
        f.bar = "there"
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), (["there"], (), ()))
        f.bar = "hi"
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), (["hi"], (), ()))

        f = Foo()
        eq_(f.bar, "hi")
        del f.bar
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), (), ["hi"]))
        assert f.bar is None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), ["hi"]))

    def test_scalar_via_lazyload_with_active(self):
        class Foo(_base.BasicEntity):
            pass

        lazy_load = None
        def lazyload(instance):
            def load(**kw):
                return lazy_load
            return load

        attributes.register_class(Foo)
        attributes.register_attribute(Foo, 'bar', uselist=False, callable_=lazyload, useobject=False, active_history=True)
        lazy_load = "hi"

        # active_history=True means the lazy callable is executed on set as well as get,
        # causing the old value to appear in the history

        f = Foo()
        eq_(f.bar, "hi")
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), ["hi"], ()))

        f = Foo()
        f.bar = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), ['hi']))

        f = Foo()
        f.bar = "there"
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), (["there"], (), ['hi']))
        f.bar = "hi"
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), ["hi"], ()))

        f = Foo()
        eq_(f.bar, "hi")
        del f.bar
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), (), ["hi"]))
        assert f.bar is None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), ["hi"]))

    def test_scalar_object_via_lazyload(self):
        class Foo(_base.BasicEntity):
            pass
        class Bar(_base.BasicEntity):
            pass

        lazy_load = None
        def lazyload(instance):
            def load(**kw):
                return lazy_load
            return load

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'bar', uselist=False, callable_=lazyload, trackparent=True, useobject=True)
        bar1, bar2 = [Bar(id=1), Bar(id=2)]
        lazy_load = bar1

        # with scalar object, the lazy callable is only executed on gets and history
        # operations

        f = Foo()
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), [bar1], ()))

        f = Foo()
        f.bar = None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), [bar1]))

        f = Foo()
        f.bar = bar2
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([bar2], (), [bar1]))
        f.bar = bar1
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ((), [bar1], ()))

        f = Foo()
        eq_(f.bar, bar1)
        del f.bar
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), [bar1]))
        assert f.bar is None
        eq_(attributes.get_state_history(attributes.instance_state(f), 'bar'), ([None], (), [bar1]))

class ListenerTest(_base.ORMTest):
    def test_receive_changes(self):
        """test that Listeners can mutate the given value.
        
        This is a rudimentary test which would be better suited by a full-blown inclusion
        into collection.py.
        
        """
        class Foo(object):
            pass
        class Bar(object):
            pass

        class AlteringListener(AttributeExtension):
            def append(self, state, child, initiator):
                b2 = Bar()
                b2.data = b1.data + " appended"
                return b2

            def set(self, state, value, oldvalue, initiator):
                return value + " modified"

        attributes.register_class(Foo)
        attributes.register_class(Bar)
        attributes.register_attribute(Foo, 'data', uselist=False, useobject=False, extension=AlteringListener())
        attributes.register_attribute(Foo, 'barlist', uselist=True, useobject=True, extension=AlteringListener())
        attributes.register_attribute(Foo, 'barset', typecallable=set, uselist=True, useobject=True, extension=AlteringListener())
        attributes.register_attribute(Bar, 'data', uselist=False, useobject=False)
        
        f1 = Foo()
        f1.data = "some data"
        eq_(f1.data, "some data modified")
        b1 = Bar()
        b1.data = "some bar"
        f1.barlist.append(b1)
        assert b1.data == "some bar"
        assert f1.barlist[0].data == "some bar appended"
        
        f1.barset.add(b1)
        assert f1.barset.pop().data == "some bar appended"
    
    
