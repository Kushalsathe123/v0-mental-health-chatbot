from config import CRISIS_KEYWORDS, EMERGENCY_CONTACTS
from database import log_crisis_alert

class CrisisDetector:
    """Detect and respond to crisis indicators"""
    
    def __init__(self, language="en"):
        self.language = language
        self.keywords = CRISIS_KEYWORDS.get(language, CRISIS_KEYWORDS["en"])
    
    def detect_crisis(self, message):
        """Detect crisis indicators in message"""
        message_lower = message.lower()
        
        for keyword in self.keywords:
            if keyword.lower() in message_lower:
                return True
        
        return False
    
    def get_emergency_response(self):
        """Get crisis response with emergency contacts"""
        contacts = EMERGENCY_CONTACTS.get(self.language, EMERGENCY_CONTACTS["en"])
        
        crisis_message = {
            "en": "I'm deeply concerned about what you've shared. Your safety is my priority.",
            "hi": "मुझे आपकी साझा की गई बातों के बारे में गहरी चिंता है। आपकी सुरक्षा मेरी प्राथमिकता है।",
            "mr": "मुझे आपकी साझा केलेल्या बातीबद्दल गहरी चिंता आहे।"
        }
        
        return {
            "message": crisis_message.get(self.language, crisis_message["en"]),
            "contacts": contacts
        }
    
    def log_alert(self, user_id, message):
        """Log crisis alert to database"""
        log_crisis_alert(user_id, message)
