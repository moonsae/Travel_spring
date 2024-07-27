import os
import pandas as pd
import cx_Oracle as cx
import datetime
import re
import requests
import json

def check_data_log(message):
    with open("check.txt", "a", encoding="utf-8-sig") as file:
        file.write(message)
        

def getSido(sidocode, cursor):
    cursor.execute("""SELECT nickname FROM sidotbl where sidocode = :sidocode""", {'sidocode': sidocode})
    row = cursor.fetchone()  
    if row:
        return row[0]
    return None

def getSigungu(sigungucode, cursor):
    cursor.execute("""SELECT name FROM SigunguTbl WHERE sigungucode = :sigungucode""", {'sigungucode': sigungucode})
    row = cursor.fetchone()  
    if row:
        return row[0]
    return None

def preData(filtered_df):
    filtered_df_sorted = filtered_df.sort_values(by='검색건수', ascending=False)
    count_100 = (filtered_df_sorted['검색건수'] >= 80).sum()
    if count_100 < 40:
        filtered_df_sorted = filtered_df_sorted.head(40)
    else:
        filtered_df_sorted = filtered_df_sorted[filtered_df_sorted['검색건수'] >= 80]
    return filtered_df_sorted
def clean_string(s):
    if isinstance(s, str):
        # 특수기호 이후의 문자 제거
        s = re.sub(r'\(.*?\)', '', s)
        s = re.sub(r'\[.*?\]', '', s)
        s = re.sub(r'\{.*?\}', '', s)
        s = re.sub(r'<.*?>', '', s)
        # 공백 및 특수문자 제거
        s = re.sub(r'\s+', '', s).lower()
    return s


def mappingAndSaveData(file_path, oracle_data, processed_data):
    # CSV 파일 불러오기
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    
    # 'OVERVIEW' 열을 문자열 타입으로 변환
    df['OVERVIEW'] = df['OVERVIEW'].astype(str)
    
    # 데이터 클린업
    processed_data['cleaned_관광지명'] = processed_data['관광지명'].apply(clean_string)
    oracle_data['cleaned_TITLE'] = oracle_data['TITLE'].apply(clean_string)

    for idx, row in processed_data.iterrows():
        filtered_name_cleaned = row['cleaned_관광지명']
        
        # TITLE에서 공백 및 특수문자 제거 후 비교하여 일치하는 데이터 찾기
        match_name = oracle_data[oracle_data['cleaned_TITLE'] == filtered_name_cleaned]
        if not match_name.empty:
            # 업데이트할 데이터가 있는 경우 첫 번째 데이터만 사용
            df.at[idx, 'CONTENTID'] = int(match_name.iloc[0]['CONTENTID'])
            df.at[idx, 'CONTENTTYPEID'] = int(match_name.iloc[0]['CONTENTTYPEID'])
            df.at[idx, 'OVERVIEW'] = str(match_name.iloc[0]['OVERVIEW'])
            df.at[idx, 'SIDOCODE'] = int(match_name.iloc[0]['SIDOCODE'])
            df.at[idx, 'SIGUNGUCODE'] = int(match_name.iloc[0]['SIGUNGUCODE'])
                        
        
   
    
    # 업데이트된 데이터프레임을 CSV 파일로 저장
    df.to_csv(file_path, index=False, encoding='utf-8-sig')  # utf-8 인코딩 사용
    print(f"Updated dataframe saved to {file_path}")

