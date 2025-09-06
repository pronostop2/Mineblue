import asyncio
import random
from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode

TOKEN = "7567457205:AAGkKhTseqlzRD08O_bpH6v574qzR3dmppw"
CHANNEL_ID = "@mines1winpredictor"

MESSAGES_TO_FORWARD = [
    {"from_chat_id": "@mines1winpredictor", "message_id": 2},
]

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def home():
    return {"status": "Bot running"}
    
def generate_grid():
    grid_size = 5
    total_stars = 6 if random.randint(1, 5) != 5 else 5
    grid = [["⬛" for _ in range(grid_size)] for _ in range(grid_size)]
    positions = random.sample(range(grid_size * grid_size), total_stars)
    for pos in positions:
        row, col = divmod(pos, grid_size)
        grid[row][col] = "💠"
    return "\n".join("".join(row) for row in grid)


async def send_signals():
    while True:
        try:
            await bot.send_message(CHANNEL_ID, "🚨 <i>Recherche de nouveau signal...</i>")
            await asyncio.sleep(random.randint(20, 30))
            grid = generate_grid()
            message = (
                "💠 SIGNAL MINES\n"
                "<i>Valide pendant 3min ......</i>\n"
                "Piège : 3 💣\n\n"
                f"{grid}\n\n"
                "👉 <a href=\"https://1wyvrz.life/v3/2158/1win-mines?p=qn1x\">Joue ici !</a>\n"
                "❓ <a href=\"https://t.me/c/2183428707/285\">Comment jouer ?</a>"
            )
            signal_message = await bot.send_message(CHANNEL_ID, message)
            await asyncio.sleep(5)
            await bot.send_message(CHANNEL_ID, "👉 <i>Jouer avant 3min...</i> ✅")
            await asyncio.sleep(160)
            await bot.send_message(CHANNEL_ID, random.choice(["✅✅✅ <i>VALIDÉ....</i> ✅✅✅💰", "✅✅✅ GREENNNNNN!!! ✅✅✅"]),
                                   reply_to_message_id=signal_message.message_id)
            sticker_id = random.choice([
                "CAACAgEAAxkBAAEPUVVou9rU2_6UHHrJ5HiuO4SEmPKPQwACLgYAApAfGEU5Y7UCSDN-aDYE",
                "CAACAgEAAxkBAAEPUVdou9rXVnYmVr1XCOjwAAH1LjqHrIwAAsoEAAIUOhlFaMm1ueUnroE2BA",
                "CAACAgIAAxkBAAEPUWNou95VmLsudbR13KHkl07BzJVPQQACdQ8AAh4V8UuN549XMF_AnzYE",
                "CAACAgEAAxkBAAEPUVtou9rtqoWHnQHFGXJIbT60trfh5AACgAYAApEXGUX_cemgOUuieTYE"
            ])
            await bot.send_sticker(CHANNEL_ID, sticker_id)
            await asyncio.sleep(random.randint(2, 5))
        except Exception as e:
            print(f"Erreur lors de l'envoi du signal : {e}")


async def forward_scheduled_messages():
    while True:
        for ref in MESSAGES_TO_FORWARD:
            try:
                await bot.forward_message(chat_id=CHANNEL_ID, from_chat_id=ref["from_chat_id"], message_id=ref["message_id"])
            except Exception as e:
                print(f"Erreur lors du transfert du message {ref}: {e}")
            await asyncio.sleep(480)
        await asyncio.sleep(400)


async def main():
    try:
        await asyncio.gather(
            send_signals(),
            forward_scheduled_messages()
)
    except Exception as e:
            print(f"Erreur dans la boucle principale : {e}")
            await asyncio.sleep(10)  # attendre avant de relancer


        
        # asyncio.create_task(send_signals())
        # asyncio.create_task(forward_scheduled_messages())
        # await dp.start_polling(bot)
    # except Exception as e:
    #     print(f"Erreur dans la boucle principale : {e}")

# Lancer le bot en arrière-plan
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(main())

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Erreur fatale : {e}")

