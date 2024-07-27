import pandas as pd
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec
okt=Okt()
import os
import glob

def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

#최종 데이터 input => 매핑 데이터 path
#가공 처리하고 done 폴더에 저장. rec_attraction_202301.csv 
def final_data(data_path):
    filename = data_path.split('/')[-1]
    rec_data = pd.read_csv(data_path, encoding='utf-8-sig')
    final_data_path=f"C:/Users/user/Desktop/travel_recommendation/final_data/final_{filename}"
    rec_data['OVERVIEW']=rec_data.OVERVIEW.apply(remove_html)
    rec_data['DATA']=None
    
    data_arr=[]
    stop_words = ['이','곳','등','것','마침내','로서','및','도','주','내','점','위','의','위해','면','후','전','여러분','늘','우리',
             '모두','옆','온','조','월','화','수','목','금','토','일','밍','시','인근','원래','때','나머지','평','예약','인터넷','홈페이지'
             ,'모바일','웹','일반인','국민','증진','타','서울시','교육청','관','지역','석','호선','층','공','번','뒤','굿','접속','끌','속',
             '마음껏','국가대표','출신','용','향','때문','더','일요일','월요일','화요일','수요일','목요일','금요일','토요일','휴무','안',
             '출구','개월','동양','아파트','가까이','초등학교','중학교','고등학교','학교','일반','터','위치','현','편','정','누','과','촌',
             '약','단','번','통','끝','정면','오른쪽','왼쪽','뒤','앞','옆','동쪽','서쪽','남쪽','북쪽','철근','콘크리트','대상','교실','학원',
             '연령','밖','시스템','네이버','통해','사전','속','결제','이용','교','지하철','버스','대중교통','자리','친','뿐','더','외','남녀',
             '노소','돌','그','매우','은','서울','부지','단체','명','신청','최대','초등학생','반','나','과연','를','서울특별시','생','사실',
             '볼','망','한눈','시내','경기도','의정부','꽤','또','대학생','중학생','고등학생','자랑','입구','교통','중','무료','시민','여러',
             '주위','정도','만큼','집','전시','로','로부터','곳곳','쓰레기','인접','만날','도보','판매','코트','전용','체력','체육',
             '인조잔디','학습장','훈련','선수','라인','마지막','이후','최초']
    for i in range(len(rec_data)):
        nouns=[]
        for word in okt.nouns(rec_data.iloc[i].OVERVIEW):
            if word not in stop_words:
                nouns.append(word)
        
        if not nouns:  # nouns가 비어 있는 경우
            rec_data.at[i, 'DATA'] = rec_data.iloc[i]['관광지명']
        else:
            str_nouns = " ".join(nouns)
            rec_data.at[i, 'DATA'] = str_nouns
        
    rec_data.to_csv(final_data_path,encoding='utf-8-sig')

def train_and_save_model(attraction_data_path):
    saved_model_path="C:/Users/user/Desktop/travel_recommendation/saved_models/"
    
    data = pd.read_csv(attraction_data_path,encoding='utf-8-sig')
    train_data=data['DATA']
    sentences = []
    for document in train_data:
        words = document.split()  # 혹은 다른 방법으로 단어를 추출해야 하는 경우 사용
        sentences.append(words)
    sentences
    
    filename = attraction_data_path.split('/')[-1]
    tmp = filename.split('_')[-1]
    number = tmp.split('.')[0]
    
    model_name=f"model_{number}.model"
    
    model = Word2Vec(sentences=sentences, vector_size=100, window=5, min_count=3,workers=4, sg=1)
    model.train(sentences,total_examples=model.corpus_count,epochs=50)

    model.save(saved_model_path+model_name)
    api_model_path = 'C:/Users/user/Desktop/TourRec/models/'  
    models_to_delete = glob.glob(os.path.join(api_model_path, '*'))
    for file_path in models_to_delete:
        try:
            os.remove(file_path)  # 파일 삭제
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
    model.save(f"{api_model_path}recw2v.model")
    
def update_server_data(year, month):
    # year와 month를 이용하여 파일명 생성
    attraction_filename = f"C:/Users/user/Desktop/travel_recommendation/final_data/final_attraction_{year}{month}.csv"
    restaurant_filename = f"C:/Users/user/Desktop/travel_recommendation/final_data/final_restaurant_{year}{month}.csv"
  
    api_data_path = 'C:/Users/user/Desktop/TourRec/data'  
    
    files_to_delete = glob.glob(os.path.join(api_data_path, '*'))
    for file_path in files_to_delete:
        try:
            os.remove(file_path)  # 파일 삭제
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    try:
        # rec_attraction.csv 저장
        attraction_df = pd.read_csv(attraction_filename)
        attraction_df.to_csv(os.path.join(api_data_path, 'rec_attraction.csv'), index=False, encoding='utf-8-sig')
        
        # rec_restaurant.csv 저장
        restaurant_df = pd.read_csv(restaurant_filename)
        restaurant_df.to_csv(os.path.join(api_data_path, 'rec_restaurant.csv'), index=False, encoding='utf-8-sig')

    except Exception as e:
        print(f"Failed to update data on the server. Reason: {e}")
    

    
    