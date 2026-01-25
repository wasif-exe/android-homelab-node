import telebot
import subprocess
import time
import threading
import os

API_TOKEN = 'YOUR_NEW_TOKEN_HERE'
ALLOWED_USERNAME = 'wasif_exe'

bot = telebot.TeleBot(API_TOKEN)
REBOOT_FLAG_FILE = "reboot_memory.txt"

target_chat_id = None
last_alert_level = 100

def get_raw_stats():
    try:
        cmd_bat = subprocess.run(['sudo', 'cat', '/sys/class/power_supply/battery/capacity'], stdout=subprocess.PIPE)
        bat = int(cmd_bat.stdout.decode('utf-8').strip())
        
        cmd_temp = subprocess.run(['sudo', 'cat', '/sys/class/power_supply/battery/temp'], stdout=subprocess.PIPE)
        temp = int(cmd_temp.stdout.decode('utf-8').strip()) / 10
        return bat, temp
    except:
        return None, None

def is_authorized(message):
    if message.from_user.username and message.from_user.username.lower() == ALLOWED_USERNAME.lower():
        return True
    return False

def battery_monitor_loop():
    global last_alert_level
    while True:
        if target_chat_id:
            bat, temp = get_raw_stats()
            if bat is not None:
                if bat <= 10 and last_alert_level > 10:
                    bot.send_message(target_chat_id, f"⚠️ **Low Battery: {bat}%**", parse_mode="Markdown")
                    last_alert_level = 10
                elif bat <= 5 and last_alert_level > 5:
                    bot.send_message(target_chat_id, f"🚨 **CRITICAL BATTERY: {bat}%**", parse_mode="Markdown")
                    last_alert_level = 5
                
                if bat > 80: last_alert_level = 100
        time.sleep(60)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_authorized(message): return
    global target_chat_id
    target_chat_id = message.chat.id
    bot.reply_to(message, "🤖 **Guardian Ready.**\nI'll alert you if battery drops.\n/status | /reboot")

@bot.message_handler(commands=['status'])
def send_status(message):
    if not is_authorized(message): return
    bat, temp = get_raw_stats()
    if bat:
        bot.reply_to(message, f"📊 **Status**\n🔋 Battery: {bat}%\n🔥 Temp: {temp}°C", parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ Sensor Error")

@bot.message_handler(commands=['reboot'])
def reboot_system(message):
    if not is_authorized(message): return
    
    bot.reply_to(message, "♻️ Rebooting... Your SSH will disconnect now.")
    
    with open(REBOOT_FLAG_FILE, "w") as f:
        f.write(str(message.chat.id))
        
    import os
    home_dir = os.path.expanduser("~")
    script_path = os.path.join(home_dir, "start.sh")
    
    subprocess.Popen(f"bash {script_path}", shell=True)

monitor_thread = threading.Thread(target=battery_monitor_loop)
monitor_thread.daemon = True
monitor_thread.start()

if os.path.exists(REBOOT_FLAG_FILE):
    try:
        with open(REBOOT_FLAG_FILE, "r") as f:
            chat_id = f.read().strip()
        
        bot.send_message(chat_id, "✅ **System Online.**\nReboot successful.", parse_mode="Markdown")
        
        target_chat_id = chat_id
        
        os.remove(REBOOT_FLAG_FILE)
    except:
        pass

print("🤖 Bot is listening...")
bot.infinity_polling()
