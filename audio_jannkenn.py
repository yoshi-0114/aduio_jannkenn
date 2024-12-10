# -*- coding: utf-8 -*-
from naoqi import ALProxy
import random
import time
import sys
import os
import subprocess

# ポート番号を指定
PORT = 

behavior_manager = ALProxy("ALBehaviorManager", "127.0.0.1", PORT)
talk = ALProxy("ALTextToSpeech", "127.0.0.1", PORT)
postureProxy = ALProxy("ALRobotPosture", "127.0.0.1", PORT)
motion = ALProxy("ALMotion", "127.0.0.1", PORT)
audio_player = ALProxy("ALAudioPlayer", "127.0.0.1", PORT)

str = ["僕の勝ちだね", "あいこだね", "負けちゃった･･･"]
path = r"C:\Python27\project\change_out.txt"
stand = "stand-811386/behavior_1"
file_contents = ""
hand_gesture = ""
random_num = 0

def open_file():
    global file_contents
    with open(path, 'r') as file:
        file_contents = file.read().strip()

def random_robot():
    global random_num, hand_gesture
    random_num = random.randint(1, 3)
    if random_num == 1:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/rock"
        hand_gesture = "rock"
    elif random_num == 2:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/scissors"
        hand_gesture = "scissors"
    elif random_num == 3:
        behavior_name = r"jannkenn_reaction-02a063/jannkenn_reaction/paper"
        hand_gesture = "paper"

    behavior_manager.startBehavior(behavior_name)

def win_or_lose():
    global file_contents, random_num
    outcomes = {
        1: {"rock": str[1], "scissors": str[0], "paper": str[2]},
        2: {"rock": str[2], "scissors": str[1], "paper": str[0]},
        3: {"rock": str[0], "scissors": str[2], "paper": str[1]}
    }
    if str[1] == outcomes[random_num][file_contents]:
        # Python3のパスを指定
        subprocess.call(["", ".\\audio.py", "restart"])
    else:
        talk.say(outcomes[random_num][file_contents])
        if str[0] == outcomes[random_num][file_contents]:
            behavior_name = "expression_reaction-82d091/expression_reaction/joy"
        elif str[2] == outcomes[random_num][file_contents]:
            behavior_name = "expression_reaction-82d091/expression_reaction/sadness"
        behavior_manager.startBehavior(behavior_name)

def start_audio():
    file_name = "start.wav"
    file_path = os.path.join(os.getcwd(), file_name)
    file_id = audio_player.playFile(file_path.replace("\\", "/"))

def restart_audio():
    file_name = "restart.wav"
    file_path = os.path.join(os.getcwd(), file_name)
    file_id = audio_player.playFile(file_path.replace("\\", "/"))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "start_audio":
            start_audio()
        elif function_name == "restart_audio":
            restart_audio()
    else:
        open_file()
        random_robot()
        talk.say("Me："+hand_gesture+"  "+"You："+file_contents) #Meがロボット
        time.sleep(3)
        win_or_lose()
        time.sleep(4)
        behavior_manager.startBehavior(stand)
        exit()
