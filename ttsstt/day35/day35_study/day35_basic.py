# day35_basic.py
# 주제:[Basic: 물류센터 음성 지시 기록 품질 점검]
#
# 상황: 자동 창고 음성명령의 기록 문장 5건이 있습니다.
# 음성 인식 실행 대신 제공된 원문-인식문 쌍으로 평가 규칙을 학습합니다.
#
import re
import unicodedata
from jiwer import wer, cer, process_words
from util.print_util import pp
#
PAIRS = [
    ("첫 번째 상자를 오른쪽 선반으로 이동", "첫 번째 상자를 오른쪽 선반으로 이동"),
    ("파란 상자를 창고 입구에 배치", "파란 상자를 창고에 배치"),
    ("재고 수량 다섯 개를 확인", "재고 수량 네 개를 확인"),
    ("출고 목록을 다시 확인", "출고 목록을 반드시 다시 확인"),
    ("작업 구역 조명을 켜 주세요", "작업 구역 조명 켜 주세요")]

# pp(PAIRS[0][0])
# pp(PAIRS[1][0])


# 요구사항
# 코드에 물류 명령 5건(reference, hypothesis)을 직접 정의하세요.
# 1. 정의
def ref_hyp_define(pairs):
    references = []
    hypothesis = []
    for pair in pairs:
        references.append(pair[0])
        hypothesis.append(pair[1])
    return references, hypothesis

# 양쪽 문장에 공백 통일, 특수문자 제거, 소문자 변환을 적용하세요. O
# 2. 정규화 부터
def normalize_text(text):
    text = unicodedata.normalize('NFC', text).lower()
    text = re.sub(r'[^가-힣a-z0-9\s]', r' ', text)
    return re.sub(r'\s+', ' ', text).strip()

# 각 WER·CER·S/D/I를 계산해 화면에 표시하세요.
# 3. 평가해서 값구하기
def evaluate(reference, hypothesis):
    ref_n = normalize_text(reference)
    hyp_n = normalize_text(hypothesis)

    if not ref_n or not hyp_n:
        raise ValueError('정답 또는 예측이 없어서 오류율을 평가할 수 없습니다')

    counts = process_words(ref_n, hyp_n)

    return {
        'wer': wer(ref_n, hyp_n),
        'cer': cer(ref_n, hyp_n),
        'S': counts.substitutions,
        'D': counts.deletions,
        'I': counts.insertions,
        'reference_norm': ref_n,
        'hypothesis_norm': hyp_n
    }

# 오류가 가장 큰 명령을 찾아 설명하세요.
# wer 가장 높은 인덱스
def max_wer_error(evals):
    max_index = 0

    for index in range(len(evals)):
        if evals[index]['wer'] > evals[max_index]['wer']:
            max_index = index

    return max_index

# cer 가장 높은 인덱스
def max_cer_error(evals):
    max_index = 0

    for index in range(len(evals)):
        if evals[index]['cer'] > evals[max_index]['cer']:
            max_index = index

    return max_index


def main():
    # ref, hyp 분해
    references, hypothesis = ref_hyp_define(PAIRS)

    evals = []

    # 묶어서 평가
    for reference, hyp in zip(references, hypothesis):
        eval_result = evaluate(reference, hyp)
        evals.append(eval_result)

    for eval_result in evals:
        pp(
            f'wer= {eval_result["wer"]:.2%}\n'
            f'cer= {eval_result["cer"]:.2%}\n'
            f'S= {eval_result["S"]}\n'
            f'D= {eval_result["D"]}\n'
            f'I= {eval_result["I"]}\n'
            f'reference_norm= {eval_result["reference_norm"]}\n'
            f'hypothesis_norm= {eval_result["hypothesis_norm"]}\n'
        )

    max_wer_index = max_wer_error(evals)
    max_cer_index = max_cer_error(evals)
    pp(
        f'가장 높은 WER: {evals[max_wer_index]["wer"]:.2%}\n'
        f'정답 문장: {evals[max_wer_index]["reference_norm"]}\n'
        f'예측 문장: {evals[max_wer_index]["hypothesis_norm"]}\n'
        'WER 오류 원인: 2번 명령에서 "창고 입구에"가 "창고에"로 인식되어 위치 정보가 누락되었습니다.'
    )
    pp(
        f'가장 높은 CER: {evals[max_cer_index]["cer"]:.2%}\n'
        f'정답 문장: {evals[max_cer_index]["reference_norm"]}\n'
        f'예측 문장: {evals[max_cer_index]["hypothesis_norm"]}\n'
        'CER 오류 원인: 4번 명령에서 정답에 없는 "반드시"가 추가되었습니다.'
    )
if __name__ == '__main__':
    main()