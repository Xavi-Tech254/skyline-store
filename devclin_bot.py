import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)

# ══════════════════════════════════════════════
#   CONFIG — EDIT THESE
# ══════════════════════════════════════════════
BOT_TOKEN = "8589728931:AAFTJDW94p_BOTr-q6AXua-hunOXmbXNSDQ"          # From @BotFather
ADMIN_ID   = 6105493227                      # Your Telegram user ID (get from @userinfobot)

BOT_NAME     = "Dev Clin"
BOT_HANDLE   = "@DevClinBot"
COMPANY      = "Skyline Technologies"
TAGLINE      = "Elevating Digital Solutions"

WELCOME_MSG  = (
    "👋 Welcome to *Dev Clin* — your digital store powered by *Skyline Technologies!*\n\n"
    "🏙 _Elevating Digital Solutions_\n\n"
    "What would you like to do today? 👇"
)

# Payment details
BANK_NAME    = "MPESA"
ACCOUNT_NUM  = "0743810633"
ACCOUNT_NAME = "Clinton Oduor"

# Me button — paste your portfolio link here
ME_LINK      = "https://yourportfolio.com"
ME_LABEL     = "👤 Me"
ME_BIO       = "Built by Dev Clin 🚀\nSkyline Technologies — Elevating Digital Solutions"

# Cyberpunk image — upload to telegram and paste file_id here, OR use a public URL
# To get file_id: send the image to your bot, then check the update in logs
CYBER_IMAGE  = "https://i.imgur.com/placeholder.jpg"  # Replace with your image file_id or URL

# Contact
ADMIN_TG     = "@yourusername"
WHATSAPP     = "https://wa.me/234XXXXXXXXX"
INSTAGRAM    = "https://instagram.com/skyline_tech"

# ══════════════════════════════════════════════
#   PRODUCTS
# ══════════════════════════════════════════════
PRODUCTS = [
    {
        "id": "p1",
        "name": "School Notes Bundle",
        "category": "education",
        "price": "₦500",
        "type": "PDF",
        "desc": "Complete notes for SS1–SS3. All subjects covered.",
        "link": "",   # Google Drive link or Telegram file_id
        "icon": "📚",
        "active": True,
    },
    {
        "id": "p2",
        "name": "Business Plan Template",
        "category": "education",
        "price": "₦800",
        "type": "DOCX",
        "desc": "Professional business plan template. Editable Word format.",
        "link": "",
        "icon": "📄",
        "active": True,
    },
    {
        "id": "p3",
        "name": "Android VPN App",
        "category": "apps",
        "price": "₦1,200",
        "type": "APK",
        "desc": "Premium VPN for Android. Fast, secure, unlimited data.",
        "link": "",
        "icon": "📱",
        "active": True,
    },
    {
        "id": "p4",
        "name": "Afrobeats Mix 2024",
        "category": "music",
        "price": "₦300",
        "type": "MP3",
        "desc": "Hot afrobeats collection — 30 tracks, 45 minutes.",
        "link": "",
        "icon": "🎵",
        "active": True,
    },
    {
        "id": "p5",
        "name": "Tech Tutorial Series",
        "category": "videos",
        "price": "₦2,000",
        "type": "MP4",
        "desc": "Full coding tutorial series. Python, Web Dev & more.",
        "link": "",
        "icon": "🎬",
        "active": True,
    },
    {
        "id": "p6",
        "name": "Galaxy Tab A9",
        "category": "gadgets",
        "price": "₦85,000",
        "type": "PRODUCT",
        "desc": "Samsung Galaxy Tab A9 — brand new sealed box. Fast delivery.",
        "link": "",
        "icon": "💻",
        "active": True,
    },
]

