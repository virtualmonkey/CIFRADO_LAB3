'''
Server for attend requests from timing attack module
'''
import time 
import sys
from flask import Flask, request, jsonify
import json, os, signal

from hmac import compare_digest, digest, new
from hashlib import sha256
from secrets import token_bytes



app = Flask(__name__)

MODE = 2

SECRET_TOKEN = 'cif'

#Reference: https://sqreen.github.io/DevelopersSecurityBestPractices/timing-attack/python
#Function that takes irregular time while comparing
def str_equals(first_string, second_string):
    if len(first_string) != len(second_string):
        return False
    
    for c1, c2, in zip(first_string, second_string):
        if c1 != c2:
            return False
        time.sleep(0.01)
    return True


#Reference: https://codahale.com/a-lesson-in-timing-attacks/
#Time constant compare function
def str_equals_conts_time(first_string, second_string):
    if len(first_string) != len(second_string):
        return False
    result = 0
    for x, y in zip(first_string, second_string):
        result |= ord(x) ^ ord(y)
    return result == 0

#Reference: https://paragonie.com/blog/2015/11/preventing-timing-attacks-on-string-comparison-with-double-hmac-strategy
#Time constant compare function using HMAC (SHA256 construction) and 32-bytes random key
def str_equals_hmac(first_string, second_string):
    if len(first_string) != len(second_string):
        return False
    key = token_bytes(32)
    hmac1 = new(key, bytes(first_string, 'utf-8'), sha256)
    hmac2 = new(key, bytes(second_string, 'utf-8'), sha256)
    return compare_digest(hmac1.digest(), hmac2.digest())
    

#Reference: https://github.com/Lothiraldan
#Defining a route for token validation
@app.route("/")
def protected():
    token = request.headers.get('X-TOKEN') #getting the token from request header
    
    if not token:
        return "Missing token", 401

    if str_equals_hmac(token, SECRET_TOKEN):
        return "Welcome admin! Here is the top secret government data"

    else:
        return "Who the fu*@ are you? Get out of here now!", 403

#Route for stop server
#In linux OS: writ curl localhost:port/stop
@app.route("/stop")
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

if __name__ == "__main__":
    app.run()

