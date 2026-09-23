```python
import streamlit as st
from groq import Groq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1100px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .hero {
            text-align: center;
            padding: 2rem 0 1rem 0;
        }

        .hero h1 {
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }

        .hero p {
            font-size: 1.15rem;
            color: #888888;
        }

        .card {
            padding: 1.25rem;
            border-radius: 12px;
            border: 1px solid rgba(128, 128, 128, 0.25);
            margin-bottom: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
    <div class="hero">
        <h1>🗺️ AI Roadmap Generator</h1>
        <p>Create a personalized learning roadmap with AI.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GET GROQ CLIENT
# ============================================================

def get_groq_client():
    try:
        api_key = st.secrets["GROQ_API_KEY"]

        if not api_key:
            return None

        return Groq(api_key=api_key)

    except Exception:
        return None


# ============================================================
# GENERATE ROADMAP
# ============================================================

def generate_roadmap(
    client,
    domain,
    skill_level,
    hours_per_week,
    duration_weeks,
    goal,
):

    system_prompt = """
You are an expert learning-path designer and technical curriculum architect.

Create realistic, personalized learning roadmaps.

The roadmap MUST:

- Match the user's current skill level.
- Respect their available hours per week.
- Respect their total learning duration.
- Progress logically from fundamentals to practical application.
- Avoid unnecessary topics.
- Include hands-on practice.
- Include projects.
- Include checkpoints.
- Include a final capstone project.
- Be achievable within the specified time.

Do NOT simply list technologies.

Think about prerequisite dependencies.

For example, a beginner learning Machine Learning should generally
learn the necessary Python, mathematics, data handling and statistics
before advanced machine-learning topics.

Return ONLY clean Markdown.

Use this exact structure:

# Learning Roadmap

## Overview

Include:
- Domain
- Skill level
- Hours per week
- Duration
- Learning goal

## Prerequisites

List the important prerequisites.

## Week 1 — [Title]

### Goals
- ...

### Topics
- ...

### Practical Tasks
- ...

### Project
- ...

### Recommended Resources
- ...

### Checkpoint
- ...

Repeat the same structure for every week.

Then include:

## Final Capstone Project

### Project
...

### Skills Tested
...

### Suggested Implementation
...

### Definition of Done
...

Finally:

## Learning Strategy

Include practical advice about:
- Daily study
- Practice
- Revision
- Projects
- Progress tracking

IMPORTANT:

Do not invent specific URLs.

You may recommend well-known resources by name, for example:

- Official Python Documentation
- MDN Web Docs
- freeCodeCamp
- Kaggle
- Real Python
- PostgreSQL Documentation

Keep the workload realistic.
"""


    user_prompt = f"""
Create a personalized learning roadmap.

DOMAIN:
{domain}

CURRENT SKILL LEVEL:
{skill_level}

AVAILABLE HOURS PER WEEK:
{hours_per_week}

TOTAL LEARNING DURATION:
{duration_weeks} weeks

LEARNING GOAL:
{goal if goal else "Become practically skilled and build portfolio projects."}

The roadmap should be appropriate for this exact combination
of skill level, time and duration.
"""


    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        temperature=0.5,
        max_tokens=7000,
    )

    return response.choices[0].message.content


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎯 Roadmap Settings")

    domain = st.text_input(
        "What do you want to learn?",
        placeholder="e.g. Python, Cyber Security, Data Science",
    )

    skill_level = st.selectbox(
        "Your current level",
        [
            "Beginner",
            "Intermediate",
            "Advanced",
        ],
    )

    hours_per_week = st.slider(
        "Hours available per week",
        min_value=1,
        max_value=40,
        value=10,
    )

    duration_weeks = st.slider(
        "Learning duration",
        min_value=1,
        max_value=52,
        value=12,
    )

    goal = st.text_area(
        "What is your goal?",
        placeholder=(
            "Example: Become job-ready and build "
            "3 portfolio projects."
        ),
        height=120,
    )

    generate = st.button(
        "🚀 Generate Roadmap",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# EMPTY STATE
# ============================================================

if "roadmap" not in st.session_state:

    st.info(
        """
        👈 Enter your learning preferences in the sidebar.

        The AI will create a roadmap based on your:

        • Domain
        • Skill level
        • Weekly study time
        • Learning duration
        • Goal
        """
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Skill Levels", "3")

    with col2:
        st.metric("Maximum Duration", "52 weeks")

    with col3:
        st.metric("Maximum Study Time", "40 hrs/week")


# ============================================================
# GENERATE
# ============================================================

if generate:

    if not domain.strip():

        st.error("Please enter a learning domain.")

    else:

        client = get_groq_client()

        if client is None:

            st.error(
                """
                Groq API key is not configured.

                Open your Streamlit Cloud app settings and add:

                GROQ_API_KEY = your_groq_api_key
                """
            )

        else:

            with st.spinner(
                "🧠 Creating your personalized roadmap..."
            ):

                try:

                    roadmap = generate_roadmap(
                        client=client,
                        domain=domain.strip(),
                        skill_level=skill_level,
                        hours_per_week=hours_per_week,
                        duration_weeks=duration_weeks,
                        goal=goal.strip(),
                    )

                    st.session_state["roadmap"] = roadmap
                    st.session_state["domain"] = domain.strip()

                except Exception as error:

                    st.error(
                        "The roadmap could not be generated."
                    )

                    with st.expander("Technical details"):
                        st.code(str(error))


# ============================================================
# DISPLAY ROADMAP
# ============================================================

if "roadmap" in st.session_state:

    st.divider()

    st.subheader(
        f"🎓 {st.session_state['domain']} Learning Roadmap"
    )

    st.markdown(
        st.session_state["roadmap"]
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            "⬇️ Download Roadmap",
            data=st.session_state["roadmap"],
            file_name="ai-learning-roadmap.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col2:

        if st.button(
            "🔄 Create New Roadmap",
            use_container_width=True,
        ):

            st.session_state.clear()
            st.rerun()
```
