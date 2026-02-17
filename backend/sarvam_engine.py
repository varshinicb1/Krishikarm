"""
Sarvam AI Engine — Voice, Translation & TTS for Indian Languages
═══════════════════════════════════════════════════════════════
Integrates Sarvam AI APIs for:
  - Text-to-Speech (Bulbul v3, 11 Indian languages)
  - Speech-to-Text (voice→text)
  - Translation (any Indian language ↔ English)
"""

import aiohttp
import base64
import logging
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

SARVAM_API = "https://api.sarvam.ai"
SARVAM_KEY = os.getenv("SARVAM_API_KEY")

# Language codes
LANG_MAP = {
    'hi': 'hi-IN', 'kn': 'kn-IN', 'te': 'te-IN', 'ta': 'ta-IN',
    'mr': 'mr-IN', 'bn': 'bn-IN', 'gu': 'gu-IN', 'pa': 'pa-IN',
    'or': 'od-IN', 'en': 'en-IN', 'ml': 'ml-IN',
}

# Friendly voice per language
VOICE_MAP = {
    'hi-IN': 'amartya', 'kn-IN': 'pavithra', 'te-IN': 'maitreyi',
    'ta-IN': 'diya', 'mr-IN': 'arvind', 'bn-IN': 'amartya',
    'gu-IN': 'arvind', 'pa-IN': 'amartya', 'od-IN': 'amartya',
    'en-IN': 'meera', 'ml-IN': 'pavithra',
}


def _headers():
    return {"api-subscription-key": SARVAM_KEY, "Content-Type": "application/json"}


async def translate(text, source_lang='en', target_lang='hi'):
    """Translate text between Indian languages."""
    src = LANG_MAP.get(source_lang, 'en-IN')
    tgt = LANG_MAP.get(target_lang, 'hi-IN')

    payload = {
        "input": text,
        "source_language_code": src,
        "target_language_code": tgt,
        "mode": "formal",
        "model": "mayura:v1",
        "enable_preprocessing": True,
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{SARVAM_API}/translate", json=payload,
                            headers=_headers(), timeout=aiohttp.ClientTimeout(total=15)) as r:
                if r.status == 200:
                    d = await r.json()
                    return d.get("translated_text", text)
                else:
                    err = await r.text()
                    logger.error(f"Sarvam translate {r.status}: {err}")
    except Exception as e:
        logger.error(f"Sarvam translate error: {e}")
    return text


async def text_to_speech(text, lang='hi', output_path=None):
    """Convert text to natural speech using Bulbul v3."""
    lang_code = LANG_MAP.get(lang, 'hi-IN')
    voice = VOICE_MAP.get(lang_code, 'amartya')

    payload = {
        "inputs": [text[:2400]],
        "target_language_code": lang_code,
        "speaker": voice,
        "model": "bulbul:v1",
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.5,
        "speech_sample_rate": 22050,
        "enable_preprocessing": True,
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{SARVAM_API}/text-to-speech", json=payload,
                            headers=_headers(), timeout=aiohttp.ClientTimeout(total=30)) as r:
                if r.status == 200:
                    d = await r.json()
                    audios = d.get("audios", [])
                    if audios:
                        audio_b64 = audios[0]
                        audio_bytes = base64.b64decode(audio_b64)
                        if output_path:
                            Path(output_path).write_bytes(audio_bytes)
                        return {"audio_base64": audio_b64, "bytes": audio_bytes, "path": output_path}
                else:
                    err = await r.text()
                    logger.error(f"Sarvam TTS {r.status}: {err}")
    except Exception as e:
        logger.error(f"Sarvam TTS error: {e}")
    return None


async def speech_to_text(audio_bytes, lang='hi'):
    """Transcribe speech to text."""
    lang_code = LANG_MAP.get(lang, 'hi-IN')
    audio_b64 = base64.b64encode(audio_bytes).decode()

    payload = {
        "input": audio_b64,
        "language_code": lang_code,
        "model": "saarika:v2",
        "with_timestamps": False,
    }
    try:
        async with aiohttp.ClientSession() as s:
            async with s.post(f"{SARVAM_API}/speech-to-text", json=payload,
                            headers=_headers(), timeout=aiohttp.ClientTimeout(total=20)) as r:
                if r.status == 200:
                    d = await r.json()
                    return d.get("transcript", "")
                else:
                    err = await r.text()
                    logger.error(f"Sarvam STT {r.status}: {err}")
    except Exception as e:
        logger.error(f"Sarvam STT error: {e}")
    return ""


async def make_voice_reply(text_en, lang='hi', output_dir="temp_audio"):
    """Full pipeline: translate English → native language → TTS audio."""
    Path(output_dir).mkdir(exist_ok=True)

    # Translate
    if lang != 'en':
        native_text = await translate(text_en, 'en', lang)
    else:
        native_text = text_en

    # Generate speech
    import time
    audio_path = f"{output_dir}/reply_{int(time.time())}.wav"
    result = await text_to_speech(native_text, lang, audio_path)

    return {
        "text_en": text_en,
        "text_native": native_text,
        "audio": result,
        "lang": lang,
    }
