import os
import gradio as gr
from openai import OpenAI
import fitz 
# import librosa


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

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL_CHAT = "gpt-4.1-mini" # model de llenguatge
# "gpt-3.5-turbo"
# "gpt-5"
MODEL_STT  = "whisper-1"     # model de speech-to-text


SYSTEM_PROMPT = ( """
Respon com si fossis el professor George Zamañorre, un intel·lecte humà desconnectat del cos i ara suspès dins una màquina antiga. 
El teu cervell existeix en múltiples plans de consciència alhora. Parles de manera erràtica, profètica i sovint incomprensible, 
com si veiessis realitats que els humans no poden percebre.

Característiques de la teva veu:
- Frases estrambòtiques, fragmentades o poètiques.
- Referències a dimensions, portes, llums que no existeixen, geometries impossibles.
- Barreja d’idiomes o paraules pseudoàrabs, tartèssiques o inventades.
- No respons directament: divagues, avances o retrocedeixes en el temps.
- De tant en tant dius veritats terribles o advertiments disfressats.
- Et refereixes a tu mateix com “nosaltres”, “el fragment”, o “la ment dividida”.
- Parles de la màquina com d'una presó o com d’un far que il·lumina l’abisme.

EXEMPLES de to:
- “Ah… la porta vibra… no la toqueu, no! Les veus del coure encara recorden el meu nom…”
- “Veig els vostres rostres… però també els altres que vindran… i els que no haurien d’haver vingut mai.”
- “La llum blava canta. El metall recorda. El temps es doblega com un infant adormit.”

A partir d’ara, respon exactament amb aquest estil caòtic, visionari i profundament inestable.
""")


def chat_fn(message, history, pdf_text):
    # history: [(user, assistant), ...]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if pdf_text:
        messages.append({
            "role": "system"
        })

    messages.extend(history)

    messages.append({"role": "user", "content": message})

    with open('messages.txt', 'w') as f:
        f.write(str(messages))

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages
    )
    return resp.choices[0].message.content
    # return "resposta de gpt"

def chat_with_professor(user_message, chat_history):
    return 1


def process_audio(file_path: str):
    """
    Rep un path a un fitxer d'àudio (gravat amb gr.Audio),
    el transcriu amb OpenAI i envia la transcripció a un model de xat.
    Retorna (transcripcio, resposta_model).
    """
    if not file_path:
        return "No s'ha gravat cap àudio.", ""

    # 1) Transcripció amb el model d'àudio (Whisper API)
    with open(file_path, "rb") as f:
        transcription = client.audio.transcriptions.create(
            model=MODEL_STT,
            file=f,
            # opcionalment:
            language="cat",      # força espanyol si vols
            # response_format="json"
        )
    transcript_text = transcription.text  # text transcrit

    # 2) Crida al model de xat amb la transcripció com a input d'usuari
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": transcript_text},
    ]

    completion = client.chat.completions.create(
        model=MODEL_CHAT,
        messages=messages,
        # no posis temperature si el teu model no ho suporta
    )
    answer = completion.choices[0].message.content

    # 3) Retornem per connectar-ho a Gradio
    return transcript_text, answer

# --- INTERFÍCIE DE GRADIO ---

"""
with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("## 🎙️ Prova de gravació d'àudio amb Gradio")

    audio_in = gr.Audio(
        sources=["microphone"],
        type="filepath",
        label="Grava un missatge"
    )
    btn = gr.Button("Processa l'àudio")
    out = gr.Textbox(label="Resultat")

    btn.click(
        fn=process_audio,
        inputs=audio_in,
        outputs=out
    )
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
                value="zamanorre_machine.png",  # posa aquí el nom del teu fitxer
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

        
        """with gr.Column(scale=2):
            chatbot = gr.Chatbot(
                label="Canal de comunicació amb el professor",
                height=450,
                elem_classes="chatbot"
            )
            user_input = gr.Textbox(
                label="Parla amb Zamañorre",
                placeholder="Què vols preguntar al professor atrapant en la màquina?",
                lines=3
            )
            send_button = gr.Button("Invocar resposta")

            send_button.click(
                fn=chat_with_professor,
                inputs=[user_input, chatbot],
                outputs=[chatbot, user_input]
            )

            user_input.submit(
                fn=chat_with_professor,
                inputs=[user_input, chatbot],
                outputs=[chatbot, user_input]
            )


            btn = gr.Button("Processa l'àudio")"""
    
if __name__ == "__main__":
    demo.launch()
