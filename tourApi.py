import urllib.request
import datetime
import json
import pandas as pd

# import requests
#
# url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
# params ={'serviceKey' : 'cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA==', 'YM' : '202403', 'NAT_CD' : '112', 'ED_CD' : 'E' }
#
# response = requests.get(url, params=params)
# print(response.content)

def getRequestUrl(url):
    req = urllib.request.Request(url) # api 요청 생성
    try:
        response = urllib.request.urlopen(req)  # api 서버로 부터 반환된 응답(결과)
        if response.getcode() == 200:  # 정상적인 응답 도착
            print(f"요청에 대한 응답 성공일시 : {datetime.datetime.now()}")
            return response.read().decode("utf-8")
    except Exception as e:
        print(e)  # 에러의 내용 출력
        print(f"에러 발생 url : {url} {datetime.datetime.now()}")
        return None

# print(getRequestUrl("http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList?YM=202403&NAT_CD=112&ED_CD=E&serviceKey="))

def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    baseUrl = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey="  # 본인 key 입력
    parameters = parameters + f"&YM={yyyymm}"
    parameters = parameters + f"&NAT_CD={nat_cd}"
    parameters = parameters + f"&ED_CD={ed_cd}"

    url = baseUrl + parameters

    responseDecode = getRequestUrl(url)
    
    if responseDecode == None: # 참이면 에러 발생!
        return None
    else:  # 정상적인 응답 성공
        return json.loads(responseDecode)


# print(getTourismStatsItem("202403", "112", "E"))
# 
# num = getTourismStatsItem("202403", "112", "E")
# num2 = num["response"]["body"]["items"]["item"]["num"]
# print(num2)

result = []
jsonResult = []
# 시작 년월과 종료 년월을 인수로 넣으면 해당 기간 동안의 출입국 관광객 수를 가져오는 함수
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):  # 국가코드, 출입국여부, 시작년도, 종료년도
    for year in range(int(nStartYear), int(nEndYear)+1): # 2020, 2023
        for month in range(1, 13):  # 1~12월
            yyyymm = f"{year}"+f"{month:0>2}"
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)

            if jsonData["response"]["body"]["items"] == "":
                print(f"현재 제공되는 데이터는 {year}년 {month-1}월 까지만 제공됩니다.")
                break

            # print(jsonData)
            natName = jsonData["response"]["body"]["items"]["item"]["natKorNm"]  # 나라 이름
            num = jsonData["response"]["body"]["items"]["item"]["num"]  # 출입국자 수
            natCd = jsonData["response"]["body"]["items"]["item"]["natCd"]  # 국가코드
            ym = jsonData["response"]["body"]["items"]["item"]["ym"]  # 해당 년월
            jsonResult.append({"nat_name":natName, "nat_cd":natCd, "yyyymm":ym, "visit_num":num})
            result.append([natName, natCd, ym, num])
            print(yyyymm)

    return jsonResult

resultTest = getTourismStatsService("112","E", "2023", "2024")
print(resultTest)
print(result)

result_df = pd.DataFrame(result, columns=["국가명","국가코드","년월일","관광객수"])
print(result_df)
result_df.to_csv("2023-2024년_출입국자수.csv",index=False, encoding="cp949")
