from picamera2 import PiCamera2
from time import sleep

camera = PiCamera()

camera.resolution = (1920, 1080)

sleep(2)

camera.capture("foto.jpg")

camera.close()

print("Foto salva")

