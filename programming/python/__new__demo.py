class Obj(object):
    def __init__(self, *args, **kwargs):
        print(f"__init__: called: {id(self)}")

    def __new__(cls, *args, **kwargs):
        print(f"__new__: calling: {id(cls)}")
        new_inst = super().__new__(cls)
        print(f"__new__: called: {id(cls)}")
        return new_inst


Obj()
