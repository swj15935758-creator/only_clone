# 관광 컨텐츠의 언어/TTS 호환성

from fastapi import HTTPException, Query, FastAPI
from day58_basic import call, PREFIX

app = FastAPI(title='관광 안내 다국어 호환성 검사')

@app.get('/guide.languages')
async def guide_languages(
        code: list[str] = Query(...),
        model: str = 'LINNET_3'
):
    if len(code) < 2 or 'auto' in code:
        raise HTTPException(422,'언어는 2개 이상, auto 제외')
    payload = await call('GET',PREFIX + '/languages')

    data = payload.get('result', payload)
    languages = data.get('languages', [])

    if not languages:
        raise HTTPException(502,'perso 언어 목록이 비어 있음')
    answer = []

    for item in code:
        # 언어에 해당하는 지원 언어 목록
        rows = [row for row in languages if row.get('code') == item]

        if not rows:
            raise HTTPException(404,f'지원 언어 코드 없음:{item}')

        answer.append({
            'code': item,
            'variants': [
                {
                    'name':row.get('name'),
                    'language':row.get('languageTag'),
                    'supportsModel' : model in row.get('supportsModel', [])
                }
                for row in rows
            ]
        })
        return {'ttsModel':model, 'languages':answer}












