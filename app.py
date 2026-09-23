```python
import streamlit as st
from groq import Groq


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "openai/gpt-oss-120b"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Roadmap Generator",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1150px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        text-align: center;
        padding: 2rem 0 1.5rem 0;
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

    .info-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
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

        <p>
            Create a personalized learning roadmap powered by AI.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GROQ CLIENT
# ============================================================

def get_groq_client():
    """
    Create Groq client using Streamlit Cloud Secrets.
    """

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        if not api_key:
            return None

        return Groq(
            api_key=api_key
        )

    except Exception:
        return None


# ============================================================
# ROADMAP GENERATOR
# ============================================================

def generate_roadmap(
    client,
    domain,
    skill_level,
    hours_per_week,
    duration_weeks,
    learning_goal,
):

    system_prompt = """
You are an expert learning-path designer,
technical curriculum architect, mentor,
and career-focused educator.

Your task is to create realistic personalized
learning roadmaps.

You MUST carefully consider:

1. The user's domain.
2. Their current skill level.
3. Their available hours per week.
4. Their total learning duration.
5. Their learning goal.

The roadmap must be realistic.

Do NOT try to teach every possible topic.

Prioritize the most important concepts required
to progress toward the user's goal.

The learning path should progress logically:

Fundamentals
→ Core Concepts
→ Intermediate Skills
→ Practical Application
→ Projects
→ Advanced Concepts
→ Capstone

Adjust the difficulty according to the user's
current level.

Adjust the workload according to the number of
hours available per week.

Do not assume the user has unlimited time.

==================================================
OUTPUT FORMAT
==================================================

Return ONLY Markdown.

Start with:

# Learning Roadmap

Then provide:

## Overview

Include:

- Domain
- Current skill level
- Hours per week
- Duration
- Learning goal

Then:

## Prerequisites

Only include important prerequisites.

Then create one section for EVERY week.

Use exactly this format:

## Week X — Week Title

### 🎯 Goals

- Goal
- Goal
- Goal

### 📚 Topics

- Topic
- Topic
- Topic

### 🛠️ Practical Tasks

- Task
- Task
- Task

### 🚀 Project

Describe a practical project for the week.

### 📖 Recommended Resources

Recommend resources by name.

Examples:

- Official Python Documentation
- MDN Web Docs
- Kaggle
- freeCodeCamp
- Real Python
- PostgreSQL Documentation

Do NOT invent URLs.

### ✅ Checkpoint

Explain what the learner should be able to do
before moving to the next week.

Repeat this structure for every week.

Then provide:

# Final Capstone Project

Include:

## Project

Describe the project.

## Skills Tested

List the skills.

## Suggested Implementation

Provide implementation steps.

## Definition of Done

Provide measurable completion criteria.

Finally provide:

# Learning Strategy

Explain:

- How to divide weekly study time.
- How much time to spend learning.
- How much time to spend practicing.
- How to use projects.
- How to revise.
- How to track progress.

IMPORTANT:

The roadmap must fit the requested duration.

Do not generate an unrealistic amount of material.

The roadmap should be practical and actionable.
"""


    user_prompt = f"""
Create a personalized learning roadmap.

USER INFORMATION
================

Domain:
{domain}

Current Skill Level:
{skill_level}

Available Hours Per Week:
{hours_per_week}

Total Learning Duration:
{duration_weeks} weeks

Learning Goal:
{learning_goal if learning_goal else "Become practically skilled and build portfolio projects."}

IMPORTANT REQUIREMENTS
=====================

Create exactly {duration_weeks} weekly sections.

Each week must have:

- Goals
- Topics
- Practical Tasks
- Project
- Recommended Resources
- Checkpoint

The workload must be realistic for approximately
{hours_per_week} hours per week.

Make the roadmap appropriate for a {skill_level.lower()} learner.

Focus on practical skill development rather than
just theoretical knowledge.
"""


    response = client.chat.completions.create(
        model=MODEL_NAME,

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

        temperature=0.4,

        max_tokens=12000,
    )

    return response.choices[0].message.content


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🎯 Roadmap Settings")

    domain = st.text_input(
        "What do you want to learn?",
        placeholder=(
            "Example: Python, Data Science, "
            "Cyber Security"
        ),
    )

    skill_level = st.selectbox(
        "Current skill level",
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
        step=1,
    )

    duration_weeks = st.slider(
        "Learning duration",
        min_value=1,
        max_value=52,
        value=12,
        step=1,
    )

    learning_goal = st.text_area(
        "Learning goal",
        placeholder=(
            "Example:\n"
            "Become job-ready and build "
            "3 portfolio projects."
        ),
        height=130,
    )

    generate_button = st.button(
        "🚀 Generate Roadmap",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# INTRODUCTION
# ============================================================

if "roadmap" not in st.session_state:

    st.info(
        """
        👈 Configure your learning preferences.

        The AI will create a personalized roadmap based on:

        • Learning domain
        • Current skill level
        • Hours available per week
        • Total learning duration
        • Personal learning goal
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Skill Levels",
            "3",
        )

    with col2:

        st.metric(
            "Maximum Duration",
            "52 weeks",
        )

    with col3:

        st.metric(
            "Maximum Study Time",
            "40 hrs/week",
        )


# ============================================================
# GENERATE ROADMAP
# ============================================================

if generate_button:

    # ------------------------------------------
    # Validate domain
    # ------------------------------------------

    if not domain.strip():

        st.error(
            "Please enter a learning domain."
        )

    else:

        # --------------------------------------
        # Get Groq client
        # --------------------------------------

        client = get_groq_client()

        if client is None:

            st.error(
                """
                ❌ Groq API key was not found.

                Go to your Streamlit Cloud app:

                Manage app → Settings → Secrets

                and add:

                GROQ_API_KEY = "your_groq_api_key"
                """
            )

        else:

            # ----------------------------------
            # Generate roadmap
            # ----------------------------------

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
                        learning_goal=learning_goal.strip(),
                    )

                    st.session_state["roadmap"] = roadmap

                    st.session_state["domain"] = (
                        domain.strip()
                    )

                    st.session_state["skill_level"] = (
                        skill_level
                    )

                    st.session_state["hours"] = (
                        hours_per_week
                    )

                    st.session_state["duration"] = (
                        duration_weeks
                    )

                except Exception as error:

                    st.error(
                        "❌ The roadmap could not be generated."
                    )

                    with st.expander(
                        "Technical error"
                    ):

                        st.code(
                            str(error)
                        )


# ============================================================
# DISPLAY ROADMAP
# ============================================================

if "roadmap" in st.session_state:

    st.divider()

    st.header(
        "🎓 Your Personalized Roadmap"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.caption("DOMAIN")

        st.write(
            st.session_state["domain"]
        )

    with col2:

        st.caption("LEVEL")

        st.write(
            st.session_state["skill_level"]
        )

    with col3:

        st.caption("DURATION")

        st.write(
            f"{st.session_state['duration']} weeks"
        )

    st.divider()

    # ------------------------------------------
    # Roadmap
    # ------------------------------------------

    st.markdown(
        st.session_state["roadmap"]
    )

    st.divider()

    # ------------------------------------------
    # Download
    # ------------------------------------------

    st.subheader(
        "📥 Save Your Roadmap"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.download_button(
            label="⬇️ Download Markdown",
            data=st.session_state["roadmap"],
            file_name=(
                "ai-learning-roadmap.md"
            ),
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