# ══════════════════════════════════════════════
#   SERVICES
# ══════════════════════════════════════════════
SERVICES = [
    {"name": "Web Development",   "price": "₦15,000+", "desc": "Full websites & web apps built from scratch.",       "icon": "🌐", "link": WHATSAPP},
    {"name": "Bot Development",   "price": "₦10,000+", "desc": "Telegram & WhatsApp bots with full features.",       "icon": "🤖", "link": WHATSAPP},
    {"name": "Graphic Design",    "price": "₦3,000+",  "desc": "Logos, flyers, banners & brand identity.",           "icon": "🎨", "link": WHATSAPP},
    {"name": "App Installation",  "price": "₦500",     "desc": "Remote installation & setup of any app.",            "icon": "📲", "link": WHATSAPP},
]

# ══════════════════════════════════════════════
#   CATEGORIES
# ══════════════════════════════════════════════
CATEGORIES = {
    "education": {"label": "📚 Education",  "id": "education"},
    "apps":      {"label": "📱 Apps / APK", "id": "apps"},
    "music":     {"label": "🎵 Music",      "id": "music"},
    "videos":    {"label": "🎬 Videos",     "id": "videos"},
    "gadgets":   {"label": "💻 Gadgets",    "id": "gadgets"},
    "education2":{"label": "📄 Documents",  "id": "documents"},
}

# ══════════════════════════════════════════════
#   HELPERS
# ══════════════════════════════════════════════
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def me_button():
    """Returns the Me inline button linking to portfolio."""
    return InlineKeyboardButton(ME_LABEL, url=ME_LINK)

def back_home_row():
    return [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]

def me_row():
    return [me_button(), InlineKeyboardButton("📞 Contact", callback_data="contact")]

async def send_cyber_footer(update_or_query, context: ContextTypes.DEFAULT_TYPE, caption: str, keyboard):
    """Send cyberpunk image with caption and keyboard as footer of every menu."""
    full_caption = f"{caption}\n\n━━━━━━━━━━━━━━━━\n{ME_BIO}"
    try:
        if hasattr(update_or_query, 'message') and update_or_query.message:
            await update_or_query.message.reply_photo(
                photo=CYBER_IMAGE,
                caption=full_caption,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        else:
            await update_or_query.edit_message_media(
                media=InputMediaPhoto(media=CYBER_IMAGE, caption=full_caption, parse_mode="Markdown"),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    except Exception:
        # Fallback: send as text if image fails
        msg = full_caption
        if hasattr(update_or_query, 'message') and update_or_query.message:
            await update_or_query.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await update_or_query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

# ══════════════════════════════════════════════
#   /start  — MAIN MENU
# ══════════════════════════════════════════════
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍 Shop",       callback_data="shop"),
         InlineKeyboardButton("🛠 Services",   callback_data="services")],
        [InlineKeyboardButton("🔗 Links",      callback_data="links"),
         InlineKeyboardButton("ℹ About",       callback_data="about")],
        [me_button(), InlineKeyboardButton("📞 Contact", callback_data="contact")],
    ]
    await send_cyber_footer(update, context, WELCOME_MSG, keyboard)

