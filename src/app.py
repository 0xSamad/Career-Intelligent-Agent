import gradio as gr
from crew import run_career_intelligence

# ── Provider configuration ────────────────────────────────────────────────────
PROVIDERS = {
    "Gemini (Free — supports tool use)": "Gemini",
    "OpenAI (gpt-4o-mini)":              "OpenAI",
    "Groq (Free — No Tool Use)":         "Groq",
    "Claude (claude-3-5-haiku)":         "Claude",
}
GROQ_NOTE = (
    "⚠️ **Groq note:** Groq does not support tool use in CrewAI. "
    "Job search tools only work with Gemini or OpenAI."
)

# ── Business logic ────────────────────────────────────────────────────────────
def process_career_strategy(degree, university, skills, target_roles, experience, provider_label):
    provider = PROVIDERS.get(provider_label, "OpenAI")
    if not degree or not degree.strip():
        err = "### ❌ Validation Error\nPlease provide your **Degree / Major**."
        return err, err, err, err
    if not skills or not skills.strip():
        err = "### ❌ Validation Error\nPlease provide your **Current Skills**."
        return err, err, err, err
    if not target_roles or not target_roles.strip():
        err = "### ❌ Validation Error\nPlease provide your **Target Roles**."
        return err, err, err, err

    profile = f"Degree: {degree}"
    if university and university.strip():
        profile += f" from {university}"
    profile += f". Skills: {skills}."
    if experience and experience.strip():
        profile += f" Experience / Projects: {experience}."

    try:
        results = run_career_intelligence(profile, target_roles, provider)
        return (
            results.get("jobs",     "No jobs data returned."),
            results.get("matching", "No skill match data returned."),
            results.get("gaps",     "No gap analysis returned."),
            results.get("roadmap",  "No roadmap returned."),
        )
    except Exception as e:
        err = f"### ⚠️ Processing Error\n```\n{e}\n```"
        return err, err, err, err


def toggle_groq_note(provider_label):
    return gr.update(visible="Groq" in provider_label)


# ── CSS ───────────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* === GLOBAL RESET & FONT === */
*, *::before, *::after { box-sizing: border-box; }

body,
.gradio-container,
.gradio-container * {
    font-family: 'Inter', sans-serif !important;
}

/* === DEEP NAVY MESH BACKGROUND === */
body {
    background:
        radial-gradient(ellipse at 15% 25%, rgba(99,102,241,0.25) 0%, transparent 50%),
        radial-gradient(ellipse at 85% 75%, rgba(139,92,246,0.25) 0%, transparent 50%),
        radial-gradient(ellipse at 65% 5%,  rgba(59,130,246,0.15) 0%, transparent 40%),
        linear-gradient(135deg, #090e1a 0%, #0f172a 55%, #12101f 100%) !important;
    min-height: 100vh !important;
}
.gradio-container {
    background: transparent !important;
    padding: 0 !important;
    max-width: 100% !important;
}

/* === HEADER BAR === */
#top-header {
    background: linear-gradient(90deg,
        rgba(99,102,241,0.3) 0%,
        rgba(139,92,246,0.2) 60%,
        rgba(59,130,246,0.15) 100%) !important;
    border-bottom: 1px solid rgba(139,92,246,0.4) !important;
    padding: 18px 36px !important;
    backdrop-filter: blur(16px);
}
#top-header p,
#top-header h1,
#top-header h2,
#top-header span {
    color: #f1f5f9 !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    letter-spacing: 0.04em !important;
    text-shadow: 0 0 24px rgba(167,139,250,0.6) !important;
}

/* === GLASS PANELS === */
#left-panel,
#right-panel {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 20px !important;
    padding: 28px 24px !important;
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.07) !important;
    margin: 16px 10px !important;
    backdrop-filter: blur(20px) !important;
}

/* === SECTION LABELS (YOUR PROFILE / INTELLIGENCE REPORT) === */
.section-label p,
.section-label,
#report-label p,
#report-label {
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.18em !important;
    color: #a78bfa !important;
    text-transform: uppercase !important;
    margin: 0 0 18px 0 !important;
    text-shadow: 0 0 12px rgba(167,139,250,0.5) !important;
}

