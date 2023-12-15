from telethon.sync import TelegramClient, events
import time, json
import asyncio, aiofiles
import aiosqlite, random
import logging, datetime
import os

if not os.path.exists('logs'):
    os.makedirs('logs')

log_format = '%(asctime)s - %(levelname)s %(message)s'

today = datetime.date.today()
day = today.day
month = today.month
year = today.year
logging.basicConfig(filename=f'logs/{year}-{day}-{month}-main.log', level=logging.INFO, format=log_format)

enable = False
last_event = time.time()
last_messages = dict()
delay = 0
delay_messages = [5, 10]


async def getData():
    while True:
        try:
            async with aiosqlite.connect('ChatsAndAccounts.db') as conn:
                cursor = await conn.cursor()
                await cursor.execute("SELECT * FROM ChatsAndAccounts")
                rows = await cursor.fetchall()
                return rows
        except:
            await asyncio.sleep(0.5)


async def updateData(id, new_data):
    while True:
        try:
            async with aiosqlite.connect('ChatsAndAccounts.db') as conn:
                cursor = await conn.cursor()
                await cursor.execute("UPDATE ChatsAndAccounts SET data = ? WHERE account_id = ?",
                                     (new_data, id))
                await conn.commit()
                break
        except Exception as error:
            logging.error(error)
            await asyncio.sleep(0.5)

def check (e):
    return e.mentioned or e.is_private

async def runClient(client, number, delay):
    await client.start(phone=str(number))

    timeLocal = dict()

    rows = await getData()
    for row in rows:
        for _ in row[1].split(","):
            second = _.split(":")
            chat_id = second[0]
            if chat_id[0] == '-' or chat_id[0].isdigit():
                chat_id = int(chat_id)
            timeEvent = float(second[1])
            timeLocal[chat_id] = timeEvent

    async with aiofiles.open('config.json', 'r') as file_data:
        data = await file_data.read()
    data = json.loads(data)
    message = data['message']
    answer = data['answer']

    chat_ids = []
    for _ in data['accounts']:
        for i in data['accounts'][_].split(','):
            cur = i.split(':')
            chat_ids.append(cur[0])

    @client.on(events.NewMessage(incoming=True, func=check)) 
    async def handler(event):
        #if str(event.chat_id) in chat_ids:
        await event.reply(answer)
        if enable:
            logging.info(f'Account {number} answered to {event.chat_id}')

    @client.on(events.Raw)
    async def handler(update):
        if time.time() < delay + 1.:
            return
        global last_event
        if time.time() < last_event + 2:
            return
        else:
            last_event = time.time()
        global last_messages
        if time.time() < last_messages[number]:
            return
        global enable
        exist = False
        for _ in timeLocal:
            if timeLocal[_] < time.time():
                exist = True
                break
        if exist == False:
            return
        global delay_messages
        user = await client.get_me()
        rows = await getData()

        for row in rows:
            account = row[0].split(":")
            num = account[2]
            if num != number:
                continue
            new_data = ""
            old_data = row[1]

            for chat_info in row[1].split(","):
                second = chat_info.split(":")
                chat_id = second[0]
                if chat_id[0] == '-' or chat_id[0].isdigit():
                    chat_id = int(chat_id)

                timeEvent = float(second[1])
                period = int(second[2])
                curTime = time.time()
                if curTime > timeEvent + 5 and curTime > timeLocal[chat_id] + 5 and curTime > last_messages[number]:
                    timeLocal[chat_id] = curTime + period
                    try:
                        await client.send_message(chat_id, message)
                        if enable:
                            logging.info(f'Account {number} sent message to {chat_id}')
                        last_messages[number] = time.time() + float(random.randint(delay_messages[0], delay_messages[1]))
                    except Exception as error:
                        if enable:
                            logging.error(f'Account {number} error {error}')

                    new_data += f"{chat_id}:{time.time() + period + float(random.randint(delay_messages[0], delay_messages[1]))}:{period},"
                else:
                    new_data += f"{chat_info},"
            new_data = new_data[:-1]
            if new_data != old_data:
                await updateData(row[0], new_data)

    await client.run_until_disconnected()


async def initiate():
    async with aiofiles.open('config.json', 'r') as file_data:
        data = await file_data.read()
    data = json.loads(data)
    global enable
    global delay
    global delay_messages
    global last_messages
    if data['logging']['enable'] == 'true':
        enable = True
    delay = int(data['delay_messages']['delay_between_accounts'])
    delay_messages = data['delay_messages']['delay_between_messages']
    async with aiosqlite.connect('ChatsAndAccounts.db') as conn:
        cursor = await conn.cursor()

        await cursor.execute('''
                        CREATE TABLE IF NOT EXISTS ChatsAndAccounts (
                            account_id TEXT PRIMARY KEY,
                            data TEXT
                        )
                    ''')
        await conn.commit()

        rows = await getData()

        await cursor.execute("DELETE FROM ChatsAndAccounts")
        await conn.commit()
        ti = dict()
        for row in rows:
            for _ in row[1].split(','):
                obj = _.split(':')
                ti[obj[0]] = obj[1]

        for _ in data['accounts']:
            data_time = ""
            for i in data['accounts'][_].split(','):
                cur = i.split(':')
                t = time.time() + float(random.randint(delay_messages[0], delay_messages[1]))
                chat_id = cur[0]
                if cur[0] in ti:
                    if float(ti[cur[0]]) > t:
                        t = ti[cur[0]]
                data_time += f"{chat_id}:{float(t)}:{cur[1]},"
            data_time = data_time[:-1]
            await cursor.execute("INSERT INTO ChatsAndAccounts (account_id, data) VALUES (?, ?)",
                                 (_, data_time))

            await conn.commit()


async def main():
    await initiate()
    rows = await getData()
    global delay
    coroutine = []
    i = 0
    for row in rows:
        account = row[0].split(":")
        id = int(account[0])
        hash = account[1]
        number = account[2]
        last_messages[number] = time.time() + float(random.randint(delay_messages[0], delay_messages[1]))
        coroutine.append(runClient(TelegramClient(f'user{i}', id, hash), number, time.time() + delay * (i + 1)))
        i += 1
    await asyncio.gather(*coroutine)


if __name__ == "__main__":
    asyncio.run(main())
