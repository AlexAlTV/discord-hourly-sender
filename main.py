import discord
import asyncio
import os
import sys
from datetime import datetime

USER_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

if not USER_TOKEN or not CHANNEL_ID:
    print("Ошибка: не заданы переменные окружения DISCORD_TOKEN и CHANNEL_ID")
    sys.exit(1)

class SelfBot(discord.Client):
    async def on_ready(self):
        print(f"✅ Запущен как {self.user}")
        self.loop.create_task(self.hourly_sender())

    async def hourly_sender(self):
        await self.wait_until_ready()
        channel = self.get_channel(CHANNEL_ID)
        if channel is None:
            print("❌ Канал не найден!")
            return

        target_minute = 24  # <--- ОТПРАВКА В 24 МИНУТУ КАЖДОГО ЧАСА

        while not self.is_closed():
            now = datetime.now()
            # Вычисляем, сколько секунд до следующей 24-й минуты
            if now.minute < target_minute:
                seconds_until_target = (target_minute - now.minute) * 60 - now.second
            elif now.minute > target_minute:
                seconds_until_target = (60 - now.minute + target_minute) * 60 - now.second
            else:
                # Если сейчас ровно 24 минуты, то ждём 1 час
                seconds_until_target = 3600 - now.second
                if seconds_until_target == 0:
                    seconds_until_target = 3600

            await asyncio.sleep(seconds_until_target)

            msg = (
                "╔⚔️[MyPvE] CLAN ⚔️\n"
                " | ⚔️ Requirement: {1k Gold|2k silver| plat or dim bypass } (DM to check)\n"
                " | ⬆️ Clan Level: 5\n"
                " | 🍀 Upgrades: BP XP 50| Shop 3 lvl\n"
                " | 🚫 Low Requirements\n"
                " ╰ 📥 DM <@1212260703424217160>   or me to apply now!"
            )
            try:
                await channel.send(msg)
                print(f"✅ Отправлено в {datetime.now().strftime('%H:%M:%S')}")
            except discord.errors.HTTPException as e:
                if e.status == 429:
                    retry_after = e.retry_after
                    print(f"⏳ Rate limit {retry_after:.0f} сек, ждём...")
                    await asyncio.sleep(retry_after + 2)
                    try:
                        await channel.send(msg)
                        print(f"✅ Отправлено после ожидания в {datetime.now().strftime('%H:%M:%S')}")
                    except Exception as e2:
                        print(f"❌ Ошибка при повторной отправке: {e2}")
                else:
                    print(f"❌ Ошибка: {e.status} - {e.text}")
            except Exception as e:
                print(f"❌ Неизвестная ошибка: {e}")

client = SelfBot()
client.run(USER_TOKEN)
