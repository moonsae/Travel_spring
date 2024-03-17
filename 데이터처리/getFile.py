import pandas as pd
from glob import glob
import cx_Oracle as cx
import requests
import json
import pprint
import numpy

file_path="C:/Users/user/Desktop/데이터파일/강원/"
file_route="/*.csv"
food_path="C:/Users/user/Desktop/데이터파일/음식점/강원/"
food_route=".csv"
data_path="C:/Users/user/Desktop/데이터파일/가공데이터/강원/"

#장소파일과 음식파일을 가공함
def allSpotfile(region):
    file_names=glob(file_path+region+file_route)
    spot=pd.DataFrame()
    for file_name in file_names:
        temp=pd.read_csv(file_name,sep=',',encoding='cp949')
        spot=pd.concat([spot,temp])
    food=pd.read_csv(food_path+region+food_route , encoding='cp949')
    unnamed_columns = [col for col in spot.columns if 'Unnamed' in col]
    spot = spot.drop(columns=unnamed_columns)
    spot=spot[spot['검색건수']>100]
    food=food[food['검색건수']>100]
    spot=spot[spot['소분류 카테고리'] != '공연시설']
    spot=spot[spot['중분류 카테고리'] != '기타관광']
    spot = spot.sort_values(by=['중분류 카테고리', '검색건수'], ascending=[True, False])
    spot = spot[~(spot['관광지명'].str.contains('점') & ~spot['관광지명'].str.contains('본점'))]
    food = food[~(food['관광지명'].str.contains('점') & ~food['관광지명'].str.contains('본점'))]
    return spot, food

#db에 저장된 데이터 가져오기
def loadDB(sidocode):
    dsn=cx.makedsn('localhost',1521,'testdb') #오라클에 대한 주소 정보
    db=cx.connect('scott','tiger')
    cursor=db.cursor() #데이터를 담을 메모리명
    cursor.execute("""SELECT * FROM CONTENTINFOTBL WHERE sigungucode = :sidocode""",{'sidocode': sidocode})
    row=cursor.fetchall() #한 행씩 fetch
    colname=cursor.description #데이터 칼럼명 추출
    oracle_data=pd.DataFrame(row,columns=[desc[0] for desc in cursor.description]) #데이터베이스에 있는 데이터를 데이터프레임형태로 바꿈
    db.close()
    return oracle_data
#db에 저장된 시도에 대한 텍스트 가져오기(예시: 서울, 인천)
def GetSido(sigungucode):
    dsn=cx.makedsn('localhost',1521,'testdb') #오라클에 대한 주소 정보
    db=cx.connect('scott','tiger')
    cursor=db.cursor() #데이터를 담을 메모리명
    cursor.execute("""SELECT name FROM SigunguTbl WHERE sigungucode = :sigungucode""",{'sigungucode': sigungucode})
    row = cursor.fetchone() #한 행씩 fetch
    sido = row[0]
    db.close()
    return sido

#db데이터와 파일데이터 합침
def mergeData(oracle, csv_file):
    data=pd.merge(oracle,csv_file, how='inner',left_on='TITLE', right_on='관광지명', indicator=True)
    #공백을 없애고 다시 합침
    unmatched_csv = csv_file[~csv_file['관광지명'].isin(data['관광지명'])]
    unmatched_oracle = oracle[~oracle['TITLE'].isin(data['TITLE'])]
    unmatched_oracle.loc[:, 'TITLE'] = unmatched_oracle['TITLE'].str.replace(' ', '')
    data2 = pd.merge(unmatched_oracle, unmatched_csv,how='inner',left_on='TITLE', right_on='관광지명',indicator=True)
    total = pd.concat([data,data2])
    columns_to_drop = [9] + list(range(16, 25)) + [28]
    total = total.drop(total.columns[columns_to_drop], axis=1)
    for i, row in total.iterrows():
        if pd.isnull(row['FIRSTIMAGE']):
            #이미지가 없는 관광지의 기본 이미지 설정
            total.at[i, 'FIRSTIMAGE']='http://korean.visitkorea.or.kr/resources/images/common/no_img_01.png'
        if pd.isnull(row['MLEVEL']):
            total.at[i, 'MLEVEL']=6
    total.rename(columns={'중분류 카테고리':'MCATEGORY','소분류 카테고리':'SCATEGORY','검색건수':'SEARCHCOUNT'},inplace=True)
    total.drop_duplicates(subset='CONTENTID', keep='first', inplace=True)
    return total
#음식점 데이터에 있는 카페 정보를 장소 데이터로 옮김
def getDataFile(oracle,spotdata,fooddata):
    spot_data=mergeData(oracle, spotdata)
    food_data=mergeData(oracle, fooddata)
    cafe_data=food_data[food_data['SCATEGORY']=='카페/찻집']
    spot_data = pd.concat([spot_data, cafe_data], ignore_index=True)
    food_data = food_data[food_data['SCATEGORY'] != '카페/찻집']
    return spot_data, food_data
#각 데이터 파일을 csv형태로 저장
def saveFile(region,spotdata,fooddata):
    spotdata.to_csv(data_path+region+'spot'+food_route, encoding='utf-8-sig', index=False)
    fooddata.to_csv(data_path+region+'food'+food_route, encoding='utf-8-sig', index=False)
    print('저장완료') 

## getOverviewList과 getFinalData은 api호출해 각 데이터의 overivew를 저장하기 위한 용도임. 하지만 너무 느려서 주피터로 돌려버림
def getOverviewList(data):
    info_list=[]
    for i in range(len(data)):
        key="개인의 api key"
        url="https://apis.data.go.kr/B551011/KorService1/detailCommon1?serviceKey="+str(key)+"&MobileOS=ETC&MobileApp=AppTest&_type=json&contentId="+str(data.loc[i].CONTENTID)+"&contentTypeId="+str(data.loc[i].CONTENTTYPEID)+"&defaultYN=N&firstImageYN=N&areacodeYN=N&catcodeYN=N&addrinfoYN=N&mapinfoYN=N&overviewYN=Y"
        response=requests.get(url)
        contents = response.text
        rjson = json.loads(contents)
        info_list.append(pd.json_normalize(rjson,['response', 'body', 'items', 'item']))
    info_df=pd.concat(info_list,ignore_index=True)
    return info_df

def getFinalData(data):
    overview=getOverviewList(data)
    print("성공")
    overview['contentid']=overview['contentid'].astype(int)
    final_data = pd.merge(data, overview, how='inner', left_on=['CONTENTID'], right_on=['contentid'], indicator=True)
    columns_to_drop =list(range(18, 20)) + [21]
    final_data = final_data.drop(final_data.columns[columns_to_drop], axis=1)
    final_data.drop_duplicates(subset='CONTENTID', keep='first', inplace=True)
    return final_data


