import streamlit as st
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Initialize NLTK tools
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Predefined intents and responses for tyre sales
INTENTS = {
    "greeting": {
        "patterns": [r"hi|hello|hey|greetings"],
        "responses": ["Hello! Welcome to TyreWorld. How can I assist you with your tyre needs today?"]
    },
    "tyre_types": {
        "patterns": [r"tyre types|types of tyres|what tyres do you have|tyre kinds"],
        "responses": ["We offer a variety of tyres including All-Season, Winter, Performance, and Off-Road tyres. Could you specify your vehicle type or driving needs?"]
    },
    "pricing": {
        "patterns": [r"price|cost|how much|pricing"],
        "responses": ["Tyre prices vary based on size and type. For example, All-Season tyres start at $50 each. Please provide the tyre size or vehicle model for an accurate quote."]
    },
    "availability": {
        "patterns": [r"available|in stock|do you have|availability"],
        "responses": ["Most tyre sizes are in stock! Please tell me the specific tyre size or brand you're looking for, and I'll check availability."]
    },
    "support": {
        "patterns": [r"help|support|issue|problem|installation"],
        "responses": ["We provide full support including installation guidance and warranty information. What's the specific issue or question you have?"]
    },
    "store_location": {
        "patterns": [r"store|location|where are you|address"],
        "responses": ["Our main store is at 123 Tyre Avenue, Auto City. Would you like directions or information about our online ordering options?"]
    },
    "goodbye": {
        "patterns": [r"bye|goodbye|thank you|thanks"],
        "responses": ["Thank you for choosing TyreWorld! Feel free to reach out anytime. Goodbye!"]
    }
}

# Function to preprocess user input
def preprocess_text(text):
    text = text.lower().strip()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words and token.isalnum()]
    return tokens, text

# Function to detect intent
def detect_intent(user_input):
    tokens, raw_text = preprocess_text(user_input)
    for intent, data in INTENTS.items():
        for pattern in data["patterns"]:
            if re.search(pattern, raw_text, re.IGNORECASE):
                return intent, data["responses"][0]
    return None, "I'm sorry, I didn't understand that. Could you please clarify or ask about tyre types, pricing, or support?"

# Streamlit app
def main():
    st.set_page_config(page_title="TyreWorld Customer Service Chatbot", page_icon="🚗")
    st.title("TyreWorld Customer Service Chatbot")
    st.markdown("Ask about tyre types, pricing, availability, or get support for your tyre needs!")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Welcome to TyreWorld! How can I help you today?"}]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Type your question here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get chatbot response
        intent, response = detect_intent(user_input)
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

if _name_ == "_main_":
    main()
