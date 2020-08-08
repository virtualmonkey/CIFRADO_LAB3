'''
Server for attend requests from timing attack module
'''
import time 
from flask import Flask, request

app = Flask(__name__)

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

#Reference: https://github.com/Lothiraldan
#Defining a route for token validation
@app.route("/")
def protected():
    token = request.headers.get('X-TOKEN') #getting the token from request header
    
    if not token:
        return "Missing token", 401
    
    if str_equals_conts_time(token, SECRET_TOKEN):
        return "Welcome admin! Here is the top secret government data"
    else:
        return "Who the fu*@ are you? Get out of here now!", 403


if __name__ == "__main__":
    app.run()

