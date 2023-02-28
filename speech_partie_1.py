import os
import openai
import azure.cognitiveservices.speech as speechsdk


# Set up API keys and credentials
openai.api_key = "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"
speech_key = "48d09128b4cf44aa8c70d9e528261235"
speech_region = "francecentral"

# Set up speech recognition
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
speech_config.speech_recognition_language = "fr-FR"
audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

# Set up OpenAI API
openai_engine = "davinci"

# Function to recognize speech from microphone
def recognize_from_microphone():
    recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Speak into your microphone.")
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return ""

# Function to answer a question using OpenAI API
def answer_question(question):
    response = openai.Completion.create(
        engine=openai_engine,
        prompt=question,
        max_tokens=100,
        stop=None,
        temperature=0.7,
    )

    if response.choices and len(response.choices) > 0 and response.choices[0].text.strip() != "":
        return response.choices[0].text.strip()
    else:
        return "Je ne comprends pas la question."

# Main function to run the program
def main():
    while True:
        question = recognize_from_microphone()
        if question != "":
            print("Question: {}".format(question))
            answer = answer_question(question)
            print("Réponse: {}".format(answer))
        else:
            print("Je n'ai pas entendu de question. Veuillez réessayer.")

if __name__ == "__main__":
    main()

