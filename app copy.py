import tensorflow as tf
import cv2
from keras.src.legacy.preprocessing.image import ImageDataGenerator
import easyocr
from scrapplaca import buscar_fipe
import os

# Verificar se a pasta "Positivas" existe e criá-la se não existir
if not os.path.exists('imagens_placas/Positivas'):
    os.makedirs('imagens_placas/Positivas')

# Inicialize o leitor de OCR
reader = easyocr.Reader(['pt'])

# Inicialize a câmera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera")
    exit()

# Criar um ImageDataGenerator para pré-processamento de imagens
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

# Carregar dados de treinamento e validação
dataset_treinamento = datagen.flow_from_directory(
    'D:/kaliiw/pdv/placa-api/imagens_placas',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',  # ou 'categorical' se houver mais de duas classes
    subset='training'
)

dataset_validacao = datagen.flow_from_directory(
    'D:/kaliiw/pdv/placa-api/imagens_placas',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary',  # ou 'categorical' se houver mais de duas classes
    subset='validation'
)

# Definir e compilar o modelo TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')  # sigmoid para problemas de classificação binária
])

model.compile(optimizer='adam',
              loss='binary_crossentropy',  # se nao for agora vou quebrar essa merdaaaaa
              metrics=['accuracy'])

# Treinar o modelo
model.fit(dataset_treinamento, epochs=10, validation_data=dataset_validacao)

def preprocess_plate_image(frame, detection):

    bbox = detection[0]
    x1, y1 = bbox[0]
    x2, y2 = bbox[2]

    plate_region = frame[y1:y2, x1:x2]

  
    plate_image = cv2.resize(plate_region, (128, 128))


    plate_image = plate_image / 255.0

    plate_image = plate_image.reshape(1, 128, 128, 3)

    return plate_image


while True:
    ret, frame = cap.read()
    if not ret:
        print("Erro ao ler o quadro")
        break

    # Converta o quadro para escala de cinza
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Use o leitor de OCR para encontrar texto na imagem
    results = reader.readtext(gray)

    for detection in results:
        text = detection[1]

        # Se o texto for uma placa válida
        if len(text) in [7, 8]:
            print("Placa detectada:", text)

            # Realize pré-processamento na região da placa, se necessário

            # Faça a busca de informações da placa
            dados_fipe = buscar_fipe(text)
            if dados_fipe:
                print("Informações da placa:", dados_fipe)
            else:
                print("Não foi possível obter informações da placa", text)

            # Pré-processar a imagem da placa e fazer a previsão com o modelo TensorFlow
            plate_image = preprocess_plate_image(frame, detection)
            prediction = model.predict(plate_image)
            if prediction > 0.5:
                print("Placa reconhecida")
                
                # Salvar a imagem da placa positiva
                cv2.imwrite('imagens_placas/Positivas/{}.jpg'.format(text), frame)
                
            else:
                print("Não é uma placa de carro")

    # Exiba o quadro
    cv2.imshow('Video', frame)
    
    # Aguarde pela tecla 'q' para sair do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libere a câmera e feche todas as janelas
cap.release()
cv2.destroyAllWindows()
