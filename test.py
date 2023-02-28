import tensorflow as tf
from tensorflow.keras import layers, models

# Paramètres du modèle
num_classes = 30

# Créer le modèle
model = models.Sequential([
    layers.LSTM(128, return_sequences=True, input_shape=(None, 13)),
    layers.LSTM(64),
    layers.Dense(32, activation='relu'),
    layers.Dense(num_classes, activation='softmax')
])

# Compiler le modèle
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.save('my_model')
