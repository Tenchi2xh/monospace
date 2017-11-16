from functools import wraps
import inspect


def auto_properties(initializer):
   names = inspect.getargspec(initializer)[0]

   @wraps(initializer)
   def wrapper(self, *args, **kwargs):
       for name, arg in zip(names[1:], args) + kwargs.items():
           setattr(self, name, arg)
       initializer(self, *args, **kargs)

   return wrapper
