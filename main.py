import os
import json
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ.get("KAKAO_TOKEN")
TARGET_URL = os.environ.get("TARGET_URL")

def send_kakao_message(text):
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    payload = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": text,
            "link": {
                "web_url": TARGET_URL,
                "mobile_web_url": TARGET_URL
            }
        })
    }
    requests.post(url, headers=headers, data=payload)

def check_reservation():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text()

        # '접수중' 또는 '예약가능' 상태가 감지되면 내 카톡으로 알림 발송
        if "접수중" in text or "예약가능" in text:
            send_kakao_message("🚨 [골프장 취소표 알림]\n빈자리가 나왔습니다! 지금 바로 예약하세요.")
            print("카카오톡 알림 발송 완료!")
        else:
            print("현재 잔여 자리가 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_reservation()
