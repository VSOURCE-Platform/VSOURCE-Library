# -*- coding: utf-8 -*-
# @Author   : Ecohnoch(xcy)
# @File     : demo.py
# @Function : TODO

import vsource_algorithm

if __name__ == '__main__':
    username = 'api_user@vsource.club'
    password = 'my_api_user_123'
    vsource_algorithm.login(username, password)

    face_path1 = 'examples/0008_01.jpg'
    face_path2 = 'examples/0010_01.jpg'
    score = vsource_algorithm.face_recognition(face_path1, face_path2)
    print(score)

    audio_path1 = 'examples/0.wav'
    audio_path2 = 'examples/1.wav'
    score = vsource_algorithm.speaker_recognition(audio_path1, audio_path2)
    print(score)