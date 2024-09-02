class Error:

  def __init__(_, parent):
    parent.errors = {}



class Quiggle:

  def __init__(self):
    self.bind(Error)

  def bind(self, C):
    C(self)