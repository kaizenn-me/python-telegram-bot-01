import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes


# Logging for debugging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# List of waifu categories and default settings
categories = [
    "waifu", "neko", "bully", "cuddle", "cry", "hug", "kiss", "lick", "pat", "smug",
    "bonk", "yeet", "blush", "smile", "wave", "highfive", "handhold", "nom", "bite",
    "glomp", "slap", "kill", "kick", "happy", "wink", "poke", "dance", "cringe", "trap",
    "blowjob"
]
settings = {'mode': 'sfw'}
last_generated_url = {}

# Start function to show the main menu
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = []
    for i in range(0, len(categories), 3):  # Display categories in rows with 3 columns
        row = [
            InlineKeyboardButton(categories[i].capitalize(), callback_data=categories[i]),
            InlineKeyboardButton(categories[i+1].capitalize(), callback_data=categories[i+1]) if i+1 < len(categories) else None,
            InlineKeyboardButton(categories[i+2].capitalize(), callback_data=categories[i+2]) if i+2 < len(categories) else None,
        ]
        keyboard.append([btn for btn in row if btn])  # Avoid None buttons
    keyboard.append([InlineKeyboardButton("Settings", callback_data='settings')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Waifu Generator! Select a waifu category:", reply_markup=reply_markup)

# Function to generate waifu based on the selected category
async def generate_waifu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    category = query.data

    # Call the waifu.pics API with the selected category and mode
    api_url = f'https://api.waifu.pics/{settings["mode"]}/{category}'
    response = requests.get(api_url)
    if response.status_code == 200:
        waifu_url = response.json().get('url')
        last_generated_url[query.from_user.id] = waifu_url  # Save the last generated URL

        # Display the waifu image with "Download Image" and "Back to Main Menu" options
        keyboard = [
            [InlineKeyboardButton("Download Image", url=waifu_url)],
            [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_photo(waifu_url, caption=f"Here is a {category} for you! 🌸", reply_markup=reply_markup)
    else:
      
      await query.message.reply_text(
         "🌸✨ *Oopsie\\!* ✨🌸\n\n"
         "If you choose *NSFW* content, you can only enjoy these categories:\n"
         "💖 *Waifu* 🐾, *Neko* 🐱, *Trap* 🎀, and *Blowjob* 💋\n\n"
         "But if you choose *SFW*, you have so many sweet options:\n"
         "🌸 *Waifu* 🐾, *Neko* 🐱, *Bully* 😈, *Cuddle* 🤗, *Cry* 😢, *Hug* 🤗,\n"
         "💕 *Kiss* 😘, *Lick* 👅, *Pat* 👋, *Smug* 😏, *Bonk* 🔨, *Yeet* 💨,\n"
         "😊 *Blush* 😊, *Smile* 😄, *Wave* 👋, *Highfive* ✋, *Handhold* 🤝,\n"
         "🍬 *Nom* 🍬, *Bite* 😋, *Glomp* 🤗, *Slap* ✋, *Kill* 💀, *Kick* 🦵,\n"
         "🎉 *Happy* 😀, *Wink* 😉, *Poke* 👉, *Dance* 💃, *Cringe* 😖\n\n"
          "Choose wisely\\! 🌈💖",
    parse_mode="MarkdownV2"
)

        
# Function for Waifu Settings (NSFW or SFW)
async def waifu_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("NSFW", callback_data='nsfw')],
        [InlineKeyboardButton("SFW", callback_data='sfw')],
        [InlineKeyboardButton("Back to Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Choose image mode:", reply_markup=reply_markup)

# Function to set waifu mode to NSFW or SFW
async def set_waifu_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    mode = query.data
    settings['mode'] = mode  # Update mode setting
    await query.answer(f"Mode set to {mode.upper()}")
    await waifu_settings(update, context)  # Return to waifu settings menu

# Language Settings function (display only, does not change language)
async def language_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("Indonesia", callback_data='lang_id')],
        [InlineKeyboardButton("Japan", callback_data='lang_jp')],
        [InlineKeyboardButton("Back to Settings", callback_data='settings')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Choose language (currently only supports English):", reply_markup=reply_markup)

# Function to display the settings menu
async def settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Waifu Settings", callback_data='waifu_settings')],
        [InlineKeyboardButton("Language", callback_data='language')],
        [InlineKeyboardButton("Back to Main Menu", callback_data='main_menu')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.edit_text("Select the settings to change:", reply_markup=reply_markup)

# Function for the "Back to Main Menu" button
async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await start(query, context)  # Call the start function to return to the main menu

def main() -> None:
    # Your Telegram bot API key
    application = Application.builder().token("PASTE YOUR BOT TOKEN HERE :3").connect_timeout(60).build()

    # Setting up handlers for commands and callbacks
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(generate_waifu, pattern='^(' + '|'.join(categories) + ')$'))
    application.add_handler(CallbackQueryHandler(waifu_settings, pattern='^waifu_settings$'))
    application.add_handler(CallbackQueryHandler(set_waifu_mode, pattern='^(nsfw|sfw)$'))
    application.add_handler(CallbackQueryHandler(language_settings, pattern='^language$'))
    application.add_handler(CallbackQueryHandler(settings_menu, pattern='^settings$'))
    application.add_handler(CallbackQueryHandler(main_menu, pattern='^main_menu$'))

    # Running the bot
    application.run_polling()

if __name__ == "__main__":
    main()
