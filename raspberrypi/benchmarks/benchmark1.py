from picamera2 import Picamera2
import cv2
import pytesseract
import easyocr
import time

# benchmark1.py: teste inicial, feito no meu PC e no pi3; resultados inconclusivos

# idioma de reconhecimento pt e pt-br do easyocr
# reader = easyocr.Reader(['pt'])

# inicia a câmera (mudei pra picamera2)
picam2 = Picamera2()
picam2.start()

# variavel camera recebe o que o opencv tá capturando como vídeo. 
# camera = cv2.VideoCapture(0)
# camera = cv2.VideoCapture("/xx/xx/xx/xx")
# 0 = capturar a câmera/webcam; se tiver várias câmeras, sobe de 1 em 1 (1 pra segunda, 2 pra terceira, etc.)
# "video.mp4" = capturar o arquivo de vídeo chamado video.mp4


# esse while para se status (ler abaixo) retornar false ou se a tecla Q for pressionada
while True:
    # a função .read sempre retorna 2 variáveis em uma ordem definida:
    # a primeira é um boleano que define se o video foi capturado com sucesso (nesse caso status)
    # e a segunda é a imagem q está sendo capturada no momento (nesse caso foto)
    foto = picam2.capture_array()
    # pré-processamento pro pytesseract: transforma RGB em 1 canal para ajudar os OCRs no processamento (gray/BGR2GRAY),
    imgcinza = cv2.cvtColor(foto, cv2.COLOR_BGR2GRAY)
    # e converte a imagem acizentada (gray) em preto e branco para aumentar o contraste entre texto e fundo
    limitemin, thresh = cv2.threshold(imgcinza, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # explicação mais técnica: 0 = número de limite, onde locais da imagem com valores acima de 0 ficam
    # brancos e abaixo de 0 ficam pretos, esse número vai ser mudado pelo thresh_otsu que define ele
    # de forma automática, assim o limite é flexível e muda automaticamente pra cada imagem

    # copia o frame atual pros dois OCRs poderem ler
    foto_pytesseract = foto.copy()
    # foto_easyocr = foto.copy()

    # exibição de tempo de processamento e texto processado, com uso da imagem cinza + binarizada
    start_time = time.time()
    text_pytesseract = pytesseract.image_to_string(thresh, lang='por')
    time_pytesseract = time.time() - start_time

    # exibição de tempo de processamento e texto processado, com uso da imagem cinza
    # start_time = time.time()
    # results_easyocr = reader.readtext(imgcinza)
    # text_easyocr = " ".join([result[1] for result in results_easyocr])
    # time_easyocr = time.time() - start_time

    # desenha os resultados em cima da imagem
    cv2.putText(foto_pytesseract,  text_pytesseract, (10,70),
              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(foto_pytesseract, text_pytesseract, (10, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # cv2.putText(foto_easyocr, f"EasyOCR: {time_easyocr:.2f}s", (10, 30), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    # cv2.putText(foto_easyocr, text_easyocr, (10, 70), 
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # exibição dos resultados do benchmark; hconcat só mostra duas imagens horizontalmente
    # combined = cv2.hconcat([foto_pytesseract, foto_easyocr])
    combined = cv2.hconcat([foto_pytesseract, foto_pytesseract])

    cv2.imshow("benchmark dos ocrs", combined)

    # tecla Q pra fechar
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # pequena pausa pra aliviar a CPU
    time.sleep(1.5)

# libera a câmera
picam2.stop()

# fecha tudo
cv2.destroyAllWindows()