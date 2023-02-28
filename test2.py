import tensorflow as tf
import pyaudio
import numpy as np

# Paramètres du modèle
input_shape = (16000, 1)
num_classes = 30

# Charger le modèle
model = tf.keras.models.load_model('my_model')

# Créer un dictionnaire de correspondance entre les sorties du modèle et les commandes vocales
commands = ['yes', 'no', 'up', 'down', 'left', 'right', 'on', 'off', 'stop', 'go', 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'bed', 'bird', 'cat', 'dog', 'happy', 'house', 'marvin', 'sheila', 'tree', 'wow']
mapping = dict(zip(range(num_classes), commands))

# Fonction pour prétraiter les données audio
def preprocess(audio):
    audio = audio.astype(np.float32) / 32767.0
    audio = np.expand_dims(audio, axis=-1)
    audio = tf.image.resize(audio, size=input_shape[:2])
    return audio

# Fonction pour prédire la commande vocale
def predict(audio):
    audio = preprocess(audio)
    prediction = model.predict(audio)[0]
    predicted_index = np.argmax(prediction)
    predicted_command = mapping[predicted_index]
    return predicted_command

# Paramètres de capture audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK_SIZE = 1024

# Initialiser PyAudio
p = pyaudio.PyAudio()

# Ouvrir le flux audio
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE)

# Boucle de capture et de prédiction
while True:
    # Lire les données audio
    data = stream.read(CHUNK_SIZE)
    data = np.frombuffer(data, dtype=np.int16)

    # Prédire la commande vocale
    command = predict(data)
    print(command)
