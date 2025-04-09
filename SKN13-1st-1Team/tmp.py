from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

import pandas as pd
import time

import pymysql


# 1. ChromeDriver 경로 지정
chromedriver_path = "C:/Workspace/Python/SKN13_boooms/chromedriver-win64/chromedriver.exe"  # 예: "C:/chromedriver.exe" 또는 "/usr/local/bin/chromedriver"

options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # 헤드리스 모드 (브라우저 UI 없이 실행)

service = Service(chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)

# 2. driver 통한 페이지 이동
driver.get("https://taas.koroad.or.kr/sta/acs/exs/typical.do?menuId=WEB_KMP_OVT_UAS_ASA")

wait = WebDriverWait(driver, 10)

# 3. 교통사고(DB) 접근
accident_db_selector = '#ddMenuTree0 > div:nth-child(3) > a.node'
accident_db_link = driver.find_element(By.CSS_SELECTOR, accident_db_selector)
accident_db_link.click()
time.sleep(2)

# 3. 교통사고(DB) 중분류 접근
by_accident_selector = '#ddMenuTree17 > div:nth-child(11) > a.node'
by_accident_link = driver.find_element(By.CSS_SELECTOR, by_accident_selector)
by_accident_link.click()
time.sleep(2)

# 4. 유형별 교통사고 접근
by_driver_accident_type_selector = '#sdMenuTree79'
by_driver_accident_type_link = driver.find_element(By.CSS_SELECTOR, by_driver_accident_type_selector)
by_driver_accident_type_link.click()
time.sleep(2)

# 5. 연도(드랍다운박스) 선택
# driver.find_element(By.CSS_SELECTOR, '#startYear').click()
# time.sleep(2)
# dropdown = Select(driver.find_element(By.CSS_SELECTOR, '#stratYear'))
# dropdown.select_by_visible_text('2023년').click()
# time.sleep(2)

# driver.find_element(By.CSS_SELECTOR, '#endYear').click()
# time.sleep(2)
# dropdown = Select(driver.find_element(By.CSS_SELECTOR, '#endYear'))
# dropdown.select_by_visible_text('2023년').click()
# time.sleep(2)

# 6. 조회버튼 클릭
driver.find_element(By.CSS_SELECTOR, '#searchDiv > ul.top01-03 > li:nth-child(2) > input').click()

time.sleep(5)

# iframe 전환
iframes = driver.find_elements(By.TAG_NAME, "iframe")
print("Number of iframes:", len(iframes))
print(iframes)
driver.switch_to.frame('eosFrame')


soup = BeautifulSoup(driver.page_source, "html.parser")

# 1. "OctagonGrid" 테이블에서 행 레이블(연령대 및 지표) 추출
label_rows = soup.select("#OctagonGrid > tbody > tr")
age_measure_labels = []
current_age_group = None

for row in label_rows:
    cells = row.find_all("td")
    if len(cells) == 2:
        # 첫 번째 셀은 연령대(필요시 rowspan 속성으로 여러 행 적용)
        age_td, measure_td = cells
        current_age_group = age_td.get_text(strip=True)
        measure = measure_td.get_text(strip=True)
    elif len(cells) == 1:
        measure = cells[0].get_text(strip=True)
    else:
        continue

    # '합계'와 '연령불명'은 제외
    if current_age_group not in ["합계", "연령불명"]:
        age_measure_labels.append((current_age_group, measure))

# 2. 사고유형 헤더 - 합계 컬럼은 없으므로, 오직 네 가지만 사용
accident_type_headers = ["차대사람", "차대차", "차량단독", "철길건널목"]

# 3. 데이터 테이블 (#dataSession)에서 실제 값 추출
data_rows = soup.select("#dataSession > tbody > tr")

# 첫 번째 행(전체 합계 행)을 건너뛰고, 이후 연령불명 행은 제외하도록, 
# age_measure_labels의 길이에 맞게 슬라이싱 (합계 행은 맨 위에 있으므로 [1: ...])
data_rows = data_rows[1:len(age_measure_labels)+1]

all_data = []
for idx, row in enumerate(data_rows):
    # 각 행의 모든 셀 데이터 읽기 (콤마 제거)
    cells = row.find_all("td")
    values = [td.get_text(strip=True).replace(",", "") for td in cells]
    # 첫 번째 셀은 합계이므로 건너뛰고, 나머지 값들만 사용
    # values[1:] 는 [차대사람, 차대차, 차량단독, 철길건널목] 순서로 존재한다고 가정
    age, measure = age_measure_labels[idx]
    for i, value in enumerate(values[1:]):  
        all_data.append({
            "연령대": age,
            "지표": measure,
            "사고유형": accident_type_headers[i],
            "건수": int(value) if value.isdigit() else None
        })

# 4. DataFrame 생성 및 결과 확인
df = pd.DataFrame(all_data)
print(df.head(10))

'''
내가 DB에 우선적으로 넣어야할 데이터.
- 연령대
- 지표
- 사고유형
- (연도)
'''

# connection =  pymysql.connect(host="127.0.0.1",
#                                      port=3306,
#                                      user="root",
#                                      password="1111",
#                                      db="01_proj")


# cursor = connection.cursor()

    # 데이터 삽입 쿼리
# insert_query = "INSERT INTO AgeGroup (ID, AGE_RANGE)) VALUES (%s, %s)"

insert_sql = "INSERT INTO AgeGroup (ID, AGE_RANGE) VALUES (%s, %s)"

with pymysql.connect(host="127.0.0.1", port=3306, user='root', password='1111', db='01_proj') as conn:
    with conn.cursor() as cursor:
        result = cursor.execute(insert_sql, [1, all_data[0]["연령대"]])
        conn.commit()
        print("처리 행수:", result)
