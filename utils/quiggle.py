class Error:

  def __init__(self, parent):
    parent.errors = {}
    parent.err = self

  def test(self):
    print(self)

class Quiggle:

  def __init__(self):

    self.bind(Error)

  def bind(self, C):
    C(self)

  def set_class_props(self, C, obj = {}):
		  # class dict variable
    d = C.__class__.__dict__
      # fill dict with class keys
    for key in d.keys():
        # exclude default methods
      if not key.startswith('__'):
          obj[key] = d[key]
    return obj