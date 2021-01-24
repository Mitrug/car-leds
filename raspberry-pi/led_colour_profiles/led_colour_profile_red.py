from rpi_ws281x import Color

class RedLedColourProfile:
	
	name = 'Red'
	
	def __init__(self, strip):
		self.strip = strip
		
	def run(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(255, 0, 0))
		self.strip.show()
