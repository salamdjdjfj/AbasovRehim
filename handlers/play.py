import os
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty

import aiofiles
import aiohttp
import converter
import ffmpeg
import requests
from cache.admins import admins as a
from callsmusic import callsmusic
from callsmusic.callsmusic import client as USER
from callsmusic.queues import queues
from config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    THUMB_IMG,
    CMD_IMG,
    UPDATES_CHANNEL,
    que,
)
from downloaders import youtube
from helpers.admins import get_administrators
from helpers.channelmusic import get_chat_id
from helpers.chattitle import CHAT_TITLE
from helpers.decorators import authorized_users_only
from helpers.filters import command, other_filters
from helpers.gets import get_url, get_file_name
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtube_search import YoutubeSearch

# plus

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []


def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        else:
            await cb.answer("💡 yalnız admin bu düyməyə toxuna bilər !", show_alert=True)
            return

    return decorator


def transcode(filename):
    ffmpeg.input(filename).output(
        "input.raw", 
        format="s16le", 
        acodec="pcm_s16le", 
        ac=2, 
        ar="48k"
    ).overwrite_output().run()
    os.remove(filename)

def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(title, thumbnail, ctitle):
    async with aiohttp.ClientSession() as session, session.get(thumbnail) as resp:
          if resp.status == 200:
              f = await aiofiles.open("background.png", mode="wb")
              await f.write(await resp.read())
              await f.close()
    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/regular.ttf", 52)
    font2 = ImageFont.truetype("etc/medium.ttf", 76)
    draw.text((27, 538), f"Playing on {ctitle[:8]}..", (0, 0, 0), font=font)
    draw.text((27, 612), f"{title[:18]}...", (0, 0, 0), font=font2)
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command(["playlist", f"playlist@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
async def playlist(client, message):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    queue = que.get(message.chat.id)
    if not queue:
        await message.reply_text("❌ **hazırda heç bir musiqi oxunmur**")
    temp = []
    for t in queue:
        temp.append(t)
    now_playing = temp[0][0]
    by = temp[0][1].mention(style="md")
    msg = "💡 **indi** oxunur {}".format(message.chat.title)
    msg += "\n\n• " + now_playing
    msg += "\n• Req By " + by
    temp.pop(0)
    if temp:
        msg += "\n\n"
        msg += "🔖 **Növbədə Mahnı:**"
        for song in temp:
            name = song[0]
            usr = song[1].mention(style="md")
            msg += f"\n\n• {name}"
            msg += f"\n• Req by {usr}"
    await message.reply_text(msg, reply_markup=keyboard)

# ============================= Settings =========================================

def updated_stats(chat, queue, vol=100):
    if chat.id in callsmusic.pytgcalls.active_calls:
        stats = "⚙ Parametrlər**{}**".format(chat.title)
        if len(que) > 0:
            stats += "\n\n"
            stats += "• həcm: `{}%`\n".format(vol)
            stats += "• mahnı ifa olunub: `{}`\n".format(len(que))
            stats += "• indi oxunur: **{}**\n".format(queue[0][0])
            stats += "• tərəfindən sorğu: {}".format(queue[0][1].mention(style="md"))
    else:
        stats = None
    return stats


def r_ply(type_):
    if type_ == "play":
        pass
    else:
        pass
    mar = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹", "leave"),
                InlineKeyboardButton("⏸", "puse"),
                InlineKeyboardButton("▶️", "resume"),
                InlineKeyboardButton("⏭", "skip"),
            ],
            [
                InlineKeyboardButton("📖 PLAY-LIST", "playlist"),
            ],
            [InlineKeyboardButton("🗑 Close", "cls")],
        ]
    )
    return mar


@Client.on_message(
    command(["player", f"player@{BOT_USERNAME}"]) & filters.group & ~filters.edited
)
@authorized_users_only
async def settings(client, message):
    global que
    playing = None
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        playing = True
    queue = que.get(message.chat.id)
    stats = updated_stats(message.chat, queue)
    if stats:
        if playing:
            await message.reply(stats, reply_markup=r_ply("pause"))

        else:
            await message.reply(stats, reply_markup=r_ply("play"))
    else:
        await message.reply(
            "😕 **səsli söhbət tapılmadı**\n\n» zəhmət olmasa əvvəlcə səsli çatı aktiv edin"
        )


