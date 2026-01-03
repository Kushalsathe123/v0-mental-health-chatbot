import streamlit as st
from therapy_modules import get_module
from database import get_therapy_progress, update_therapy_progress
from config import THERAPY_MODULES

def show_therapy_modules(user_id, language):
    """Display therapy modules"""
    st.set_page_config(page_title="Therapy Modules", layout="wide")
    
    st.markdown("""
        <style>
            .module-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 2rem;
                border-radius: 10px;
                margin: 1rem 0;
                cursor: pointer;
            }
            .lesson-item {
                background-color: #f8f9fa;
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 5px;
                border-left: 4px solid #667eea;
            }
            .exercise-item {
                background-color: #e8f4f8;
                padding: 1rem;
                margin: 0.5rem 0;
                border-radius: 5px;
                border-left: 4px solid #4ba3c3;
            }
            .progress-bar {
                background-color: #e0e0e0;
                border-radius: 10px;
                height: 20px;
                margin: 0.5rem 0;
            }
            .progress-fill {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
                height: 100%;
                border-radius: 10px;
                width: {percent}%;
                transition: width 0.3s ease;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Therapy Modules")
    st.markdown("Choose a module to start your healing journey")
    
    # Display available modules
    cols = st.columns(3)
    
    for idx, (module_key, module_info) in enumerate(THERAPY_MODULES.items()):
        with cols[idx % 3]:
            if st.button(
                module_info["name"],
                key=f"module_{module_key}",
                use_container_width=True,
                help=module_info["description"]
            ):
                st.session_state.selected_module = module_key
    
    # Show selected module content
    if "selected_module" in st.session_state:
        module_key = st.session_state.selected_module
        module = get_module(module_key, language)
        
        if module:
            st.divider()
            st.subheader(THERAPY_MODULES[module_key]["name"])
            
            # Progress tracking
            progress = get_therapy_progress(user_id, module_key)
            st.markdown(f"**Your Progress: {progress}%**")
            st.progress(progress / 100)
            
            # Lessons
            st.subheader("Lessons")
            lessons = module.get_lessons()
            
            for lesson in lessons:
                with st.expander(f"Lesson {lesson['id']}: {lesson['title']}"):
                    st.write(lesson["content"])
            
            # Exercises
            st.subheader("Exercises")
            exercises = module.get_exercises()
            
            for exercise in exercises:
                st.markdown(f"""
                    <div class="exercise-item">
                        <strong>{exercise['title']}</strong> ({exercise['duration']})<br>
                        {exercise['description']}
                    </div>
                """, unsafe_allow_html=True)
            
            # Update progress
            new_progress = st.slider(
                "Update your progress:",
                0,
                100,
                progress,
                step=10,
                key=f"progress_{module_key}"
            )
            
            if new_progress != progress:
                update_therapy_progress(user_id, module_key, new_progress)
                st.success(f"Progress updated to {new_progress}%!")
