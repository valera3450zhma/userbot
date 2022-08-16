import random

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from contextlib import suppress
import re

from time import sleep

# сюда встав коди
import res

app = Client("my_account", api_id=876100, api_hash="ab03c3758ababdad2d8859e08244ae40")

# константи
nickname = res.nickname
# -1001564474914 - тестовий канал, -1001191692234 - ше один тестовий канал, -1001180084919 - петя
listen_to = res.listen_to  # по ідеї можна вказати тег, наприклад "mcpetya_slivy"
forward_to = res.forward_to
random_bot = res.random_bot
soledar = res.soledar
clan = res.clan
mc_petya_chat = res.mc_petya_chat
mc_petya_channel = res.mc_petya_channel

# назви дропів
drop = ["пил і гнилі недоїдки", "класове спорядження", "дрин і щит", "пошкоджений уламок бронетехніки",
        "🛡 Уламок", "50 гривень", "ящиком горілки", "мертвий русак", "Мухомор королівський", "упаковок фольги",
        "Крім гаманця", "ручний протитанковий", "неушкоджений Бронежилет", "парадна форма"]

# назви дропів для виведення стати
drop_texts = ["⚪ Пил і гнилі недоїдки", "⚪ Класове спорядження", "⚪ Дрин і щит", "⚪ Уламок", "⚪ Цілий уламок",
              "🔵 50 гривень", "🔵 Ящик горілки", "🔵 Мертвий русак", "🟣 Мухомор королівський", "🟣 Шапочка",
              "🟣 Їжа", "🟡 РПГ-7", "🟡 Бронік Вагнерівця", "🟡 Погон"]

petya_texts = res.petya_texts


# репости мц педі
@app.on_message(filters.chat(int(mc_petya_chat)))
def mc_petya(_, message):
    chat_id = message.chat.id
    if message.sender_chat is not None and message.sender_chat.id == int(mc_petya_channel):
        app.send_message(chat_id, random.choice(petya_texts), reply_to_message_id=message.id)


@app.on_edited_message(filters.chat(listen_to))
def mc_petya(_, message):
    app.forward_messages(forward_to, listen_to, message.id, disable_notification=True)


@app.on_message(filters.command("info", "!") & filters.me)
def info(_, message):
    app.send_message(message.chat.id, message.reply_to_message)


@app.on_message(filters.command("mcpetya", "!"))
def info(_, message):
    app.send_message(message.chat.id, random.choice(petya_texts))


@app.on_message(filters.command("get_user", "!") & filters.me)
def get_user(_, message):
    app.send_message(message.chat.id, app.get_users(message.reply_to_message.text))


@app.on_message(filters.command("get_chat", "!") & filters.me)
def get_user(_, message):
    app.send_message(message.chat.id, app.get_chat(message.reply_to_message.text))


# кидання боїв
@app.on_message(filters.command("rusak", "!"))
def rusak_battle(_, message):
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.id)
    splited = message.text.split(" ")
    # якшо повідомлення від себе
    if len(splited) == 2 and message.from_user.username == nickname:
        fight(_, int(splited[1]), message)
    # якшо від іншого чела
    elif len(splited) == 3:
        # якшо звертаються до тебе
        if splited[1] == nickname:
            fight(_, int(splited[2]), message)


# хавка
@app.on_message(filters.command("feed", "!") & filters.me)
def rusak_feed(_, message):
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.id)
    app.send_message(chat_id, "/feed")
    app.send_message(soledar, "/mine")
    app.send_message(chat_id, "/swap")
    app.send_message(chat_id, "/feed")
    app.send_message(soledar, "/mine")
    app.send_message(chat_id, "/swap")
    app.send_message(chat_id, "/woman")


# БД
@app.on_message(filters.command("bd", "!") & filters.me)
def rusak_bd(_, message):
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.id)
    sent = app.send_message(random_bot, "/rusak")
    sleep(1)
    bd_message = get_message(random_bot, sent.id + 1)
    remaining_bd = 10000 - int(bd_message.caption.split()[15])
    times = int(remaining_bd / 300)
    if times <= 0:
        return
    app.send_message(random_bot, f"Жди {times} сек")
    sent = app.send_message(random_bot, "/shop")
    sleep(1)
    shop_message = get_message(random_bot, sent.id + 1)
    for i in range(times):
        shop_message.click(0, timeout=1)
    app.send_message(chat_id, "/rusak")


