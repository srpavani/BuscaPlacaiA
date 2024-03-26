# 1. Coletar Imagens de Placas Reais

# 2. Pré-processamento de Imagem

# 3. Treinar o Modelo
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

# Criar um ImageDataGenerator
datagen = ImageDataGenerator(rescale=1./255)

# Carregar imagens do diretório
dataset = datagen.flow_from_directory(
    'D:\kaliiw\pdv\placa-api\imagens_placas',
    target_size=(128, 128),
    batch_size=32,
    class_mode='binary'  # binary porque temos duas classes: com placa e sem placa
)



# Definir e compilar o modelo
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

# Treinar o modelo
model.fit(dataset, epochs=10)

# 4. Avaliar o Modelo
# (opcional) Avalie o modelo usando um conjunto de validação separado

# 5. Integrar o Modelo Treinado
# Use o modelo treinado para reconhecimento de placas em seu sistema
