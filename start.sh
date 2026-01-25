#!/bin/bash

echo "🔴 Shutting down old services..."
sudo pkill tailscaled
sudo pkill AdGuardHome
pkill filebrowser
pkill -f dashboard.py
pkill -f bot.py
sleep 2

pkill sshd
sshd

echo "🚀 Starting Tailscale..."
cd ~/AdGuardHome
sudo tailscaled --tun=userspace-networking --state=tailscaled.state > /dev/null 2>&1 &
sleep 5

echo "🛡️ Starting AdGuard Home..."
sudo ./AdGuardHome > /dev/null 2>&1 &
sleep 2

echo "☁️ Starting File Browser..."
filebrowser -p 8080 -r /sdcard/MyCloud -a 0.0.0.0 > /dev/null 2>&1 &
sleep 2

echo "📊 Starting Dashboard & Bot..."
cd ~
nohup python dashboard.py > /dev/null 2>&1 &
nohup python bot.py > /dev/null 2>&1 &
sleep 2

echo " "
echo "✅ SYSTEM ONLINE"
echo "---------------------------------"
echo "   - Tailscale:   Active"
echo "   - AdGuard:     Port 3000"
echo "   - Cloud:       Port 8080"
echo "   - Dashboard:   Port 5000"
echo "   - Telegram:    Listening"
echo "---------------------------------"
