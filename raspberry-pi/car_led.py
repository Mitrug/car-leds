from rpi_ws281x import *
from car_led_database import update_active_profile, get_active_profile, is_led_enabled
import time
import logging
from led_colour_profiles.led_colour_profile_red import *
from led_colour_profiles.led_colour_profile_blue import *

# LED strip configuration:
LED_COUNT      = 120     # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    
strip = None
profiles = []  

def clear_led_strip():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    
def getProfile(name):
    for profile in profiles:
        if profile.name == name:
            return profile
    return None

    
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    profiles.append(RedLedColourProfile(strip))
    profiles.append(BlueLedColourProfile(strip))

    try:
        while True:
            if is_led_enabled() == 'true':
                profile = getProfile(get_active_profile())
                
                if profile != None:
                    profile.run()
            else:
                clear_led_strip()
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    
    clear_led_strip()
