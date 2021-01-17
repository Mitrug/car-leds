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
        c.execute('''DROP TABLE LED_PROFILE_COLOURS''')
        c.execute('''DROP TABLE LED_PROFILES''')
        c.execute('''DROP TABLE LED_PROPERTIES''')
    except sqlite3.OperationalError:
        pass

def create_tables():
    c = conn.cursor()
    
    c.execute('''CREATE TABLE LED_PROPERTIES (
                key text NOT NULL,
                value text NOT NULL)''')
                
    c.execute('''CREATE TABLE LED_PROFILES (
                name text NOT NULL,
                active BOOLEAN NOT NULL CHECK (active IN (0,1)))''')
                
    c.execute('''CREATE TABLE LED_PROFILE_COLOURS (
                    led_profile_id INTEGER NOT NULL,
                    led_index INTEGER NOT NULL,
                    led_colour INTEGER NOT NULL,
                    PRIMARY KEY (led_profile_id, led_index),
                    FOREIGN KEY (led_profile_id) REFERENCES LED_PROFILES (rowid))''')   
    conn.commit() 
    
def insert_led_properties():            
    c = conn.cursor()
	
    c.execute('''INSERT INTO LED_PROPERTIES(key, value) VALUES ("LED_ENABLED", "true")''')
    conn.commit()
    
def add_strip_with_one_colour(ledProfileId, name, active, hexCode):
    c = conn.cursor()

    c.execute('''INSERT INTO LED_PROFILES(rowid, name, active) VALUES (?, ?, ?)''', (ledProfileId, name, active))   

    for i in range(LED_COUNT):
        whiteColorInteger = int(hexCode, 16)
        c.execute('''INSERT INTO LED_PROFILE_COLOURS(led_profile_id, led_index, led_colour) VALUES (?, ?, ?)''', (ledProfileId, i, whiteColorInteger))  
    conn.commit()          
        
def update_active_profile(profile_name):	
    c = conn.cursor()

    c.execute('''SELECT rowid
                FROM LED_PROFILES
                WHERE name = ?''', (profile_name,)) 
    rows = c.fetchall()
    if len(rows) == 0:
        raise ValueError("LED profile name does not exist")

    logging.info("Disabling all active profiles")
    c.execute('''UPDATE LED_PROFILES
                SET ACTIVE = 0
                WHERE rowid = (
                    SELECT rowid
                    FROM LED_PROFILES
                    WHERE ACTIVE = 1)''')
                    
    logging.info("Updating active profile to " + profile_name)
    c.execute('''UPDATE LED_PROFILES
                SET ACTIVE = ?
                WHERE name = ?''', (1, profile_name))  
    conn.commit()
    
def get_profiles():
    c = conn.cursor()

    c.execute('''SELECT name
                FROM LED_PROFILES''') 
    return [x for xs in c.fetchall() for x in xs]


def current_active_profile() -> int:
    c = conn.cursor()

    c.execute('''SELECT rowid
                FROM LED_PROFILES
                WHERE active = 1''')
    rows = c.fetchone()
    
    return int(rows[0]) 
    
def get_current_active_profile_name():
    c = conn.cursor()

    c.execute('''SELECT name
                FROM LED_PROFILES
                WHERE active = 1''')
    rows = c.fetchone()
    
    return str(rows[0])     
    
def get_profile_colours(profile_id):
    c = conn.cursor()   
    
    c.execute('''SELECT led_colour
                FROM LED_PROFILE_COLOURS
                WHERE led_profile_id = ?
                ORDER BY led_index ASC;''', (profile_id,))
    rows = c.fetchall() 
    colours = []
    for row in rows:
        colours.append(row[0])
        
    return colours  
    
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
    
def main():
    logging.info("Running database initial setup")
        
    clean_database()
    create_tables()
    
    add_strip_with_one_colour(1, "WHITE", 0, "ffffff")
    add_strip_with_one_colour(2, "RED", 1, "ff0000")
    add_strip_with_one_colour(3, "BLUE", 0, "00ff00")
    add_strip_with_one_colour(4, "GREEN", 0, "0000ff")
    
    insert_led_properties()
    
    logging.info("Executed successfully")
    
@atexit.register
def cleanup_connection():
    conn.close()
    
if __name__ == '__main__':
    main()      
