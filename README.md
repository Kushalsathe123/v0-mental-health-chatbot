# Mental Health Awareness Chatbot

A comprehensive Streamlit-based mental health support application with AI-powered chatbot, mood tracking, crisis detection, and therapy modules.

## Features

- **AI-Powered Chatbot**: Multilingual support (English, Hindi, Marathi) with empathetic responses
- **Crisis Detection**: Automatic detection of crisis keywords with emergency contact information
- **Mood Tracking**: Track mood patterns with visualizations and analytics
- **Therapy Modules**: 
  - Anger Management
  - Breakup Recovery
  - Social Anxiety
  - Stress Management
- **Offline Resources**: Books, articles, meditation guides, and self-care checklists
- **User Authentication**: Secure login and registration with password hashing
- **Data Privacy**: SQLite database with secure data storage

## Installation

1. Clone the repository:
\`\`\`bash
git clone <repository-url>
cd mental-health-chatbot
\`\`\`

2. Create a virtual environment:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Create `.env` file:
\`\`\`bash
cp .env.example .env
\`\`\`

5. Run the application:
\`\`\`bash
streamlit run app.py
\`\`\`

## Configuration

### Environment Variables

- `DATABASE_PATH`: Path to SQLite database (default: `data/mental_health_chatbot.db`)
- `API_KEY`: Optional API key for AI model integration
- `MODEL_NAME`: AI model to use (default: Mistral-7B)

### Languages

Supported languages:
- English
- Hindi
- Marathi

Users can change language in the sidebar.

## Database Schema

### users
- id, username, password_hash, email, preferred_language, created_at

### chat_history
- id, user_id, message, response, language, timestamp

### mood_logs
- id, user_id, mood, intensity, notes, timestamp

### crisis_alerts
- id, user_id, trigger_message, timestamp

### therapy_progress
- id, user_id, module_name, completion_percentage, last_accessed

## Safety Features

- Crisis detection with emergency contacts
- Immediate support resources
- Grounding techniques and coping strategies
- Safety planning resources
- Data privacy and secure authentication

## Limitations

This chatbot is a support tool, not a replacement for professional mental health care. For serious mental health concerns, please consult a mental health professional.

## License

MIT License

## Support

For issues or suggestions, please open an issue on the repository.
