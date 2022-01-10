# (C) 2021 VeezMusic-Project

from helpers.decorators import authorized_users_only
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)


@Client.on_callback_query(filters.regex("cbstart"))
async def cbstart(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Xoş gəlmisiniz [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !**\n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) sizə yeni Telegram-ın səsli çatları vasitəsilə qruplarda musiqi oxumağa imkan verir!**

💡 **» 📚 Əmrlər düyməsini klikləməklə Botun bütün əmrlərini və onların necə işlədiyini öyrənin!**

🔖 **Bu botdan necə istifadə edəcəyinizi öyrənmək üçün » ❓ Əsas Bələdçi düyməsini sıxın!**""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Məni Qrupunuza əlavə edin ➕",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ Əsas Bələdçi", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 Əmrlər", callback_data="cbcmds"),
                    InlineKeyboardButton("❤️ Sahib", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 Söhbət Qrupu", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "📣 Kanal", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 Botlarımız", url="https://t.me/TgRobotlarim"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex("cbhelp"))
async def cbhelp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Salam !**

 » **izahı oxumaq və mövcud əmrlərin siyahısına baxmaq üçün aşağıdakı düyməni basın !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Əsas Cmd", callback_data="cbbasic"),
                    InlineKeyboardButton("📕 Qabaqcıl Cmd", callback_data="cbadvanced"),
                ],
                [
                    InlineKeyboardButton("📘 Admin Cmd", callback_data="cbadmin"),
                    InlineKeyboardButton("📗 Sudo Cmd", callback_data="cbsudo"),
                ],
                [InlineKeyboardButton("📙 Owner Cmd", callback_data="cbowner")],
                [InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbguide")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbbasic"))
async def cbbasic(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur əsas əmrlər**

🎧 [ SƏSLİ CHAT OYNA CMD ]

/play (mahnı adı) - youtube-dan mahnı oxuyun
/ytp (mahnı adı) - mahnını birbaşa youtube-dan oxuyun 
/stream (audioya cavab) - audio fayldan istifadə edərək mahnı oxuyun
/playlist - sıradakı mahnını göstərin
/song (mahnının adı) - youtube-dan mahnı yükləmək
/search (video adı) - youtube-dan ətraflı axtarış videosu
/video (video adı) - ətraflı youtube-dan videonu endir
/lyrics - (mahnı adı) lyrics scrapper

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadvanced"))
async def cbadvanced(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **burada qabaqcıl əmrlər var**

/start (qrupda) - botun canlı statusuna baxın
/reload - botu yenidən yükləyin və admin siyahısını yeniləyin
/ping - botun ping statusunu yoxlayın
/uptime - botun işləmə müddətini yoxlayın
/id - qrup/istifadəçi identifikatorunu və digərlərini göstərin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadmin"))
async def cbadmin(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **burada admin əmrləri var**

/player - musiqi ifa vəziyyətini göstərin
/pause - musiqi axınını dayandırın
/resume - musiqi dayandırıldı
/skip - növbəti mahnıya keçin
/end - musiqi axını dayandırın
/join - userbot-u qrupunuza qoşulmağa dəvət edin
/leave - userbot-a qrupunuzu tərk etməsini əmr edin
/auth - musiqi botundan istifadə etmək üçün səlahiyyətli istifadəçi
/unauth - musiqi botundan istifadə üçün icazəsiz
/control - pleyer parametrləri panelini açın
/delcmd (on | off) - del cmd funksiyasını aktivləşdirin / söndürün
/music (on / off) - qrupunuzdakı musiqi pleyeri söndürün / aktivləşdirin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbsudo"))
async def cbsudo(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **burada sudo əmrləri var**

/leaveall - köməkçiyə bütün qrupdan çıxmağı əmr edin
/stats - bot statistikasını göstərin
/rmd - bütün yüklənmiş faylları silin
/clear - bütün .jpg faylları silin
/eval (sorğu) - kodu icra edin
/sh (sorğu) - kodu işlədin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbowner"))
async def cbowner(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur sahibin əmrləri**

/stats - bot statistikasını göstərin
/broadcast (mesaja cavab verin) - botdan yayım mesajı göndərin
/block (istifadəçi identifikatoru - müddət - səbəb) - botunuzdan istifadə etmək üçün istifadəçini bloklayın
/unblock (istifadəçi identifikatoru - səbəb) - botunuzdan istifadə üçün blokladığınız istifadəçini blokdan çıxarın
/blocklist - botunuzdan istifadə üçün bloklanmış istifadəçinin siyahısını sizə göstərin

📝 Qeyd: bu bota məxsus bütün əmrlər heç bir istisnasız olaraq botun sahibi tərəfindən icra edilə bilər..

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbhelp")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbguide"))
async def cbguide(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **BU BOTDAN NECƏ İSTİFADƏ EDİLMƏK:**

1.) **əvvəlcə məni öz qrupuna əlavə et.**
 2.) **sonra məni admin kimi tanıt və anonim admin istisna olmaqla bütün icazələri ver.**
 3.) **məni təbliğ etdikdən sonra admin siyahısını yeniləmək üçün qrupa /reload yazın.**
3.) **qrupunuza @{ASSISTANT_NAME} əlavə edin və ya onu dəvət etmək üçün /join yazın.**
 4.) **musiqi çalmağa başlamazdan əvvəl ilk olaraq video çatı yandırın.**

