'''
체스판은 8×8크기이고, 검정 칸과 하얀 칸이 번갈아가면서 색칠되어 있다. 가장 왼쪽 위칸 (0,0)은 하얀색이다.
체스판의 상태가 주어졌을 때, 하얀 칸 위에 말이 몇 개 있는지 출력하는 프로그램을 작성하시오.
'''

# def solution(board):
#     answer = 0
#     board_1D = sum(board, [])

#     for i in range(0, len(board_1D), 2):
#         if board_1D[i] == 'F':
#             answer += 1

#     return answer

board = []
for i in range(8):
    board.append(list(input()))
answer = 0

for i in range(len(board)):
    if i % 2 == 0:
        for s in range(0, len(board[0]), 2):
            if board[i][s] == 'F':
                answer += 1
    else:
        for s in range(1, len(board[0]), 2):
            if board[i][s] == 'F':
                answer += 1

print(answer)