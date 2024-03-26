import cv2
import easyocr

# Inicializar o leitor EasyOCR
reader = easyocr.Reader(['en'])

# Capturar vídeo da câmera
cap = cv2.VideoCapture(0)

# Verificar se a câmera foi inicializada corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

# Sinalizador de término
terminate_flag = False

while not terminate_flag:
    # Ler um quadro do vídeo
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler o quadro")
        break

    # Exibir o quadro em uma janela
    cv2.imshow('Video', frame)

    # Converter o quadro para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar placas no quadro
    results = reader.readtext(gray)

    # Extrair texto das placas detectadas
    for detection in results:
        text = detection[1]
        print("Placa do veículo:", text)

    # Verificar se o usuário pressionou a tecla 'q' para sair do loop
    if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
        terminate_flag = True

# Liberar a captura de vídeo e fechar todas as janelas
cap.release()
cv2.destroyAllWindows()
