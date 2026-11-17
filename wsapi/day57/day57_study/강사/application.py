# day57_application.py
# 쇼핑몰 상품 이미지 업로드: 파일 시그니쳐와 크기 검증

import hashlib
from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI(title='쇼핑몰 상품 이미지 검증 API')

LIMIT = 2 * 1024 * 1024 # 2Mbytes

@app.post('/images/inspect')
async def inspect_image(file: UploadFile = File(...)):

    try:
        content = await file.read(LIMIT + 1)
    finally:
        await file.close()

    if len(content) > LIMIT:
        raise HTTPException(413, detail='2M 초과')

    # 이미지 파일의 상위 바이트들 확인, 확장자만 확인하면 안됨
    if content.startswith(b'\x89PNG\r\n\x1a\n'): # PNG
        kind, extension = 'PNG', '.png'
    elif content.startswith(b'\xff\xd8\xff'): # JPEG
        kind, extension = 'JPEG', '.jpg'
    else:
        raise HTTPException(415, detail='PNG 또는 JPEG만 허용')

    return {
        'filename': file.filename,
        'extension': extension,
        'format': kind,
        'bytes': len(content),
        'sha256': hashlib.sha256(content).hexdigest()
    }

