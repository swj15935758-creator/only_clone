# day57_challenge_client.py

import os

import requests
from dotenv import load_dotenv

load_dotenv()

URL = 'http://127.0.0.1:8003/trip/recommend'


def main():
    key = os.getenv('TRAVEL_API_KEY', '').strip()
    headers = {'X-Travel-Key': key} if key else {}
    payload = {
        'city': '서울',
        'days': 3,
        'interests': ['역사', '자연', '음식'],
    }

    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
    except requests.Timeout:
        print('요청 시간 초과')
        return
    except requests.HTTPError as error:
        print('HTTP 오류:', error.response.status_code)
        return
    except requests.exceptions.JSONDecodeError:
        print('서버 응답이 JSON 형식이 아닙니다.')
        return
    except requests.RequestException:
        print('서버 연결 또는 요청 오류')
        return

    for item in result['recommendations']:
        print(f"{item['day']}일차: {item['place']} ({item['interest']})")


if __name__ == '__main__':
    main()