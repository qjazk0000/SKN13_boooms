def solution(n, k):
    answer = n  # 먹을 수 있는 총 치킨 수
    coupons = n  # 얻을 수 있는 총 쿠폰 수 
    while coupons >= k: # k보다 작을 시 더 이상 치킨 주문 X
        free = coupons // k
        answer += free
        coupons = (coupons % k) + free
    return answer

print(solution(4, 3))
print(solution(10, 3))
print(solution(100, 5))