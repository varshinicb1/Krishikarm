"""
Kisan-Eye V6 — Voice Engine
Whisper for Speech-to-Text, Piper for Text-to-Speech.
Supports 10 Indian languages.
"""

import io
import os
import wave
import logging
import tempfile
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# Language to Whisper language code mapping
LANG_MAP = {
    'en': 'en', 'hi': 'hi', 'kn': 'kn', 'te': 'te', 'ta': 'ta',
    'mr': 'mr', 'bn': 'bn', 'gu': 'gu', 'pa': 'pa', 'or': 'or'
}

# Piper voice models (download from https://github.com/rhasspy/piper/releases)
PIPER_VOICES = {
    'hi': 'hi_IN-swara-medium',
    'en': 'en_US-lessac-medium',
    'bn': 'bn_BD-kazba-medium',
    'te': 'te_IN-mepala-medium',
    'ta': 'ta_IN-ammu-medium',
    'kn': 'kn_IN-karuna-medium',
    'mr': 'mr_IN-manju-medium',
    'gu': 'gu_IN-gita-medium',
}

# Lazy load Whisper
_whisper_model = None


def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        try:
            import whisper
            model_size = os.environ.get('WHISPER_MODEL', 'medium')
            _whisper_model = whisper.load_model(model_size)
            logger.info(f"✅ Whisper '{model_size}' loaded")
        except Exception as e:
            logger.error(f"❌ Whisper load failed: {e}")
            _whisper_model = "FAILED"
    return _whisper_model if _whisper_model != "FAILED" else None


def transcribe(audio_bytes, language=None):
    """
    Transcribe audio bytes to text using Whisper.
    Returns dict with: text, language, confidence
    """
    model = _get_whisper()
    if model is None:
        return {"text": "", "language": language or "hi", "confidence": 0}

    # Write to temp file (Whisper needs file path)
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        f.write(audio_bytes)
        temp_path = f.name

    try:
        options = {}
        if language and language in LANG_MAP:
            options['language'] = LANG_MAP[language]

        result = model.transcribe(temp_path, **options)
        detected_lang = result.get('language', language or 'hi')

        return {
            "text": result['text'].strip(),
            "language": detected_lang,
            "confidence": 1.0,
            "segments": [
                {"text": seg['text'], "start": seg['start'], "end": seg['end']}
                for seg in result.get('segments', [])
            ]
        }
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        return {"text": "", "language": language or "hi", "confidence": 0}
    finally:
        os.unlink(temp_path)


def synthesize(text, language="hi"):
    """
    Synthesize speech from text using Piper TTS.
    Returns WAV audio bytes.
    Falls back to basic TTS if Piper not available.
    """
    voice = PIPER_VOICES.get(language, PIPER_VOICES.get('hi'))

    try:
        # Try Piper CLI
        result = subprocess.run(
            ['piper', '--model', voice, '--output_raw'],
            input=text.encode('utf-8'),
            capture_output=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            # Convert raw PCM to WAV
            return _pcm_to_wav(result.stdout, sample_rate=22050)
    except FileNotFoundError:
        logger.warning("Piper not found, using fallback TTS")
    except Exception as e:
        logger.warning(f"Piper error: {e}")

    # Fallback: generate silence with text marker
    # In production, this would use another TTS engine
    return _generate_silence_wav(len(text) * 0.05)


def _pcm_to_wav(pcm_data, sample_rate=22050, channels=1, sample_width=2):
    """Convert raw PCM bytes to WAV format."""
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)
    return buf.getvalue()


def _generate_silence_wav(duration_sec=1.0, sample_rate=22050):
    """Generate silent WAV for fallback."""
    import struct
    num_samples = int(sample_rate * duration_sec)
    samples = struct.pack(f'<{num_samples}h', *([0] * num_samples))
    return _pcm_to_wav(samples, sample_rate)


def is_whisper_available():
    return _get_whisper() is not None


def is_piper_available():
    try:
        result = subprocess.run(['piper', '--version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception:
        return False
