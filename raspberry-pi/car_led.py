from rpi_ws281x import *
from car_led_database import update_active_profile, current_active_profile, get_profile_colours as db_get_profile_colours, is_led_enabled as db_is_led_enabled
import time
import logging

# LED strip configuration:
LED_COUNT      = 120     # Number of LED pixels.
LED_PIN        = 12      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
    
strip = None
active_profile = None
led_enabled = None

def get_profile_colours() -> [Color]:    
    active_profile = current_active_profile()
    
    colours = db_get_profile_colours(active_profile)
    
    if len(colours) < LED_COUNT:
        logging.info("Missing LED colour info for " + str(LED_COUNT - len(colours)) + " LEDs")
    
    ledColours = []
    for i in range(LED_COUNT):
        hexColor = 0
        if i < len(colours):
            hexColor = hex(colours[i]).lstrip("0x").zfill(6)
        else:
            hexColor = 'ffffff'
                
        rbg = tuple(int(hexColor[j:j+2], 16) for j in (0, 2, 4))
        ledColours.append(Color(int(rbg[0]), int(rbg[2]), int(rbg[1])))
    
    return ledColours    

def update_led_strip(colours):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, colours[i])
    strip.show()
    
def reload_led_profile():
    ledColours = get_profile_colours()    
    update_led_strip(ledColours)
    
def change_in_active_profile() -> bool:
    return active_profile != current_active_profile()

def clear_led_strip():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

    
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    
    led_enabled = db_is_led_enabled()
    
    reload_led_profile()  
    
    try:
        while True:
            db_led_enabled = db_is_led_enabled()
            if led_enabled != db_led_enabled:
                led_enabled = db_led_enabled
                if led_enabled == 'true':
                    reload_led_profile()
                else:
                    clear_led_strip()
                
            if change_in_active_profile() == True and led_enabled == 'true':
                reload_led_profile()
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
        
    clear_led_strip()
