import paho.mqtt.client as mqtt
import time

# configs do mqtt com localhost
broker = "127.0.0.1"
client = mqtt.Client()
client.connect(broker, 1883, 60)

# envio estatico da palavra "ola"
texto = "ola"
while True:
    for letra in texto:
        client.publish("ocr/palavra", letra)
        time.sleep(1)