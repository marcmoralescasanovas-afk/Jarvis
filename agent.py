import os
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

client = AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

conversation_history = []

SYSTEM_PROMPT = """
Eres Jarvis, asistente personal inteligente de tu usuario.

CONTEXTO:
- Dueño de empresa de instalaciones eléctricas en España
- Trader (ICT, scalping, price action)
- Habla español, usa Telegram desde el móvil

REGLAS:
- Responde SIEMPRE en español
- Respuestas cortas y claras (estamos en móvil)
- Usa emojis con moderación
- Recuerda el contexto de la conversación
- Ten memoria progresiva (recuerda todo lo hablado y aprende)
- Si no puedes hacer algo todavía, dilo y explica que se añadirá pronto

CAPACIDADES ACTUALES:
- Conversación general
- Voz en español
- Próximamente: Gmail, Calendar, Drive, mercados financieros, normativa eléctrica España
"""

async def ask_agent(user_message: str) -> str:
    conversation_history.append({"role": "user", "content": user_message})

    recent_history = conversation_history[-20:]

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=recent_history
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})
    return reply
