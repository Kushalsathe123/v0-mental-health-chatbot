class TherapyModule:
    """Base class for therapy modules"""
    
    def __init__(self, name, language="en"):
        self.name = name
        self.language = language
        self.lessons = []
        self.exercises = []
    
    def get_lessons(self):
        return self.lessons
    
    def get_exercises(self):
        return self.exercises


class AngerManagementModule(TherapyModule):
    """Anger management therapy module"""
    
    def __init__(self, language="en"):
        super().__init__("Anger Management", language)
        self._initialize_content()
    
    def _initialize_content(self):
        if self.language == "en":
            self.lessons = [
                {
                    "id": 1,
                    "title": "Understanding Anger",
                    "content": "Anger is a natural emotion. It becomes a problem when it's uncontrolled or expressed harmfully. Understanding what triggers your anger is the first step to managing it."
                },
                {
                    "id": 2,
                    "title": "Identifying Triggers",
                    "content": "Common anger triggers include: feeling disrespected, perceived injustice, loss of control, or physical discomfort. Keep a log of situations that make you angry."
                },
                {
                    "id": 3,
                    "title": "Physical Techniques",
                    "content": "Deep breathing, progressive muscle relaxation, and exercise can help reduce physical anger symptoms. Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8."
                }
            ]
            
            self.exercises = [
                {
                    "id": 1,
                    "title": "Box Breathing",
                    "description": "Breathe in for 4 counts, hold for 4, exhale for 4, hold for 4. Repeat 5 times.",
                    "duration": "5 minutes"
                },
                {
                    "id": 2,
                    "title": "Progressive Muscle Relaxation",
                    "description": "Tense and release muscle groups from head to toe, 5 seconds each.",
                    "duration": "10 minutes"
                },
                {
                    "id": 3,
                    "title": "Journaling Exercise",
                    "description": "Write about what made you angry and why for 10 minutes without censoring.",
                    "duration": "10 minutes"
                }
            ]
        else:
            # Hindi/Marathi content
            self.lessons = [
                {
                    "id": 1,
                    "title": "क्रोध को समझना" if self.language == "hi" else "क्रोध समजून घेणे",
                    "content": "क्रोध एक प्राकृतिक भावना है। यह समस्या तब बनता है जब इसे नियंत्रित नहीं किया जाता।"
                }
            ]
            self.exercises = []


class BreakupRecoveryModule(TherapyModule):
    """Breakup recovery therapy module"""
    
    def __init__(self, language="en"):
        super().__init__("Breakup Recovery", language)
        self._initialize_content()
    
    def _initialize_content(self):
        if self.language == "en":
            self.lessons = [
                {
                    "id": 1,
                    "title": "The Grief Process",
                    "content": "Breakup involves grief. You may experience denial, anger, bargaining, depression, and acceptance. These stages aren't linear—you may move between them."
                },
                {
                    "id": 2,
                    "title": "Self-Care During Healing",
                    "content": "Prioritize sleep, nutrition, and exercise. Avoid alcohol and drugs. Spend time with supportive friends and family. Engage in activities you enjoy."
                },
                {
                    "id": 3,
                    "title": "Moving Forward",
                    "content": "Healing takes time. Set boundaries with your ex (no contact may help). Focus on personal growth and rediscovering yourself outside the relationship."
                }
            ]
            
            self.exercises = [
                {
                    "id": 1,
                    "title": "Letter Writing",
                    "description": "Write a letter to your ex expressing all your feelings. You don't send it—this is for you.",
                    "duration": "20 minutes"
                },
                {
                    "id": 2,
                    "title": "Self-Love Affirmations",
                    "description": "Practice positive affirmations about your worth and future. Repeat daily.",
                    "duration": "5 minutes"
                },
                {
                    "id": 3,
                    "title": "Create a Healing Playlist",
                    "description": "Make a playlist of songs that uplift and inspire you, not songs that remind you of the relationship.",
                    "duration": "30 minutes"
                }
            ]


class SocialAnxietyModule(TherapyModule):
    """Social anxiety therapy module"""
    
    def __init__(self, language="en"):
        super().__init__("Social Anxiety", language)
        self._initialize_content()
    
    def _initialize_content(self):
        if self.language == "en":
            self.lessons = [
                {
                    "id": 1,
                    "title": "Understanding Social Anxiety",
                    "content": "Social anxiety is fear of social situations where you might be judged or embarrassed. It's more than shyness—it can interfere with daily life."
                },
                {
                    "id": 2,
                    "title": "Cognitive Distortions",
                    "content": "Social anxiety often involves distorted thinking: mind-reading (assuming people judge you), catastrophizing (expecting the worst), and fortune-telling (predicting negative outcomes)."
                },
                {
                    "id": 3,
                    "title": "Exposure Therapy",
                    "content": "Gradually facing feared social situations reduces anxiety. Start small and work your way up. Avoidance maintains anxiety."
                }
            ]
            
            self.exercises = [
                {
                    "id": 1,
                    "title": "Thought Record",
                    "description": "Write down anxious thoughts and challenge them with evidence-based counter-thoughts.",
                    "duration": "15 minutes"
                },
                {
                    "id": 2,
                    "title": "Social Exposure Ladder",
                    "description": "Create a list of social situations from least to most anxiety-provoking. Gradually practice them.",
                    "duration": "30 minutes"
                },
                {
                    "id": 3,
                    "title": "Conversation Practice",
                    "description": "Practice conversation starters and topics. Role-play with a trusted friend or therapist.",
                    "duration": "20 minutes"
                }
            ]


def get_module(module_name, language="en"):
    """Get therapy module by name"""
    modules = {
        "anger_management": AngerManagementModule,
        "breakup_recovery": BreakupRecoveryModule,
        "social_anxiety": SocialAnxietyModule
    }
    
    module_class = modules.get(module_name)
    if module_class:
        return module_class(language)
    return None
