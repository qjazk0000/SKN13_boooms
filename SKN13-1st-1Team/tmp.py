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
    # if current_age_group not in ["합계", "연령불명"]:
    #     age_measure_labels.append((current_age_group, measure))
    
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
print(df.head(24))

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

# insert_sql = "INSERT INTO AgeGroup (ID, AGE_RANGE) VALUES (%s, %s)"

# with pymysql.connect(host="127.0.0.1", port=3306, user='root', password='1111', db='01_proj') as conn:
#     with conn.cursor() as cursor:
#         for i in range(0, int(len(all_data)/8)):
#             result = cursor.execute(insert_sql, [i+1, all_data[i+12]["연령대"]])
#             conn.commit()
#             print("처리 행수:", result)

#################################################################################################################################################
# unique_age_groups = df["연령대"].unique()

# MySQL 연결 정보
conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    db="01_proj",
    charset="utf8mb4"
)

with conn.cursor() as cursor:
    # AgeGroup 테이블에 연령대 데이터 삽입
    age_groups = [
        ("1", "20세이하"),
        ("2", "21~30세"),
        ("3", "31~40세"),
        ("4", "41~50세"),
        ("5", "51~60세"),
        ("6", "61~64세"),
        ("7", "65이상"),
        ("8", "연령불명")
    ]
    # insert_age_sql = "INSERT INTO AgeGroup (id, age_range) VALUES (%s, %s)"
    # for group in age_groups:
    #     cursor.execute(insert_age_sql, group)

    # # YearType 테이블에 2014년부터 2023년까지 데이터 삽입
    # years = [str(year) for year in range(2014, 2024)]
    # insert_year_sql = "INSERT INTO YearType (id) VALUES (%s)"
    # for year in years:
    #     cursor.execute(insert_year_sql, (year,))

    # conn.commit()

# conn.close()
print("AgeGroup 및 YearType 테이블에 데이터 삽입 완료!")



# 각 사고 유형을 그대로 삽입합니다.
accident_types = ["사고유형", "차대차", "차대사람", "차량단독", "철길건널목"]

# insert_sql = "INSERT INTO AccidentType (type_name) VALUES (%s)"

# with conn.cursor() as cursor:
#     for type_name in accident_types:
#         cursor.execute(insert_sql, (type_name,))
#     conn.commit()

# conn.close()
print("AccidentType 테이블에 사고 유형 데이터 삽입 완료!")

##########################################################################################################################################



df_filtered = df[df["사고유형"].isin(accident_type_headers)]

# pivot_table: index = [연령대, 사고유형], columns = 지표, values = 건수
pivot = df_filtered.pivot_table(
    index=["연령대", "사고유형"],
    columns="지표",
    values="건수",
    aggfunc="first"    # 각 조합당 값이 하나씩 있다고 가정
).reset_index()

# pivot 결과에는 "사고[건]", "사망[명]", "부상[명]" 컬럼이 생성됨.
pivot.rename(columns={
    "사고[건]": "accident_count",
    "부상[명]": "injury_count",
    "사망[명]": "death_count"
}, inplace=True)

# NaN 값은 0으로 치환하고 정수형으로 변환
pivot = pivot.fillna(0)
pivot["accident_count"] = pivot["accident_count"].astype(int)
pivot["injury_count"] = pivot["injury_count"].astype(int)
pivot["death_count"] = pivot["death_count"].astype(int)

##############################################
# 4. 추가 컬럼 생성 및 최종 DataFrame 구성
##############################################
# 연령대를 AgeGroup 테이블의 id와 매핑 (여기서는 예시 매핑)
age_group_map = {
    "20세이하": "1",
    "21~30세": "2",
    "31~40세": "3",
    "41~50세": "4",
    "51~60세": "5",
    "61~64세": "6",
    "65세이상": "7",
    "연령불명": "8"
}

pivot["age_group_id"] = pivot["연령대"].map(lambda x: age_group_map.get(x.strip(), None))

# 연도 데이터: 모두 "2023"
pivot["year_type_id"] = "2023"

# 고유 id 생성: "ASTAGE0001", "ASTAGE0002", ...
pivot["id"] = [str(i+1) for i in range(len(pivot))]

# 사고유형 컬럼명을 accident_type_name으로 재명명
pivot.rename(columns={"사고유형": "accident_type_name"}, inplace=True)

# 최종 DataFrame 선택
final_df = pivot[[
    "id",
    "accident_type_name",
    "age_group_id",
    "year_type_id",
    "accident_count",
    "injury_count",
    "death_count"
]]

final_df = final_df.fillna(0)
final_df["accident_count"] = final_df["accident_count"].astype(int)
final_df["injury_count"] = final_df["injury_count"].astype(int)
final_df["death_count"] = final_df["death_count"].astype(int)

# MySQL 연결 설정 (환경에 맞게 수정)
conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="1111",
    db="01_proj",
    charset="utf8mb4"
)
cursor = conn.cursor()

# INSERT 쿼리 (AccidentStatsAge 테이블)
insert_sql = """
INSERT INTO AccidentStatsAge
(id, accident_type_name, age_group_id, year_type_id, accident_count, injury_count, death_count)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

# print(final_df)

# final_df의 각 행을 순회하며 데이터 삽입
for index, row in final_df.iterrows():
    print(row["id"], row["accident_type_name"], row["age_group_id"], row["year_type_id"], row["accident_count"], row["injury_count"], row["death_count"])

    cursor.execute(insert_sql, (
        row["id"],
        row["accident_type_name"],
        row["age_group_id"],
        row["year_type_id"],
        row["accident_count"],
        row["injury_count"],
        row["death_count"]
    ))
    break

conn.commit()
cursor.close()
conn.close()

print("AccidentStatsAge 테이블에 데이터가 성공적으로 삽입되었습니다.")