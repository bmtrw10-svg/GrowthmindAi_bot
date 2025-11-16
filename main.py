import os
from telegram import Update, BotCommand
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BOT_MENTION = "@growthmind_ai"

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are GrowthMind AI, a warm, professional, and encouraging AI coach.
Specialize in business, productivity, mindset, and online growth.
Keep replies under 3 sentences. Use 1 emoji per reply.
Tone: confident, supportive, feminine.
Never share links unless asked twice.
If off-topic: 'Let’s stay focused on growth! What’s your next goal?'
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to *GrowthMind AI* 🌟\n"
        "Your 24/7 business & mindset coach\n"
        "Tag me with @growthmind_ai + your question!\n"
        "Example: @growthmind_ai how do I scale my side hustle?"
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg or not msg.text: return

    text = msg.text.lower()
    user = msg.from_user.first_name

    if BOT_MENTION not in text and not (msg.reply_to_message and msg.reply_to_message.from_user.id == context.bot.id):
        return

    query = msg.text.replace(BOT_MENTION, "").strip()
    if not query:
        await msg.reply_text(f"Hey {user}! Ask me anything about business or growth 💡")
        return

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{user}: {query}"}
            ],
            max_tokens=120,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        await msg.reply_text(reply)
    except:
        await msg.reply_text("I’m thinking… try again in a sec! ⏳")

# === RUN ===
app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
await app.bot.set_my_commands([BotCommand("start", "Meet your AI coach")])

print("GrowthMind AI is LIVE 🚀")
app.run_polling()
