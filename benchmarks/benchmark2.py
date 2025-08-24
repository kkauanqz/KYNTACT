from picamera2 import Picamera2
import cv2
import pytesseract
import easyocr
import time

# benchmark2.py: teste inicial no pi 4, depois da instalação do módulo de câmera; easyocr talvez precise de mais configuração pra rodar,
# e aparentemente pytesseract não funciona sem pre-processamento

# inicia a câmera especificando formato
picam2 = Picamera2()
config = picam2.create_preview_configuration({"format": "XRGB8888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

# inicia easyocr 
reader = easyocr.Reader(['en', 'pt']) # ingles e pt pra ficar mais fácil de testar

while True:
    
    # qualquer coisa com "time" é pra saber quanto tempo estão levando pra processar a imagem
    start_total = time.time()

    # captura frames da câmera em vetor
    frame = picam2.capture_array()

    # pytesseract
    start_tess = time.time()
    text_tess = pytesseract.image_to_string(frame, lang="por+eng")  # ajusta idiomas
    tess_time = time.time() - start_tess

    # easyocr
    start_easy = time.time()
    results_easy = reader.readtext(frame)
    text_easy = " ".join([res[1] for res in results_easy])
    easy_time = time.time() - start_easy

    # exibição de info no console caso a interface trave demais
    print("="*50)
    print(f"[Pytesseract - {tess_time:.2f}s]")
    print(text_tess.strip())
    print(f"[EasyOCR - {easy_time:.2f}s]")
    print(text_easy.strip())

    # exibição dos resultados do benchmark lado a lado
    # copia o frame recebido da picamera2 pro canvas fazer arte
    canvas = frame.copy()
    #
    h, w, _ = canvas.shape
    overlay = canvas.copy()

    # coloca o texto em uma caixa em baixo da interface
    cv2.rectangle(overlay, (0, h-100), (w, h), (0,0,0), -1)
    alpha = 0.7
    canvas = cv2.addWeighted(overlay, alpha, canvas, 1-alpha, 0)

    # inscrição dos resultados
    cv2.putText(canvas, f"Tesseract ({tess_time:.2f}s): {text_tess[:50]}",
                (10, h-70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
    cv2.putText(canvas, f"EasyOCR   ({easy_time:.2f}s): {text_easy[:50]}",
                (10, h-40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,200,255), 2)

    cv2.imshow("benchmark dos ocrs", canvas)

    # 1 segundo entre as capturas
    key = cv2.waitKey(1000) & 0xFF
    # se tecla 27 (esc) for apertada, fecha
    if key == 27:
        break

# fecha tudo e para a picamera2
cv2.destroyAllWindows()
picam2.stop()