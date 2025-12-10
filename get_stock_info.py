import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import pandas as pd

# env 불러오기
load_dotenv()
now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# 추후 데이터 저장을 위한 폴더
data_path = f'./datas/{now}'
os.makedirs(data_path, exist_ok=True)

# 주요 키들 불러오기
API_KEY = os.getenv("API_KEY")
webhook_url = os.getenv("Webhook_url")

# NVIDIA, Microsoft(OpenAI), Alphabet(구글), Amazon(AWS 클라우드 AI 서비스), Meta, 삼전 순으로
symbols = ["NVDA", "MSFT", "GOOGL", "AMZN", "META"]
names = ['엔비디아-젠슨 황', '마이크로소프트(OpenAI)-사티아 나델라(+샘 알트먼)', '구글-순다르 피차이', '아마존-앤디 재시', '메타-마크 저커버그']

middle_data = []
for count, (sym, name) in enumerate(zip(symbols, names)):
    
    # 분회 최대 5회니까 12초에 하나씩, 안전빵으로 13초에 하나씩
    time.sleep(13)
    
    # 주간으로 가져오기.
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={sym}&apikey={API_KEY}'
    response = requests.get(url)
    
    # 정상이라면
    if response.status_code == 200:
        
        print(f"데이터는 미국시간 기준이고 아래의 출력은 한국시간 기준입니다.\n")
        print(f"다음은 {now}의, {name}의 주식 정보입니다.")
        data = response.json()

        # 이번주 데이터만 뽑아 오기
        weekly_data = data['Weekly Time Series']
        latest_date = sorted(weekly_data.keys(), reverse=True)[0]
        latest_info = weekly_data[latest_date]

        msg = f"📌 *{name} ({sym})* — {latest_date}\n"
        for key, value in latest_info.items():
            print(f"{key}: {value}")
            msg += f"- {key}: {value}\n"
        
        middle_data.append(msg)
        
    else:
        print(f"{name} 호출 실패, 상태 코드: {response.status_code}")
if response.status_code == 200:
    # csv 파일로 저장.
    # csv_file = os.path.join(data_path,f"{now}.csv")
    
    # for data, n in zip(middle_data,names):
    #     data['company'] = n
    # final_data = pd.DataFrame(middle_data)
    # final_data.set_index('company', inplace=True)
    # final_data.to_csv(csv_file, encoding='utf-8-sig')

    # slack으로 전송
    final_message = f"📊 *주간 AI 빅테크 주가 업데이트 ({now})*\n\n" + "\n\n".join(middle_data)
    
    requests.post(webhook_url, json={"text": final_message})
# print(response.status_code)
'''
200 → 정상

400 → 잘못된 요청 (파라미터 확인)

401 → 인증 실패 (API key 확인)

403 → 접근 권한 없음

404 → URL이 없음

500 → 서버 문제
'''
