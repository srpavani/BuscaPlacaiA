import cv2
import easyocr
from scrapplaca import buscar_fipe
reader = easyocr.Reader(['pt'])

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler o quadro")
        break

    cv2.imshow('Video', frame)

    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    camera = reader.readtext(gray)

    for placaDetectada in camera:
        placa = placaDetectada[1]
        if(len(placa)==7 or len(placa)==8):
            print(placa)
            dados_fipe = buscar_fipe(placa)
            if dados_fipe:
                print(dados_fipe)
            else:
                print('Não foi possível obter informações da placa', placa)       
    
   
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
