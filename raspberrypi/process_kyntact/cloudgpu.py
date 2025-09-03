from flask import Flask, request, jsonify
# from ultralytics import YOLO
import easyocr
import cv2
import numpy as np
from pyngrok import ngrok

# cria servidor web
app = Flask(__name__)

# https://courses.opencv.org/courses/course-v1:PyTorch+Bootcamp+Deep-Learning/courseware/8d83a7eb2e1b485e88120e4ac77a3520/3bf6e633acc6432ab06a6f868f7d0b6b/1?activate_block_id=block-v1%3APyTorch%2BBootcamp%2BDeep-Learning%2Btype%40vertical%2Bblock%40c3f958f2888842cab574cc3a168b5cd6
# bootcamp pytorch pra treinar yolo/easyyoloocr
# https://github.com/aqntks/Easy-Yolo-OCR

# carrega modelos
# model = YOLO("yolov8x.pt")   # versão e idioma do yolo // certificar que o colab tem o arquivo nativamente, se não usar 'files.upload()' (?)
reader = easyocr.Reader(['pt']) # idioma do easyocr

@app.route("/ocr", methods=["POST"])
def ocr_api():
    try:
        # recebe imagem do Pi
        img_bytes = request.files['image'].read()
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

# --------------------------------------
# detecta objetos
# results = model(img)
# detections = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes else []
# --------------------------------------

        textos = []

# --------------------------------------
# for box in detections:
    # x1, y1, x2, y2 = map(int, box[:4])
    # crop = img[y1:y2, x1:x2]
# --------------------------------------

        # opencv: adicionar mais pré processamento e treinamento
        crop = img
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        gray = cv2.GaussianBlur(gray, (3,3), 0)

        # binarização alternativa otsu
        _, thresh =cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # morfologia (opcional)
        kernel = np.ones((2,2), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        # adaptação à rotação
        # coords = np.column.stack(np.where(thresh > 0))
        # if len(coords > 0:
                 # cv2.cv2.minAreaRect(coords)[-1]
                 # if angle < -55:
                # )



# --------------------------------------
      # binarização
      # thresh = cv2.adaptiveThreshold(
          # gray,                  # imagem em escala de cinza
          # 255,                   # valor máximo após o threshold (255 = branco)
          # cv2.ADAPTIVE_THRESH_MEAN_C,  # ou cv2.ADAPTIVE_THRESH_GAUSSIAN_C
          # cv2.THRESH_BINARY,     # tipo de binarização
          # 11,                    # tamanho do bloco (tem que ser ímpar, tipo 11, 13, 15...)
          # 2                      # valor subtraído da média
      # )
# --------------------------------------

        ocr_res = reader.readtext(gray, contrast_ths=0.5, adjust_contrast=0.7)
        #, text_threshold=0.5, remove informações(texto) poluentes



        for (_, text, _) in ocr_res:
            if len(text.strip()) > 1:  # filtra textos muito curtos
                textos.append(text.strip())

        return jsonify({"textos": textos})

    except Exception as e:
        return jsonify({"error": str(e)})

ngrok.set_auth_token("31kJtDVtgd8rzr8vvsPzAlXUwCX_7HXLqFXJF66uWZbrGfM78")

# exibe porta de acesso usando o ngrok
public_url = ngrok.connect(5000)
print("URL:", public_url)

# inicia servidor flask/ngrok em uma thread pra poder rodar mais códigos
app.run(host="0.0.0.0", port=5000, threaded=True)
