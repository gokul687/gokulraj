import streamlit as st
import json
import random
import pickle

# Load intents
with open("intents.json") as file:
    data = json.load(file)

# Load vectorizer and models
with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("model_logreg.pkl", "rb") as f:
    model_logreg = pickle.load(f)
with open("model_rf.pkl", "rb") as f:
    model_rf = pickle.load(f)
with open("model_svm.pkl", "rb") as f:
    model_svm = pickle.load(f)
with open("model_nb.pkl", "rb") as f:
    model_nb = pickle.load(f)

# Dictionary of models
models = {
    "Logistic Regression": model_logreg,
    "Random Forest": model_rf,
    "SVM": model_svm,
    "Naive Bayes": model_nb
}

# Get a chatbot response from a model
def get_response(user_input, model):
    X = vectorizer.transform([user_input])
    predicted_tag = model.predict(X)[0]

    for intent in data["intents"]:
        if intent["tag"] == predicted_tag:
            return random.choice(intent["responses"])
    return "Sorry, I don't understand that."

# Streamlit UI
st.set_page_config(page_title="Smart Chatbot", layout="centered")
st.title("AI Customer Support Chatbot")
st.write("This chatbot uses four different machine learning models to understand your query and respond.")

# User input
user_input = st.text_input("Ask your question below:")

# Model selection
model_choice = st.selectbox("Choose a model to respond with:", ["All"] + list(models.keys()))

# Display response(s)
if user_input:
    st.markdown("### Response(s):")
    if model_choice == "All":
        for name, model in models.items():
            response = get_response(user_input, model)
            st.text_area(f"{name} says:", response, height=80)
    else:
        selected_model = models[model_choice]
        response = get_response(user_input, selected_model)
        st.text_area("Chatbot says:", response, height=100)
