import cv2
import time
import requests
import numpy as np
from picamera2 import Picamera2
import threading
import os
import serial

# url do servidor flask/ngrok fixo
url_servidor = "https://3eed27489550.ngrok-free.app/ocr"
# fotos por segundo
fps = 1
# compressao da imagem jpeg (mais alto = mais qualidade e mais latencia)
qualidade_jpeg = 70
# resolução da imagem
largura, altura = 960, 540
# delay entre envios
delay_envio = 1.5

# salvar imagem de teste
salvar_teste = False

caminho_testes = os.path.expanduser("~/Desktop/KYNTACT-local/Nino/testes")

# inicia a câmera
cam = Picamera2()
# configura resolucao da camera
cam.configure(cam.create_preview_configuration(main={"size": (largura, altura)})) # resolução HD
cam.start()
# espera 1.5s para ajustes automaticos
time.sleep(1.5)	

# abertura da porta serial
ser = serial.Serial("/dev/serial0", 9600, timeout=2)
# limita a 1 thread enviando por vez
ser_limit = threading.Lock()

# função pra enviar img e receber ocr
def envioImg(bytes_img):
    try:
        arquivos = {'image': ('frame.jpg', bytes_img, 'image/jpeg')}
        resposta = requests.post(url_servidor, files=arquivos, timeout=15)
        resultado = resposta.json()

        if "textos" in resultado:
            textos = [t["text"] for t in resultado["textos"]]
            print("encontrado:", textos)

            if textos:
                # escreve mensagem
                mensagem = " ".join(textos) + "\n"

               with ser_limit:
                # envia mensagem 
                   ser.write((mensagem).encode())
                   ser.flush()
             
                if salvar_teste:
                    quadro_teste = cv2.imdecode(np.frombuffer(bytes_img, np.uint8), cv2.IMREAD_COLOR)
                    for t in resultado["textos"]:
                        bbox = np.array(t["bbox"], dtype=int)
                        cv2.polylines(quadro_teste, [bbox], isClosed=True, color=(0,255,0), thickness=2)
                        cv2.putText(quadro_teste, t["text"], tuple(bbox[0]),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                    nome_arquivo  = f"{caminho_testes}/teste_{int(time.tine())}.jpg"
                    cv2.imwrite(nome_arquivo, quadro_teste)
        else:
            # caso nao venha textos
            print("erro servidor:", resultado)

    except Exception as e:
        # caso ocorra erro de conexão ou exceção
        print("erro conexao:", e)

# inicia tempo do próximo envio
prox_envio = time.time()

while True:
    if time.time() >= prox_envio:
        inicio = time.time()

        # captura imagem
        quadro = cam.capture_array()

        # remove canal alpha se presente
        if quadro.shape[2] == 4:
            quadro = cv2.cvtColor(quadro, cv2.COLOR_BGRA2BGR)

        # converte para jpeg e define qualidade
        _, buffer = cv2.imencode('.jpg', quadro, [int(cv2.IMWRITE_JPEG_QUALITY), qualidade_jpeg])
        # transforma em bytes
        bytes_img = buffer.tobytes()

        # envia imagem em thread separada para não travar loop
        threading.Thread(target=envioImg, args=(bytes_img,), daemon=True).start()

        # atualiza tempo do próximo envio
        prox_envio = inicio + delay_envio

        time.sleep(0.01)
