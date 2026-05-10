# Career Intelligence Agent

The Career Intelligence Agent is an AI-powered assistant built with **CrewAI** and **Gradio**. It performs a data-driven gap analysis of your current profile against live job market demands, generating a highly personalized, actionable upskilling roadmap.

## Features

- **Multi-Agent Orchestration**: Utilizes a suite of AI agents working sequentially to scout jobs, match your profile, analyze skills gaps, and design a learning roadmap.
- **Live Job Search**: Integrates with the Adzuna API (with a robust DuckDuckGo search fallback) to pull real, up-to-date job market data.
- **Multi-Model Support**: Easily switch between leading LLMs including OpenAI, Gemini, Groq, and Claude directly from the UI.
- **Elegant UI**: Features a premium, customized Gradio interface with modern typography, gradients, and interactive layouts.

## Agent Workflow

The system is powered by four specialized agents operating in a sequential pipeline:
1. **Career Scout**: Searches the live job market based on your target interests and extracts the top active job postings.
2. **Profile Matcher**: Cross-references your degree, skills, and experience against the scouted job requirements, scoring each skill as ✅ (expert), 🔶 (intermediate), or ❌ (missing) and calculating an overall match percentage.
3. **Skills Gap Analyst**: Prioritizes your missing skills and researches real-world average salary data for your target role.
4. **Career Roadmap Planner**: Generates an actionable, week-by-week 8-week learning plan detailing specific courses and projects needed to close your skills gap.

## Setup

Follow these steps to run the application locally:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd career-intelligence-agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Populate the `.env` file at the root of the project with your respective API keys. You only need the keys for the models/services you intend to use.
   ```env
   OPENAI_API_KEY=your_key_here
   GROQ_API_KEY=your_key_here
   MISTRAL_API_KEY=your_key_here
   TOGETHER_API_KEY=your_key_here
   GEMINI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ADZUNA_APP_ID=your_id_here
   ADZUNA_APP_KEY=your_key_here
   ```

4. **Run the application:**
   ```bash
   python src/app.py
   ```
   The application will launch on your local host (typically `http://127.0.0.1:7860`). Open this URL in your browser to interact with the agent.
