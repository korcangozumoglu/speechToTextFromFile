# import library
import getopt
import math
import os
import shutil
import time
import traceback

import speech_recognition as sr
from pydub import AudioSegment

from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import sys
import os


class SplitWavAudioMubin:
    def __init__(self, folder, filename, new_folder):
        self.folder = folder
        self.filename = filename
        self.filepath = folder + '\\' + filename
        self.new_folder = new_folder

        self.audio = AudioSegment.from_wav(self.filepath)

    def get_duration(self):
        return self.audio.duration_seconds

    def single_split(self, from_sec, to_sec, split_filename):
        t1 = from_sec * 1000
        t2 = to_sec * 1000
        split_audio = self.audio[t1:t2]
        split_audio.export(self.new_folder + '\\' + split_filename, format="wav")

    def multiple_split(self, number_of_part):
        total_seconds = math.ceil(self.get_duration())
        part_seconds = math.ceil(total_seconds / number_of_part)
        j = 1
        for i in range(0, total_seconds, part_seconds):
            split_fn = str(j) + '_' + self.filename
            if i + part_seconds > total_seconds:
                split_size = total_seconds - i
            else:
                split_size = i + part_seconds
            self.single_split(i, split_size, split_fn)
            j += 1
            if i == total_seconds - part_seconds:
                print('All split successfully')

try:
    folder_path = os.getcwd()
    new_folder_path = folder_path + "\\split_files"
    isExist = os.path.exists(new_folder_path)
    if not isExist:
        os.mkdir(new_folder_path)
    else:
        shutil.rmtree(new_folder_path)
        os.mkdir(new_folder_path)



    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    file = filename.split("/")[-1]

    if file.split(".")[1] != "wav":
        audio = AudioSegment.from_file(file)
        new_filename = file.split(".")[0] + ".wav"
        print(f"Converting {file} to {new_filename}...")
        audio.export(new_filename, format="wav")
        file = new_filename
        print("converted")

    file_size = os.path.getsize(file)
    part_count = math.ceil(file_size / 5000000)  # 5mb
    split_wav = SplitWavAudioMubin(folder_path, file, new_folder_path)
    split_wav.multiple_split(number_of_part=part_count)

    # Initiаlize  reсоgnizer  сlаss  (fоr  reсоgnizing  the  sрeeсh)
    r = sr.Recognizer()
    # Reading Audio files as source
    #  listening  the  аudiо  file  аnd  stоre  in  аudiо_text  vаriаble
    print('Converting audio transcripts into text...')
    with open(folder_path + '\\script.txt', 'w', encoding='utf-8') as f:
        for i in range(1, part_count + 1):
            with sr.AudioFile(new_folder_path + "\\" + str(i) + "_" + file) as source:
                audio_text = r.record(source)
                # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
                try:
                    # using google speech recognition
                    text = r.recognize_google(audio_text, language="tr-tr")
                    f.write(text)
                    f.write('\n')
                except Exception as ex:
                    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                    message = template.format(type(ex).__name__, ex.args)
                    print(message)
            print("%" + str(math.ceil(100 * (i / part_count))) + " completed.")

    print('Finished')

    time.sleep(3)

except Exception as ex:
    ex_type, ex_value, ex_traceback = sys.exc_info()

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" % ex_value)
    print("Stack trace : %s" % stack_trace)
    time.sleep(30)
