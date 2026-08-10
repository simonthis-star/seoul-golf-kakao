import os
import json
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("KAKAO_TOKEN")
TARGET_URL_STR = os.environ.get("TARGET_URL")

# 쉼표(,)로 구분된 주소 5개를 쪼개서 목록으로 만듭니다.
target_urls = [url.strip() for url in TARGET_URL_STR.split(",") if url.strip()]

# 📌 주의: 비밀상자(Secrets)에 넣으신 주소 순서와 똑같이 적혀있어야 합니다!
golf_names = ["영등포", "은평", "동대문", "도봉", "강동"]

def send_kakao_message(text, target_url):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": target_url,
                "mobile_web_url": target_url
            }
        })
    }
    requests.post(url, headers=headers, data=payload)

def check_reservation():
    headers = {"User-Agent": "Mozilla/5.0"}
    
    # 5개의 주소를 하나씩 순서대로 방문하며 확인합니다.
    for i, url in enumerate(target_urls):
        # 만약 주소 개수보다 이름 개수가 적으면 임시 이름으로 대체합니다.
        name = golf_names[i] if i < len(golf_names) else f"골프장{i+1}"
        
        try:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text()

            # '접수중' 또는 '예약가능' 상태가 감지되면 해당 구장 이름으로 알림 발송
            if "접수중" in text or "예약가능" in text:
                msg = f"🚨 [{name} 파크골프장]\n빈자리가 나왔습니다! 늦기 전에 예약하세요."
                send_kakao_message(msg, url)
                print(f"[{name}] 카카오톡 알림 발송 완료!")
            else:
                print(f"[{name}] 현재 잔여 자리가 없습니다.")
        except Exception as e:
            print(f"[{name}] 오류 발생: {e}")

if __name__ == "__main__":
    check_reservation()
