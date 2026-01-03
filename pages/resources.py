import streamlit as st

def show_resources(language):
    """Display offline resources and support information"""
    st.set_page_config(page_title="Resources", layout="wide")
    
    st.markdown("""
        <style>
            .resource-card {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 5px solid #667eea;
            }
            .resource-title {
                color: #667eea;
                font-weight: bold;
                font-size: 1.2rem;
                margin-bottom: 0.5rem;
            }
            .highlight-box {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
            }
        </style>
    """, unsafe_allow_html=True)
    
    resources_content = {
        "en": {
            "title": "Mental Health Resources",
            "sections": {
                "Books & Articles": [
                    {"title": "Feeling Good", "author": "David D. Burns", "description": "Classic on cognitive therapy and depression management"},
                    {"title": "The Body Keeps the Score", "author": "Bessel van der Kolk", "description": "Understanding trauma and recovery"},
                    {"title": "Mindfulness for Beginners", "author": "Jon Kabat-Zinn", "description": "Introduction to mindfulness meditation"}
                ],
                "Meditation & Mindfulness": [
                    {"title": "10-Minute Breathing Exercise", "description": "Simple breathing technique to reduce anxiety"},
                    {"title": "Body Scan Meditation", "description": "Progressive relaxation from head to toe"},
                    {"title": "Loving-Kindness Meditation", "description": "Develop compassion for yourself and others"}
                ],
                "Healthy Habits": [
                    {"title": "Sleep Hygiene", "description": "Tips for better sleep quality"},
                    {"title": "Nutrition for Mental Health", "description": "Foods that support mental wellbeing"},
                    {"title": "Exercise Benefits", "description": "How physical activity improves mood"}
                ],
                "Safety Planning": [
                    {"title": "Create Your Safety Plan", "description": "Warning signs, coping strategies, and support contacts"},
                    {"title": "Grounding Techniques", "description": "5-4-3-2-1 and other grounding exercises"},
                    {"title": "Crisis Prevention", "description": "Identifying triggers and early intervention"}
                ]
            }
        },
        "hi": {
            "title": "मानसिक स्वास्थ्य संसाधन",
            "sections": {
                "किताबें और लेख": [
                    {"title": "अच्छा महसूस करना", "author": "डेविड डी बर्न्स", "description": "संज्ञानात्मक थेरेपी पर क्लासिक"},
                    {"title": "शरीर कहानी बताता है", "author": "बेसल वैन डेर कोल्क", "description": "आघात और पुनर्वास को समझना"}
                ],
                "ध्यान और माइंडफुलनेस": [
                    {"title": "10-मिनट की श्वास व्यायाम", "description": "चिंता कम करने की सरल तकनीक"},
                    {"title": "शरीर स्कैन ध्यान", "description": "प्रगतिशील विश्राम"}
                ],
                "स्वस्थ आदतें": [
                    {"title": "नींद की स्वच्छता", "description": "बेहतर नींद के लिए टिप्स"},
                    {"title": "मानसिक स्वास्थ्य के लिए पोषण", "description": "मानसिक कल्याण का समर्थन करने वाले खाद्य पदार्थ"}
                ]
            }
        }
    }
    
    content = resources_content.get(language, resources_content["en"])
    
    st.title(content["title"])
    
    for section_name, items in content["sections"].items():
        st.subheader(section_name)
        
        for item in items:
            title = item.get("title", "")
            author = item.get("author", "")
            description = item.get("description", "")
            
            st.markdown(f"""
                <div class="resource-card">
                    <div class="resource-title">{title}</div>
                    {f"<strong>By:</strong> {author}<br>" if author else ""}
                    {description}
                </div>
            """, unsafe_allow_html=True)
    
    # Self-care checklist
    st.divider()
    st.subheader("Daily Self-Care Checklist")
    
    checklist_items = {
        "en": [
            "I got 7-9 hours of sleep",
            "I moved my body (exercise, walk, stretch)",
            "I ate nutritious meals",
            "I practiced gratitude",
            "I connected with someone I care about",
            "I practiced a relaxation technique",
            "I took breaks from screens"
        ],
        "hi": [
            "मुझे 7-9 घंटे की नींद मिली",
            "मैंने अपने शरीर को हिलाया",
            "मैंने पौष्टिक भोजन खाया",
            "मैंने कृतज्ञता का अभ्यास किया",
            "मैंने किसी से जुड़ा",
            "मैंने एक विश्राम तकनीक का अभ्यास किया",
            "मैंने स्क्रीन से ब्रेक लिया"
        ]
    }
    
    checklist = checklist_items.get(language, checklist_items["en"])
    
    for item in checklist:
        st.checkbox(item, key=item)
