from flask import Flask, request, Response, jsonify
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue
from led_pins import led_pins
import time
import socket
import pickle
from zeroconf import __version__, ServiceInfo, Zeroconf

# setup the zeroconf stuff here
r = Zeroconf()

desc = {'version': '0.10', 'a': 'test value', 'b': 'another value'}
info = ServiceInfo("_http._tcp.local.",
                   "My Service Name._http._tcp.local.",
                   socket.inet_aton("169.254.236.221"), 9999, 0, 0, desc)

r.register_service(info)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 9999))
s.listen(1)


GPIO.setmode(led_pins['mode'])
GPIO.setup(led_pins['red'], GPIO.OUT)
GPIO.setup(led_pins['blue'], GPIO.OUT)
GPIO.setup(led_pins['green'], GPIO.OUT)

# This sets up the PWM for al'l of them
rp = GPIO.PWM(led_pins['red'], 100)  
bp = GPIO.PWM(led_pins['blue'], 100)  
gp = GPIO.PWM(led_pins['green'], 100) 
rp.start(0)
bp.start(0)
gp.start(0)
r_val = 0
b_val = 0
g_val = 0
rate_change = 0
state = 1
try:
    while 1:
        conn, addr = s.accept()
        got = pickle.loads(conn.recv(1024))
        rate_change = float(got['rate'])
        state = int(got['state'])
        b_done = False
        r_done = False
        g_done = False
        if state:
            #g_val = float(got['green'])
            changer = 0
            while (not b_done) or (not g_done) or (not r_done):
                if r_val < float(got['red']):
                    r_val += 1
                elif not r_done:
                    r_val = float(got['red'])
                    r_done = True
                if g_val < float(got['green']):
                    g_val += 1
                elif not g_done:
                    g_val = float(got['green'])
                    g_done = True
                if b_val < float(got['blue']):
                    b_val += 1
                elif not b_done:
                    b_val = float(got['blue'])
                    b_done = True

                rp.ChangeDutyCycle(r_val)
                gp.ChangeDutyCycle(g_val)
                bp.ChangeDutyCycle(b_val)
                time.sleep(rate_change)
        else:
            # This is where we change the values slowly
            while r_val != 0 or b_val !=0 or g_val !=0:
                if r_val > 0:
                    r_val -= 1
                else:
                    r_val = 0
                
                if g_val > 0:
                    g_val -= 1
                else:
                    g_val = 0
    
                if b_val > 0:
                    b_val -= 1 
                else:
                    b_val = 0
                rp.ChangeDutyCycle(r_val)
                gp.ChangeDutyCycle(g_val)
                bp.ChangeDutyCycle(b_val)
                time.sleep(rate_change)
            
        conn.close()
        time.sleep(1)
except KeyboardInterrupt:
     r.unregister_service(info)

        