# Нагадування про роботу
@app.on_message(filters.command("workers", "!") & filters.me)
def rusak_workers(_, message):
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.id)
    sent = app.send_message(random_bot, "/clan_settings")
    sleep(1)
    settings_message = get_message(random_bot, sent.id + 1)
    with suppress(TimeoutError):
        settings_message.click(6, timeout=1)
    sleep(1)
    with suppress(TimeoutError):
        get_message(random_bot, settings_message.id + 1).click(0, timeout=1)
    workers_message = get_message(random_bot, settings_message.id + 1)
    workers_split = workers_message.text.split("\n")
    lazy_users_ids = []
    for i in range(len(workers_split)):
        if "🟥" in workers_split[i]:
            user_id = int(re.findall("\\b\\d+", workers_split[i])[0])
            lazy_users_ids.append(user_id)
    if len(lazy_users_ids) == 0:
        app.send_message(chat_id, "Сьогодні всі відпрацювали зміну")
        return
    lazy_users = []
    for id in lazy_users_ids:
        try:
            lazy_users.append(app.get_users(id))
        except:
            pass
    main_cycles = int(len(lazy_users) / 3)
    adjust_cycle = int(len(lazy_users) % 3)
    messages_texts = []
    for i in range(main_cycles):
        text = "Не працювали:\n\n"
        for k in range(3):
            text += "@" + lazy_users[0].username + "\n"
            lazy_users.pop(0)
        text += "\n/work"
        messages_texts.append(text)
    if adjust_cycle > 0:
        text = "Не працювали:\n\n"
        for k in range(adjust_cycle):
            text += "@" + lazy_users[0].username + "\n"
            lazy_users.pop(0)
        text += "\n/work"
        messages_texts.append(text)
    for message_text in messages_texts:
        app.send_message(chat_id, message_text)


@app.on_message(filters.command("heal", "!"))
def buy_heal(_, message):
    chat_id = message.chat.id
    app.send_message(chat_id, "чекаю хп в боті")
    sent = app.send_message(random_bot, "/rusak")
    sleep(2)
    health_message = get_message(random_bot, sent.id + 1)
    health = int(health_message.caption.split()[18])
    if health < 30:
        app.send_message(chat_id, "треба аптечку")
        sent = app.send_message(random_bot, "/shop")
        sleep(2)
        bot_shop = get_message(random_bot, sent.id + 1)
        bot_shop.click(3)
        app.send_message(chat_id, "купив аптечку")
    else:
        app.send_message(chat_id, "норм, жити можна")


@app.on_message(filters.command("click", "!") & filters.me)
def click_buttons(_, message):
    chat_id = message.chat.id
    app.delete_messages(chat_id, message.id)
    splited = message.text.split(" ")
    times = int(splited[1])
    start_message_id = message.reply_to_message.id
    buy_heal(_, message)
    click(_, start_message_id, times, chat_id)


# auto-battle
@app.on_message(filters.regex(re.compile(r'^.+?Починається.+?битва.+?$')))
def auto_battle(_, message):
    if "міжчатова" not in message.text:
        sleep(random.randint(10, 50))
    elif "міжчатова" in message.text and message.chat.id != int(clan):
        return
    try:
        message.click(0, timeout=3)
    except TimeoutError:
        pass


# auto-send-battle
@app.on_message(filters.regex(re.compile(r'^Міжчатова.+?завершена!.+?$')))
def auto_battle(_, message):
    chat_id = message.chat.id
    if chat_id == int(clan):
        app.send_message(chat_id, "/war")


@app.on_message(filters.command("info", "!"))
def info(_, message):
    app.send_message(message.chat.id, message.reply_to_message)


@app.on_message(filters.command("guide", "!"))
def guide(_, message):
    text = "гайд по командах\n\n\n!rusak *число* - надсилає *число* боїв\n\n" \
           "!rusak *нікнейм* *число* - надсилає від імені *нікнейм* *чило* боїв\n\n" \
           "!heal - хілить\n\n" \
           "!click *число* - тільки для того хто надсилає команду, реплайнувши на повідомлення, починає клікати" \
           "по *число* повідомлень починаючи з реплайнутого\n\n" \
           "!ebash, !cluck - да.\n\n" \
           "!packs *число* - відкриває *число* паків"
    app.send_message(message.chat.id, text)


@app.on_message(filters.command("ebash", "!"))
def ebash(_, message):
    chat_id = message.chat.id
    if chat_id != -751052700:
        return
    splited = message.text.split(" ")
    times = 30
    target = splited[1]
    if target != nickname:
        return
    fight(_, times, message)
    text = f"!cluck {message.from_user.username}"
    sent = app.send_message(chat_id, "получаю ід повідомлення")
    to_reply = get_message(chat_id, sent.id - 1).id
    app.send_message(chat_id, text, reply_to_message_id=to_reply)


