import pandas as pd 
from sqlalchemy import create_engine

df = pd.read_csv(r"C:\Workspace\Python\SKN13_boooms\SKN13-1st-1Team\accidents_by_age_and_type2014.csv")

# DB 연결정보
user = 'root'
password = '1111'
host = 'localhost' 
port = 3306
database = '01_proj'

# SQLAlchemy 엔진 생성
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4")

# 테이블 사용 (없으면 자동생성)
df.to_sql('accidentstatsage',con=engine,index=False,if_exists='replace')