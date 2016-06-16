import unittest

from command import HTBCommand

# Here's HTBCommand "unit tests".
class HTBCommandTest(unittest.TestCase):

	def testTooShort(self):
		instance = HTBCommand('/time')
		self.assertEqual('ERROR', instance.command)
		self.assertEqual(None, instance.name)
		self.assertEqual(None, instance.minutes)

	def testDefault(self):
		instance = HTBCommand('/timer')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Sprint', instance.name)
		self.assertEqual(60, instance.minutes)

	def testConfig(self):
		instance = HTBCommand('/timer config token')
		self.assertEqual('CONFIG', instance.command)
		self.assertEqual('token', instance.name)
		self.assertEqual(None, instance.minutes)

	def testOnlyMinutes(self):
		instance = HTBCommand('/timer 60')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Sprint', instance.name)
		self.assertEqual(60, instance.minutes)

	def testOnlyMinutes2(self):
		instance = HTBCommand('/timer 6')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Sprint', instance.name)
		self.assertEqual(6, instance.minutes)

	def testOnlyMinutes3(self):
		instance = HTBCommand('/timer 100')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Sprint', instance.name)
		self.assertEqual(100, instance.minutes)

	def testOnlyMinutes4(self):
		instance = HTBCommand('/timer 0.001')
		self.assertEqual(None, instance.command)
		self.assertEqual(None, instance.name)
		self.assertEqual(None, instance.minutes)

	def testOnlyMinutes5(self):
		instance = HTBCommand('/timer -1')
		self.assertEqual(None, instance.command)
		self.assertEqual(None, instance.name)
		self.assertEqual(None, instance.minutes)

	def testOnlyName(self):
		instance = HTBCommand('/timer Test')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Test', instance.name)
		self.assertEqual(60, instance.minutes)

	def testNameAndMinutes(self):
		instance = HTBCommand('/timer Test 5')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Test', instance.name)
		self.assertEqual(5, instance.minutes)

	def testNameAndMinutes1(self):
		instance = HTBCommand('/timer Test -5')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Test', instance.name)
		self.assertEqual(None, instance.minutes)

	def testNameAndMinutes2(self):
		instance = HTBCommand('/timer Test 0.001')
		self.assertEqual('NEW', instance.command)
		self.assertEqual('Test', instance.name)
		self.assertEqual(None, instance.minutes)

	def test3Things(self):
		instance = HTBCommand('/timer name token 6')
		self.assertEqual(None, instance.command)
		self.assertEqual(None, instance.name)
		self.assertEqual(None, instance.minutes)

def main():
	unittest.main()

if __name__ == '__main__':
	main()