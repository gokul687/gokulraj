import streamlit as st
import time

# Dictionary of common customer support queries and responses
responses = {
    "hi": "Hello! How can I assist you today?",
    "hello": "Hi there! Welcome to our customer support. What's your question?",
    "order status": "Please provide your order ID, and I'll check the status for you!",
    "track order": "To track your order, share your order ID, and I'll fetch the details.",
    "return": "To initiate a return, please share your order ID and reason for return.",
    "refund": "For refunds, provide your order ID, and I'll guide you through the process.",
    "contact": "You can reach us at support@example.com or call 1-800-123-4567.",
    "hours": "Our support hours are 9 AM to 5 PM, Monday to Friday.",
    "thanks": "You're welcome! Anything else I can help with?",
    "bye": "Goodbye! Have a great day!",
}

# Function to get chatbot response
def get_response(user_input):
    user_input = user_input.lower().strip()
    # Check for matching query in responses
    for key in responses:
        if key in user_input:
            return responses[key]
    # Default response for unrecognized queries
    return "I'm sorry, I didn't understand that. Could you please rephrase or ask about order status, returns, refunds, or contact info?"

# Streamlit app
def main():
    # Set page title and icon
    st.set_page_config(page_title="Customer Support Chatbot", page_icon="🤖")

    # App header
    st.title("🤖 Customer Support Chatbot")
    st.write("Ask about order status, returns, refunds, or contact info. Type 'bye' to end the chat.")

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get and display bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                time.sleep(1)  # Simulate processing time
                response = get_response(user_input)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
