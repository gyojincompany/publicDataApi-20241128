import urllib.request
import datetime

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

# print(getRequestUrl("http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList?YM=202403&NAT_CD=112&ED_CD=E&serviceKey=cTWUGiJR%2FGRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA%3D%3D"))

def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    baseUrl = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?&serviceKey=cTWUGiJR%2FGRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA=="
    parameters = parameters + f"&YM={yyyymm}"
    parameters = parameters + f"&NAT_CD={nat_cd}"
    parameters = parameters + f"&ED_CD={ed_cd}"

    url = baseUrl + parameters

    responseDecode = getRequestUrl(url)
