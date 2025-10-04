# instalação dos pacotes
!pip install -q --upgrade ultralytics flask pyngrok easyocr opencv-python-headless symspellpy
!ngrok update

# início do código
from flask import Flask, request, jsonify
import easyocr
import cv2
import numpy as np
from pyngrok import ngrok
from symspellpy import SymSpell, Verbosity
import re
import unicodedata
import os
import urllib.request

# criação do server web
app = Flask(__name__)

reader = easyocr.Reader(['pt']) # idioma do easyocr

# inicializa symspell
sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# link do dicionário br sem acentos da ime
url_dict = "https://www.ime.usp.br/~pf/dicios/br-sem-acentos.txt"
arquivo_dict = "br-sem-acentos.txt"

# baixa o dicionário se não existir
if not os.path.exists(arquivo_dict):
    urllib.request.urlretrieve(url_dict, arquivo_dict)

# converte pro formato symspell (palavra + frequência 1)
arquivo_dict_symspell = "dicionario_frequencia_pt_BR.txt"
if not os.path.exists(arquivo_dict_symspell):
    with open(arquivo_dict, "r", encoding="utf-8") as f, open(arquivo_dict_symspell, "w", encoding="utf-8") as out:
        for linha in f:
            palavra = linha.strip().lower()
            if palavra:
                out.write(f"{palavra} 1\n")

# carrega o dicionário
sym_spell.load_dictionary(arquivo_dict_symspell, term_index=0, count_index=1)

# descapitaliza e desacentua palavras
def corrigir_texto(texto: str) -> str:
    # tira acentos e deixa tudo minúsculo
    texto_processado = "".join(
        c for c in unicodedata.normalize('NFD', texto) if not unicodedata.combining(c)
    ).lower()

    # cprreção de palavras
    def corrige_palavra(match):
        w = match.group()
        if len(w) <= 2 or w.isdigit():
            return w
        sugestoes = sym_spell.lookup(w, Verbosity.CLOSEST, max_edit_distance=2)
        return sugestoes[0].term if sugestoes else w

    # aplica a correção no texto inteiro de uma vez
    texto_corrigido = re.sub(r'\b\w+\b', corrige_palavra, texto_processado)
    return texto_corrigido

# EasyOCR
@app.route("/ocr", methods=["POST"])
def ocr_api():
    try:
        # recebe imagem em grayscale
        img_bytes = request.files['image'].read()
        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)

        # aumento de contraste
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        img = clahe.apply(img)
        img = cv2.normalize(img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

        # leitura OCR
        ocr_res = reader.readtext(img, contrast_ths=0.5, adjust_contrast=0.7)

        textos_corrigidos = []
        for item in ocr_res:
            if len(item) != 3:
                continue  # ignora entradas inesperadas
            bbox, text, conf = item
            if len(text.strip()) > 1:
                texto_corrigido = corrigir_texto(text)
                textos_corrigidos.append({
                    "text": texto_corrigido,
                    "bbox": [[int(x), int(y)] for (x, y) in bbox]
                })

        return jsonify({"textos": textos_corrigidos})

    except Exception as e:
        return jsonify({"error": str(e)})

# configuração do ngrok
ngrok.set_auth_token("31kJtDVtgd8rzr8vvsPzAlXUwCX_7HXLqFXJF66uWZbrGfM78")
public_url = ngrok.connect(5000)
print("URL:", public_url)

# inicia servidor Flask/ngrok
app.run(host="0.0.0.0", port=5000, threaded=True)