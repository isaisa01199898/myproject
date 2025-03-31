from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
import os
from dotenv import load_dotenv
import google.generativeai as genai
from .forms import TestForm, PageForm

ser_data=40
data1=100
data2=40
data3=50
data4=60
data5=30
data6=88
data7=68


# .envファイルの読み込み
load_dotenv()

# APIキーの設定
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Generative AIの設定
genai.configure(api_key=GOOGLE_API_KEY)

# ビュー関数
def generate_response(request):
    # 入力プロンプト
    prompt = request.GET.get('prompt', 'user_input')

    # モデルの生成
    gemini_pro = genai.GenerativeModel("gemini-pro")
    response = gemini_pro.generate_content(prompt)

    # 結果をJSONレスポンスとして返す
    return JsonResponse({'response': response.text})
def prompt_view(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            # 必要な処理をここに追加
            return redirect('diary:index')
    else:
        form = TestForm()
    return render(request, 'diary/index.html', {'form': form})

class IndexView(View):
    template_name = "diary/index.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['default_value'] = "ここに初期値を設定"  # ← 初期値を設定
        return context
    def post(self, request, *args, **kwargs):
        context = {
            'form': TestForm(request.POST),  # フォームデータを受け取る
        }
        if context['form'].is_valid():  # フォームのバリデーションを確認
            user_input = context['form'].cleaned_data['user_input']  # 入力内容を取得
            print(user_input)  # 入力内容を確認

            # Geminiモデルを呼び出して回答を取得
            try:
                gemini_pro = genai.GenerativeModel("gemini-pro")
                response = gemini_pro.generate_content(user_input)
                context['message'] = response.text
            except Exception as e:
                print(f"Error: {e}")
                context['message'] = "モデルの呼び出しに失敗しました。"

        return render(request, "diary/index.html", context)

    def get(self, request):
        now_time = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d日 %H:%M:%S")
        my_dict = {
                "now_time": now_time , 
                "ser_data":ser_data , 
                "data1":data1 ,
                "data2":data2,
                "data3":data3,
                "data4":data4,
                "data5":data5,
                "data6":data6,
                "data7":data7,
                'form': TestForm(),
                'insert_forms': '初期値', 
        }
        if (request.method == 'POST'):
            my_dict['insert_forms'] = '文字列:' + request.POST['text'] + '\n整数型:' + request.POST['num']
            my_dict['form'] = TestForm(request.POST)
        return render(
            request, "diary/index.html", my_dict)  

class PageCreateView(View):
    def get(self, request):
        form = PageForm()
        return render(request, 'diary/prompt.html', {'form': form})
    def post(self, request):
        form = PageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary:index')
        return render(request, 'diary/prompt.html', {'form': form})

index = IndexView.as_view()
prompt = PageCreateView.as_view()