@Client.on_message(
    command(["music", f"music@{BOT_USERNAME}"])
    & ~filters.edited
    & ~filters.bot
    & ~filters.private
)
@authorized_users_only
async def music_onoff(_, message):
    global DISABLED_GROUPS
    try:
        message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "**• istifadə:**\n\n `/music on` & `/music off`"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ("ON", "on", "On"):
        lel = await message.reply("`emal olunur...`")
        if not message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **musiqi pleyeri artıq işə salınıb.**")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(f"✅ **musiqi pleyeri işə salındı**\n\n💬 `{message.chat.id}`")

    elif status in ("OFF", "off", "Off"):
        lel = await message.reply("`emal olunur...`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("» **musiqi pleyeri artıq söndürülüb.**")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(f"✅**musiqi pleyeri söndürüldü**\n\n💬 `{message.chat.id}`")
    else:
        await message.reply_text(
"**• istifadə:**\n\n `/music on` & `/music off`"
        )


@Client.on_callback_query(filters.regex(pattern=r"^(playlist)$"))
async def p_cb(b, cb):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ],
            [InlineKeyboardButton("🔙 Geri qayıt", callback_data="menu")],
        ]
    )

    global que
    que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    cb.message.chat
    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("❌ **Hazırda heç bir musiqi səslənmir**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **indi oxunur** on {}".format(cb.message.chat.title)
        msg += "\n\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔖 **Növbədə Mahnı:**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n\n• {name}"
                msg += f"\n• Req by {usr}"
        await cb.message.edit(msg, reply_markup=keyboard)


@Client.on_callback_query(
    filters.regex(pattern=r"^(play|pause|skip|leave|puse|resume|menu|cls)$")
)
@cb_admin_check
async def m_cb(b, cb):

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Gʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"),
                InlineKeyboardButton(
                    "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ],
            [InlineKeyboardButton("🔙 Geri qayıt", callback_data="menu")],
        ]
    )

    global que
    if (
        cb.message.chat.title.startswith("Kanal Musiqisi: ")
        and chat.title[14:].isnumeric()
    ):
        chat_id = int(chat.title[13:])
    else:
        chat_id = cb.message.chat.id
    qeue = que.get(chat_id)
    type_ = cb.matches[0].group(1)
    cb.message.chat.id
    m_chat = cb.message.chat

    cb.message.reply_markup.inline_keyboard[1][0].callback_data
    if type_ == "pause":
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            await cb.answer(
                "userbot səsli söhbətə qoşulmayıb.", show_alert=True
            )
        else:
            await callsmusic.pytgcalls.pause_stream(chat_id)
            
            await cb.answer("musiqi dayandı")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("play")
            )

    elif type_ == "play":
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            await cb.answer(
                "userbot səsli söhbətə qoşulmayıb.", show_alert=True
            )
        else:
            await callsmusic.pytgcalls.resume_stream(chat_id)
            
            await cb.answer("musiqi davam etdi")
            await cb.message.edit(
                updated_stats(m_chat, qeue), reply_markup=r_ply("pause")
            )

    elif type_ == "playlist":
        queue = que.get(cb.message.chat.id)
        if not queue:
            await cb.message.edit("❌ **Hazırda heç bir musiqi oxunmur**")
        temp = []
        for t in queue:
            temp.append(t)
        now_playing = temp[0][0]
        by = temp[0][1].mention(style="md")
        msg = "💡 **indi oxunur** {}".format(cb.message.chat.title)
        msg += "\n• " + now_playing
        msg += "\n• Req by " + by
        temp.pop(0)
        if temp:
            msg += "\n\n"
            msg += "🔖 **Növbədə Mahnı:**"
            for song in temp:
                name = song[0]
                usr = song[1].mention(style="md")
                msg += f"\n\n• {name}"
                msg += f"\n• Req by {usr}"
        await cb.message.edit(msg, reply_markup=keyboard)

    elif type_ == "resume":
        psn = "▶ musiqinin səsləndirilməsi bərpa edildi"
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            await cb.answer(
                "səsli çat bağlı deyil və ya artıq oxunur", show_alert=True
            )
        else:
            await callsmusic.pytgcalls.resume_stream(chat_id)
            await cb.message.edit(psn, reply_markup=keyboard)

    elif type_ == "puse":
        spn = "⏸ musiqinin səsləndirilməsi dayandırıldı"
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            await cb.answer(
                "səsli söhbət qoşulmayıb və ya artıq dayandırılıb", show_alert=True
            )
        else:
            await callsmusic.pytgcalls.pause_stream(chat_id)
            await cb.message.edit(spn, reply_markup=keyboard)

    elif type_ == "cls":
        await cb.message.delete()

    elif type_ == "menu":
        stats = updated_stats(cb.message.chat, qeue)
        marr = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏹", "leave"),
                    InlineKeyboardButton("⏸", "puse"),
                    InlineKeyboardButton("▶️", "resume"),
                    InlineKeyboardButton("⏭", "skip"),
                ],
                [
                    InlineKeyboardButton("📖 PLAY-LIST", "playlist"),
                ],
                [InlineKeyboardButton("🗑 Close", "cls")],
            ]
        )
        await cb.message.edit(stats, reply_markup=marr)

    elif type_ == "skip":
        nmq = "❌ __Queues__-də daha musiqi yoxdur\n\n» **istifadəçi robotu gedir** səsli çatda"
        mmk = "⏭ növbəti musiqiyə keçdiniz"
        if qeue:
            qeue.pop(0)
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            await cb.answer(
                "köməkçi səsli söhbətə qoşulmayıb !", show_alert=True
            )
        else:
            callsmusic.queues.task_done(chat_id)
            
            if callsmusic.queues.is_empty(chat_id):
                await callsmusic.pytgcalls.leave_group_call(chat_id)
                
                await cb.message.edit(
                    nmq,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("🗑 Bağla", callback_data="close")]]
                    ),
                )
            else:
                await callsmusic.pytgcalls.change_stream(
                    chat_id, 
                    InputStream(
                        InputAudioStream(
                            callsmusic.queues.get(chat_id)["file"],
                        ),
                    ),
                )
                await cb.message.edit(mmk, reply_markup=keyboard)

    elif type_ == "leave":
        hps = "✅ ***musiqi oxutma bitdi**"
        for x in callsmusic.pytgcalls.active_calls:
            ACTV_CALLS.append(int(x.chat_id))
        if int(chat_id) not in ACTV_CALLS:
            try:
                callsmusic.queues.clear(chat_id)
            except QueueEmpty:
                pass
            await callsmusic.pytgcalls.leave_group_call(chat_id)
            await cb.message.edit(
                hps,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🗑 Bağla", callback_data="close")]]
                ),
            )
        else:
            await cb.answer(
                "userbot səsli söhbətə qoşulmayıb.", show_alert=True
            )


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(_, message: Message):
    chat_id = get_chat_id(message.chat)
    bttn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Command Syntax", callback_data="cmdsyntax")
            ],[
                InlineKeyboardButton("🗑 Bağla", callback_data="close")
            ]
        ]
    )
    
    nofound = "😕 **sorğu etdiyiniz mahnını tapa bilmədim**\n\n» **düzgün mahnı adını və ya ifaçının adını da daxil edin**"
    
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔎 **axtarılır...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id
    try:
        user = await USER.get_me()
    except:
        user.first_name = "musiqi köməkçisi"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Kanal Musiqisi: "):
                    await lel.edit(
                        f"💡 **zəhmət olmasa əvvəlcə istifadəçi robotunu kanalınıza əlavə edin.**",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+","https://t.me/joinchat/")
                except:
                    await lel.edit(
                        "💡 **Məndən istifadə etmək üçün aşağıdakı icazələrə malik Administrator** olmalıyam:\n\n» ❌ __Mesajları silin__\n» ❌ __İstifadəçiləri qadağan edin__\n» ❌ __İstifadəçiləri əlavə edin__\n» ❌ __Səsli söhbəti idarə edin__\n\n**Sonra  yazın / yenidən yükləyin**",
                    )
                    return
                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        f"✅ **userbot uğurla söhbətə daxil oldu**",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"🔴 **Daşqın Gözləmə Xətası** 🔴 \n\n**userbot istifadəçi botu üçün çoxsaylı qoşulma sorğularına görə bu qrupa qoşula bilmir.**"
                        f"\n\n**və ya əlavə edin @{ASSISTANT_NAME} bu qrupa əl ilə daxil olun, sonra yenidən cəhd edin.**",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"» **userbot bu çatda deyil və ya bu qrupda qadağan edilib !**\n\n**bandan çıxarın @{ASSISTANT_NAME} və yenidən bu qrupa əl ilə əlavə edin və ya /reload yazın və yenidən cəhd edin."
        )
        return
    text_links = None
    if message.reply_to_message:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            pass
        entities = {}
        toxt = message.reply_to_message.text or message.reply_to_message.caption
        if message.reply_to_message.entities:
            entities = message.reply_to_message.entities + entities
        elif message.reply_to_message.caption_entities:
            entities = message.reply_to_message.entities + entities
        urls = [
            entity for entity in entities if entity.type == "url"
        ]
        text_links = [
            entity for entity in entities if entity.type == "text_link"
        ]
    else:
        urls = None
    if text_links:
        urls = True
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    rpk = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
    audio = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ **davamlı musiqi** `{DURATION_LIMIT}` **dəqiqə, oynaya bilmirəm !**"
            )
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• Mᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("• Cʟᴏsᴇ", callback_data="cls"),
                ],
                [
                    InlineKeyboardButton(
                        "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
            ]
        )
        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/fa2cdb8a14a26950da711.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        message.from_user.first_name
        await generate_cover(title, thumbnail, ctitle)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name))
            else file_name
        )
    elif urls:
        query = toxt
        await lel.edit("🔎 **axtarış...**")
        ydl_opts = {"format": "bestaudio/best"}
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:70]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            ctitle = message.chat.title
            ctitle = await CHAT_TITLE(ctitle)
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            results[0]["url_suffix"]
        except Exception as e:
            await lel.delete()
            await message.reply_photo(
                photo=f"{CMD_IMG}",
                caption=nofound,
                reply_markup=bttn,
            )
            print(str(e))
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("• Mᴇɴᴜ", callback_data="menu"),
                    InlineKeyboardButton("• Cʟᴏsᴇ", callback_data="cls"),
                ],
                [
                    InlineKeyboardButton(
                        "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
            ]
        )
        message.from_user.first_name
        await generate_cover(title, thumbnail, ctitle)
        file_path = await converter.convert(youtube.download(url))
    else:
        query = ""
        for i in message.command[1:]:
            query += " " + str(i)
        print(query)
        ydl_opts = {"format": "bestaudio/best"}

        try:
            results = YoutubeSearch(query, max_results=5).to_dict()
        except:
            await lel.edit(
                "😕 **mahnı adı aşkarlanmadı**\n\n» **zəhmət olmasa oynamaq istədiyiniz mahnının adını qeyd edin**"
            )
        try:
            toxxt = "\n"
            j = 0
            user = user_name
            emojilist = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            while j < 5:
                toxxt += f"{emojilist[j]} [{results[j]['title'][:25]}...](https://youtube.com{results[j]['url_suffix']})\n"
                toxxt += f" ├ 💡 **Duration** - `{results[j]['duration']}`\n"
                toxxt += f" └ ⚡ __Powered by {BOT_NAME}__\n\n"
                j += 1
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "1️⃣", callback_data=f"plll 0|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "2️⃣", callback_data=f"plll 1|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "3️⃣", callback_data=f"plll 2|{query}|{user_id}"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            "4️⃣", callback_data=f"plll 3|{query}|{user_id}"
                        ),
                        InlineKeyboardButton(
                            "5️⃣", callback_data=f"plll 4|{query}|{user_id}"
                        ),
                    ],
                    [InlineKeyboardButton(text="🗑 Bağla", callback_data="cls")],
                ]
            )
            await message.reply_photo(
                photo=f"{THUMB_IMG}",
                caption=toxxt,
                reply_markup=keyboard,
            )
            await lel.delete()
            
            return
        
        except:
            pass

            try:
                url = f"https://youtube.com{results[0]['url_suffix']}"
                title = results[0]["title"][:70]
                thumbnail = results[0]["thumbnails"][0]
                thumb_name = f"{title}.jpg"
                ctitle = message.chat.title
                ctitle = await CHAT_TITLE(ctitle)
                thumb = requests.get(thumbnail, allow_redirects=True)
                open(thumb_name, "wb").write(thumb.content)
                duration = results[0]["duration"]
                results[0]["url_suffix"]
            except Exception as e:
                await lel.delete()
                await message.reply_photo(
                    photo=f"{CMD_IMG}",
                    caption=nofound,
                    reply_markup=bttn,
                )
                print(str(e))
                return
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• Mᴇɴᴜ", callback_data="menu"),
                        InlineKeyboardButton("• Cʟᴏsᴇ", callback_data="cls"),
                    ],
                    [
                        InlineKeyboardButton(
                            "• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                        )
                    ],
                ]
            )
            message.from_user.first_name
            await generate_cover(title, thumbnail, ctitle)
            file_path = await converter.convert(youtube.download(url))
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await lel.delete()
        await message.reply_photo(
            photo="final.png",
            caption=f"💡 **Trek növbəyə əlavə edildi »** `{position}`\n\n🏷 **ad:** [{title[:35]}...]({url})\n⏱ **Müddət:** `{duration}`\n🎧 **tərəfindən sorğu:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except Exception as e:
            await lel.edit(
                "😕 **səsli söhbət tapılmadı**\n\n» zəhmət olmasa əvvəlcə səsli çatı aktiv edin"
            )
            return
        await lel.delete()
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Name:** [{title[:70]}]({url})\n⏱ **Müddət:** `{duration}`\n💡 **Vəziyyət:** `Oynanır`\n"
             + f"🎧 **Müraciət edən:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")


