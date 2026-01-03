import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/mental_health_chatbot.db")

# AI Model Configuration
MODEL_NAME = os.getenv("MODEL_NAME", "mistralai/Mistral-7B-Instruct-v0.1")
API_KEY = os.getenv("API_KEY", "")

# Languages
SUPPORTED_LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr"
}

# Crisis Keywords
CRISIS_KEYWORDS = {
    "en": ["suicide", "kill myself", "harm myself", "die", "overdose", "cut myself"],
    "hi": ["आत्महत्या", "खुद को मार", "खुद को नुकसान", "मरना", "ओवरडोज"],
    "mr": ["आत्महत्या", "स्वत:ला मारणे", "स्वत:ला हानी", "मरणे"]
}

# Emergency Contacts
EMERGENCY_CONTACTS = {
    "en": {
        "National Suicide Prevention Lifeline": "988",
        "Crisis Text Line": "Text HOME to 741741",
        "International Association for Suicide Prevention": "https://www.iasp.info/resources/Crisis_Centres/"
    },
    "hi": {
        "आत्महत्या रोकथाम हेल्पलाइन": "9152987821",
        "AASRA": "9820466726"
    },
    "mr": {
        "आत्महत्या रोकथाम हेल्पलाइन": "9152987821"
    }
}

# Therapy Modules
THERAPY_MODULES = {
    "anger_management": {
        "name": "Anger Management",
        "description": "Learn techniques to manage and control anger"
    },
    "breakup_recovery": {
        "name": "Breakup Recovery",
        "description": "Healing guidance after a relationship ends"
    },
    "social_anxiety": {
        "name": "Social Anxiety",
        "description": "Strategies to manage social anxiety"
    },
    "stress_management": {
        "name": "Stress Management",
        "description": "Techniques to reduce and manage stress"
    }
}
