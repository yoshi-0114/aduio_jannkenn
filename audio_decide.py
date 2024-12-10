import speech_recognition as sr
import wave
import time
import pyaudio
import subprocess
import sys

FORMAT        = pyaudio.paInt16
SAMPLE_RATE   = 44100
CHANNELS      = 1
INPUT_DEVICE_INDEX = 0
CALL_BACK_FREQUENCY = 3

OUTPUT_TXT_FILE = "./" + "output.txt"
OUTPUT_WAV_FILE = "./" + "output.wav"
error_txt = "読み取れませんでした。2秒後にもう1度録音します。"
judge = 0
# Python2.7のパスを指定
python27_path = ""

def look_for_audio_input():
    pa = pyaudio.PyAudio()
    pa.terminate()

def callback(in_data, frame_count, time_info, status):
    global sprec, frames

    try:
        frames.append(in_data)
        audiodata  = sr.AudioData(in_data, SAMPLE_RATE, 2)
        sprec_text = sprec.recognize_google(audiodata, language='ja-JP')

        with open(OUTPUT_TXT_FILE,'w') as f:
            f.write(sprec_text)

    except sr.UnknownValueError:
        pass

    except sr.RequestError as e:
        pass

    finally:
        return (None, pyaudio.paContinue)

def realtime_textise():
    global sprec, frames
    frames = []

    sprec = sr.Recognizer()

    audio  = pyaudio.PyAudio()

    stream = audio.open(format             = FORMAT,
                        rate               = SAMPLE_RATE,
                        channels           = CHANNELS,
                        input_device_index = INPUT_DEVICE_INDEX,
                        input              = True,
                        frames_per_buffer  = SAMPLE_RATE*CALL_BACK_FREQUENCY,
                        stream_callback    = callback)

    print("Record for 2 seconds")
    time.sleep(2)
    print("finish Recording")

    stream.start_stream()

    time.sleep(2)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(OUTPUT_WAV_FILE, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

def name_changes():
    file_path = OUTPUT_TXT_FILE
    change_txt = ""
    global judge
    judge = 0
    with open(file_path, 'r') as file:
        file_contents = file.read().strip()
    if (file_contents in "グー" or file_contents in "ぐー" or file_contents in "Goo"):
        change_txt = "rock"
    elif (file_contents in "パー" or file_contents in "ぱー" or file_contents in "Par"):
        change_txt = "paper"
    elif (file_contents == "チョキ" or file_contents in "ちょき" or file_contents in "長期"):
        change_txt = "scissors"
    else:
        print(error_txt)
        judge = 1

    if judge == 0:
        with open("change_out.txt", 'w') as f:
            f.write(change_txt)
        print(file_contents)
        print(change_txt)

def reset_txt():
    with open("output.txt", 'w') as f:
        f.write("empty")

if __name__ == '__main__':
    reset_txt()
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "restart":
            subprocess.call([python27_path, ".\\audio_jannkenn.py", "restart_audio"])
    else:
        subprocess.call([python27_path, ".\\audio_jannkenn.py", "start_audio"])
    look_for_audio_input()
    realtime_textise()
    name_changes()
    while judge != 0:
        time.sleep(2)
        reset_txt()
        if len(sys.argv) > 1:
            function_name = sys.argv[1]
            if function_name == "restart":
                subprocess.call([python27_path, ".\\jaudio_annkenn.py", "restart_audio"])
        else:
            subprocess.call([python27_path, ".\\audio_jannkenn.py", "start_audio"])
        look_for_audio_input()
        realtime_textise()
        name_changes()
    subprocess.call([python27_path, ".\\audio_jannkenn.py"])
