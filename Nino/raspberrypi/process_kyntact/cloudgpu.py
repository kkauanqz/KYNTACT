from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np

# cria servidor web
app = Flask(__name__)

# carrega OCR
reader = easyocr.Reader(['pt'])

@app.route("/ocr", methods=["POST"])
def ocr_api():
    try:
        # recebe imagem do Pi
        img_bytes = request.files['image'].read()
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

        # pré-processamento para OCR
        # garante que a imagem tem 3 canais (BGR)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        # converte para cinza
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # CLAHE técnica de aprimorar contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)

        # OCR
        ocr_res = reader.readtext(gray)

        # filtra caracteres estranhos
        textos = []
        permitidos = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789ÀÁÂÃÄÅÇÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÝàáâãäåçèéêëìíîïòóôõöùúûüýÿ "

        # bbox pra exibir área de detecção nas imgs
        for (bbox, text, prob) in ocr_res:
            filtrado = ''.join([c for c in text if c in permitidos])
            if len(filtrado.strip()) > 0:
                textos.append({"text": filtrado.strip(), "bbox": np.array(bbox, dtype=float).tolist()})

        # retorna resultado em json
        return jsonify({"textos": textos})

    except Exception as e:
        # caso ocorra erro
        return jsonify({"error": str(e)})

# endereçamento e autenticação
ngrok.set_auth_token("31kJtDVtgd8rzr8vvsPzAlXUwCX_7HXLqFXJF66uWZbrGfM78")
public_url = ngrok.connect(5000)
print("URL:", public_url)

# inicia servidor
app.run(host="0.0.0.0", port=5000, threaded=True)
