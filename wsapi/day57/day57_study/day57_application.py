# day57_application.py
# 주제:Application: 온라인 쇼핑몰 상품 이미지 메타데이터 검사 API
# 캠퍼스 WAV 분석과 다른 주제로 상품 이미지 업로드 API를 설계합니다.

import hashlib
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

# [요구사항
# POST /images/inspect에서 PNG/JPEG 파일을 업로드합니다.
# 최대 2MiB이며 잘못된 파일은 415, 크기 초과는 413을 반환합니다.
# 파일의 magic bytes를 검사하고 filename, extension, bytes, sha256을 JSON으로 응답합니다.
# 업로드 후 자원을 닫고, 해시 계산 과정에서 파일 내용을 로그에 출력하지 않습니다.
# PNG/JPEG/텍스트 위장 파일/2MiB 초과 파일을 각각 검증합니다.]

MAX_IMAGE_BYTES = 2 * 1024 * 1024

app = FastAPI(title='상품 이미지 메타데이터 검사 API')


class Image(BaseModel):
    filename: str
    extension: str
    bytes: int


class ImageResponse(Image):
    sha256: str


@app.post('/images/inspect', response_model=ImageResponse)
async def inspect(file: UploadFile = File(...)):
    filename = file.filename or ''

    try:
        data = await file.read(MAX_IMAGE_BYTES + 1)
    finally:
        await file.close()

    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(413, '파일 크기는 최대 2MiB입니다.')

    extension = Path(filename).suffix.lower()

    if extension == '.png':
        if not data.startswith(b'\x89PNG\r\n\x1a\n'):
            raise HTTPException(415, 'PNG 파일 형식이 아닙니다.')

    elif extension in ('.jpg', '.jpeg'):
        if not data.startswith(b'\xff\xd8\xff'):
            raise HTTPException(415, 'JPEG 파일 형식이 아닙니다.')

    else:
        raise HTTPException(415, 'PNG 또는 JPEG 파일만 허용합니다.')

    return ImageResponse(
        filename=filename,
        extension=extension,
        bytes=len(data),
        sha256=hashlib.sha256(data).hexdigest()
    )