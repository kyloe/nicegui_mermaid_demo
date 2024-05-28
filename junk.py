

class X():
	def __init__(self):
		self = B()


class B(X):
	def __init__(self):
		self.value="HELLO"

class C():
	def __init__(self):
		print("DID IT")

a = X()
print(a.value)


