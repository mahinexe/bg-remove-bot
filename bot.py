import os
import uuid
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from rembg import remove
from PIL import Image

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("BOT_TOKEN not set")

# Directories for temporary files
DOWNLOAD_DIR = "downloads"
OUTPUT_DIR = "outputs"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome! This bot removes background from images automatically. "
        "Send a photo or reply to an image with /removebg. "
        "Supported formats: JPG, PNG, WEBP. Fast and easy to use. "
        "Developed by: Mohammodullah Al Mahin - @being_lame"
    )

# /about command
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "BG Remover Bot\n"
        "Removes background from your images automatically.\n"
        "Fast and easy to use.\n"
        "Developed by: Mohammodullah Al Mahin - @being_lame\n"
        "Supported formats: JPG, PNG, WEBP"
    )

# Function to remove background from an image
def remove_bg_file(input_path, output_path):
    with Image.open(input_path) as img:
        result = remove(img)
        result.save(output_path)

# General image handler (for sending images normally)
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    await process_image(msg)

# /removebg command handler
async def removebg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    # Check if user replied to an image
    if msg.reply_to_message:
        await process_image(msg.reply_to_message)
    else:
        await msg.reply_text("Please reply to an image with /removebg command.")

# Process image function (used by both handlers)
async def process_image(msg):
    try:
        if msg.photo:
            file = await msg.photo[-1].get_file()
        elif msg.document and msg.document.mime_type.startswith("image"):
            file = await msg.document.get_file()
        else:
            await msg.reply_text("Please send a valid image file.")
            return

        uid = str(uuid.uuid4())
        input_path = f"{DOWNLOAD_DIR}/{uid}.png"
        output_path = f"{OUTPUT_DIR}/{uid}_out.png"

        await file.download_to_drive(input_path)
        remove_bg_file(input_path, output_path)

        await msg.reply_document(
            document=open(output_path, "rb"),
            caption="Background removed successfully"
        )

        # Clean up
        os.remove(input_path)
        os.remove(output_path)

    except Exception:
        await msg.reply_text("Failed to process the image.")

# Main function
def main():
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("removebg", removebg))
    app.add_handler(CommandHandler("about", about))

    # General image messages
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, handle_image))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