def data_preprocessing_and_mapping(year, month):
    message=""
    merged_data_path = "C:/Users/user/Desktop/travel_recommendation/merged_data/" + year + "/" + month
    # 폴더 존재 여부 확인, 폴더 내에 있는 지역 데이터를 모두 합하여 저장하는 역할
    if os.path.exists(merged_data_path):
        with open("district_code.txt", 'r') as file:
            lines = file.readlines()
        dsn = cx.makedsn('localhost', 1521, 'testdb')  # 오라클에 대한 주소 정보
        db = cx.connect('scott', 'tiger')
        cursor = db.cursor()  # 데이터를 담을 메모리명
        for line in lines:
            line = int(line.strip())
            if line < 40:
                city = getSido(line, cursor)
                attraction_file_name = os.path.join(merged_data_path, f"{city}_Attraction_{year}{month}.csv")
                restaurant_file_name = os.path.join(merged_data_path, f"{city}_Restaurant_{year}{month}.csv")
                if os.path.exists(restaurant_file_name):
                    print(city)
                    attraction_file = pd.read_csv(attraction_file_name, encoding='utf-8-sig')
                    restaurant_file = pd.read_csv(restaurant_file_name, encoding='utf-8-sig')
                    attraction_df = preData(attraction_file)
                    restaurant_df = preData(restaurant_file)
                    cursor.execute("""SELECT * FROM CONTENTINFOTBL WHERE sidocode = :sidocode""", {'sidocode': line})
                    row = cursor.fetchall()  # 한 행씩 fetch
                    colname = cursor.description  # 데이터 칼럼명 추출
                    content_data = pd.DataFrame(row, columns=[desc[0] for desc in cursor.description])
                else:
                    continue
            else:
                district = getSigungu(line, cursor)
                city = getSido(line // 1000, cursor)
                attraction_file_name = os.path.join(merged_data_path, f"{city}_Attraction_{year}{month}.csv")
                restaurant_file_name = os.path.join(merged_data_path, f"{city}_Restaurant_{year}{month}.csv")
                if os.path.exists(restaurant_file_name):
                    print(city, district)
                    attraction_file = pd.read_csv(attraction_file_name, encoding='utf-8-sig')
                    restaurant_file = pd.read_csv(restaurant_file_name, encoding='utf-8-sig')
                    attraction_filtered_df = attraction_file[attraction_file['시/군/구'] == district]
                    restaurant_filtered_df = restaurant_file[restaurant_file['시/군/구'] == district]
                    check_attraction_filtered_df = attraction_filtered_df[attraction_filtered_df['소분류 카테고리'] != '카페/찻집']
                    if len(check_attraction_filtered_df) == 0 or len(restaurant_filtered_df) == 0:
                        message=f"{city} - {district} 데이터 없음\n"
                        check_data_log(message)
                        continue
                    attraction_df = preData(attraction_filtered_df)
                    restaurant_df = preData(restaurant_filtered_df)
                    cursor.execute("""SELECT * FROM CONTENTINFOTBL WHERE sigungucode = :sigungucode""", {'sigungucode': line})
                    row = cursor.fetchall()  # 한 행씩 fetch
                    colname = cursor.description  # 데이터 칼럼명 추출
                    content_data = pd.DataFrame(row, columns=[desc[0] for desc in cursor.description])
                else:
                    continue
            
            # 데이터 필터링
            attraction_df = attraction_df[attraction_df['소분류 카테고리'] != '공연시설']
            attraction_df = attraction_df[attraction_df['소분류 카테고리'] != '쇼핑몰']
            attraction_df = attraction_df[attraction_df['소분류 카테고리'] != '백화점']
            attraction_df = attraction_df[attraction_df['중분류 카테고리'] != '기타관광']
            attraction_df = attraction_df[~(attraction_df['관광지명'].str.contains('점') & ~attraction_df['관광지명'].str.contains('본점'))]
            restaurant_df = restaurant_df[~(restaurant_df['관광지명'].str.contains('점') & ~restaurant_df['관광지명'].str.contains('본점'))]
            
            # 데이터 매핑 및 저장
            mappingAndSaveData(attraction_file_name, content_data, attraction_df)
            mappingAndSaveData(restaurant_file_name, content_data, restaurant_df)
            
            
            
        db.close()
    else:
        print("해당 날짜의 정보가 없음")
        
        
def update_data_to_api(data_file_path):
    # 파일 데이터 불러오기
    data = pd.read_csv(data_file_path, encoding='utf-8-sig')
    for i in range(len(data)):
        # OVERVIEW가 빈 칸인 경우에만 API 호출
        if pd.isna(data.loc[i, 'OVERVIEW']) or data.loc[i, 'OVERVIEW'].strip() == '':
            key = "IPBFFgHWZCZ%2BRHt7qbizPtt0CDstpVbqy4sgYZTYVINFyZgaCtYhQJxJxLKsxvQh1hE7QJHI%2FpZ7F70VcTrPlQ%3D%3D"
            url = (
                "https://apis.data.go.kr/B551011/KorService1/detailCommon1?serviceKey="
                + str(key)
                + "&MobileOS=ETC&MobileApp=AppTest&_type=json&contentId="
                + str(data.loc[i, 'CONTENTID'])
                + "&contentTypeId="
                + str(data.loc[i, 'CONTENTTYPEID'])
                + "&defaultYN=N&firstImageYN=N&areacodeYN=N&catcodeYN=N&addrinfoYN=N&mapinfoYN=N&overviewYN=Y"
            )

            try:
                response = requests.get(url)
                response.raise_for_status()  # HTTP 에러 발생 시 예외 발생

                contents = response.text
                rjson = json.loads(contents)

                # API 응답에서 'overview' 가져오기
                if (
                    'response' in rjson and
                    'body' in rjson['response'] and
                    'items' in rjson['response']['body'] and
                    'item' in rjson['response']['body']['items']
                ):
                    item = rjson['response']['body']['items']['item'][0]
                    overview = item.get('overview', '')

                    # 데이터 업데이트
                    #data.loc[i, 'OVERVIEW'] = overview
                    cleaned_overview = overview.replace("\n", "")
                    data.loc[i, 'OVERVIEW'] = cleaned_overview

                else:
                    check_data_log(f"API 응답 형식 오류: contentid={data.loc[i, 'CONTENTID']}, 관광지명={data.loc[i, '관광지명']}")

            except requests.RequestException as e:
                check_data_log(f"API 호출 실패: contentid={data.loc[i, 'CONTENTID']}, 관광지명={data.loc[i, '관광지명']}, 오류: {e}")

    # 업데이트된 데이터를 저장
    data.to_csv(data_file_path, encoding='utf-8-sig', index=False) 
    print(f"API 호출 성공: 데이터가 {data_file_path}에 저장되었습니다.")
    
def update_oracle_data(attraction_path, restaurant_path):
    # Oracle 연결 설정
    dsn = cx.makedsn('localhost', 1521, 'testdb')
    db = cx.connect('scott', 'tiger', dsn=dsn)
    cursor = db.cursor()

    try:
        # REC 값을 일괄적으로 3으로 업데이트
        cursor.execute("UPDATE contentinfotbl SET rec = 3")
        db.commit()

        # 1. attraction_path의 CSV 파일 처리
        attraction_data = pd.read_csv(attraction_path, encoding='utf-8-sig')
        for index, row in attraction_data.iterrows():
            contentid = row['CONTENTID']
            overview = row['OVERVIEW']

            # REC 업데이트
            cursor.execute("UPDATE contentinfotbl SET rec = 1 WHERE CONTENTID = :contentid", {'contentid': contentid})

            # OVERVIEW 업데이트 (만약 오라클의 OVERVIEW가 NULL인 경우에만 업데이트)
            cursor.execute("UPDATE contentinfotbl SET OVERVIEW = :overview WHERE CONTENTID = :contentid AND OVERVIEW IS NULL", {'overview': overview, 'contentid': contentid})

        # 변경사항 저장
        db.commit()

        # 2. restaurant_path의 CSV 파일 처리
        restaurant_data = pd.read_csv(restaurant_path, encoding='utf-8-sig')
        for index, row in restaurant_data.iterrows():
            contentid = row['CONTENTID']
            overview = row['OVERVIEW']

            # REC 업데이트
            cursor.execute("UPDATE contentinfotbl SET rec = 2 WHERE CONTENTID = :contentid", {'contentid': contentid})

            # OVERVIEW 업데이트 (만약 오라클의 OVERVIEW가 NULL인 경우에만 업데이트)
            cursor.execute("UPDATE contentinfotbl SET OVERVIEW = :overview WHERE CONTENTID = :contentid AND OVERVIEW IS NULL", {'overview': overview, 'contentid': contentid})

        # 변경사항 저장
        db.commit()

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        db.rollback()  # 롤백 처리

    finally:
        # Oracle 연결 해제
        cursor.close()
        db.close()
     
#merged_data_path에 저장된 데이터를 모두 합친 후 mapping_data_path에 저장
def merge_mapping_data(year,month):
    merged_data_path = "C:/Users/user/Desktop/travel_recommendation/merged_data/" + year + "/" + month
    mapping_data_path="C:/Users/user/Desktop/travel_recommendation/mapped_data/"
    
    # 결과 파일 이름
    attraction_output_filename = f"attraction_{year}{month}.csv"
    restaurant_output_filename = f"restaurant_{year}{month}.csv" 
    
    # 빈 DataFrame 생성
    attraction_df = pd.DataFrame()
    restaurant_df = pd.DataFrame()
    
    # 입력 폴더 내의 파일 목록 가져오기
    file_list = os.listdir(merged_data_path)
    # 파일을 하나씩 처리
    for file_name in file_list:
        if file_name.endswith(".csv"):
            file_path = os.path.join(merged_data_path, file_name)
        
            # 파일 이름을 기준으로 Attraction 또는 Restaurant인지 판별
            if "Attraction" in file_name:
                # Attraction 파일을 읽어서 DataFrame에 추가
                df = pd.read_csv(file_path)
                attraction_df = pd.concat([attraction_df, df], ignore_index=True)
            elif "Restaurant" in file_name:
                # Restaurant 파일을 읽어서 DataFrame에 추가
                df = pd.read_csv(file_path)
                restaurant_df = pd.concat([restaurant_df, df], ignore_index=True)

    # Step 1: contentid가 0인 데이터 삭제
    attraction_df = attraction_df[attraction_df['CONTENTID'] != 0]
    restaurant_df = restaurant_df[restaurant_df['CONTENTID'] != 0]

    # Step 2: 중복된 contentid가 있는 데이터 삭제
    attraction_df = attraction_df.drop_duplicates(subset=['CONTENTID'], keep='first')
    restaurant_df = restaurant_df.drop_duplicates(subset=['CONTENTID'], keep='first')
    
    # Step 3: 특정 열 삭제
    columns_to_drop = ['순위', '도로명주소', '중분류 카테고리', '소분류 카테고리']
    attraction_df = attraction_df.drop(columns=columns_to_drop)
    restaurant_df = restaurant_df.drop(columns=columns_to_drop)

    # 결과 파일을 저장할 경로 및 파일명 설정
    attraction_output_path = os.path.join(mapping_data_path, attraction_output_filename)
    restaurant_output_path = os.path.join(mapping_data_path, restaurant_output_filename)

    # 결과 파일 저장
    attraction_df.to_csv(attraction_output_path, index=False, encoding='utf-8-sig')
    restaurant_df.to_csv(restaurant_output_path, index=False, encoding='utf-8-sig')

    print(f"Attraction 데이터가 {attraction_output_path}에 저장되었습니다.")
    print(f"Restaurant 데이터가 {restaurant_output_path}에 저장되었습니다.")
    
    update_data_to_api(attraction_output_path)
    update_data_to_api(restaurant_output_path)
    
    update_oracle_data(attraction_output_path,restaurant_output_path)
