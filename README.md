# youtube-dl and ffmpeg Windows Explorer Integration
Download videos from YouTube/Twitch/Twitter and more (any platform that is supported by youtube-dl) right in the Windows Explorer, without installing any shady shareware apps!

![Screenshot](https://user-images.githubusercontent.com/30384331/108196593-2ee3dd00-7111-11eb-955b-a2f3c29f58cc.png)

I made this script for myself, since I reference other YouTube videos and memes a lot in my own content and needed an easy way to download videos in an editing-friedly format (DNxHR 25 FPS in my case).

### Supported formats:
* Audio: MP3, WAV
* Video: MP4 H.264, MOV DNxHR

### How to use it
1. Right-click on "Raw" and save the file
2. Double-click on the .reg file and confirm adding the keys to the registry
3. Copy the video link, go to the folder where you want to download it
4. Right click on the empty space and choose your option
5. Voilà!

This script requires **youtube-dl** and **ffmpeg**.
**To install youtube-dl and ffmpeg:**

Open a PowerShell as Administrator and run:
```
Set-ExecutionPolicy Bypass -Scope Process
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install youtube-dl ffmpeg
```
