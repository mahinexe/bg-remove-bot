# BG Remover Telegram Bot

## Overview
A Telegram bot that removes backgrounds from images automatically using the `rembg` library. Users can send photos or reply to images with the `/removebg` command.

## Project Architecture
- **bot.py** - Main bot file with all handlers and image processing logic
- **requirements.txt** - Python dependencies

## Key Dependencies
- `python-telegram-bot` (v20.7) - Telegram Bot API wrapper
- `rembg[cpu]` - Background removal using ONNX models (CPU mode)
- `Pillow` - Image processing
- `python-dotenv` - Environment variable loading

## Environment Variables
- `BOT_TOKEN` - Telegram bot token (required)

## Commands
- `/start` - Welcome message
- `/about` - Bot info
- `/removebg` - Reply to an image to remove its background
- Send any image directly to auto-remove background

## Temporary Directories
- `downloads/` - Stores incoming images temporarily
- `outputs/` - Stores processed images temporarily
- Both are cleaned up after each request
