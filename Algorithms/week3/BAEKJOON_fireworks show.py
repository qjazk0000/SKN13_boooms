'''
학생들은 3주가 지난 기념으로 매점에서 1월 1일이 지나 싸게 파는 폭죽을 사서 터뜨리고 있다.
폭죽쇼를 하는 동안 N명의 학생들이 폭죽을 터뜨린다. 그리고 이 N명의 학생은 각각 일정한 주기로 폭죽을 터뜨린다.
물론 이 주기는 학생들마다 같을 수도, 다를 수도 있다.
그리고 우리는 초 단위로 관찰을 하고, 폭죽 역시 초 단위로 터진다.
폭죽쇼가 끝날 때까지 얼마나 많은 시간동안 밤하늘에 폭죽이 터지는 것을 볼 수 있는지 궁금해 하는 조교를 도와주자.
'''
import numpy as np
n, time = map(int, input().split())
firework_period = [int(input()) for _ in range(n)]

firework_count = np.zeros(time)

for period in firework_period:
    for i in range(firework_count):
        if i % period == 0 and firework_count[i] != 1:
            firework_count[i] = 1
    


print(firework_count.)
