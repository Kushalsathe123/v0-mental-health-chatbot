import streamlit as st
import os
from config import SUPPORTED_LANGUAGES
from database import init_database
from auth import authenticate_user, create_user, get_user_language, update_user_language
from chatbot import ChatbotEngine
from crisis_detection import CrisisDetector
from database import save_chat_message, get_user_id

# Initialize database
init_database()

# Page configuration
st.set_page_config(
    page_title="Mental Health Chatbot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
        :root {
            --primary: #667eea;
            --secondary: #764ba2;
            --success: #56ab2f;
            --danger: #d32f2f;
            --warning: #ff9800;
            --info: #2196f3;
            --light: #f8f9fa;
            --dark: #2c3e50;
        }
        
        body {
            background-color: var(--light);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .chat-message {
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 8px;
        }
        
        .user-message {
            background-color: var(--primary);
            color: white;
            margin-left: 2rem;
        }
        
        .bot-message {
            background-color: #e8e8ff;
            color: var(--dark);
            margin-right: 2rem;
        }
        
        .crisis-alert {
            background-color: var(--danger);
            color: white;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "language" not in st.session_state:
    st.session_state.language = "English"
if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Authentication section
def show_auth():
    """Display authentication interface"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_user")
        login_password = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", use_container_width=True):
            user_id = authenticate_user(login_username, login_password)
            if user_id:
                st.session_state.authenticated = True
                st.session_state.user_id = user_id
                st.session_state.username = login_username
                st.session_state.language = get_user_language(user_id)
                st.session_state.chatbot = ChatbotEngine(
                    "en" if st.session_state.language == "English" else "hi"
                )
                st.success("Logged in successfully!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    with col2:
        st.subheader("Register")
        reg_username = st.text_input("Username", key="reg_user")
        reg_email = st.text_input("Email (optional)", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_pass")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.button("Register", use_container_width=True):
            if reg_password != reg_confirm:
                st.error("Passwords don't match")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters")
            elif create_user(reg_username, reg_password, reg_email):
                st.success("Account created! Please login.")
            else:
                st.error("Username already exists")

# Main app
def show_main_app():
    """Display main application interface"""
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>Mental Health Support Chatbot</h1>
            <p>Your companion for mental health and wellbeing</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.subheader(f"Welcome, {st.session_state.username}!")
        
        # Language selection
        language_options = list(SUPPORTED_LANGUAGES.keys())
        current_lang_idx = language_options.index(st.session_state.language) if st.session_state.language in language_options else 0
        selected_language = st.selectbox(
            "Language",
            language_options,
            index=current_lang_idx,
            key="lang_select"
        )
        
        if selected_language != st.session_state.language:
            st.session_state.language = selected_language
            lang_code = SUPPORTED_LANGUAGES[selected_language]
            update_user_language(st.session_state.user_id, selected_language)
            st.session_state.chatbot = ChatbotEngine(lang_code)
            st.rerun()
        
        st.divider()
        
        # Navigation
        st.subheader("Navigation")
        page = st.radio(
            "Choose a section:",
            ["Chat", "Mood Tracker", "Therapy Modules", "Resources", "Crisis Support"]
        )
        
        st.divider()
        
        # Logout
        if st.button("Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.username = None
            st.session_state.chatbot = None
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content
    lang_code = SUPPORTED_LANGUAGES.get(st.session_state.language, "en")
    
    if page == "Chat":
        show_chat_page(lang_code)
    elif page == "Mood Tracker":
        from pages.mood_tracking import show_mood_tracking
        show_mood_tracking(st.session_state.user_id, lang_code)
    elif page == "Therapy Modules":
        from pages.therapy import show_therapy_modules
        show_therapy_modules(st.session_state.user_id, lang_code)
    elif page == "Resources":
        from pages.resources import show_resources
        show_resources(lang_code)
    elif page == "Crisis Support":
        from pages.crisis_response import show_crisis_response
        show_crisis_response(lang_code)

def show_chat_page(language):
    """Display chat interface"""
    st.subheader("Chat with Support")
    
    # Initialize chatbot if needed
    if st.session_state.chatbot is None:
        st.session_state.chatbot = ChatbotEngine(language)
    
    # Chat history display
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                    <div class="chat-message user-message">
                        <strong>You:</strong> {message['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="chat-message bot-message">
                        <strong>Support Bot:</strong> {message['content']}
                    </div>
                """, unsafe_allow_html=True)
    
    # Crisis detection and response
    crisis_detector = CrisisDetector(language)
    
    # User input
    user_input = st.text_area("Type your message:", height=100, key="chat_input")
    
    if st.button("Send", use_container_width=True):
        if user_input.strip():
            # Check for crisis
            if crisis_detector.detect_crisis(user_input):
                crisis_detector.log_alert(st.session_state.user_id, user_input)
                
                st.markdown("""
                    <div class="crisis-alert">
                        <strong>We're concerned about your safety.</strong>
                        Please reach out to a mental health professional or emergency service immediately.
                        Click on "Crisis Support" in the navigation to see emergency contacts.
                    </div>
                """, unsafe_allow_html=True)
            
            # Generate response
            response = st.session_state.chatbot.generate_response(user_input)
            
            # Save to database
            save_chat_message(st.session_state.user_id, user_input, response, language)
            
            # Update session
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            
            st.rerun()

# Main execution
if not st.session_state.authenticated:
    st.markdown("""
        <div class="main-header">
            <h1>Mental Health Support Chatbot</h1>
            <p>Your safe space for mental health support and guidance</p>
        </div>
    """, unsafe_allow_html=True)
    
    show_auth()
else:
    show_main_app()
