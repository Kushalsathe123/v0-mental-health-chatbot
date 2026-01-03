import os
from dotenv import load_dotenv

load_dotenv()

# Try to import from transformers library for local model support
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class ChatbotEngine:
    """Main chatbot engine supporting multiple languages"""
    
    def __init__(self, language="en"):
        self.language = language
        self.conversation_history = []
        self.model = None
        self.tokenizer = None
        self.api_key = os.getenv("API_KEY")
        
        # Initialize model if transformers available
        if TRANSFORMERS_AVAILABLE and not self.api_key:
            self._initialize_local_model()
    
    def _initialize_local_model(self):
        """Initialize local Mistral model if available"""
        try:
            model_name = "mistralai/Mistral-7B-Instruct-v0.1"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                device_map="auto",
                torch_dtype="auto"
            )
        except Exception as e:
            print(f"Could not load local model: {e}")
    
    def get_system_prompt(self):
        """Get language-specific system prompt"""
        prompts = {
            "en": """You are a compassionate mental health support chatbot. Your role is to:
- Listen empathetically to users' concerns
- Provide evidence-based mental health guidance
- Suggest coping strategies and techniques
- Encourage professional help when needed
- Never diagnose or prescribe medication
- Maintain confidentiality and non-judgment
- Be supportive but realistic about limitations

Always respond with care and respect.""",
            
            "hi": """आप एक सहानुभूतिशील मानसिक स्वास्थ्य सहायता चैटबॉट हैं। आपकी भूमिका है:
- उपयोगकर्ताओं की चिंताओं को सहानुभूति से सुनना
- साक्ष्य-आधारित मानसिक स्वास्थ्य मार्गदर्शन प्रदान करना
- मुकाबला करने की रणनीति का सुझाव देना
- पेशेवर मदद लेने के लिए प्रोत्साहित करना
- कभी निदान न करें या दवा न दें
- गोपनीयता और निर्णय न लें
- सहायक लेकिन सीमाओं के बारे में यथार्थवादी हो""",
            
            "mr": """आप एक सहानुभूतिपूर्ण मानसिक स्वास्थ्य सहायता चॅटबॉट आहात. तुमचाभूमिका आहे:
- वापरकर्त्यांच्या चिंताकडे सहानुभूति सहसुनणे
- पुरावा-आधारित मानसिक स्वास्थ्य मार्गदर्शन प्रदान करणे
- सामना करण्याच्या रणनीतीचा सुझाव देणे
- व्यावसायिक मदत घेण्यास प्रोत्साहित करणे
- कधीही निदान किंवा औषध न द्या
- गोपनीयता आणि निर्णय न लिहा"""
        }
        return prompts.get(self.language, prompts["en"])
    
    def generate_response(self, user_message):
        """Generate chatbot response"""
        self.conversation_history.append({"role": "user", "content": user_message})
        
        try:
            # Use API if available
            if self.api_key:
                response = self._generate_api_response(user_message)
            # Use local model if available
            elif self.model and self.tokenizer:
                response = self._generate_local_response(user_message)
            else:
                response = self._generate_fallback_response(user_message)
            
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        except Exception as e:
            return f"I encountered an error generating a response. Please try again. Error: {str(e)}"
    
    def _generate_api_response(self, user_message):
        """Generate response using API (e.g., OpenAI, Anthropic)"""
        import requests
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        messages.extend(self.conversation_history)
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return self._generate_fallback_response(user_message)
    
    def _generate_local_response(self, user_message):
        """Generate response using local model"""
        system_prompt = self.get_system_prompt()
        prompt = f"{system_prompt}\n\nUser: {user_message}\n\nAssistant:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            **inputs,
            max_length=500,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.split("Assistant:")[-1].strip()
    
    def _generate_fallback_response(self, user_message):
        """Generate fallback response when no AI available"""
        fallback_responses = {
            "en": [
                "I understand you're going through something. Can you tell me more about what you're feeling?",
                "That sounds challenging. Have you considered talking to a mental health professional?",
                "It's important to take care of yourself. What support systems do you have in place?",
                "I'm here to listen. What's on your mind?"
            ],
            "hi": [
                "मुझे समझ आता है कि आप कुछ कठिन समय से गुजर रहे हैं।",
                "यह चुनौतीपूर्ण लगता है। क्या आपने किसी मानसिक स्वास्थ्य पेशेवर से बात करने पर विचार किया है?",
                "अपना ख्याल रखना महत्वपूर्ण है।"
            ]
        }
        
        responses = fallback_responses.get(self.language, fallback_responses["en"])
        import random
        return random.choice(responses)
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def change_language(self, language_code):
        """Change chatbot language"""
        self.language = language_code
        self.clear_history()
