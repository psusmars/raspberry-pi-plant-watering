# External module imp
import RPi.GPIO as GPIO
import datetime
from datetime import datetime
import time
import dateutil.parser

init = False
dry = 0
DURATION_TO_WATER_IN_SECONDS = 3

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"

def get_last_watered_as_datetime():
    last_watered = get_last_watered()
    if "NEVER" in last_watered:
        return None
    else:
        return dateutil.parser.parse(last_watered)

def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def init_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    
def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while True:
            time.sleep(delay)
            plant_is_wet = not get_status(pin = water_sensor_pin) == dry
            if plant_is_wet:
            last_watered = get_last_watered_as_datetime()
            if last_watered is None or (datetime.now() - last_watered).days > 0:
                print("Would water now")
                # pump_on(pump_pin, DURATION_TO_WATER_IN_SECONDS)
                # TODO: Remove the set last watered
                set_last_watered()
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def set_last_watered():
    with open("last_watered.txt", "w") as f:
        f.write(f"{datetime.now()}")

def pump_on(pump_pin = 7, delay = 1):
    init_output(pump_pin)
    set_last_watered()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pump_pin, GPIO.HIGH)
    
