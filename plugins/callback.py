from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from configs import START_TXT, HELP_TXT, ABOUT_TXT


@Client.on_callback_query()
async def callback(bot, query: CallbackQuery):
    data = query.data
    msg = query.message

    if data == "delete":
        try:
            await msg.delete()
            if msg.reply_to_message:
                await msg.reply_to_message.delete()
        except:
            pass

    elif data == "help":
        await msg.edit_text(
            HELP_TXT,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔧 Set Shortner", callback_data="set_shortner"),
                     InlineKeyboardButton("ℹ️ About", callback_data="about")],
                    [InlineKeyboardButton("📢 Support", url="https://t.me/Any_Url_Support")],
                    [InlineKeyboardButton("❌ Close", callback_data="delete")]
                ]
            )
        )

    elif data == "about":
        me = await bot.get_me()
        await msg.edit_text(
            ABOUT_TXT.format(me.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("📢 Updates", url="https://t.me/R2K_Bots"),
                     InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/ProfessorR2k")],
                    [InlineKeyboardButton("❓ Help", callback_data="help"),
                     InlineKeyboardButton("💰 Earn", callback_data="earn_money")],
                    [InlineKeyboardButton("🔙 Back", callback_data="start")]
                ]
            )
        )

    elif data == "set_shortner":
        await msg.edit_text(
            "🛠 Send your shortner domain and API key using:\n\n<code>/shortlink domain.com api_key</code>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔙 Back", callback_data="help"),
                     InlineKeyboardButton("❌ Close", callback_data="delete")]
                ]
            )
        )

    elif data == "earn_money":
        await msg.edit_text(
            "💸 Earn money by shortening links using any valid shortner site.\n"
            "Signup, set your domain & API, and start sharing short links.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔙 Back", callback_data="help"),
                     InlineKeyboardButton("💬 Support", url="https://t.me/Any_Url_Support")]
                ]
            )
        )

    elif data == "start":
        me = await bot.get_me()
        await msg.edit_text(
            START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔱 Help", callback_data="help"),
                     InlineKeyboardButton("💰 Earn", callback_data="earn_money")],
                    [InlineKeyboardButton("📢 Channel", url="https://t.me/R2K_Bots"),
                     InlineKeyboardButton("🛠 Repo", url="https://t.me/ProfessorR2k")],
                    [InlineKeyboardButton("❌ Close", callback_data="delete")]
                ]
            )
        )
