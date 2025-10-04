import cv2
import time
import requests
from picamera2 import Picamera2

# url do servidor colab/ngrok
url_servidor = "https://db8f132d9764.ngrok-free.app/ocr"
# fotos por segundo
fps = 1
# compressao da imagem jpeg (mais alto = mais qualidade e mais latencia)
qualidade_jpeg = 70
# redimensionamento da imagem
largura, altura = 1280, 720

# inicia a câmera
cam = Picamera2()
# configura resolucao da camera
cam.configure(cam.create_preview_configuration(main={"size": (largura, altura)}))
# inicia camera
cam.start()
# espera 1s para ajustar exposicao
time.sleep(1)

while True:
    inicio = time.time()

    # captura imagem
    quadro = cam.capture_array()

    # converte para jpeg e define qualidade
    _, buffer = cv2.imencode('.jpg', quadro, [int(cv2.IMWRITE_JPEG_QUALITY), qualidade_jpeg])
    # transforma em bytes
    bytes_img = buffer.tobytes()

    try:
        # prepara arquivo para envio binario
        arquivos = {'image': ('frame.jpg', bytes_img, 'image/jpeg')}
        # envia requisicao post para o servidor
        resposta = requests.post(url_servidor, files=arquivos, timeout=5)
        # recebe resultado em json
        resultado = resposta.json()
        # verifica se resultado contem textos
        if "textos" in resultado:
            # imprime textos reconhecidos
            print("encontrado:", resultado["textos"])
        else:
            # caso nao venha chave textos
            print("erro servidor", resultado)
    except Exception as e:
        # caso ocorra erro de conexao ou excecao
        print("erro conexao", e)

    # calcula tempo restante para manter fps
    tempo_passado = time.time() - inicio
    tempo_espera = max(0, 2.0/fps - tempo_passado)
    # espera antes do proximo loop
    time.sleep(tempo_espera)