@Client.on_callback_query(filters.regex(pattern=r"plll"))
async def lol_cb(b, cb):
    
    bttn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Command Syntax", callback_data="cmdsyntax")
            ],[
                InlineKeyboardButton("🗑 Bağla", callback_data="close")
            ]
        ]
    )
    
    nofound = "😕 **xahiş etdiyiniz mahnını tapa bilmədiniz**\n\n» **düzgün mahnı adını və ya ifaçının adını da daxil edin**"
    
    global que
    cbd = cb.data.strip()
    chat_id = cb.message.chat.id
    typed_ = cbd.split(None, 1)[1]
    try:
        x, query, useer_id = typed_.split("|")
    except:
        await cb.message.reply_photo(
            photo=f"{CMD_IMG}",
            caption=nofound,
            reply_markup=bttn,
        )
        return
    useer_id = int(useer_id)
    if cb.from_user.id != useer_id:
        await cb.answer("💡 təəssüf ki, bu sizin üçün deyil !", show_alert=True)
        return
    await cb.answer("💡 İstədiyiniz mahnı endirilir...", show_alert=True)
    x = int(x)
    try:
        cb.message.reply_to_message.from_user.first_name
    except:
        cb.message.from_user.first_name
    results = YoutubeSearch(query, max_results=5).to_dict()
    resultss = results[x]["url_suffix"]
    title = results[x]["title"][:70]
    thumbnail = results[x]["thumbnails"][0]
    duration = results[x]["duration"]
    url = f"https://www.youtube.com{resultss}"
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await cb.message.edit(
                f"❌**müddəti** `{DURATION_LIMIT}` **dəqiqədən çox olan musiqi, ifa edilə bilməz!**"
            )
            return
    except:
        pass
    try:
        thumb_name = f"{title}.jpg"
        ctitle = cb.message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    except Exception as e:
        print(e)
        return
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Mᴇɴᴜ", callback_data="menu"),
                InlineKeyboardButton("• Cʟᴏsᴇ", callback_data="cls"),
            ],
            [InlineKeyboardButton("• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")],
        ]
    )
    await generate_cover(title, thumbnail, ctitle)
    file_path = await converter.convert(youtube.download(url))
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
            loc = file_path
            appendable = [s_name, r_by, loc]
            qeue.append(appendable)
            await cb.message.delete()
            await b.send_photo(
                chat_id,
                photo="final.png",
                caption=f"💡**Track növbəyə əlavə edildi »** `{position}`\n\n🏷 **Ad:** [{title[:35]}...]({url})\n⏱ **Müddət:** `{duration}`\n🎧 **tərəfindən sorğu:** {cb.from_user.mention}",
                reply_markup=keyboard,
            )
    else:
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        try:
            r_by = cb.message.reply_to_message.from_user
        except:
            r_by = cb.message.from_user
            loc = file_path
            appendable = [s_name, r_by, loc]
            qeue.append(appendable)
            await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
            await cb.message.delete()
            await b.send_photo(
                chat_id,
                photo="final.png",
                caption=f"🏷 **Ad:** [{title[:70]}]({url})\n⏱ **Müddət:** `{duration}`\n💡 **Vəziyyət:** `Oynanır`\n"
                 + f"🎧 **Müraciət edən:** {cb.from_user.mention}",
                reply_markup=keyboard,
            )
            if path.exists("final.png"):
                os.remove("final.png")


