import cv2
import time
import requests
import numpy as np
from picamera2 import Picamera2

# url do servidor flask/ngrok fixo
url_servidor = "https://d9404a14953a.ngrok-free.app/ocr"
# fotos por segundo
fps = 1
# compressao da imagem jpeg (mais alto = mais qualidade e mais latencia)
qualidade_jpeg = 70
# redimensionamento da imagem
largura, altura = 800, 600
# salvar imagem/video de teste
salvar_teste = True

# inicia a câmera
cam = Picamera2()
# configura resolucao da camera
cam.configure(cam.create_preview_configuration(main={"size": (largura, altura)}))
# inicia camera
cam.start()
# espera 1s para ajustar exposicao
time.sleep(1)

if salvar_teste:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('ocr_teste.avi', fourcc, fps, (largura, altura))

while True:
    inicio = time.time()

    # captura imagem
    quadro = cam.capture_array()

    # remove canal alpha se presente
    if quadro.shape[2] == 4:
        quadro = cv2.cvtColor(quadro, cv2.COLOR_BGRA2BGR)

    # converte para escala de cinza
    gray = cv2.cvtColor(quadro, cv2.COLOR_BGR2GRAY)

    # equalização adaptativa CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray = clahe.apply(gray)

    # converte pra jpeg e define qualidade
    _, buffer = cv2.imencode('.jpg', gray, [int(cv2.IMWRITE_JPEG_QUALITY), qualidade_jpeg])
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
            print("encontrado:", [t["text"] for t in resultado["textos"]])
        else:
            # caso nao venha chave textos
            print("erro servidor:", resultado)

    except Exception as e:
        # caso ocorra erro de conexao ou excecao
        print("erro conexao:", e)

    if salvar_teste and "textos" in resultado:
        quadro_teste = quadro.copy()
        for t in resultado["textos"]:
            bbox = np.array(t["bbox"], dtype=int)
            # desenha retangulo em torno do texto
            cv2.polylines(quadro_teste, [bbox], isClosed=True, color=(0,255,0), thickness=2)
            # escreve o texto no canto do box
            cv2.putText(quadro_teste, t["text"], tuple(bbox[0]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

        # salva frame individual
        cv2.imwrite(f"teste_{int(time.time())}.jpg", quadro_teste)
        # adiciona frame ao vídeo
        out.write(cv2.resize(quadro_teste, (largura, altura)))

    # calcula tempo restante para manter fps
    tempo_passado = time.time() - inicio
    tempo_espera = max(0, 1.0/fps - tempo_passado)
    time.sleep(tempo_espera)

if salvar_teste:
    out.release()