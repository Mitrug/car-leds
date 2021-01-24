import sqlite3
import atexit
import logging

LED_COUNT = 120
DATABASE_PATH = '/home/pi/Desktop/car-leds/raspberry-pi/car_led.db'

conn = sqlite3.connect(DATABASE_PATH)

logging = logging.getLogger()

def clean_database():
    c = conn.cursor()

    try:
        c.execute('''DROP TABLE LED_PROPERTIES''')
    except sqlite3.OperationalError:
        pass

def create_tables():
    c = conn.cursor()
    
    c.execute('''CREATE TABLE LED_PROPERTIES (
                key text NOT NULL,
                value text NOT NULL)''')
                 
    conn.commit() 
    
def insert_led_properties():            
    c = conn.cursor()
	
    c.execute('''INSERT INTO LED_PROPERTIES(key, value) VALUES ("LED_ENABLED", "true")''')
    c.execute('''INSERT INTO LED_PROPERTIES(key, value) VALUES ("ACTIVE_PROFILE", "Blue")''')
    conn.commit()
        
    
def is_led_enabled():
    c = conn.cursor()

    c.execute('''SELECT value
                FROM LED_PROPERTIES
                WHERE key = "LED_ENABLED"''')
    rows = c.fetchone()
    
    return str(rows[0])   
    
def set_led_enabled(value):
    c = conn.cursor()
                    
    c.execute('''UPDATE LED_PROPERTIES
                SET value = ?
                WHERE key = "LED_ENABLED"''', (value,))
    conn.commit()
 
def get_active_profile():
    c = conn.cursor()

    c.execute('''SELECT value
                FROM LED_PROPERTIES
                WHERE key = "ACTIVE_PROFILE"''')
    rows = c.fetchone()
    
    return str(rows[0])
    
    
def update_active_profile(profile_name):
    c = conn.cursor()
                    
    c.execute('''UPDATE LED_PROPERTIES
                SET value = ?
                WHERE key = "ACTIVE_PROFILE"''', (profile_name,))
    conn.commit()
    
    
def main():
    logging.info("Running database initial setup")
        
    clean_database()
    create_tables()
    
    insert_led_properties()
    
    logging.info("Executed successfully")
    
@atexit.register
def cleanup_connection():
    conn.close()
    
if __name__ == '__main__':
    main()      