@Client.on_message(command(["ytplay", f"ytplay@{BOT_USERNAME}"]) & other_filters)
async def ytplay(_, message: Message):
    chat_id = get_chat_id(message.chat)
    bttn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Command Syntax", callback_data="cmdsyntax")
            ],[
                InlineKeyboardButton("🗑 Bağla", callback_data="close")
            ]
        ]
    )
    
    nofound = "😕 **istədiyiniz mahnını tapa bilmədim**\n\n» **düzgün mahnı adını və ya ifaçının adını da daxil edin**"
    
    global que
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("🔎 **axtarış...**")
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "music assistant"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                if message.chat.title.startswith("Channel Music: "):
                    await lel.edit(
                        f"💡 **zəhmət olmasa əvvəlcə istifadəçi robotunu kanalınıza əlavə edin**",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+","https://t.me/joinchat/")
                except:
                    await lel.edit(
                        "💡 **Məndən istifadə etmək üçün aşağıdakı icazələrə malik Administrator olmalıyam:\n\n» ❌ __Mesajları silin__\n» ❌ __İstifadəçiləri qadağan edin__\n» ❌ __İstifadəçiləri əlavə edin__\n» ❌ __Səsli söhbəti idarə edin__\n\n**  Sonra /reload** yazın",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await lel.edit(
                        f"✅ **userbot uğurla çata daxil oldu**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    # print(e)
                    await lel.edit(
                        f"🔴 **Food Gözləmə Xətası** 🔴 \n\n**userbot istifadəçi robotu üçün çoxsaylı qoşulma sorğularına görə bu qrupa qoşula bilmir.**"
                        f"\n\n**və ya @{ASSISTANT_NAME} adlı şəxsi bu qrupa əl ilə əlavə edin, sonra yenidən cəhd edin.**",
                    )
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"» **userbot bu çatda deyil və ya bu qrupda qadağan edilib !**\n\n**@{ASSISTANT_NAME} blokundan çıxarın və yenidən bu qrupa əl ilə əlavə edin və ya /reload yazın, sonra yenidən cəhd edin.**"
        )
        return

    query = ""
    for i in message.command[1:]:
        query += " " + str(i)
    print(query)
    await lel.edit("🔄 **vc-yə qoşulur...**")
    ydl_opts = {"format": "bestaudio/best"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:70]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        ctitle = message.chat.title
        ctitle = await CHAT_TITLE(ctitle)
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]

    except Exception as e:
        await lel.delete()
        await message.reply_photo(
            photo=f"{CMD_IMG}",
            caption=nofound,
            reply_markup=bttn,
        )
        print(str(e))
        return
    try:
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60
        if (dur / 60) > DURATION_LIMIT:
            await lel.edit(
                f"❌ **müddəti** `{DURATION_LIMIT}` **dəqiqədən çox olan musiqi, ifa etmək mümkün deyil!**"
            )
            return
    except:
        pass
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("• Mᴇɴᴜ", callback_data="menu"),
                InlineKeyboardButton("• Cʟᴏsᴇ", callback_data="cls"),
            ],
            [InlineKeyboardButton("• Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")],
        ]
    )
    await generate_cover(title, thumbnail, ctitle)
    file_path = await converter.convert(youtube.download(url))
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALLS.append(int(x.chat_id))
    if int(chat_id) in ACTV_CALLS:
        position = await queues.put(chat_id, file=file_path)
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        await lel.delete()
        await message.reply_photo(
            photo="final.png",
            caption=f"💡 **Trek növbəyə əlavə edildi »** `{position}`\n\n🏷 **Ad:** [{title[:35]}...]({url})\n⏱ **Müddət** `{duration}`\n🎧 **tərəfindən sorğu:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
    else:
        chat_id = get_chat_id(message.chat)
        que[chat_id] = []
        qeue = que.get(chat_id)
        s_name = title
        r_by = message.from_user
        loc = file_path
        appendable = [s_name, r_by, loc]
        qeue.append(appendable)
        try:
            await callsmusic.pytgcalls.join_group_call(
                chat_id, 
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
                stream_type=StreamType().local_stream,
            )
        except:
            await lel.edit(
                "😕 **səsli söhbət tapılmadı**\n\n» zəhmət olmasa əvvəlcə səsli çatı aktiv edin"
            )
            return
        await lel.delete()
        await message.reply_photo(
            photo="final.png",
            caption=f"🏷 **Ad:** [{title[:70]}]({url})\n⏱ **Müddət:** `{duration}`\n💡 **Vəziyyət:** `Oynanır`\n"
             + f"🎧 **Müraciət edən:** {message.from_user.mention}",
            reply_markup=keyboard,
        )
        os.remove("final.png")
