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
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbhelp")]]
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

📌 **istifadəçi robotu video çata qoşulmayıbsa, video çatın artıq aktiv olub olmadığına əmin olun və ya /leave sonra /join yazın.**

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
        return await query.answer("💡 yalnız admin bu düyməyə toxuna bilər !", show_alert=True)
    await query.edit_message_text(
        f"""📚 **bu xüsusiyyət məlumatıdır:**
        
**💡 Xüsusiyyət:** qruplarda spamın qarşısını almaq üçün istifadəçilər tərəfindən göndərilən hər əmrləri silin !

❔ istifadə:**

 1️⃣ funksiyanı aktiv etmək üçün:
      » növü `/delcmd on`
    
 2️⃣funksiyanı söndürmək üçün:
      » növü `/delcmd off`
      
⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbback")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbcmds"))
async def cbhelps(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""✨ **Salam** [{query.message.chat.first_name}](tg://user?id={query.message.chat.id}) !

» **izahı oxumaq və mövcud əmrlərin siyahısına baxmaq üçün aşağıdakı düyməni basın !**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📚 Əsas Cmd", callback_data="cblocal"),
                    InlineKeyboardButton("📕 Qabaqcıl Cmd", callback_data="cbadven"),
                ],
                [
                    InlineKeyboardButton("📘 Admin Cmd", callback_data="cblamp"),
                    InlineKeyboardButton("📗 Sudo Cmd", callback_data="cblab"),
                ],
                [InlineKeyboardButton("📙 Owner Cmd", callback_data="cbmoon")],
                [InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbstart")],
            ]
        ),
    )


@Client.on_callback_query(filters.regex("cbhowtouse"))
async def cbguides(_, query: CallbackQuery):
    await query.edit_message_text(
f"""❓ **BU BOTDAN NECƏ İSTİFADƏ EDİLMƏK:**

 1.) **əvvəlcə məni öz qrupuna əlavə et.**
 2.) **sonra məni admin kimi tanıt və anonim admin istisna olmaqla bütün icazələri ver.**
3.) **məni əlavə etdikdən sonra /reload yazıb admin siyahısını yeniləyin.**
3.) ** @{ASSISTANT_NAME} qrupunuza əlavə edon və ya ASSISTANTI dəvət etmək üçün /join yazın.**
 4.) **musiqi başlatmazdan əvvəl ilk olaraq video çatı yandırın.**

📌 **istifadəçi robotu video çata qoşulmayıbsa, video çatın artıq aktiv olub olmadığına əmin olun və ya /leave sonra /join yazın.**

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbstart")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblocal"))
async def cblocal(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur əsas əmrlər**

🎧 [ SƏSLİ CHAT OYNA CMD ]

/play (mahnı adı) - youtube-dan mahnı oxuyun
 /ytp (mahnı adı) - mahnını birbaşa youtube-dan səsləndirin
 /stream (audioya cavab) - audio fayldan istifadə edərək mahnı oxuyun
/playlist - siyahı mahnısını növbədə göstərmək
/song (mahnının adı) - youtube-dan mahnı yükləmək
/search (video adı) - youtube-dan ətraflı axtarış videosu
/video (video adı) - ətraflı youtube-dan videonu endir
 /lyrics - (mahnı adı) lyrics scrapper

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbadven"))
async def cbadven(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **burada qabaqcıl əmrlər var**

/start (qrupda) - botun canlı statusuna baxın
/reload - botu yenidən yükləyin və admin siyahısını yeniləyin
/ping - bot ping statusunu yoxlayın
/uptime - botun işləmə müddətini yoxlayın
/id - qrup/istifadəçi identifikatorunu və digərlərini göstərin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblamp"))
async def cblamp(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur admin əmrləri**

/player - musiqi ifa vəziyyətini göstərir
 /pause - musiqi axınını dayandırın
 /resume - musiqinin dayandırıldığını davam etdirin
/skip - növbəti mahnıya keçin
 /end - musiqi axını dayandırın
 /join - istifadəçi robotunu qrupunuza qoşulmağa dəvət edin
/leave - istifadəçi robotuna qrupunuzu tərk etməsini əmr edin
 /auth - musiqi botundan istifadə etmək üçün səlahiyyətli istifadəçi
 /unauth - musiqi botundan istifadə üçün icazəsiz
 /control - oyunçu parametrləri panelini açın
 /delcmd (on | off) - del cmd funksiyasını aktivləşdirin / söndürün
 /music (on / off) - qrupunuzda musiqi pleyeri söndürün / aktivləşdirin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cblab"))
async def cblab(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur sudo əmrləri**

/leaveall - köməkçiyə bütün qrupdan çıxmağı əmr edin
 /stats - bot statistikasını göstərir
 /rmd - bütün yüklənmiş faylları silin
 /clear - bütün .jpg faylları silin
 /eval (sorğu) - kodu icra edin
 /sh (sorğu) - kodu işlədin

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cbmoon"))
async def cbmoon(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""🏮 **budur sahibin əmrləri**

/stats - bot statistikasını göstərin
/broadcast - botdan yayım mesajı göndərin
/block (istifadəçi identifikatoru - müddət - səbəb) - istifadəçini botunuzdan istifadə etməsi üçün bloklayın
/unblock (istifadəçi identifikatoru - səbəb) - botunuzdan istifadə etdiyinə görə blokladığınız istifadəçini blokdan çıxarın
/blocklist - botunuzdan istifadə üçün bloklanmış istifadəçinin siyahısını sizə göstərin

📝 Qeyd: bu bota məxsus bütün əmrlər heç bir istisnasız olaraq botun sahibi tərəfindən icra edilə bilər..

⚡ __Powered by {BOT_NAME} A.I__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cbcmds")]]
        ),
    )


@Client.on_callback_query(filters.regex("cmdhome"))
async def cmdhome(_, query: CallbackQuery):
    
    bttn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Command Syntax", callback_data="cmdsyntax")
            ],[
                InlineKeyboardButton("🗑 Bağla", callback_data="close")
            ]
        ]
    )
    
    nofound = "😕 **sorğu etdiyiniz mahnını tapa bilmədim**\n\n» **düzgün mahnı adını və ya ifaçının adını da qeyd edin**"
    
    await query.edit_message_text(nofound, reply_markup=bttn)


@Client.on_callback_query(filters.regex("cmdsyntax"))
async def cmdsyntax(_, query: CallbackQuery):
    await query.edit_message_text(
        f"""****Səsli Çatda musiqi oxutmaq üçün Sintaksisi** əmri:**

• `/play (query)` - youtube vasitəsilə musiqi oxutmaq üçün
 • `/ytp (query)` - birbaşa youtube vasitəsilə musiqi oxutmaq üçün

⚡ __Powered by {BOT_NAME}__""",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Geri qayıt", callback_data="cmdhome")]]
        ),
    )
