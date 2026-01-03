import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database import save_mood_log, get_mood_history

def show_mood_tracking(user_id, language):
    """Display mood tracking interface"""
    st.set_page_config(page_title="Mood Tracker", layout="wide")
    
    # Styling
    st.markdown("""
        <style>
            .mood-card {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 10px;
                margin: 0.5rem 0;
                border-left: 5px solid #667eea;
            }
            .mood-emoji {
                font-size: 2rem;
                margin: 0 0.5rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("Mood Tracker")
    
    # Mood input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("How are you feeling today?")
        
        mood_options = {
            "en": ["Excellent", "Good", "Neutral", "Poor", "Terrible"],
            "hi": ["बेहतरीन", "अच्छा", "तटस्थ", "खराब", "भयानक"],
            "mr": ["उत्तम", "चांगला", "तटस्थ", "वाईट", "भयंकर"]
        }
        
        mood_list = mood_options.get(language, mood_options["en"])
        selected_mood = st.selectbox("Select your mood:", mood_list, key="mood_selector")
        
    with col2:
        st.subheader("Intensity (1-10)")
        intensity = st.slider("How intense is this feeling?", 1, 10, 5, key="intensity_slider")
    
    # Notes
    notes = st.text_area("Add any notes (optional):", placeholder="What triggered this mood? Any additional context?")
    
    # Save mood button
    if st.button("Save Mood Entry"):
        save_mood_log(user_id, selected_mood, intensity, notes)
        st.success("Mood entry saved!")
    
    st.divider()
    
    # Analytics section
    st.subheader("Your Mood Analytics")
    
    mood_history = get_mood_history(user_id)
    
    if mood_history:
        # Convert to DataFrame
        df = pd.DataFrame(mood_history, columns=["Mood", "Intensity", "Timestamp"])
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        
        # Create visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            # Mood intensity over time
            fig_line = px.line(
                df.sort_values("Timestamp"),
                x="Timestamp",
                y="Intensity",
                title="Mood Intensity Over Time",
                labels={"Intensity": "Intensity (1-10)", "Timestamp": "Date"}
            )
            fig_line.update_layout(hovermode="x unified")
            st.plotly_chart(fig_line, use_container_width=True)
        
        with col2:
            # Mood distribution
            mood_counts = df["Mood"].value_counts()
            fig_pie = px.pie(
                values=mood_counts.values,
                names=mood_counts.index,
                title="Mood Distribution"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Statistics
        st.subheader("Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_intensity = df["Intensity"].mean()
            st.metric("Average Intensity", f"{avg_intensity:.1f}/10")
        
        with col2:
            max_intensity = df["Intensity"].max()
            st.metric("Peak Intensity", f"{max_intensity}/10")
        
        with col3:
            min_intensity = df["Intensity"].min()
            st.metric("Lowest Intensity", f"{min_intensity}/10")
        
        with col4:
            total_entries = len(df)
            st.metric("Total Entries", total_entries)
        
        # Recent entries
        st.subheader("Recent Mood Entries")
        recent_df = df.sort_values("Timestamp", ascending=False).head(10)
        
        for idx, row in recent_df.iterrows():
            st.markdown(f"""
                <div class="mood-card">
                    <strong>{row['Mood']}</strong> - Intensity: {row['Intensity']}/10
                    <br><small>{row['Timestamp'].strftime('%Y-%m-%d %H:%M')}</small>
                </div>
            """, unsafe_allow_html=True)
        
        # Export data
        st.subheader("Export Your Data")
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Mood History as CSV",
            data=csv,
            file_name="mood_history.csv",
            mime="text/csv"
        )
    
    else:
        st.info("No mood entries yet. Start tracking your mood to see analytics!")