📌 **istifadəçi robotu video çata qoşulmayıbsa, video çatın artıq aktiv olub olmadığına əmin olun və ya /çıxıb, sonra yenidən /qoşulun yazın.**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📚 Əmrlər siyahısı", callback_data="cbhelp")],
                [InlineKeyboardButton("🗑 Bağla", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("close"))
async def close(_, query: CallbackQuery):
    await query.message.delete()


@Client.on_callback_query(filters.regex("cbback"))
async def cbback(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 yalnız admin bu düyməyə toxuna bilər !", show_alert=True)
    await query.edit_message_text(
        "**💡 burada botun idarəetmə menyusu var :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ pause", callback_data="cbpause"),
                    InlineKeyboardButton("▶️ resume", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("⏩ skip", callback_data="cbskip"),
                    InlineKeyboardButton("⏹ stop", callback_data="cbend"),
                ],
                [InlineKeyboardButton("⛔ anti cmd", callback_data="cbdelcmds")],
                [InlineKeyboardButton("🗑 Bağla", callback_data="close")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbdelcmds"))
async def cbdelcmds(_, query: CallbackQuery):
    a = await _.get_chat_member(query.message.chat.id, query.from_user.id)
    if not a.can_manage_voice_chats:
        return await query.answer("💡 only admin can tap this button !", show_alert=True)
    await query.edit_message_text(
        f"""📚 **this is the feature information:**
        
**💡 Feature:** delete every commands sent by users to avoid spam in groups !

❔ usage:**

 1️⃣ to turn on feature:
     » type `/delcmd on`
    
 2️⃣ to turn off feature:
     » type `/delcmd off`
      
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbback")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Hello** [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !

» **press the button below to read the explanation and see the list of available commands !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Basic Cmd", callback_data="cblocal"),
                    InlineKeyboardButton("📕 Advanced Cmd", callback_data="cbadven"),
                ],
                [
                    InlineKeyboardButton("📘 Admin Cmd", callback_data="cblamp"),
                    InlineKeyboardButton("📗 Sudo Cmd", callback_data="cblab"),
                ],
                [InlineKeyboardButton("📙 Owner Cmd", callback_data="cbmoon")],
                [InlineKeyboardButton("🔙 Go Back", callback_data="cbstart")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""❓ **HOW TO USE THIS BOT:**

1.) **first, add me to your group.**
2.) **then promote me as admin and give all permissions except anonymous admin.**
3.) **after promoting me, type /reload in group to update the admin list.**
3.) **add @{ASSISTANT_NAME} to your group or type /join to invite her.**
4.) **turn on the video chat first before start to play music.**

📌 **if the userbot not joined to video chat, make sure if the video chat already turned on, or type /leave then type /join again.**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblocal"))
async def cblocal(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **here is the basic commands**

🎧 [ VOICE CHAT PLAY CMD ]

/play (song name) - play song from youtube
/ytp (song name) - play song directly from youtube 
/stream (reply to audio) - play song using audio file
/playlist - show the list song in queue
/song (song name) - download song from youtube
/search (video name) - search video from youtube detailed
/video (video name) - download video from youtube detailed
/lyric - (song name) lyrics scrapper

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadven"))
async def cbadven(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **here is the advanced commands**

/start (in group) - see the bot alive status
/reload - reload bot and refresh the admin list
/ping - check the bot ping status
/uptime - check the bot uptime status
/id - show the group/user id & other

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblamp"))
async def cblamp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **here is the admin commands**

/player - show the music playing status
/pause - pause the music streaming
/resume - resume the music was paused
/skip - skip to the next song
/end - stop music streaming
/join - invite userbot join to your group
/leave - order the userbot to leave your group
/auth - authorized user for using music bot
/unauth - unauthorized for using music bot
/control - open the player settings panel
/delcmd (on | off) - enable / disable del cmd feature
/music (on / off) - disable / enable music player in your group

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblab"))
async def cblab(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **here is the sudo commands**

/leaveall - order the assistant to leave from all group
/stats - show the bot statistic
/rmd - remove all downloaded files
/clear - remove all .jpg files
/eval (query) - execute code
/sh (query) - run code

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmoon"))
async def cbmoon(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **here is the owner commands**

/stats - show the bot statistic
/broadcast - send a broadcast message from bot
/block (user id - duration - reason) - block user for using your bot
/unblock (user id - reason) - unblock user you blocked for using your bot
/blocklist - show you the list of user was blocked for using your bot

📝 note: all commands owned by this bot can be executed by the owner of the bot without any exceptions.

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cmdhome"))
async def cmdhome(_, query: CallbackQuery):
    
    bttn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Command Syntax", callback_data="cmdsyntax")
            ],[
                InlineKeyboardButton("🗑 Close", callback_data="close")
            ]
        ]
    )
    
    nofound = "😕 **couldn't find song you requested**\n\n» **please provide the correct song name or include the artist's name as well**"
    
    await query.edit_message_text(nofound, reply_markup=bttn)


@Client.on_callback_query(filters.regex("cmdsyntax"))
async def cmdsyntax(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""**Command Syntax** to play music on **Voice Chat:**

• `/play (query)` - for playing music via youtube
• `/ytp (query)` - for playing music directly via youtube

⚡ __Powered by {BOT_NAME}__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Go Back", callback_data="cmdhome")]]
        ),
    )
