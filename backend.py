import os
from typing import Optional, Tuple
from enum import Enum

from openai import OpenAI


FALLBACK_API_KEY = (
    "sk-proj-NBiuO5F6pg2dB8JtWpZSqBwVQrax7yg27JQxS1tt8gXRUnNxiGy7kjrhA-"
    "h5_lpdhN6Q7tJdfDT3BlbkFJJ__FLxEP0INfnuVr5wU5LFBBgEFWfzku5AGeD_P7-4BfC93Ax3p"
    "ZFbQl3bQUflls3zaZLLBZUA"
)
MODEL_CHAT = "gpt-5.1"
MODEL_STT = "whisper-1"
MODEL_TTS = "tts-1"

"""
TIPUS DE VEUS DISPONIBLES 
'coral' dona
'ash' home1
'alloy' home2
'echo' neutra jove
'sage' home jove
'shimmer' neutra jove
'verse' dona madura
'fable'
"""
TTS_VOICE = 'fable'

TTS_OUTPUT_PATH = "response.wav"

CHAT_LOG_PATH = "chat.log"

class Sender(Enum):
    USER = "User"
    PROF = "Prof. Zamañorre"


def _load_system_prompt() -> str:
    prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as prompt_file:
        return prompt_file.read().strip()


def _build_client() -> OpenAI:
    env_key = os.environ.get("OPENAI_API_KEY", "").strip()
    api_key = env_key or FALLBACK_API_KEY
    if not api_key:
        raise RuntimeError("No OpenAI API key configured.")
    return OpenAI(api_key=api_key)

SYSTEM_PROMPT = _load_system_prompt()
client = _build_client()

def write_log(message: str, sender: Sender):
    try:
        with open(CHAT_LOG_PATH, "a", encoding="utf-8") as log_file:
            log_file.write(f"{sender.value}: {message}\n")
        print(f"[DEBUG] Escrit al log: {CHAT_LOG_PATH}")
    except Exception as e:
        print(f"[ERROR] No s'ha pogut escriure al log: {e}")


def process_audio(file_path: str) -> Tuple[str, str]:
    """
    Entry point for the UI. Orchestrates Whisper transcription and chat response.
    """
    
    """ MODE PRODUCCIÓ
    if not file_path:
        return "No s'ha gravat cap àudio.", ""

    transcription_text = callWhisperModel(file_path)
    return callChatModel(transcription_text)
    """

    """MODE DE PROVES"""
    if file_path:
        transcription_text = callWhisperModel(file_path)
    else:
        transcription_text = "Hola, com estàs?  "    

    write_log(transcription_text, Sender.USER)
    return callChatModel(transcription_text)


def callWhisperModel(file_path: str) -> str:
    """
    Rep un path a un fitxer d'àudio i crida al model de transcripció.
    Retorna el text transcrit.
    """
    with open(file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=MODEL_STT,
            file=audio_file,
            language="ca",
        )
    return transcription.text


def callChatModel(transcript_text: str) -> Tuple[str, str]:
    """
    Rep un text de transcripció i crida al model de xat.
    Retorna (transcripció, resposta del model).
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": transcript_text},
    ]

    completion = client.chat.completions.create(
        model=MODEL_CHAT,
        messages=messages,
    )
    answer = completion.choices[0].message.content

    write_log(answer, Sender.PROF)
    return transcript_text, answer


def read_answer(answer_text: str) -> Optional[str]:
    """
    Genera un fitxer d'àudio amb la resposta del model.
    """
    if not answer_text:
        return None

    synthesis = client.audio.speech.create(
        model=MODEL_TTS,
        voice=TTS_VOICE,
        response_format="wav",
        input=answer_text,
    )

    with open(TTS_OUTPUT_PATH, "wb") as out_file:
        out_file.write(synthesis.read())

    return TTS_OUTPUT_PATH
