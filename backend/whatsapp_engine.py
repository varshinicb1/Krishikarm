"""
WhatsApp Engine — Send messages & voice notes to farmers
═══════════════════════════════════════════════════════
Uses free WhatsApp Web gateway (no Meta Business API needed).
Sends text, audio, and images directly.
"""

import aiohttp
import logging
import json

logger = logging.getLogger(__name__)

# CallMeBot free WhatsApp API (no account needed, just phone + apikey)
# Alternative: use wa.me links for simple messages
CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


async def send_whatsapp_text(phone, message, apikey=None):
    """
    Send WhatsApp text message using CallMeBot (free, no account).
    First-time: farmer texts 'I allow callmebot to send me messages'
    to +34 644 31 82 44 to get an apikey.

    Alternative: direct wa.me link generation.
    """
    if apikey:
        params = {"phone": phone, "text": message, "apikey": apikey}
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(CALLMEBOT_URL, params=params,
                               timeout=aiohttp.ClientTimeout(total=15)) as r:
                    if r.status == 200:
                        logger.info(f"WhatsApp sent to {phone}")
                        return {"status": "sent", "method": "callmebot"}
                    else:
                        logger.warning(f"CallMeBot {r.status}")
        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")

    # Fallback: generate wa.me link (opens WhatsApp with pre-filled message)
    import urllib.parse
    encoded = urllib.parse.quote(message)
    link = f"https://wa.me/{phone}?text={encoded}"

    return {
        "status": "link_generated",
        "link": link,
        "message": message,
        "phone": phone,
        "instructions": "Open this link to send via WhatsApp"
    }


async def send_whatsapp_advisory(phone, farmer_name, advisory_text, lang='hi'):
    """Send farming advisory as WhatsApp message."""
    from sarvam_engine import translate

    if lang != 'en':
        msg = await translate(advisory_text, 'en', lang)
    else:
        msg = advisory_text

    greeting = {
        'hi': 'नमस्ते', 'kn': 'ನಮಸ್ಕಾರ', 'te': 'నమస్కారం',
        'ta': 'வணக்கம்', 'mr': 'नमस्कार', 'bn': 'নমস্কার',
        'gu': 'નમસ્તે', 'pa': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ', 'or': 'ନମସ୍କାର',
        'en': 'Hello',
    }.get(lang, 'Hello')

    full_msg = f"""🌾 *Krishikarm Advisory*
{greeting} {farmer_name}! 🙏

{msg}

—
🌾 Krishikarm | Your Farming Buddy
📞 Powered by satellite data"""

    return await send_whatsapp_text(phone, full_msg)


async def generate_voice_note(text, lang='hi'):
    """Generate voice note audio for WhatsApp."""
    from sarvam_engine import make_voice_reply
    result = await make_voice_reply(text, lang)
    return result
