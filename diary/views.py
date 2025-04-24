import numpy as np
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os
from groq import Groq
import random
from .forms import TestForm, PageForm
import Serial
# Load environment variables
load_dotenv()
GROQ_API_KEY = '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'
ser = serial.Serial('com4',9600)
data = []
liking



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
            'now_time': datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M:%S"),
            'ser_data': ser_data,
            **sample_values,
            'form': TestForm(),
            'insert_forms': '初期値',
            'message': None,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        while len(data) < 15:
          line = ser.readline().decode('utf-8').strip()
          data.append(line)
      
          ser.close()
      
          try:
              sensor_data = float(data[14])
              break
          except ValueError:
              sensor_data = None
              break

        # Simulate sensor data
        print("start")
        print(f"{sensor_data}")
        judebox = None
        message = None

        if sensor_data is not None:
            if 75 <= sensor_data <= 85:
                judebox = "集中"
            elif sensor_data < 75:
                judebox = "not集中"
            else:
                judebox = "super集中"

        # AI processing based on mode and user liking
        if judebox == "not集中" and liking == 1:
            # 四字熟語リクエスト
            prompt_text = '勉強している人を励ます四字熟語を一つだけ挙げてください。'
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
                message = f"モデルの呼び出しに失敗しました: {e}"
        print(f"{message}")
        # Prepare context for rendering
        context = {
            'now_time': datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y年%m月%d日 %H:%M:%S"),
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
