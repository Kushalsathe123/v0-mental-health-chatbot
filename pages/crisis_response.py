import streamlit as st
from crisis_detection import CrisisDetector
from config import EMERGENCY_CONTACTS

def show_crisis_response(language):
    """Display crisis response page"""
    crisis_detector = CrisisDetector(language)
    
    st.set_page_config(page_title="Crisis Support", layout="wide")
    
    # Styling
    st.markdown("""
        <style>
            .crisis-container {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 2rem;
                border-radius: 10px;
                color: white;
                text-align: center;
            }
            .emergency-contacts {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
            .contact-item {
                background-color: white;
                padding: 1rem;
                margin: 0.5rem 0;
                border-left: 4px solid #667eea;
                border-radius: 4px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="crisis-container">
            <h1>We're Here for You</h1>
            <p>If you're in crisis, please reach out for immediate help</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Get emergency contacts
    contacts = EMERGENCY_CONTACTS.get(language, EMERGENCY_CONTACTS["en"])
    
    st.markdown("### Emergency Support Contacts")
    for contact_name, contact_info in contacts.items():
        st.markdown(f"""
            <div class="contact-item">
                <strong>{contact_name}</strong><br>
                {contact_info}
            </div>
        """, unsafe_allow_html=True)
    
    # Additional resources
    st.markdown("### Safety Planning Resources")
    
    resources = {
        "en": {
            "Create a Safety Plan": "Work with a mental health professional to develop strategies",
            "Identify Warning Signs": "Know what triggers your crisis responses",
            "Build Your Support Network": "List people you can call during difficult times"
        },
        "hi": {
            "सुरक्षा योजना बनाएं": "एक मानसिक स्वास्थ्य पेशेवर के साथ काम करें",
            "चेतावनी संकेत पहचानें": "जानें कि क्या आपकी संकट प्रतिक्रिया को ट्रिगर करता है",
            "अपना समर्थन नेटवर्क बनाएं": "कठिन समय में कॉल करने के लिए लोगों की सूची बनाएं"
        }
    }
    
    resource_dict = resources.get(language, resources["en"])
    for resource, description in resource_dict.items():
        st.info(f"**{resource}**: {description}")
    
    # Self-harm prevention
    st.markdown("### Immediate Coping Strategies")
    
    strategies = {
        "en": [
            "Take deep breaths: Breathe in for 4 counts, hold for 4, exhale for 4",
            "5-4-3-2-1 Technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
            "Cold Water: Splash cold water on your face or hold ice cubes",
            "Movement: Take a walk, dance, or do gentle exercise",
            "Reach Out: Call a friend, family member, or hotline"
        ],
        "hi": [
            "गहरी सांसें लें: 4 गिनती तक सांस लें, रोकें, फिर छोड़ें",
            "5-4-3-2-1 तकनीक: 5 चीजें नाम दें जो आप देखते हैं",
            "ठंडा पानी: अपने चेहरे पर ठंडा पानी डालें",
            "आंदोलन: टहलें या व्यायाम करें",
            "संपर्क करें: किसी मित्र या हेल्पलाइन को कॉल करें"
        ]
    }
    
    strategies_list = strategies.get(language, strategies["en"])
    for idx, strategy in enumerate(strategies_list, 1):
        st.write(f"{idx}. {strategy}")
