import os
from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
import subprocess
import json
from glob import glob
CREATE_NO_WINDOW = 0x08000000
ffmpegBinPath = "C:\\Desktop\\ffmpeg-20181123-fa08345-win64-static\\bin\\"

probeExe = ffmpegBinPath + "ffprobe.exe"
ffmpegExe = ffmpegBinPath + "ffmpeg.exe"
class thclass(object):
    def __init__(cls):
        cls.root = None
        pass
    def get_file(cls, directory="", title="Select a file", filetypes=None):
        if not filetypes:
            filetypes = (("all files","*.*"))
        return tkFileDialog.askopenfilename(initialdir=directory, title=title, filetypes=filetypes)
    def __enter__(cls, *args):
        cls.root = Tk()
        return cls
        pass
    
    def __exit__(cls, *args):
        cls.root.destroy()
        pass

class CodecInfo(object):
    def __init__(cls, jcodecInfo):
        cls.jcodecInfo = jcodecInfo
        cls.vstream = None
        cls.astream = None
        for stream in jcodecInfo.get('streams'):
            codecType = stream.get('codec_type')
            disposition = stream.get('disposition')
            isDefault = disposition.get('default')
            # gets the default stream (or only stream)
            if codecType in 'video' and (isDefault or cls.vstream is None):
                cls.vstream = stream
                pass
            elif codecType in 'audio' and (isDefault or cls.astream is None):
                cls.astream = stream
            


if __name__ == "__main__":        
    with thclass() as win:
        print type(win)
        fn = win.get_file(directory=r"F:\Download\tv", filetypes=(("video","*.mkv"),("all files","*.*")))
        #root.filename = tkFileDialog.askopenfilename(initialdir = r"F:\tv",title = "Select file",filetypes = (("video","*.mkv"),("all files","*.*")))
        #print (root.filename)
        #fname = root.filename
        dirname = os.path.dirname(fn)
        print "Dir:", os.path.dirname(fn)

    for fn in glob(dirname + "/*.mkv"):
        fn = fn.replace("\\","/")
        print fn
        fsize = os.path.getsize(fn)
        print "{0:,} bytes".format(fsize)

        probe = [probeExe,
                 "-v", "quiet",
                 "-print_format", "json",
                 "-show_format",
                 "-show_streams", fn]
        results = subprocess.check_output(probe, creationflags=CREATE_NO_WINDOW)
        jresults = json.loads(results)
        ci = CodecInfo(jresults)
        print "Codec:", ci.vstream['codec_name']
        print "Width:", ci.vstream['width']
        print "Height:", ci.vstream['height']
        print "Aspect Ratio:", ci.vstream['display_aspect_ratio']
        if ci.vstream['display_aspect_ratio'] != "16:9":
            print "Warning! Video is not 16:9. Continue?"
            answer = raw_input("y/n: ")
            if answer != "y":
                exit()
        else:
            print "16:9 detected. Proceeding."

        if ci.vstream['codec_name'] in ["hevc", "vp9"]:
            print "Already H.265 / VP9 / HEVC. Skipping."
            continue
        # adds hevc to filename, fix 1920x1080 references in filename
        outfile = fn.replace(".mkv", ".hevc.mkv").replace("1080", "720").replace("1920", "1280")
        print "Writing to:", outfile
        convert = [ffmpegExe,
                   "-i", fn,
                   # scales down (or up?) video to 1280x720
                   "-vf", "scale=1280x720",
                   # converts 5.1 to 2.0 stereo downmix for dolby matrix
                   "-af", "pan=stereo|FL < 1.0*FL + 0.707*FC + 0.707*BL|FR < 1.0*FR + 0.707*FC + 0.707*BR",
                   # hevc using amd encoder. Change to hevc_nvenc for Nvidia cards.
                   "-c:v", "hevc_amf",
                   # Variance Based Adaptive Quantization
                   "-vbaq", "1",
                   # Fixes seeking with hevc amd encoder
                   "-gops_per_idr", "1",
                   outfile]
        try:
            results = subprocess.check_output(convert, creationflags=CREATE_NO_WINDOW)
        except subprocess.CalledProcessError as e:
            raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        print "Done."
        tgt = fn.replace(".mkv", ".tmp")
        print "Renaming {0} to {1}".format(fn, tgt)
        os.rename(fn, tgt)
        print "Renamed."
    print "Cleanup starting."
    for fn in glob(dirname + "/*.tmp"):
        fn = fn.replace("\\", "/")
        print "Removing {0}...".format(fn)
        os.remove(fn)
