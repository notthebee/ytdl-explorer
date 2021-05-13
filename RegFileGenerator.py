from textwrap import dedent
import os
from string import ascii_lowercase

class RegGenerator():
    def __init__(self):
        self.types = {
            "h264": {'options': '', 'icon': 18, 'subformats':True, 'name': 'Download video (H.264)'},
            "dnxhr": {'options': '--format=bestvideo+bestaudio --exec=\'ffmpeg -i {} -c:v dnxhd -profile:v dnxhr_lb -vf fps=25/1,format=yuv422p -c:a pcm_s16le {}.mov & del {}\'', 'icon': 41, 'subformats': False, 'name': 'Download video (DNxHR 25 FPS)'},
            "mp3": {'options': '--continue -f bestaudio -x --audio-format mp3', 'icon': 103, 'subformats': False, 'name': 'Download audio (MP3)'},
            "wav": {'options': '--continue -f bestaudio -x --audio-format wav', 'icon': 80, 'subformats': False, 'name': 'Download audio (WAV)'},
            "playlist": {'options': '--yes-playlist -o \'%%(playlist)s/%%(playlist_index)s - %%(title)s.%%(ext)s\' -i --continue --format=bestvideo+bestaudio[ext=m4a]/best --merge-output-format=mp4', 'icon': 97, 'subformats': False, 'name': 'Download playlist (H.264)'},
            "playlist_mp3": {'options': '--yes-playlist -o \'%%(playlist)s/%%(playlist_index)s - %%(title)s.%%(ext)s\' -i --continue --format=bestaudio -x --audio-format mp3', 'icon': 128, 'subformats': False, 'name': 'Download playlist (MP3)'},
        }
        self.reg_common = "HKEY_CLASSES_ROOT\Directory\Background\shell\YoutubeDL"
        self.command_common = \
        """
        @="powershell.exe -Command
        \\"$latest = Invoke-WebRequest -Uri https://github.com/ytdl-org/youtube-dl/releases/latest -Method get -MaximumRedirection 0 -UseBasicParsing -ErrorAction Ignore;
        $latest = ($latest.headers.location -split '/')[-1];
        $current = youtube-dl --version; if($current -ne $latest) { Write-Output 'Youtube-DL needs to be updated. Please grant the administrator privileges in the next dialog.';
        Start-Sleep -s 5;
        start-process powershell.exe '-Command Write-Host \\"Please wait while youtube-dl is being updated. The process might take a couple of minutes depending on your Internet connection. This is a one-time process\\";
        youtube-dl -U' -Verb RunAs -Wait};
        youtube-dl $(Get-Clipboard) 
        --continue
        --no-check-certificate
        """
        self.command_common = " ".join(self.command_common.split())
        self.command_common_end = '\\""'
        self.start = \
        """
        Windows Registry Editor Version 5.00
        ; Youtube downloader context menu
        ; by notthebee

        ; Deleting the previous version
        [-{reg_common}]


        [{reg_common}]
        "MUIVerb"="youtube-dl"
        "SubCommands"=""

        [{reg_common}\shell]

        """.format(reg_common = self.reg_common)
        self.start = dedent(self.start)

    def gen_all(self):
        types_string = ""
        count = 0
        for type, subtypes in self.types.items():
            reg_root_dir = "[{reg_common}\shell\{alpha_type}_{type}]".format(reg_common = self.reg_common, alpha_type = ascii_lowercase[count], type = type)
            if subtypes['subformats']:
                    at = '"MUIVerb"'
                    subcommands = '"SubCommands"=""'
                    reg_root_dir_command = reg_root_dir[:-1] + "\shell]"

                    subformats = \
                    """
                    [{rrdc}\\a_best]
                    @="Best quality"

                    [{rrdc}\\a_best\\command]
                    {command_common} --format=bestvideo+bestaudio[ext=m4a]/best --merge-output-format=mp4 {command_end}

                    [{rrdc}\\b_1080p]
                    @="1080p"

                    [{rrdc}\\b_1080p\\command]
                    {command_common} --format=bestvideo[height<=1080]+bestaudio[ext=m4a]/best --merge-output-format=mp4 -o '%%(title)s_1080.%%(ext)s' {command_end}

                    [{rrdc}\\c_720p]
                    @="720p"

                    [{rrdc}\\c_720p\\command]
                    {command_common} --format=bestvideo[height<=720]+bestaudio[ext=m4a]/best --merge-output-format=mp4 -o '%%(title)s_720.%%(ext)s' {command_end}
                    """.format(rrdc = reg_root_dir_command[1:-1], command_common = self.command_common, command_end = self.command_common_end)
                    command = dedent(subformats)
            else:
                    at = "@"
                    subcommands = ""
                    reg_root_dir_command = reg_root_dir[:-1] + "\command]"
                    command = self.command_common + " " + subtypes['options'] + self.command_common_end
            reg_name = '{}="{}"'.format(at, subtypes['name'])
            icon = '"Icon"="imageres.dll,{}"'.format(subtypes['icon'])

            result_string = ("\n").join([reg_root_dir, reg_name, subcommands, icon, reg_root_dir_command, command, ""]).replace("\n\n", "\n")
            types_string += "\n" + result_string
            count += 1
        result = self.start + types_string
        cwd = os.path.dirname(os.path.realpath(__file__))
        file = os.path.join(cwd, 'ytdl.reg')
        with open(file, "w+") as regfile:
            regfile.write(result.strip())
        


RegGenerator().gen_all()