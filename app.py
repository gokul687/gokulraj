import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize NLTK
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Define the knowledge base (FAQ-style)
knowledge_base = {
    "What are your business hours?": "Our business hours are Monday to Friday, 9 AM to 5 PM, and Saturday, 10 AM to 2 PM.",
    "How can I track my order?": "You can track your order by logging into your account on our website and visiting the 'Order History' section. You'll find a tracking link there.",
    "What is your return policy?": "We offer a 30-day return policy. Items must be unused and in original packaging. Please contact support to initiate a return.",
    "How do I contact support?": "You can contact our support team via email at support@company.com or call us at 1-800-123-4567 during business hours.",
    "Do you offer international shipping?": "Yes, we offer international shipping to select countries. Please check our shipping page for details.",
    "How can I reset my password?": "To reset your password, go to the login page and click 'Forgot Password.' Follow the instructions sent to your email."
}

# Preprocess text (tokenize, remove stopwords, stem)
def preprocess_text(text):
    # Initialize stemmer and stopwords
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))
    
    # Tokenize
    tokens = word_tokenize(text.lower())
    
    # Remove punctuation and stopwords, then stem
    tokens = [stemmer.stem(token) for token in tokens if token not in string.punctuation and token not in stop_words]
    
    return ' '.join(tokens)

# Find the best response from the knowledge base
def get_response(user_input):
    # Preprocess user input
    processed_input = preprocess_text(user_input)
    
    # Preprocess knowledge base questions
    processed_questions = [preprocess_text(q) for q in knowledge_base.keys()]
    
    # Add user input to the list for vectorization
    processed_questions.append(processed_input)
    
    # Vectorize text using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(processed_questions)
    
    # Calculate cosine similarity between user input and knowledge base questions
    similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
    
    # Find the index of the most similar question
    best_match_idx = similarities.argmax()
    best_score = similarities[0][best_match_idx]
    
    # Threshold for similarity (adjust as needed)
    if best_score > 0.3:  # If similarity is high enough
        question = list(knowledge_base.keys())[best_match_idx]
        return knowledge_base[question]
    else:
        return "I'm sorry, I couldn't understand your query. Please try rephrasing or contact our support team at support@company.com."

# Streamlit app
def main():
    st.title("Customer Support Chatbot")
    st.write("Ask me anything about our services, and I'll do my best to help!")

    # Initialize session state for chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Create a container for chat history
    chat_container = st.container()

    # Input form for user query
    with st.form(key='chat_form', clear_on_submit=True):
        user_input = st.text_input("Type your question here:", key="user_input")
        submit_button = st.form_submit_button(label="Send")

    # Process user input when submitted
    if submit_button and user_input:
        # Get chatbot response
        response = get_response(user_input)
        
        # Add user query and response to chat history
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", response))

    # Display chat history
    with chat_container:
        for sender, message in st.session_state.chat_history:
            if sender == "You":
                st.markdown(f"*You*: {message}")
            else:
                st.markdown(f"*Bot*: {message}")

if _name_ == "_main_":
    main()
