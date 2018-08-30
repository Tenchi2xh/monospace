from functools import wraps
import inspect


def auto_properties(initializer):
   names = inspect.getargspec(initializer)[0]

   @wraps(initializer)
   def wrapper(self, *args, **kwargs):
       for name, arg in list(zip(names[1:], args)) + list(kwargs.items()):
           setattr(self, name, arg)
       initializer(self, *args, **kwargs)

   return wrapper


def auto_repr(Class):
    class Representable(Class):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __repr__(self):
            return repr(vars(self))

    return Representable


def indent_json_like(string, indent=2):
    level = 0
    result = ""
    in_quotes = False
    in_parens = False
    for char in string:
        result += char
        if char == "'":
            in_quotes = not in_quotes
        elif char == "(":
            in_parens = True
        elif char == ")":
            in_parens = False

        if char == "{" or char == "[":
            level += 1
            result += "\n"
            result += " " * (indent * level)
        elif char == "}" or char == "]":
            level -= 1
            result = result[:-1]
            result += "\n"
            result += " " * (indent * level)
            result += char
        elif char == "," and not in_quotes and not in_parens:
            result += "\n"
            result += " " * (indent * level - 1)
    return result