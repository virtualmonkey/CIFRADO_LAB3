# Message Integrity Lab

This repo contains two implementations related with message integrity

    - cypher.py
    - timingAttack.py
    - server.py

the two last are for the same purpose.

## Installation

After cd to the cloned repo let's create a new virtual environment:

```sh
$ python3 -m venv venv
```

Activate it (linux OS)
```sh
$ source venv/bin/activate
```

Install all the dependencies:

```sh
$ pip3 install -r requeriments.txt
```


## Running

For SHA-256 implmentation run: 

```sh
$ python3 cipher.py
```

**For timingAttack implementation**

There are three ways to compare the token
    
    - str_equals
    - str_equals_hmac
    - str_equals_conts_time

the first one is the one is the worst because with that way of comparison the atacker will know the token
basically because compare character by character is timing predictable when is asserted.

So, choose the function that you want to prove and modify the sever.py file 

```python
app.route("/")
def protected():
    token = request.headers.get('X-TOKEN') #getting the token from request header
    
    if not token:
        return "Missing token", 401

    #edit this function with the functions alredy mentioned
    if str_equals_hmac(token, SECRET_TOKEN):
        return "Welcome admin! Here is the top secret government data"

    else:
        return "Who the fu*@ are you? Get out of here now!", 403

```

You can even change the SECRET_TOKEN as follow:

```python

SECRET_TOKEN = 'boyah'

```

**But remember, the size of the has to be edited as well in timingAttack.py** 


```python
#for string boyah
TOKEN_SIZE = 5

```

Start the server

```sh
$ python3 server.py
```

Now, run the timingAttack file

```sh
$ python3 timingAttack.py
```

## Results

You should get something like this


**For str_equals**
![alt text](https://github.com/virtualmonkey/CIFRADO_LAB3/blob/master/no_time_constant.png)

**For str_equals_conts_time**
![alt text](https://github.com/virtualmonkey/CIFRADO_LAB3/blob/master/time_constant_XOR.png)

**For str_equals_hmac**
![alt text](https://github.com/virtualmonkey/CIFRADO_LAB3/blob/master/time_constant_hmac.png)


## Demo

[Video](https://youtu.be/cPeBtGOMj94)