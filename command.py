class HTBCommand(object):

	def __init__(self, raw):
		self.raw = raw
		self.minutes = None
		self.command = None
		self.name = None
		self.parse(self.raw)

	def parse(self, raw):
		if (len(raw) < 6):
			self.command = 'ERROR'

		# /timer
		if (len(raw) == 6):
			self.default()

		# /timer *
		if (len(raw) > 7):
			self.parseSuffix(raw[7:len(raw)])


	def parseSuffix(self, rawSuffix):

		# /timer config <token>
		if (rawSuffix.find('config') > -1):
			self.parseConfig(rawSuffix[7:len(rawSuffix)])
			return

		# /timer <minutes>
		if (unicode(rawSuffix).isnumeric()):
			self.default()
			self.parseOnlyMinutes(rawSuffix)
			return

		# /timer <name>
		if(rawSuffix.isalpha()):
			self.default()
			self.parseOnlyName(rawSuffix)
			return

		split = rawSuffix.split()

		# /timer <name> <minutes>
		if(len(split) == 2):
			self.default()
			self.parseOnlyMinutes(split[1])
			self.parseOnlyName(split[0])
		

	def parseConfig(self, rawConfig):
		self.command = 'CONFIG'
		self.name = rawConfig

	def parseOnlyMinutes(self, rawSuffix):
		if(rawSuffix.isdigit()):
			try:
	   			self.minutes = int(rawSuffix)
			except ValueError:
				self.minutes = None

		if(rawSuffix.isdigit() == False):
			self.minutes = None

	def parseOnlyName(self, rawSuffix):
		if(rawSuffix.isalpha()):
			self.name = rawSuffix

	def default(self):
		self.minutes = 60
		self.name = 'Sprint'
		self.command = 'NEW'

