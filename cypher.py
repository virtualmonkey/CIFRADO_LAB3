import hashlib
import hmac
import base64

message = bytes('Cifrado de informacion seccion 10', 'utf-8')
secret = bytes('CC3078', 'utf-8')

signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
print("El primer mensaje: ") 
print(base64.b64decode(signature).hex())

message = bytes('La implementacion de este ejercicio fue sencilla', 'utf-8')
secret = bytes('MAC', 'utf-8')

signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
print("El segundo mensaje: ")
print(base64.b64decode(signature).hex())
