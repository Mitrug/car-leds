from rpi_ws281x import Color

class BlueLedColourProfile:
	
	name = 'Blue'
	
	def __init__(self, strip):
		self.strip = strip
		
	def run(self):
		for i in range(self.strip.numPixels()):
			self.strip.setPixelColor(i, Color(0, 0, 255))
		self.strip.show()
