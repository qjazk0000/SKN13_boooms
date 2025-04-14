def solution(wallet, bill):
    answer = 0  # 지폐 접은 횟수 저장

    while min(bill) > min(wallet) or max(bill) > max(wallet):
        if bill[0] > bill[1]:
            bill[0] //= 2
            
        else:
            bill[1] //= 2

        answer += 1
            

    return answer