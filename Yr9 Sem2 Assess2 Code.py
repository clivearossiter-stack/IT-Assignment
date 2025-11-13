from machine import Pin, Timer
import time

# Setup
buzzer = Pin(15,Pin.OUT)
button = Pin(0,Pin.IN, Pin.PULL_UP)
led = Pin(9, Pin.OUT)

# State
timer_running = False
start_time = None
last_press_time = 0
elapsed_time = 0
egg_status = 0 #0 is uncooked, 1 is runny yolk, 2 is soft boiled and 3 is hard boiled

def alert(times, duration, pause):
    for _ in range(times):
        buzzer.on()
        led.on()
        time.sleep(duration)
        buzzer.off()
        led.off()
        time.sleep(pause)

def handle_button(pin):
    global timer_running, start_time, last_press_time, elapsed_time, egg_status
    if (time.time() - last_press_time) > 0.3: #ignore accidental multiple press 
        if not timer_running:
            start_time = time.time()
            last_press_time = time.time()
            timer_running = True
            print("Timer started")
        else:
            timer_running = False
            last_press_time = time.time()
            led.off()
            buzzer.off()
            elapsed_time = time.time() - start_time
            print("Timer stopped:",elapsed_time,"s")
            elapsed_time = 0
            egg_status = 0

button.irq(trigger=Pin.IRQ_FALLING, handler=handle_button)

# Main loop
while True:
    if timer_running:
        elapsed_time = time.time() - start_time

        if  360 <= elapsed_time < 480 and egg_status == 0:  # 6 to 8 minutes
            print("Runny")
            alert(1, 0.4, 0.4)
            egg_status = 1

        elif 480 <= elapsed_time < 600 and egg_status == 1:  # 8 to 10 minutes
            print("Soft Boiled")
            alert(2, 0.8, 0.8)
            egg_status = 2

        elif elapsed_time >= 600 and egg_status == 2:  # 10 minutes
            print("Hard Boiled")
            alert(3, 1.5, 1.5)
            egg_status = 3

    time.sleep(0.1)