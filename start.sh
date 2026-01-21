#!binbash

echo 🔴 Shutting down old servers...
sudo pkill tailscaled
sudo pkill AdGuardHome
pkill filebrowser
pkill sshd
sleep 2

echo 🔑 Starting SSH Server...
sshd

echo 🚀 Starting Tailscale (The Pipe)...
# Assumes state file is in AdGuardHome folder
cd ~AdGuardHome
sudo tailscaled --tun=userspace-networking --state=tailscaled.state  devnull 2&1 &
sleep 5

echo 🛡️ Starting AdGuard Home (The Filter)...
sudo .AdGuardHome  devnull 2&1 &
sleep 2

echo ☁️ Starting File Browser (The Cloud)...
filebrowser -p 8080 -r sdcardMyCloud -a 0.0.0.0  devnull 2&1 &

echo ✅ ALL SYSTEMS ONLINE.
echo    - SSH       Active (Port 8022)
echo    - Tailscale Active
echo    - AdGuard   Active (Port 3000)
echo    - Cloud     Active (Port 8080)
echo 
echo Press CTRL+C to stop everything.

# Keep script running to hold processes
wait