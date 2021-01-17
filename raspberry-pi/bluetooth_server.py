from bluetooth import *
import re
from car_led_database import update_active_profile, get_profiles, get_current_active_profile_name, is_led_enabled, set_led_enabled
import logging

logging.basicConfig(level=logging.INFO)

def is_activate_led_profile_command(command) -> bool:
    return re.search('active_led_profile: .+', command) != None

def is_get_led_profiles(command) -> bool:
    return re.search('get_profiles', command) != None
    
def is_get_active_led_profile(command) -> bool:
    return re.search('get_active_profile', command) != None

def is_get_led_enabled(command) -> bool:
    return re.search('is_led_enabled', command) != None
    
def is_set_led_enabled(command) -> bool:
    return re.search('set_led_enabled', command) != None    
    
def execute_comand_activate_led_profile(client_sock, command):
    m = re.search('active_led_profile: (?P<profile_name>.+)', command)    
    profile_name = m.group("profile_name")
    try:
        update_active_profile(profile_name)
        client_sock.send("active_profile: " + profile_name + "\r\n");
    except ValueError:
        pass
    
def execute_command_get_led_profiles(client_sock):
    client_sock.send("configured_profiles: " + ', '.join(get_profiles()) + "\r\n")
 
def execute_command_get_active_led_profile(client_sock):
    client_sock.send("active_profile: " + get_current_active_profile_name() + "\r\n")   
    
def execute_command_is_led_enabled(client_sock):
    client_sock.send("led_enabled: " + is_led_enabled() + "\r\n")     
    
def execute_command_set_led_enabled(client_sock, command):
    m = re.search('set_led_enabled: (?P<led_enabled>.+)', command)    
    led_enabled = m.group("led_enabled")
    set_led_enabled(led_enabled)
    client_sock.send("led_enabled: " + led_enabled + "\r\n")           


def route_command(client_sock, command):
    logging.info("Received command: \"" + command + "\"")
    if is_activate_led_profile_command(command):
        execute_comand_activate_led_profile(client_sock, command)
    elif is_get_led_profiles(command):
        execute_command_get_led_profiles(client_sock)
    elif is_get_active_led_profile(command):
        execute_command_get_active_led_profile(client_sock)  
    elif is_get_led_enabled(command):
        execute_command_is_led_enabled(client_sock)
    elif is_set_led_enabled(command):
        execute_command_set_led_enabled(client_sock, command)

def main():
    server_sock=BluetoothSocket( RFCOMM )
    server_sock.bind(("",PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    advertise_service( server_sock, "SampleServer",
                       service_id = uuid,
                       service_classes = [ uuid, SERIAL_PORT_CLASS ],
                       profiles = [ SERIAL_PORT_PROFILE ] )
                       
    logging.info("Waiting for connection on RFCOMM channel %d" % port)
    
    while True:
        client_sock, client_info = server_sock.accept()
        logging.info("Accepted connection from " + str(client_info[0]))

        try:
            while True:
                data = client_sock.recv(1024).decode('utf-8').rstrip()
                for command in data.splitlines():
                    route_command(client_sock, command)           
        except IOError:
            pass

        logging.info("Client disconnected " + str(client_info[0]))

        client_sock.close()
    server_sock.close()
    logging.info("Closed Bluetooth server socket")
    
    
if __name__ == '__main__':
    main()
