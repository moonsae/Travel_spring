import os
import pandas as pd
import cx_Oracle as cx
import glob
import datetime

def find_file(category, file_name, year, month):
    base_path = "C:/Users/user/Desktop/travel_recommendation"
    
    path = os.path.join(base_path, category)
    
    file_name = f"{file_name}_{year:04d}{month:02d}.csv"
    
    file_path = os.path.join(path, file_name)
    
    if os.path.exists(file_path):
        return file_path
    else:
        return None
    
def execution_log(year, month):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{current_time} {year}-{month}에 관한 작업실행\n---------------------------------------\n"
    with open("check.txt", "a", encoding="utf-8-sig") as file:
        file.write(log_entry)
def check_data_log(city, message):
    log_entry = f"{city} {message}\n"
    with open("check.txt", "a", encoding="utf-8-sig") as file:
        file.write(log_entry)
        
def getSido(sidocode, cursor):
    cursor.execute("""SELECT nickname FROM sidotbl where sidocode = :sidocode""", {'sidocode': sidocode})
    row = cursor.fetchone()  
    if row:
        return row[0]
    return None

def save_merged_csv(df, output_file_name, output_path):
    if not df.empty:
        os.makedirs(output_path, exist_ok=True)
        df.to_csv(os.path.join(output_path, output_file_name), index=False, encoding='utf-8-sig')
        print(f"{output_file_name} 파일이 성공적으로 저장되었습니다.")
        
def getCafeData(attraction_df,restaurant_df):
    cafe_data=restaurant_df[restaurant_df['소분류 카테고리']=='카페/찻집']
    attraction_df = pd.concat([attraction_df, cafe_data], ignore_index=True)
    restaurant_df = restaurant_df[restaurant_df['소분류 카테고리'] != '카페/찻집']
    return attraction_df, restaurant_df


def filter_sort_classify(year,month):
    execution_log(year, month)
    message=''
    attraction_path = "C:/Users/user/Desktop/travel_recommendation/raw_data/attraction/"
    attraction_folder = attraction_path + year + "/" + month
    restaurant_path = "C:/Users/user/Desktop/travel_recommendation/raw_data/restaurant/"
    restaurant_folder = restaurant_path + year + "/" + month
    merged_data_path="C:/Users/user/Desktop/travel_recommendation/merged_data/"+ year + "/" + month

    # 폴더 존재 여부 확인, 폴더 내에 있는 지역 데이터를 모두 합하여 저장하는 역할
    if os.path.exists(attraction_folder) and os.path.exists(restaurant_folder):
        file = open("city_code.txt", 'r')
        lines = file.readlines()
        dsn=cx.makedsn('localhost',1521,'testdb') #오라클에 대한 주소 정보
        db=cx.connect('scott','tiger')
        cursor=db.cursor() #데이터를 담을 메모리명
        for line in lines:
            line = int(line.strip())
            sido=getSido(line,cursor)
            attraction_sido=attraction_folder+"/"+sido 
            restaurant_sido=restaurant_folder+"/"+sido 
            if os.path.exists(attraction_sido) and os.path.exists(restaurant_sido):
                attraction_folder_info=os.listdir(attraction_sido)
                restaurant_folder_info=os.listdir(restaurant_sido)
                if len(attraction_folder_info)==0 or len(restaurant_folder_info)==0: #해당 폴더 비어있음
                    message="데이터 파일이 존재하지 않음"
                    check_data_log(sido,message)
                else:
                    attraction_csv_found = any(file.endswith('.csv') for file in attraction_folder_info)
                    restaurant_csv_found = any(file.endswith('.csv') for file in restaurant_folder_info)
                    if not attraction_csv_found or not restaurant_csv_found : #관광지 csv파일 존재하지 않음, 다른 형식의 파일이 존재
                        message="잘못된 데이터 형식의 파일이 존재함"
                        check_data_log(sido,message)
                    else:
                        attraction_csv_files = glob.glob(f"{attraction_sido}/*.csv")
                        restaurant_csv_files = glob.glob(f"{restaurant_sido}/*.csv")

                        # 모든 CSV 파일을 읽어서 하나의 데이터프레임으로 결합
                        attraction_combined_csv = pd.concat((pd.read_csv(f, encoding='cp949') for f in attraction_csv_files), ignore_index=True)
                        restaurant_combined_csv = pd.concat((pd.read_csv(f, encoding='cp949') for f in restaurant_csv_files), ignore_index=True)

                        #카페 데이터 처리
                        attraction_combined_csv,restaurant_combined_csv=getCafeData(attraction_combined_csv,restaurant_combined_csv)
                        
                        attraction_combined_csv['CONTENTID'] = 0
                        attraction_combined_csv['CONTENTTYPEID'] = 0
                        attraction_combined_csv['OVERVIEW'] = ''
                        attraction_combined_csv['SIDOCODE'] = 0
                        attraction_combined_csv['SIGUNGUCODE'] = 0
    
                        restaurant_combined_csv['CONTENTID'] = 0
                        restaurant_combined_csv['CONTENTTYPEID'] = 0
                        restaurant_combined_csv['OVERVIEW'] = ''
                        attraction_combined_csv['SIDOCODE'] = 0
                        attraction_combined_csv['SIGUNGUCODE'] = 0
                        
                        # 결합된 데이터프레임을 새로운 CSV 파일로 저장
                        attraction_file_name = sido+"_Attraction_"+year+month+".csv"
                        restaurant_file_name = sido+"_Restaurant_"+year+month+".csv"
                        save_merged_csv(attraction_combined_csv, attraction_file_name, merged_data_path)
                        save_merged_csv(restaurant_combined_csv, restaurant_file_name, merged_data_path)
            else:
                message="데이터 파일 경로 존재하지 않음"
                check_data_log(sido,message)
        db.close()
        file.close()
    else:
        print("해당 폴더가 존재하지 않습니다.")

