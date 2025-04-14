# def solution(cpr):
#     answer = []
#     basic_order = ["check", "call", "pressure", "respiration", "repeat"]
#     for action in cpr:
#         for i in range(len(basic_order)):
#             if action == basic_order[i]:
#                 answer.append(i+1)
                
#     return answer



def solution(cpr):
    answer = []
    order = ["check", "call", "pressure", "respiration", "repeat"]

    for action in cpr:
        answer = [order.index(action) + 1 for action in cpr if action in order]
    
    return answer

cpr = ["call", "respiration", "repeat", "check", "pressure"]

print(solution(cpr))