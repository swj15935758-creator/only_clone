# # day5_extra.py
# # [Python 별찍기]
#
# # ※ 공통 조건
# # - 문자열 반복 연산('*' * n, ' ' * n 등)은 사용하지 않습니다.
# # - for문 또는 중첩 for문을 사용합니다.
# # - 필요한 경우 if문을 사용합니다.
# # - 모든 문제는 n = 5를 기준으로 작성합니다. 단, X자와 십자가 문제는 n = 9를 사용합니다.
#
# # 1. 왼쪽 직각삼각형
# # 다음과 같이 출력하세요.
# #
# # *
# # **
# # ***
# # ****
# # # *****
# n=5
# for i in range(1,n+1):
#     for j in range(i):
#         print('*', end="")
#     print()
#
# print()
# #
# # for i in range(1,n+1):
# #     print('*' * i)
# #
# # # 2. 역직각삼각형
# # # 다음과 같이 출력하세요.
# # #
# # # *****
# # # ****
# # # ***
# # # **
# # # *
# #
# # # print()
# # for i in range(n,0,-1):
# #     print('*' * i)
#
# for i in range(n,0,-1):
#     for j in range(i):
#         print('*', end="")
#     print()
#
# # for i in range(1, n+1):
# #     for j in range(i):
# #         print(' ' * (n-j) + '*' * i, end='')
#
#
# # 3. 오른쪽 정렬 직각삼각형
# # 다음과 같이 출력하세요.
# #
# #     *
# #    **
# #   ***
# #  ****
# # *****
#
#
# for i in range(1, n + 1): # 줄의수
#     for j in range(n - i): # 공백의 수
#         print(' ', end='')
#     for j in range(i): #공백 다음의 수
#         print('*', end='')
#     print()
#
# # # 4. 피라미드
# # # 다음과 같이 출력하세요.
# # #
# # #     *
# # #    ***
# # #   *****
# # #  *******
# # # *********
# #
# #
# #
# for i in range(1, n+1):
#     for j in range(n - i):
#         print(' ', end='')
#
#     for j in range(i - 1):
#         print('*', end='')
#
#     for j in range(i):
#         print('*', end='')
#
#     for j in range(n - i):
#         print(' ', end='')
#     print()
#
#
#
# # # 5. 역피라미드
# # # 다음과 같이 출력하세요.
# # #
# # # *********
# # #  *******
# # #   *****
# # #    ***
# # #     *
# #
# for i in range(1, n+1):
#
#     for j in range(1, i):
#         print(' ', end='')
#
#     for j in range(n - i):
#         print('*', end='')
#
#     for j in range(n - i + 1):
#         print('*', end='')
#
#     for j in range(1, i):
#         print(' ', end='')
#     print()
#
#
#
# # 6. 다이아몬드
# # 다음과 같이 출력하세요.
# #
# #     *
# #    ***
# #   *****
# #  *******
# # *********
# #  *******
# #   *****
# #    ***

n=5
# for i in range(1, n+1):
#     for j in range(n - i):
#         print(' ', end='')
#
#     for j in range(i - 1):
#         print('*', end='')
#
#     for j in range(i):
#         print('*', end='')
#     for j in range(n - i):
#         print(' ', end='')
#     print()
#
# for i in range(2, n+1):
#
#     for j in range(1, i):
#         print(' ', end='')
#
#     for j in range(n - i):
#         print('*', end='')
#
#     for j in range(n - i + 1):
#         print('*', end='')
#
#     for j in range(1, i):
#         print(' ', end='')
#     print()
# ========================================================================
# # 7. 속이 빈 피라미드
# # 다음과 같이 출력하세요.
# #
# #     *
# #    * *
# #   *   *
# #  *     *
# # *********
# n= 5
# for i in range(1, n + 1):
#     if i == n:  # 맨 마지막 줄(n)일 때 바닥을 채웁니다.
#         for j in range(1, n + 1):
#             print('*', end='')
#         for j in range(1, n):
#             print('*', end='')
#     else:
#         for j in range(1, n - i + 1):  #  시작 공백 개수 조정
#             print(' ', end='')
#         print('*', end='')  # 왼쪽 벽면 별 출력
#
#     if i > 1:  # 꼭짓점(i=1)이 아닐 때만 내부 공백과 오른쪽 별을 출력합니다.
#         for j in range(0, i - 1):  # 공백 추가
#             print(' ', end='')
#         for j in range(0, i - 2):  # 추가 공백
#             print(' ', end='')
#         if i != n :
#             print('*', end='')  # 오른쪽 벽면 별 출력
#     print()


# n= 5
# for i in range(1,n+1):
#
#     for j in range(n-i):
#         print(' ',end=' ')
#     for j in range(1, 2*i):
#         if i==n:
#             print('*',end=" ")
#         elif j==1 or j==2*i -1:
#             print('*',end=" ")
#         else:
#             print(' ',end=" ")
#     print()
# 8. 속이 빈 사각형
# 다음과 같이 출력하세요.
#
# *****
# *   *
# *   *
# *   *
# *****
# for i in range(n): # 줄의 수 ( 행의 수 )
#     for j in range(n): # 열의 수
#         if i == 0 or i == n -1 or j == 0 or j == n-1:
#             print('*', end='')
#         else:
#             print(' ', end='')
#     print()



# 9. X자
# n = 9일 때 다음과 같이 출력하세요.
#
# *       *
#  *     *
#   *   *
#    * *
#     *
#    * *
#   *   *
#  *     *
# *       *

# n=5
# for i in range(2*n - 1):
#     for j in range(2*n - 1):
#         if j == i or j == 2*n -i -2:
#             print('*',end=" ")
#         else:
#             print(' ',end=" ")
#     print()

# 10. 속이 빈 모래시계 모양
# 다음과 같이 출력하세요.
#
# *********
#  *     *
#   *   *
#    * *
#     *
#    * *
#   *   *
#  *     *
# *********

n=5

for i in range(n): # 줄의 수 0 ~ 4
    # 왼쪽 공백
    print(' '*i,end='')
    width = 2 * (n - i ) -1 # 각 줄에서 별의 넓이 9 ~ 1
    for j in range(width):
        if i == 0: # 첫번쨰 줄은 별만
            print('*',end='')
        elif j == 0 or j == width-1: # 양끝 별
            print('*',end='') #
        else: print(' ',end='') # 중간 공백
    print()
# 아래쪽
for i in range(n - 2 , -1, -1): # 줄의 수 3 ~ 0
    # 왼쪽 공백
    print(' '*i,end='')
    width = 2 * (n - i ) -1 # 각 줄에서 별의 넓이 9 ~ 1
    for j in range(width):
        if i == 0: # 첫번쨰 줄은 별만
            print('*',end='')
        elif j == 0 or j == width-1: # 양끝 별
            print('*',end='') #
        else: print(' ',end='') # 중간 공백
    print()











