from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from configs import *


@Client.on_callback_query()
async def callback(bot, query):
    me = await bot.get_me()
    data = query.data
    msg = query.message

    if data == "delete":
        await msg.delete()
        try:
            await msg.reply_to_message.delete()
        except:
            pass

    elif data == "help":
        await msg.edit(
            HELP_TXT.format(me.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Aʙᴏᴜᴛ ★", callback_data="about")],
                    [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ ⌘", url="https://telegram.me/Any_Url_Support")],
                    [InlineKeyboardButton("Rᴇᴘᴏ 🛠", url="https://telegram.me/ProfessorR2k"),
                     InlineKeyboardButton("Bᴀᴄᴋ ✰", callback_data="start")]
                ]
            )
        )

    elif data == "about":
        await msg.edit(
            ABOUT_TXT.format(me.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Uᴘᴅᴀᴛᴇs 🙌", url="https://telegram.me/R2K_Bots"),
                     InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ ⚡", url="https://telegram.me/ProfessorR2k")],
                    [InlineKeyboardButton("Hᴇʟᴩ Mᴇɴᴜ ⁂", callback_data="help")],
                    [InlineKeyboardButton("Rᴇᴘᴏ 🛠", url="https://telegram.me/ProfessorR2k")],
                    [InlineKeyboardButton("Bᴀᴄᴋ 𖦹", callback_data="start")]
                ]
            )
        )

    elif data == "set_shortner":
        await msg.edit(
            "Use the following command to set your shortener:\n\n<code>/setshortner example.com api</code>",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Hᴇʟᴩ Mᴇɴᴜ 🙌", callback_data="help")],
                    [InlineKeyboardButton("Bᴀᴄᴋ ✌", callback_data="help"),
                     InlineKeyboardButton("Rᴇᴘᴏ 🛠", url="https://telegram.me/ProfessorR2k")]
                ]
            )
        )

    elif data == "start":
        await msg.edit(
            START_TXT.format(query.from_user.mention),
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Hᴇʟᴩ Mᴇɴᴜ", callback_data="help")],
                    [InlineKeyboardButton("Cʜᴀɴɴᴇʟ", url="https://telegram.me/R2K_Bots"),
                     InlineKeyboardButton("Sᴜᴩᴩᴏʀᴛ", url="https://telegram.me/Any_Url_Support")],
                    [InlineKeyboardButton("Cʟᴏsᴇ ❌", callback_data="delete")]
                ]
            )
        )