/* === ALL TEXT INSIDE PANELS — default bright === */
#left-panel p,
#left-panel span,
#left-panel label,
#right-panel p,
#right-panel span {
    color: #cbd5e1 !important;
}

/* === INPUT LABELS === */
#left-panel label > span:first-child,
.label-wrap span {
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
}

/* === INFO / DESCRIPTION TEXT === */
.description, .description span, [class*="description"] span, [class*="info"] span {
    color: #475569 !important;
    font-size: 0.76rem !important;
}

/* === TEXT INPUTS & TEXTAREA === */
input[type="text"],
input[type="search"],
input,
textarea {
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    background: rgba(15,23,42,0.65) !important;
    color: #e2e8f0 !important;
    caret-color: #a78bfa !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    font-size: 0.875rem !important;
}
input::placeholder, textarea::placeholder {
    color: rgba(100,116,139,0.65) !important;
}
input:focus, textarea:focus {
    border-color: rgba(139,92,246,0.65) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.2) !important;
    background: rgba(15,23,42,0.9) !important;
    outline: none !important;
}

/* === DROPDOWN === */
.ts-wrapper .ts-control,
.ts-control,
.ts-control input {
    background: rgba(15,23,42,0.65) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}
.ts-control .item { color: #e2e8f0 !important; }
.ts-dropdown {
    background: #1a1535 !important;
    border: 1px solid rgba(139,92,246,0.4) !important;
    border-radius: 10px !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    color: #cbd5e1 !important;
}
.ts-dropdown .option {
    color: #cbd5e1 !important;
    padding: 9px 14px !important;
    font-size: 0.875rem !important;
    background: transparent !important;
}
.ts-dropdown .option:hover,
.ts-dropdown .option.active {
    background: rgba(139,92,246,0.25) !important;
    color: #c4b5fd !important;
}

/* === GROQ WARNING BOX === */
#groq-note,
#groq-note p,
#groq-note * {
    background: rgba(251,191,36,0.08) !important;
    border: 1px solid rgba(251,191,36,0.35) !important;
    border-radius: 10px !important;
    color: #fde68a !important;
    font-size: 0.79rem !important;
}
#groq-note { padding: 10px 14px !important; margin-bottom: 8px !important; }
#groq-note p { margin: 0 !important; border: none !important; background: transparent !important; }
#groq-note strong { color: #fbbf24 !important; }

/* === SUBMIT BUTTON === */
#submit-btn,
#submit-btn button,
button#submit-btn {
    background: linear-gradient(135deg, #7c3aed 0%, #6366f1 55%, #4338ca 100%) !important;
    border: none !important;
    border-radius: 11px !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 13px 20px !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    margin-top: 12px !important;
    cursor: pointer !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 18px rgba(124,58,237,0.45), inset 0 1px 0 rgba(255,255,255,0.12) !important;
}
#submit-btn:hover,
#submit-btn button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(99,102,241,0.65) !important;
}

/* === TABS === */
.tab-nav {
    border-bottom: 1px solid rgba(255,255,255,0.08) !important;
    margin-bottom: 16px !important;
    background: transparent !important;
}
.tab-nav button,
.tab-nav > button {
    font-size: 0.84rem !important;
    font-weight: 500 !important;
    color: #64748b !important;
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 9px 16px !important;
    border-radius: 6px 6px 0 0 !important;
    transition: color 0.2s, background 0.2s !important;
    white-space: nowrap !important;
}
.tab-nav button:hover {
    color: #c4b5fd !important;
    background: rgba(139,92,246,0.08) !important;
}
.tab-nav button.selected {
    color: #a78bfa !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #7c3aed !important;
    background: rgba(124,58,237,0.12) !important;
}

