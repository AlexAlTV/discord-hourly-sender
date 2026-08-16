import discord
import os
import sys

USER_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

if not USER_TOKEN or not CHANNEL_ID:
    print("Ошибка: не заданы переменные окружения DISCORD_TOKEN и CHANNEL_ID")
    sys.exit(1)

class SelfBot(discord.Client):
    async def on_ready(self):
        print(f"Бот запущен как {self.user}")
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print(f"Канал с ID {CHANNEL_ID} не найден")
            await self.close()
            return

        msg = (
            "╔⚔️[MyPvE] CLAN ⚔️\n"
            " | ⚔️ Requirement: {1k Gold|2k silver| plat or dim bypass } (DM to check)\n"
            " | ⬆️ Clan Level: 5\n"
            " | 🍀 Upgrades: BP XP 50| Shop 3 lvl\n"
            " | 🚫 Low Requirements\n"
            " ╰ 📥 DM <@1212260703424217160>   or me to apply now!"
        )
        await channel.send(msg)
        print("Сообщение отправлено")
        await self.close()

client = SelfBot()
client.run(USER_TOKEN)
