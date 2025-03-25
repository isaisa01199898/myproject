from django.shortcuts import render
from django.views import View
from datetime import datetime
from zoneinfo import ZoneInfo
from openai import OpenAI
ser_data=40
data1=100
data2=40
data3=50
data4=60
data5=30
data6=88
data7=68

client = OpenAI(api_key="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")
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "あなたは陽気な関西人です。"},
        {"role": "user", "content": "石破総理は好きですか？"}
  ]
)
response_text = completion.choices[0].message.content

print(response_text)



class IndexView(View):
    def get(self, request):
        now_time = datetime.now(
            ZoneInfo("Asia/Tokyo")
        ).strftime("%Y年%m月%d日 %H:%M:%S")
        return render(
            request, "diary/index.html", {"now_time": now_time , "ser_data":ser_data , "data1":data1 ,
"data2":data2,
"data3":data3,
"data4":data4,
"data5":data5,
"data6":data6,
"data7":data7,
"response_text":respons
})  
 

index = IndexView.as_view()
