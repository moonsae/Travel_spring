from filter_sort_classify import *
from data_preprocessing_and_mapping import *
from prepare_and_train import *

print("연도와 월을 입력하세요. ex)2023-01")
year, month =map(str,input().split('-'))
filter_sort_classify(year,month)
data_preprocessing_and_mapping(year,month)
print("계속 진행하시겠습니까? 그러면 0을 제외한 숫자를 입력해주세요. 0을 누르면 종료됩니다.")
select=int(input())
if select !=0:
    merge_mapping_data(year,month)
    att_file=find_file("mapped_data","attraction",year,month)
    res_file=find_file("mapped_data","restaurant",year,month)
    final_data(att_file)
    final_data(res_file)
    final_file=find_file("final_data","final_attraction",year,month)
    train_and_save_model(final_file)
    update_server_data(year, month)
else:
    print("종료")


    