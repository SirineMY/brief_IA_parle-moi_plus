import streamlit as st
import openai
import speech_recognition as sr
import pyttsx3


#Configure a valid API key
openai.api_key = "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"

#Initialize the speech recognition engine
r = sr.Recognizer()

st.markdown("""
<style>
div.stApp{
    background-image:url('https://wallpaperaccess.com/full/6358963.jpg');
    background-repeat: no-repaet;
    background-size: cover; 
}
header{
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)



#Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    if 'french' in voice.languages and 'femme' in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break    

STOP_PHRASE = "exit"

#Function to transcribe audio from microphone
def transcribe_audio():
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        st.markdown(
    f'<div style="background-color:#E4EFFF; border:1px solid #9FC6FF; display:inline-block; -moz-border-radius:12px 0;-webkit-border-radius:12px 0;border-radius:12px 0;">AI: Bonjour! Comment puis-je vous aider?</div>',
    unsafe_allow_html=True
)

        audio = r.listen(source)
        st.markdown(
    f'<div style="background-color:#E4EFFF;border:1px solid #9FC6FF; padding:5px; display:inline-block; -moz-border-radius:12px 0; -webkit-border-radius:12px 0; border-radius:12px 0;">Transcription en cours...</div>',
    unsafe_allow_html=True
)

    try:
        prompt = r.recognize_google(audio, language="fr-FR")
        st.markdown(
    f'<div style="text-align:right;">'
    f'<div style="display:inline-block; background-color:#CEF6D8; border:1px solid #81F79F; padding:5px; -moz-border-radius:0 12px; -webkit-border-radius:0 12px; border-radius:0 12px;">'
    f'{prompt}'
    f'</div></div>',
    unsafe_allow_html=True
)

        return prompt
    except sr.UnknownValueError:
        st.markdown(
    f'<div style="background-color:#F6CECE ; border:1px solid #FA5858; display:inline-block; padding:5px; -moz-border-radius:12px 0;-webkit-border-radius:12px 0;border-radius:12px 0;">AI: Désolé, je n/ai pas compris. Pouvez-vous répéter s/il vous plaît?</div>',
     unsafe_allow_html=True
)
        return None
    except sr.RequestError as e:
        st.write("AI: Désolé, il y a eu une erreur de service. Pouvez-vous réessayer plus tard? {0}".format(e))
        return None
#Function to speak text using the text-to-speech engine
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    # Modifier le style de la page
    st.markdown(
    f"<h1 style='color: blue; font-size: 36px;'>IA Parle-moi plus</h1>",
    unsafe_allow_html=True
)

# Modifier le style du texte
    st.markdown(
        f"<p style='color: bleu; font-size: 24px;'>Bonjour! Je suis une IA, posez-moi vos questions en français et je ferai de mon mieux pour y répondre.</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='color: blue; font-size: 18px;'>&#x1F680; C'est parti!</p>",
        unsafe_allow_html=True
    )

    while True:
        # Transcribe audio
        prompt = transcribe_audio()
        if prompt is None:
            continue
        if prompt == STOP_PHRASE:
            st.markdown(f"<p style='text-align: center;color: blue; font-size: 18px; '>&#x1F44B; Au revoir! &#x1F44B;</p>", unsafe_allow_html=True)
            break

        # Send a request to the GPT API
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.3,
        )

        # Show the response
        st.markdown(
    f'<div style="background-color:#E4EFFF;border:1px solid #9FC6FF; padding:5px; display:inline-block; -moz-border-radius:12px 0; -webkit-border-radius:12px 0; border-radius:12px 0;">Voici ma réponse: </div>',
    unsafe_allow_html=True
)
        st.markdown(
    f'<div style="background-color:#E4EFFF;border:1px solid #9FC6FF; padding:5px; display:inline-block; -moz-border-radius:12px 0; -webkit-border-radius:15px 0; border-radius:15px 0;">{response["choices"][0]["text"]}</div>',
    unsafe_allow_html=True
)
        speak_text(response["choices"][0]["text"])


if __name__ == "__main__":
    main()