# ══════════════════════════════════════════════
#   SHOP — CATEGORIES
# ══════════════════════════════════════════════
async def show_shop(query, context):
    cats = [p["category"] for p in PRODUCTS if p["active"]]
    unique_cats = list(dict.fromkeys(cats))

    cat_labels = {
        "education": "📚 Education",
        "apps":      "📱 Apps / APK",
        "music":     "🎵 Music",
        "videos":    "🎬 Videos",
        "gadgets":   "💻 Gadgets",
        "documents": "📄 Documents",
    }

    buttons = []
    row = []
    for cat in unique_cats:
        row.append(InlineKeyboardButton(cat_labels.get(cat, cat.title()), callback_data=f"cat_{cat}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append(back_home_row())
    buttons.append(me_row())

    text = "🛍 *Our Store*\n\nChoose a category to browse products 👇"
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   CATEGORY — PRODUCT LIST
# ══════════════════════════════════════════════
async def show_category(query, context, cat: str):
    items = [p for p in PRODUCTS if p["category"] == cat and p["active"]]

    if not items:
        await query.edit_message_text("No products in this category yet. Check back soon! 🙏")
        return

    cat_labels = {
        "education": "📚 Education", "apps": "📱 Apps / APK",
        "music": "🎵 Music", "videos": "🎬 Videos",
        "gadgets": "💻 Gadgets", "documents": "📄 Documents",
    }

    buttons = [[InlineKeyboardButton(f"{p['icon']} {p['name']} — {p['price']}", callback_data=f"prod_{p['id']}")] for p in items]
    buttons.append([InlineKeyboardButton("◀ Back to Shop", callback_data="shop")])
    buttons.append(me_row())

    text = f"{cat_labels.get(cat, cat.title())}\n\nSelect a product to view details 👇"
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   PRODUCT DETAIL
# ══════════════════════════════════════════════
async def show_product(query, context, prod_id: str):
    prod = next((p for p in PRODUCTS if p["id"] == prod_id), None)
    if not prod:
        await query.edit_message_text("Product not found.")
        return

    text = (
        f"{prod['icon']} *{prod['name']}*\n\n"
        f"💰 *Price:* {prod['price']}\n"
        f"📁 *Type:* {prod['type']}\n\n"
        f"{prod['desc']}\n\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"*To Purchase:*\n"
        f"🏦 Bank: *{BANK_NAME}*\n"
        f"📋 Account: *{ACCOUNT_NUM}*\n"
        f"👤 Name: *{ACCOUNT_NAME}*\n\n"
        f"After payment, tap ✅ *I've Paid* below."
    )

    buttons = [
        [InlineKeyboardButton("✅ I've Paid", callback_data=f"paid_{prod_id}")],
        [InlineKeyboardButton(f"◀ Back", callback_data=f"cat_{prod['category']}"),
         InlineKeyboardButton("🏠 Home", callback_data="home")],
        [me_button()],
    ]
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   PAYMENT CONFIRMATION
# ══════════════════════════════════════════════
async def payment_received(query, context, prod_id: str):
    prod = next((p for p in PRODUCTS if p["id"] == prod_id), None)
    if not prod:
        return

    user = query.from_user
    # Notify admin
    admin_msg = (
        f"🔔 *NEW ORDER!*\n\n"
        f"👤 User: {user.full_name}\n"
        f"🔗 Handle: @{user.username or 'N/A'}\n"
        f"🆔 ID: `{user.id}`\n\n"
        f"📦 Product: *{prod['name']}*\n"
        f"💰 Amount: *{prod['price']}*\n"
        f"📁 Type: {prod['type']}\n\n"
        f"Reply to confirm & send the file."
    )
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Admin notify failed: {e}")

    # Send file if link exists
    if prod["link"]:
        confirm_text = (
            f"✅ *Payment Received!*\n\n"
            f"Thank you! Your file is being sent now... 📤\n\n"
            f"📦 *{prod['name']}*\n\n"
            f"Thank you for shopping with *{BOT_NAME}* 🙏"
        )
        buttons = [
            [InlineKeyboardButton("🛍 Shop More", callback_data="shop"),
             InlineKeyboardButton("🏠 Home", callback_data="home")],
            [me_button()],
        ]
        await send_cyber_footer(query, context, confirm_text, buttons)
        # Send the actual file
        try:
            await context.bot.send_document(chat_id=query.from_user.id, document=prod["link"], caption=f"📦 {prod['name']} — Enjoy! 🚀\n\n_{BOT_NAME} | {COMPANY}_", parse_mode="Markdown")
        except Exception as e:
            logger.error(f"File send error: {e}")
            await context.bot.send_message(chat_id=query.from_user.id, text=f"📎 Download link: {prod['link']}")
    else:
        # No file set — admin will send manually
        confirm_text = (
            f"✅ *Payment Noted!*\n\n"
            f"Thank you! The admin has been notified and will send your file shortly. ⏳\n\n"
            f"📦 *{prod['name']}*\n\n"
            f"If you don't receive it within 10 minutes, contact us below 👇"
        )
        buttons = [
            [InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_TG.replace('@','')}")],
            [InlineKeyboardButton("🏠 Home", callback_data="home")],
            [me_button()],
        ]
        await send_cyber_footer(query, context, confirm_text, buttons)

# ══════════════════════════════════════════════
#   SERVICES
# ══════════════════════════════════════════════
async def show_services(query, context):
    text = "🛠 *Our Services*\n\n"
    for s in SERVICES:
        text += f"{s['icon']} *{s['name']}* — {s['price']}\n_{s['desc']}_\n\n"

    buttons = [
        [InlineKeyboardButton(f"📩 Order: {s['name']}", url=s["link"])] for s in SERVICES
    ]
    buttons.append(back_home_row())
    buttons.append(me_row())
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   LINKS
# ══════════════════════════════════════════════
async def show_links(query, context):
    text = "🔗 *Our Links*\n\nFind us on all platforms 👇"
    buttons = [
        [InlineKeyboardButton("💬 WhatsApp",        url=WHATSAPP)],
        [InlineKeyboardButton("📸 Instagram",       url=INSTAGRAM)],
        [InlineKeyboardButton("✈ Telegram Channel", url=f"https://t.me/{ADMIN_TG.replace('@','')}")],
        back_home_row(),
        me_row(),
    ]
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   ABOUT
# ══════════════════════════════════════════════
async def show_about(query, context):
    text = (
        f"ℹ *About {BOT_NAME}*\n\n"
        f"🏙 *{COMPANY}*\n"
        f"_{TAGLINE}_\n\n"
        f"We are a digital solutions company offering:\n"
        f"• 📦 Digital products (files, APKs, music, videos)\n"
        f"• 🎓 Educational materials\n"
        f"• 💻 Tech gadgets\n"
        f"• 🛠 Development services\n\n"
        f"All products are delivered instantly or within minutes of payment confirmation.\n\n"
        f"📲 Bot: {BOT_HANDLE}\n"
        f"📞 Admin: {ADMIN_TG}"
    )
    buttons = [
        [InlineKeyboardButton("🛍 Shop Now", callback_data="shop")],
        back_home_row(),
        me_row(),
    ]
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   CONTACT
# ══════════════════════════════════════════════
async def show_contact(query, context):
    text = (
        f"📞 *Contact Us*\n\n"
        f"We're always available to help!\n\n"
        f"💬 WhatsApp: {WHATSAPP}\n"
        f"✈ Telegram: {ADMIN_TG}\n"
        f"📸 Instagram: {INSTAGRAM}\n\n"
        f"_Response time: Usually within minutes_ ⚡"
    )
    buttons = [
        [InlineKeyboardButton("💬 WhatsApp",  url=WHATSAPP),
         InlineKeyboardButton("✈ Telegram",   url=f"https://t.me/{ADMIN_TG.replace('@','')}")],
        [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM)],
        back_home_row(),
        [me_button()],
    ]
    await send_cyber_footer(query, context, text, buttons)

# ══════════════════════════════════════════════
#   CALLBACK ROUTER
# ══════════════════════════════════════════════
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "home":
        await start(update, context)
    elif data == "shop":
        await show_shop(query, context)
    elif data == "services":
        await show_services(query, context)
    elif data == "links":
        await show_links(query, context)
    elif data == "about":
        await show_about(query, context)
    elif data == "contact":
        await show_contact(query, context)
    elif data.startswith("cat_"):
        await show_category(query, context, data[4:])
    elif data.startswith("prod_"):
        await show_product(query, context, data[5:])
    elif data.startswith("paid_"):
        await payment_received(query, context, data[5:])

# ══════════════════════════════════════════════
#   UNKNOWN MESSAGES
# ══════════════════════════════════════════════
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Use /start to open the menu!\n\n_{BOT_NAME} | {COMPANY}_",
        parse_mode="Markdown"
    )

# ══════════════════════════════════════════════
#   MAIN
# ══════════════════════════════════════════════
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    logger.info(f"🚀 {BOT_NAME} bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
