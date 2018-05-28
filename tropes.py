class TropeDef:
	'''
	A trope definition.
	'''

	def __init__(self, name):
		self.name = name
		self.referencers = []
		self.related = []
		return

	def __str__(self):
		return str(self.name)
