
import os
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from google import genai

# Render se tokens uthana
TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Naya AI Client Setup (google-genai library)
client = genai.Client(api_key=GEMINI_API_KEY)

# Render ko khush rakhne ke liye Dummy Web Server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('👋 Hello! Main aapka Wealth Vault AI hoon. Mujhse apne paise, savings, ya investment ke baare mein kuch bhi puchhiye!\n\nDeals dekhne ke liye /deals type karein.')

# Deals Command (Affiliate Marketing ke liye)
async def deals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🛍️ **Best Deals:**\n\n1. Best Finance Book: [Yahan Amazon Affiliate Link Daalein]\n2. Best Credit Card: [Yahan Affiliate Link Daalein]')

# AI se baat karne ka function (Updated for new SDK)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text("Soch raha hoon... 🤔")
    try:
        prompt = f"Aap ek expert financial advisor hain. User ne yeh pucha hai: '{user_text}'. Iska ek short, helpful aur practical jawab Hinglish mein dein."
        
        # Naye SDK aur naye model (gemini-2.5-flash) ka use
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"AI Error: {e}") # Error ko logs mein print karein
        await update.message.reply_text("Sorry bhai, abhi thoda network issue hai. Thodi der baad try karein.")

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('deals', deals))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot chal raha hai...")
    application.run_polling()
