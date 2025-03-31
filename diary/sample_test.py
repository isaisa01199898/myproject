import google.generativeai as genai

# APIキーを設定
genai.configure(api_key="AIzaSyAfMNgxSp0al9BUPWD7313RP3QjCh9nqdo")

# 利用可能なモデルをリスト表示
models = genai.list_models()
for model in models:
    print(f"Model ID: {model['name']}, Description: {model['description']}")
