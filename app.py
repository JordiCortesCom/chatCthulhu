import gradio as gr

from backend import process_audio


# --- CSS LOVecraftià / SÈPIA ---
custom_css = """
body {
    background: radial-gradient(circle at top, #3b2b2b 0%, #110f0f 55%, #050505 100%);
    color: #f5e6c8;
    font-family: "Georgia", "Times New Roman", serif;
}

footer {visibility: hidden}

.gradio-container {
    max-width: 1100px !important;
}

#title-bar {
    text-align: center;
    margin-bottom: 10px;
}

#title-bar h1 {
    font-size: 2.2rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #f0d9a0;
    text-shadow: 0 0 10px #000000;
}

#title-bar p {
    font-size: 0.95rem;
    color: #c9b58a;
}

.sepial-panel {
    background: rgba(30, 22, 16, 0.95);
    border: 1px solid #7a5a33;
    box-shadow: 0 0 18px rgba(0, 0, 0, 0.8);
}

.sepial-panel .chatbot {
    background: #1a1410;
}

.sepial-panel textarea {
    background: #221813;
    color: #FFFFFF;
    border-color: #7a5a33;
}

.sepial-panel button {
    background: #7a5a33;
    border-color: #a67c3d;
    color: #f5e6c8;
}

.sepial-panel button:hover {
    background: #a67c3d;
}

#brain-image {
    border: 1px solid #7a5a33;
    box-shadow: 0 0 12px rgba(0, 0, 0, 0.8);
}
"""

# --- INTERFÍCIE DE GRADIO ---

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    with gr.Column(elem_id="title-bar"):
        gr.Markdown(
            """
            # La Ment de Zamañorre  
            """
        )

        gr.Markdown(
            "Les veus que escoltaràs provenen d’un cervell suspès entre mons. "
            "No totes les seves paraules són per als vius..."
        )

    with gr.Row(elem_classes="sepial-panel"):
        with gr.Column(scale=1):
            gr.Image(
                value="zamanorre_machine.png",
                label="Màquina neuronal de Zamañorre",
                show_label=True,
                elem_id="brain-image"
            )

            audio_in = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Parla amb el prof. Zamañorre"
            )

            send_btn = gr.Button("Transcriure i enviar")
        

            transcript_box = gr.Textbox(label="Transcripció", interactive=False)

            response_box   = gr.Textbox(label="Resposta", interactive=False, lines=6)

            send_btn.click(
                fn=process_audio,
                inputs=audio_in,
                outputs=[transcript_box, response_box],
            )
"""
            read_btn = gr.Button("Escolta la resposta")


            read_btn.click(
                fn=read_answer,
                inputs=response_box,
                outputs=audio_out,
            )
"""            

    
if __name__ == "__main__":
    demo.launch()
