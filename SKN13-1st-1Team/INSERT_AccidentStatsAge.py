import pandas as pd
import pymysql


def insert_in_table(all_data):
    connection =  pymysql.connect(host="192.168.0.25",
                                        port=3306,
                                        user="test-connection",
                                        password="12345678",
                                        db="01_proj")

    df = pd.DataFrame(all_data)
    print(df)
    cursor = connection.cursor()


    # AgeGroup INSERT
    age_groups = df["연령대"].unique()
    print(age_groups)
    age_group_map = {age: f"AG{i+1}" for i, age in enumerate(age_groups)}

    for age, age_id in age_group_map.items():
        cursor.execute(
            "INSERT INTO AgeGroup (id, age_range) VALUES (%s, %s)",
            (age_id, age)
        )

    # AccidentType INSERT (합계 제외)
    accident_type_headers = ["차대사람", "차대차", "차량단독", "철길건널목"]
    accident_type_map = {atype: f"AT{i+1}" for i, atype in enumerate(accident_type_headers)}

    for atype, atype_id in accident_type_map.items():
        cursor.execute(
            "INSERT INTO AccidentType (type_name) VALUES (%s)",
            (atype,)
        )

    # 사고/사망/부상 지표를 하나의 행으로 합치기
    pivoted = df[df["사고유형"] != "합계"].pivot_table(
        index=["연령대", "사고유형"],
        columns="지표",
        values="건수",
        aggfunc="first"
    ).reset_index()

    # 정수 처리 (예외 대응 포함)
    pivoted["사고[건]"] = pd.to_numeric(pivoted["사고[건]"], errors="coerce")
    pivoted["사망[명]"] = pd.to_numeric(pivoted["사망[명]"], errors="coerce")
    pivoted["부상[명]"] = pd.to_numeric(pivoted["부상[명]"], errors="coerce")

    for _, row in pivoted.iterrows():
        age_id = age_group_map[row["연령대"]]
        type_id = accident_type_map[row["사고유형"]]
        accident_count = row["사고[건]"]
        death_count = row["사망[명]"]
        injury_count = row["부상[명]"]

        print(f"[{age_id} | {type_id}] 사고: {accident_count}, 사망: {death_count}, 부상: {injury_count}")


    connection.close()