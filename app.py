import streamlit as st
import requests
import json

# Title and introduction
st.title("Immo Green AI System")
st.write("Welcome to Immo Green! Your trusted real estate partner.")

# API keys and sensitive data from Streamlit Secrets
API_BASE_URL = st.secrets["api_base_url"]
API_KEY = st.secrets["api_key"]

# Login/Registration
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login / Register")
    username = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Mock login logic or actual API call
        if username and password:  # Replace with API authentication
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid credentials. Please try again.")
else:
    st.write(f"Welcome back, {username}!")
    if st.button("Log out"):
        st.session_state.logged_in = False

# Chatbot Section
st.subheader("AI Chatbot")
user_query = st.text_input("Ask anything about our services or properties:")
if user_query:
    # Mock AI response or call to an LLM like GPT
    ai_response = f"AI: [Placeholder for '{user_query}']"
    st.write(ai_response)

# Property Search Section
st.subheader("Property Search")
with st.form("search_form"):
    keyword = st.text_input("Enter keywords (e.g., Apartment in Zurich)")
    region = st.text_input("Preferred Region")
    price_range = st.slider("Price Range (in USD)", 50000, 1000000, (100000, 500000))
    submitted = st.form_submit_button("Search")
    if submitted:
        # Call client API
        search_payload = {
            "keyword": keyword,
            "region": region,
            "price_min": price_range[0],
            "price_max": price_range[1]
        }
        response = requests.post(f"{API_BASE_URL}/search", headers={"Authorization": f"Bearer {API_KEY}"}, json=search_payload)
        if response.status_code == 200:
            properties = response.json()
            for prop in properties:
                st.write(f"**{prop['name']}**: {prop['price']}")
        else:
            st.error("Failed to fetch properties. Please try again later.")

# Premium Section
st.subheader("Upgrade to Premium")
if st.button("Learn More"):
    st.write("Premium users get access to exclusive features and faster support.")
