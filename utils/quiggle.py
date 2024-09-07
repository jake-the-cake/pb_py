from utils.color import log_bug

class Error:
  def __init__(self, parent):
    parent.errors = {}
    parent.err = self

class Toolkit:
  def __init__(self, parent):
    parent.tools = self

  @staticmethod
  def default_method_log(Class, method: str) -> None:
    log_bug('"{}" class has no {} method.'.format(Class.__class__.__name__, method))

  @staticmethod
  def set_class_props(Class, object = {}):
    dictionary = Class.__class__.__dict__
    for key in dictionary.keys():
      if not key.startswith('__'): object[key] = dictionary[key]
    return object

# Quiggle Class
class Quiggle:

  def __init__(self):
    self.bind(Error)
    self.bind(Toolkit)

  def bind(self, C):
    C(self)

