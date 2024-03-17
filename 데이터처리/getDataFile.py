from getFile import *
while True:
    sigungucode = str(input("시군구코드를 입력하세요 "))

    region=GetSido(sigungucode)
    spotfile = allSpotfile(region)[0]
    foodfile = allSpotfile(region)[1]
    oracle_data=loadDB(sigungucode)
    spotData, foodData = getDataFile(oracle_data,spotfile,foodfile)
    saveFile(region,spotData,foodData)