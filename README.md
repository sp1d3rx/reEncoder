# reEncoder
takes mp4 files and upconverts them to HEVC/h.265 and resizes, mixes 5.x down to 2.x with optimal settings

Needs: FFMPEG. You can download it from here:
[https://www.ffmpeg.org/download.html](https://www.ffmpeg.org/download.html)
Choose the right one for your system, and extract the files somewhere.
Modify the .py file to point to your ffmpeg directory. It uses ffmpeg.exe and ffprobe.exe.

Set the initial directory on line 50 (or dont).

Run the .py file and it'll ask you to select a file. It will convert that file and all others that aren't already HEVC in that folder.

Troubleshooting...
1. Look at the paths to your ffmpeg.
2. Make sure the glob is the right ending. mkv/mp4 whatever your files are.
3. If you are having trouble, try "convertThis.bat". Just put this in your ffmpeg bin folder, change the paths and drag and drop a video file to it. If it doesn't convert then it'll at least tell you why.

## AS2 (RFC 4130) Implementation

This repository also contains a minimal educational implementation of the
[AS2 specification (RFC 4130)](https://datatracker.ietf.org/doc/html/rfc4130).
The implementation can be found under the ``as2`` package and provides a
simple :class:`as2.client.AS2Client` capable of building and sending basic
AS2 messages as well as utilities for parsing Message Disposition
Notifications (MDNs).

Run the unit tests with::

    python -m unittest

