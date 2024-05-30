


class X():
	def __init__(self,x):
		print(f"Class is {self.__class__.__name__} {x}")

class Y(X):
	def __init__(self):
		super().__init__('qq')

Y()
