
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
from groq import Groq
import random
from .forms import TestForm, PageForm
import serial   #pyserial
import os
import datetime
import pprint
import os  
# Load environment variables
load_dotenv()
GROQ_API_KEY = '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'
liking = "四字熟語"#おくらせるジャンル
data = []
#modele= ["#class tracking_eyeye     eye = eye_tracking()     webcam = cv2.VideoCapture(0)     if not webcam.isOpened():         print("未接続")         exit()        while True:         i = 0         _, frame = webcam.read()         print(frame.shape, frame.dtype)         # 確認         eye.refresh(frame)                print("frame before refresh:", frame.shape, frame.dtype)            # 顔＋瞳に十字線を描画した結果を取得         frame = eye.annotated_frame()            text = " "            # 状態テキスト         text = ""         if eye.is_blinking():             text = "Blinking"         elif eye.is_right():             text = "Looking right"         elif eye.is_left():             text = "Looking left"         elif eye.is_center():             text = "Looking center"         cv2.putText(frame, text, (90, 60),                     cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)            # 瞳の座標を描画         left_pupil = eye.pupil_left_coords()         right_pupil = eye.pupil_right_coords()         cv2.putText(frame, "Left pupil:  " + str(left_pupil),                     (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)         cv2.putText(frame, "Right pupil: " + str(right_pupil),                     (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)         print(f"左目の座標：{left_pupil}")         print(f"右目の座標：{right_pupil}")         now = datetime.datetime.now()         with open('log.txt', 'a', encoding='UTF-8') as f:               f.write(f'リアルタイム: {now.strftime("%Y-%m-%d %H:%M:%S")} 左目の座標：{left_pupil} 右目の座標：{right_pupil}\n')                                                                        cv2.imshow("Demo", frame)                    # Escで終了         if cv2.waitKey(1) & 0xFF == 27:                 break        webcam.release()     cv2.destroyAllWindows() "]
    
    



ser_data = 40
sample_values = {
    'data1': 100,
    'data2': 40,
    'data3': 50,
    'data4': 60,
    'data5': 30,
    'data6': 88,
    'data7': 68,
}

# ユーザーに返す形式: 1=四字熟語, 2=音楽, 3=history, 4=格言
liking = 1

# --- GROQ AI response view ---
def generate_response(request):
    user_input = request.GET.get('prompt', '質問を入力してください')
    client = Groq(api_key=GROQ_API_KEY)

    system_prompt = {"role": "system", "content": "あなたは便利なアシスタントです。質問には簡潔に答えてください。"}
    user_prompt = {"role": "user", "content": user_input}
    chat_history = [system_prompt, user_prompt]

    try:
        response = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_history,
            max_tokens=100,
            temperature=1.2
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"エラーが発生しました: {e}"

    return JsonResponse({'response': answer})


# --- Main view for index ---
class IndexView(View):
    template_name = "diary/index.html"

    def get(self, request):
        # Initial render without AI message
        context = {
            'ser_data': ser_data,
            **sample_values,
            'form': TestForm(),
            'insert_forms': '初期値',
            'message': None,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        #sinpakusuuyomitori
        ser = serial.Serial('com8',9600)
        line=''
        i=0
        data=[]
        while len(data)<14:     #forではできない
            line = ser.readline().decode('utf-8').strip()
            data.append(line)

        
            print(data)
        ser.close()
        try:
            sensor_data = float(data[-1])
            print(f"{sensor_data}")
        except :
            sensor_data = None
            print("you lose")

        # Simulate sensor data
        print("start")
        print(f"{sensor_data}")
        judebox = None
        message = None

        if sensor_data is not None:
            if 75 <= sensor_data <= 85:
                judebox = "集中"
            elif sensor_data < 75:
                judebox = "集中できていない"
            else:
                judebox = "super集中"

        # AI processing based on mode and user liking
        if judebox == "集中できていない" and liking == 1:
            # 四字熟語
            prompt_text = f'勉強に{judebox}人を励ます四字熟語を一つだけ挙げてください。(その言葉の説明も入れて)（勉強に集中できない人を励ますように）'
            try:
                client = Groq(api_key=GROQ_API_KEY)
                chat_history = [
                    {"role": "system", "content": "あなたは便利なアシスタントです。一文でおこたえください"},
                    {"role": "user", "content": prompt_text}
                ]
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=chat_history,
                    max_tokens=50,
                    temperature=1.2
                )
                message = response.choices[0].message.content
            except Exception as e:
                message = f"k: {e}"
        elif judebox == "集中" and liking == 1:
            # 四字熟語
            prompt_text = '集中してべんきょうしている人を励ます四字熟語を一つだけ挙げてください。'
            try:
                client = Groq(api_key=GROQ_API_KEY)
                chat_history = [
                    {"role": "system", "content": "あなたは便利なアシスタントです。一文でおこたえください"},
                    {"role": "user", "content": prompt_text}
                ]
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=chat_history,
                    max_tokens=50,
                    temperature=1.2
                )
                message = response.choices[0].message.content
            except Exception as e:
                message = f"k: {e}"
        # Prepare context for rendering
        context = {
            'ser_data': ser_data,
            'form': TestForm(),
            'insert_forms': '初期値',
            'message': message,
        }
        return render(request, self.template_name, context)


# --- Page creation view ---
class PageCreateView(View):
    def get(self, request):
        return render(request, 'diary/prompt.html', {'form': PageForm()})

    def post(self, request):
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary:index')
        return render(request, 'diary/prompt.html', {'form': form})


# URL configuration
index = IndexView.as_view()
prompt = PageCreateView.as_view()
