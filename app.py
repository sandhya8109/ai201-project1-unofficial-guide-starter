import gradio as gr
from query import ask

def handle_query(question):
    if not question.strip():
        return "Please enter a question.", ""
    
    result = ask(question)
    sources = "\n".join(f"• {s}" for s in result["sources"])
    return result["answer"], sources

with gr.Blocks(title="The Unofficial Guide") as demo:
    gr.Markdown("# 🎓 The Unofficial Guide\n*Ask anything about surviving college — answers drawn from real student advice.*")
    
    inp = gr.Textbox(
        label="Your question",
        placeholder="e.g. What should I pack for my dorm room?",
        lines=2
    )
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=10)
    sources = gr.Textbox(label="Retrieved from", lines=3)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

demo.launch()