@app.on_message(filters.command("cluck", "!"))
def force_click(_, message):
    chat_id = message.chat.id
    if chat_id != -751052700:
        return
    splited = message.text.split(" ")
    times = 30
    target = splited[1]
    if target != nickname:
        return
    start_message_id = message.reply_to_message.id
    buy_heal(_, message)
    click(_, start_message_id, times, chat_id)
    app.send_message(chat_id, "наклікався")
    sleep(5)
    fight(_, times, message)
    text = f"!cluck {message.from_user.username}"
    sent = app.send_message(chat_id, "получаю ід повідомлення")
    to_reply = get_message(chat_id, sent.id - 1).id
    app.send_message(chat_id, text, reply_to_message_id=to_reply)


@app.on_message(filters.command("packs", "!"))
def analyze(_, message):
    pack_price = 20
    chat_id = message.chat.id
    # якшо запущено в чаті, відмінному від чату з ботом
    if chat_id != 1466731329:
        app.send_message(chat_id, "всі дивіться, я дебіл")
        return
    splited = message.text.split(" ")
    packs = int(splited[1])
    sent = app.send_message(random_bot, "/shop")
    sleep(1)
    money_message = get_message(random_bot, sent.id + 1)
    money = int(money_message.text.split()[2])
    to_spend = packs * pack_price
    if to_spend > money * 0.95 or packs <= 0:
        app.send_message(chat_id, "далбайоб, йди заробляй")
        return
    main_commands = int(packs / 30)
    adjust_commands = packs % 30
    app.send_message(chat_id, f"Буде відкрито {packs} паки/-ів, "
                              f"тобто буде надіслано 30*{main_commands} команд, "
                              f"та {adjust_commands} команд для довершення")
    sleep(3)
    messages_to_forward = []
    start = 511585
    received_drops = []
    for i in range(len(drop)):
        received_drops.append(0)
    for i in range(30 if main_commands != 0 else 0):
        messages_to_forward.append(start)
        start -= 1

    open_packs(_, chat_id, main_commands, messages_to_forward, received_drops)

    start = 511585
    messages_to_forward = []
    for i in range(adjust_commands):
        messages_to_forward.append(start)
        start -= 1

    do_open_packs(_, chat_id, adjust_commands, messages_to_forward, received_drops)

    stats = f"Статистика по відкриттю {packs} паків\n"
    for i in range(len(drop)):
        stats += f"{drop_texts[i]} - {received_drops[i]}\n"
    app.send_message(chat_id, stats)


def open_packs(_, chat_id, commands, messages_to_forward, received_drops):
    for i in range(commands):
        app.forward_messages(chat_id, -786803186, messages_to_forward)
        sleep(5)
        pack_id = app.send_message(chat_id, "получаю ід повідомлення").id - 1
        click(_, pack_id, 30, chat_id)
        for j in range(pack_id - 30, pack_id + 1):
            msg = get_message(chat_id, j)
            for k in range(len(drop)):
                if drop[k] in msg.text:
                    received_drops[k] = received_drops[k] + 1
        app.send_message("Random_UAbot", "/feed")


def do_open_packs(_, chat_id, commands, messages_to_forward, received_drops):
    for i in range(1 if commands != 0 else 0):
        app.forward_messages(chat_id, -786803186, messages_to_forward)
        sleep(5)
        pack_id = app.send_message(chat_id, "получаю ід повідомлення").id - 1
        click(_, pack_id, commands, chat_id)
        for j in range(pack_id - commands, pack_id + 1):
            msg = get_message(chat_id, j)
            for k in range(len(drop)):
                if drop[k] in msg.text:
                    received_drops[k] = received_drops[k] + 1
        app.send_message("Random_UAbot", "/feed")


def fight(_, times, message):
    chat_id = message.chat.id
    # нормалізуєм кількість боїв
    if times < 1:
        app.send_message(chat_id, "мало, ставлю 1")
        times = 1
    elif times > 30:
        app.send_message(chat_id, "задофіга, ставлю 30")
        times = 30
    for i in range(times):
        try:
            if i == 0:
                buy_heal(_, message)
            inline_results = app.get_inline_bot_results("Random_UAbot")
            app.send_inline_bot_result(chat_id, inline_results.query_id, inline_results.results[0].id)
            sleep(0.5)
        except FloodWait as e:
            sleep(e.value)
    app.send_message(chat_id, "кінчив")


def click(_, start_message_id, times, chat_id):
    if times > 30:
        app.send_message(chat_id, "задофіга, ставлю 30")
        times = 30
    elif times < 1:
        app.send_message(chat_id, "дурачок? буде 1")
        times = 1
    for i in range(start_message_id - times, start_message_id + 1):
        message_to_click = app.get_messages(chat_id, i)
        try:
            message_to_click.click(0, timeout=1)
        except TimeoutError as e:  # skip timeout
            pass
        except ValueError as e:  # skip non-battle messages
            pass


def get_message(chat_id, sent_id):
    message = app.get_messages(chat_id, sent_id)
    if message.empty:
        get_message(chat_id, sent_id)
    return message


app.run()
