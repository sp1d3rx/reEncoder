# reEncoder
takes mp4 files and upconverts them to HEVC/h.265 and resizes, mixes 5.x down to 2.x with optimal settings

Needs: FFMPEG. You can download it from here:
https://ffmpeg.zeranoe.com/builds/
Choose the right one for your system, and extract the files somewhere.
Modify the .py file to point to your ffmpeg directory. It uses ffmpeg.exe and ffprobe.exe.

Set the initial directory on line 50 (or dont).

Run the .py file and it'll ask you to select a file. It will convert that file and all others that aren't already HEVC in that folder.

Troubleshooting...
If you are having trouble, try "convertThis.bat". Just put this in your ffmpeg bin folder, change the paths and drag and drop a video file to it. If it doesn't convert then it'll at least tell you why.
