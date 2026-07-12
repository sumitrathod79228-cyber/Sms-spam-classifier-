import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download required NLTK resources only once
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# Load model and vectorizer
with open("vectorizer.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open("model.pkl", "rb") as f:
    model = pickle.load(f)


def transform_text(text):
    text = text.lower()
    words = nltk.word_tokenize(text)

    filtered_words = []

    for word in words:
        if word.isalnum():
            if word not in stop_words and word not in string.punctuation:
                filtered_words.append(ps.stem(word))

    return " ".join(filtered_words)


# Streamlit UI
st.set_page_config(page_title="SMS Spam Classifier", page_icon="📩")

st.title("📩 Email/SMS Spam Classifier")

input_sms = st.text_area("Enter your message")

if st.button("Predict"):

    transformed_sms = transform_text(input_sms)

    vector_input = tfidf.transform([transformed_sms])

    prediction = model.predict(vector_input)[0]

    if prediction == 1:
        st.error("🚨 Spam Message")
    else:
        st.success("✅ Not Spam")
