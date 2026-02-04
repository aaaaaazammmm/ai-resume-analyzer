import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000/analyze"


def analyze_resume(resume_file, job_description):
    if resume_file is None:
        return "Please upload a resume."

    # Gradio gives file path, so open manually
    with open(resume_file, "rb") as f:
        files = {
            "resume": ("resume.pdf", f.read(), "application/pdf")
        }

    data = {
        "job_description": job_description
    }

    response = requests.post(BACKEND_URL, files=files, data=data, timeout=120)

    if response.status_code != 200:
        return f"Backend error: {response.status_code}\n{response.text}"

    r = response.json()

    strengths = "\n- ".join(r["strengths"])
    suggestions = "\n- ".join(r["suggestions"])

    output = f"""
🎯 Match Score: {r['match_score']}%

✅ Matched Skills:
{', '.join(r['matched_skills'])}

⚠️ Missing Skills:
{', '.join(r['missing_skills'])}

💪 Strengths:
- {strengths}

💡 Suggestions:
- {suggestions}

📝 Summary:
{r['summary']}
"""

    return output


with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Resume Analyzer")
    gr.Markdown("Upload your resume and paste Job Description to see your match score.")

    with gr.Row():
        resume = gr.File(label="Upload Resume (PDF)")
        jd = gr.Textbox(lines=12, label="Job Description")

    analyze = gr.Button("Analyze Resume", variant="primary")

    result = gr.Textbox(lines=20, label="Result")

    analyze.click(analyze_resume, inputs=[resume, jd], outputs=result)

demo.launch()
