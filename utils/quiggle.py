class Error:

  def __init__(self):
    self.errors = {}



class Quiggle:

  def __init__(self):
    self.bind(Error)

  def bind(self, C):
    C(self)