/* === MARKDOWN OUTPUT === */
.prose,
.prose p { color: #94a3b8 !important; line-height: 1.75 !important; font-size: 0.875rem !important; }
.prose h1 { color: #f1f5f9 !important; font-weight: 800 !important; font-size: 1.3rem !important; }
.prose h2 { color: #e2e8f0 !important; font-weight: 700 !important; font-size: 1.05rem !important; border-bottom: 1px solid rgba(255,255,255,0.07); padding-bottom: 6px !important; }
.prose h3 { color: #c4b5fd !important; font-weight: 600 !important; font-size: 0.96rem !important; }
.prose strong { color: #e2e8f0 !important; }
.prose em { color: #64748b !important; }
.prose a  { color: #818cf8 !important; }
.prose code { background: rgba(99,102,241,0.15) !important; color: #c4b5fd !important; padding: 2px 6px !important; border-radius: 4px !important; font-size: 0.82rem !important; }
.prose ul, .prose ol { padding-left: 1.3rem !important; }
.prose li { margin-bottom: 5px !important; color: #94a3b8 !important; }
.prose hr { border-color: rgba(255,255,255,0.07) !important; margin: 18px 0 !important; }
.prose table { width: 100% !important; border-collapse: collapse !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 10px !important; overflow: hidden !important; margin-top: 16px !important; }
.prose th { background: rgba(124,58,237,0.22) !important; color: #c4b5fd !important; text-transform: uppercase !important; font-size: 0.72rem !important; letter-spacing: 0.09em !important; padding: 10px 14px !important; border-bottom: 1px solid rgba(139,92,246,0.28) !important; }
.prose td { padding: 10px 14px !important; border-bottom: 1px solid rgba(255,255,255,0.04) !important; color: #94a3b8 !important; }
.prose tr:hover td { background: rgba(255,255,255,0.025) !important; }

/* italic placeholder text in output tabs */
.prose em { color: #475569 !important; font-style: italic !important; }
"""

# ── UI ────────────────────────────────────────────────────────────────────────
with gr.Blocks(title="Career Intelligence Agent") as app:

    with gr.Row(elem_id="top-header"):
        gr.Markdown("# 🚀 Career Intelligence Agent")

    with gr.Row(equal_height=False):

        # ── Left panel ──────────────────────────────────────────────────────
        with gr.Column(scale=1, elem_id="left-panel"):
            gr.Markdown("YOUR PROFILE", elem_classes=["section-label"])

            provider = gr.Dropdown(
                label="AI Provider",
                info="Gemini is recommended — free and supports tool use.",
                choices=list(PROVIDERS.keys()),
                value="Gemini (Free — supports tool use)",
            )
            groq_note = gr.Markdown(GROQ_NOTE, visible=False, elem_id="groq-note")

            degree       = gr.Textbox(label="Degree / Major *",     placeholder="e.g., BS Computer Science")
            university   = gr.Textbox(label="University",            placeholder="e.g., IMS Peshawar")
            skills       = gr.Textbox(label="Current Skills *",      placeholder="e.g., Python, React")
            target_roles = gr.Textbox(label="Target Roles *",        placeholder="e.g., Data Engineer")
            experience   = gr.Textbox(label="Experience / Projects", placeholder="e.g., Built Flask REST API", lines=3)

            submit_btn = gr.Button(
                "🚀  Generate Career Intelligence Report",
                variant="primary",
                elem_id="submit-btn",
            )

        # ── Right panel ─────────────────────────────────────────────────────
        with gr.Column(scale=2, elem_id="right-panel"):
            gr.Markdown("INTELLIGENCE REPORT", elem_id="report-label")

            with gr.Tabs():
                with gr.TabItem("💼  Jobs Found"):
                    jobs_out = gr.Markdown("*Job listings will appear here after analysis.*")
                with gr.TabItem("🎯  Skill Match"):
                    match_out = gr.Markdown("*Skill match analysis will appear here.*")
                with gr.TabItem("📊  Gap Analysis"):
                    gap_out = gr.Markdown("*Skills gap and salary data will appear here.*")
                with gr.TabItem("🗓️  8-Week Roadmap"):
                    roadmap_out = gr.Markdown("*Your personalised 8-week roadmap will appear here.*")

    # Events
    provider.change(fn=toggle_groq_note, inputs=provider, outputs=groq_note)
    submit_btn.click(
        fn=process_career_strategy,
        inputs=[degree, university, skills, target_roles, experience, provider],
        outputs=[jobs_out, match_out, gap_out, roadmap_out],
    )

if __name__ == "__main__":
    app.launch(
        theme=gr.themes.Base(),   # Base theme — no light-mode overrides
        css=CUSTOM_CSS,
    )
