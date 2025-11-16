from dotenv import load_dotenv
import os

print("🔍 Загружаем переменные из .env...")
load_dotenv()

token = os.getenv("BOT_TOKEN")
channel = os.getenv("CHANNEL_ID")

print()
if token:
    print("✅ BOT_TOKEN: загружен (последние 5 символов):", token[-5:])
else:
    print("❌ BOT_TOKEN: НЕ НАЙДЕН! Проверь .env и путь к нему.")
    
if channel:
    print("✅ CHANNEL_ID:", channel)
else:
    print("❌ CHANNEL_ID: не задан")
    
print("\n💡 Готово! Теперь можно запускать бота.")
