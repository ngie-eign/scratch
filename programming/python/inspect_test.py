import inspect


def foo():
    frame = inspect.stack()[1][0]
    name = frame.f_code.co_name
    print("current frame: %r (type = %s)" % (dir(frame.f_code), type(frame.f_code)))
    print("name = %s" % (name,))
    module = inspect.getmodule(name)
    print("module = %s" % (module,))


def bar():
    foo()


bar()

print(__name__)
