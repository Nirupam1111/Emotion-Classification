import streamlit as st
import numpy as np
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem import PorterStemmer
import pickle
stopwords = set(nltk.corpus.stopwords.words('english'))


# load files
lg = pickle.load(open('logistic_regresion.pkl','rb'))
tfidf_vectorizer = pickle.load(open('tfidf_vectorizer.pkl','rb'))
lb = pickle.load(open('label_encoder.pkl','rb'))

def clean_text(text):
    stemmer = PorterStemmer()
    text = re.sub("[^a-zA-Z]", " ", text)
    text = text.lower()
    text = text.split()
    text = [stemmer.stem(word) for word in text if word not in stopwords]
    return " ".join(text)

def predict_emotion(input_text):
    cleaned_text = clean_text(input_text)
    input_vectorized = tfidf_vectorizer.transform([cleaned_text])

    # Predict emotion
    predicted_label = lg.predict(input_vectorized)[0]
    predicted_emotion = lb.inverse_transform([predicted_label])[0]
    label =  np.max(lg.predict(input_vectorized))

    return predicted_emotion,label


# App
st.title("Human Emotions Detection App")

# taking input from user
user_input = st.text_input("Enter your text here: ")

if st.button("Predict"):
    predicted_emotion, label = predict_emotion(user_input)
    st.write("Predicted Emotion:", predicted_emotion)
    st.write("Probability:", label)

