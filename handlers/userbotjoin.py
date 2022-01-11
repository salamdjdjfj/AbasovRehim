import asyncio
from callsmusic.callsmusic import client as USER
from config import BOT_USERNAME, SUDO_USERS
from helpers.decorators import authorized_users_only, sudo_users_only, errors
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant


@Client.on_message(
    command(["join", f"join@{BOT_USERNAME}"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def join_group(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "• **icazəm yoxdur:**\n\n» ❌ __İstifadəçilər əlavə edin__",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"

    try:
        await USER.join_chat(invitelink)
    except UserAlreadyParticipant:
        pass
    except Exception as e:
        print(e)
        await message.reply_text(
            f"🛑 Daşqın Gözləmə Xətası 🛑 \n\n**userbot istifadəçi botu üçün çoxlu qoşulma sorğuları səbəbindən qrupunuza qoşula bilmədi**"
             "\n\n**və ya köməkçini əl ilə Qrupunuza əlavə edin və yenidən cəhd edin**",
        )
        return
    await message.reply_text(
        f"✅ **uuserbot uğurla çata daxil oldu**",
    )


@Client.on_message(
    command(["leave", f"leave@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def leave_group(client, message):
    try:
        await USER.send_message(message.chat.id, "✅ userbot çatı uğurla tərk etdi")
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "❌ **userbot qrupunuzu tərk edə bilmədi, gözlənilməz ola bilər.**\n\n**» və ya istifadəçi robotunu qrupunuzdan əl ilə qovun**"
        )

        return


@Client.on_message(command(["leaveall", f"leaveall@{BOT_USERNAME}"]))
@sudo_users_only
async def leave_all(client, message):
    if message.from_user.id not in SUDO_USERS:
        return

    left = 0
    failed = 0
    lol = await message.reply("🔄 **userbot** bütün söhbətləri tərk edir !")
    async for dialog in USER.iter_dialogs():
        try:
            await USER.leave_chat(dialog.chat.id)
            left += 1
            await lol.edit(
                f"Userbot bütün qrupu tərk edir...\n\nSol: {left} söhbət.\nFailed: {failed} söhbət."
            )
        except:
            failed += 1
            await lol.edit(
               f"İstifadəçi robotu gedir...\n\nSol: {left} söhbətlər.\nuğursuz: {failed} söhbətlər."
            )
        await asyncio.sleep(0.7)
    await client.send_message(
        message.chat.id, f"✅ Burdan ayrıldı: {left} söhbət.\n❌ Uğursuz: {failed} söhbətlər."
    )
