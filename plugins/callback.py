from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from configs import START_TXT, HELP_TXT, ABOUT_TXT, SUPPORT_GROUP, UPDATES_CHANNEL


@Client.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data
    user = query.from_user
    msg = query.message

    if data == "help":
        await msg.edit_text(
            HELP_TXT,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Updates", url=f"https://t.me/{UPDATES_CHANNEL}")],
                [InlineKeyboardButton("🎨 Format", callback_data="set_format"),
                 InlineKeyboardButton("🖋️ Caption", callback_data="set_caption")],
                [InlineKeyboardButton("🔙 Back", callback_data="start")]
            ])
        )

    elif data == "about":
        await msg.edit_text(
            ABOUT_TXT.format(client.me.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{UPDATES_CHANNEL}")],
                [InlineKeyboardButton("👥 Support", url=f"https://t.me/{SUPPORT_GROUP}")],
                [InlineKeyboardButton("🔙 Back", callback_data="start")]
            ])
        )

    elif data == "start":
        await msg.edit_text(
            START_TXT.format(user.mention),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔱 Help", callback_data="help"),
                 InlineKeyboardButton("💰 Earn", callback_data="earn_money")],
                [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{UPDATES_CHANNEL}")],
                [InlineKeyboardButton("❌ Close", callback_data="delete")]
            ])
        )

    elif data == "earn_money":
        await msg.edit_text(
            "<b>💸 Earn Money by Sharing Short Links!</b>\n\n"
            "➤ Use your own shortener with a monetized domain.\n"
            "➤ Share the links on social media, YouTube, etc.\n"
            "➤ Earn money whenever someone clicks!\n\n"
            "💡 Use /shortlink to set your site and API key.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="help")]
            ])
        )

    elif data == "set_format":
        await msg.edit_text(
            "🎨 <b>Choose your preferred link format</b>\n\n"
            "Use:\n<code>/setformat bold</code>\n\n"
            "<b>Available options:</b>\n"
            "- bold\n- italic\n- mono\n- plain",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="help")]
            ])
        )

    elif data == "set_caption":
        await msg.edit_text(
            "🖋️ <b>Set a custom caption that appears before shortened links</b>\n\n"
            "Use:\n<code>/setcaption Your caption text</code>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="help")]
            ])
        )

    elif data == "delete":
        try:
            await msg.delete()
        except:
            await query.answer("❌ Can't delete this message", show_alert=True)
