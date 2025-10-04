from picamera2 import Picamera2
import cv2
import pytesseract
import easyocr
import time
from ultralytics import YOLO

# benchmark3.py: teste com yolo e pré-processamento

# inicia o yolo com o modelo base
model = yolo("yolov8n.pt")

# inicia a câmera especificando formato e config
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (2592, 1944)})
picam2.configure(config)
picam2.set_controls({
    "AeEnable": False, # desativa filtro automatico da câmera
})
picam2.start()

# pré-processamento pro pytesseract
def preprocess_ocr(img):
    # reduz ruído
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    # escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # aumenta o tamanho em 2x
    scale_percent = 200
    width = int(gray.shape[1] * scale_percent / 100)
    height = int(gray.shape[0] * scale_percent / 100)
    gray = cv2.resize(gray, (width, height), interpolation=cv2.INTER_LINEAR)
    # contraste
    gray = cv2.equalizeHist(gray)
    # filtro de nitidez
    kernel = [[0,-1,0], [-1,5,-1], [0,-1,0]]
    gray = cv2.filter2D(gray, -1, kernel)
    # binarização
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh

# loop principal de captura
while True:

    # qualquer coisa com "time" é pra saber quanto tempo estão levando pra processar a imagem
    start_time = time.time()

    # captura frames da câmera em vetor
    frame = picam2.capture_array()

    # converte BGRA pra BGR se necessário
    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    # detecta regiões de interesse com yolo
    results = model(frame, verbose=False)
    crops = []
    boxes = []

    # se yolo achou algum objeto aplicavel, recorta e deixa só ele no frame
    if results[0].boxes is not None and len(results[0].boxes) > 0:
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            crops.append(frame[y1:y2, x1:x2])
            boxes.append((x1, y1, x2, y2))
    else:
        # se não achou nada, passa o frame inteiro
        crops.append(frame)
        boxes.append((0,0,frame.shape[1], frame.shape[0]))

    # roda o OCR no frame recebido do yolo
    texts_found = []
    for crop in crops:
        ocr_img = preprocess_ocr(crop)
        text = pytesseract.image_to_string(
            ocr_img, lang="por", config="--oem 3 --psm 7"
        )
        if text.strip():
            texts_found.append(text.strip())

    # exibição dos resultados na interface
    # copia o frame recebido da picamera2 pro canvas fazer arte
    canvas = frame.copy()
    #
    h, w, _ = canvas.shape
    overlay = canvas.copy()

    # desenha caixas e textos encontrados
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = box
        cv2.rectangle(canvas, (x1, y1), (x2, y2), (0,255,0), 2)
        if i < len(texts_found):
            cv2.putText(canvas, texts_found[i], (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    elapsed = time.time() - start_time
    print("="*50)
    print(f"Tempo por foto: {elapsed:.2f}s")
    for txt in texts_found:
        print(txt)

    cv2.imshow("OCR com yolo + Tesseract", canvas)

    # 2 segundos entre as capturas
    key = cv2.waitKey(2000) & 0xFF
    # se tecla 27 (esc) for apertada, fecha
    if key == 27:
        break

# fecha tudo e para a picamera2
cv2.destroyAllWindows()
picam2.stop()