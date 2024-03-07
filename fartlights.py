import network
import socket
import machine
import time

# Replace with your actual SSID and password
ssid = 'YOUR_SSID'
password = 'YOUR_PASSWORD'

# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

# Wait for connection
while not station.isconnected():
    time.sleep(1)

print('Connected to Wi-Fi')

# Setup LEDs
led_pins = [2, 3] # Add your GPIO pins here
leds = [machine.Pin(pin, machine.Pin.OUT) for pin in led_pins]

# Function to toggle LEDs
def toggle_leds():
    for led in leds:
        led.toggle()

# Setup socket web server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Handle clients
while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n':
            break
    
    # Toggle LEDs and broadcast fart when a client connects
    toggle_leds()
    response = "Fart broadcasted to the universe!"
    cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
    cl.send(response)
    cl.close()

# Cleanup
s.close()
