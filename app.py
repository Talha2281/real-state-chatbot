import streamlit as st
import requests

# Streamlit configuration
st.set_page_config(page_title="Immo Green AI Chatbot", layout="wide")

# Welcome animation and introduction
def show_welcome():
    st.title("Welcome to Immo Green AI!")
    st.video("https://www.example.com/welcome-video.mp4")  # Replace with actual video URL
    st.write("""
        At Immo Green AI, we offer advanced real estate services tailored to your needs.
        Discover, buy, rent, or manage properties efficiently with our AI-powered system.
    """)

# Login and user session
def login():
    st.sidebar.title("Login")
    with st.sidebar.form("login_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        submit_button = st.form_submit_button("Login")

        if submit_button:
            st.session_state["user_logged_in"] = True
            st.session_state["user_email"] = email
            st.success("Login successful! Redirecting...")
            st.experimental_rerun()

# Chatbot functionality
def chatbot():
    # Display categories
    st.write("Welcome back! How can we assist you today?")
    option = st.selectbox("Choose a category:", [
        "Buy or sell real estate",
        "Rental and management",
        "Renovation",
        "Construction projects and planning"
    ])

    # Search functionality
    if st.button("Ask a Question"):
        query = st.text_input("Search for a property (e.g., 'Apartment in Zurich'):")
        if query:
            st.write(f"Searching for: {query}")
            # Filter options
            price = st.number_input("Price (Max):", step=1000, value=500000)
            size = st.number_input("Size (Min in sqft):", step=100, value=500)
            condition = st.selectbox("Condition:", ["New", "Renovated", "Old"])
            region = st.text_input("Region (e.g., Zurich):")
            property_type = st.selectbox("Property Type:", ["Apartment", "House", "Land", "Commercial"])
            
            # Placeholder for results
            st.write("Results:")
            st.write("Fetching results...")  # Replace with actual API or data logic

    # AI Chat consultation
    user_question = st.text_input("Ask the chatbot a question:")
    if st.button("Consult"):
        if user_question.strip():
            with st.spinner("Generating response..."):
                response = gimni_chat_response(user_question)  # Call the function for API interaction
                st.write(f"**Immo Green AI:** {response}")
        else:
            st.warning("Please enter a question!")

# Gimni API integration
@st.cache_resource
def gimni_chat_response(user_query):
    api_key = st.secrets["GIMNI_API_KEY"]  # Store your API key in Streamlit Secrets
    endpoint = "https://api.gimni.com/chat"  # Replace with the actual API endpoint
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"query": user_query}
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("response", "No response available.")
    else:
        return f"Error: {response.status_code}"

# Main application flow
if "user_logged_in" not in st.session_state:
    st.session_state["user_logged_in"] = False

if not st.session_state["user_logged_in"]:
    show_welcome()
    st.info("Please log in to access all features.")
    login()
else:
    chatbot()
