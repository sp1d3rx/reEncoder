@echo off
C:\Users\you...\Desktop\ffmpeg-20181123-fa08345-win64-static\bin\ffmpeg.exe -i %1 -vf scale=1280x720 -af "pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR" -gops_per_idr 1 -vbaq 1 -c:v hevc_amf C:\Users\you...\Desktop\ffmpeg-20181123-fa08345-win64-static\bin\test.hevc.mkv
pause
