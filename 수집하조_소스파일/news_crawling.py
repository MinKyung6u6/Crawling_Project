import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def newsCrawling(result,code,page):
    for idx in range(1,page+1):
        newsURL='https://finance.naver.com/item/news_news.naver?code=%s&page=%s&sm=title_entity_id.basic&clusterId='%(code,idx)
        response=urllib.request.urlopen(newsURL)
        soupData=BeautifulSoup(response,'html.parser')

        title=soupData.findAll('td',attrs={'class','title'})
        info=soupData.findAll('td',attrs={'class':'info'})
        date=soupData.findAll('td',attrs={'class','date'})

        for i in range(len(title)):
            news_title=title[i].getText()
            news_link='https://finance.naver.com/'+title[i].find("a")["href"]
            news_info=info[i].string
            news_date=date[i].string
            result.append([news_title]+[news_link]+[news_info]+[news_date])

        print("[%s page] 완료 !" % idx)


def main():
    result = []

    company = input("기업의 이름을 정확히 입력하세요 : ")
    data = {
            '카카오': {
                'code': '035720',
                'page': 329
            },
            '카카오게임즈':{
                'code':'293490',
                'page':56
            },
            '카카오뱅크': {
                'code': '323410',
                'page': 168
            },
            '카카오페이': {
                'code': '377300',
                'page': 129
            }
        }

    print('===========================================================')
    print('================== 뉴스 크롤링을 시작합니다. ==================')
    print('===========================================================')

    newsCrawling(result,data[company]['code'],data[company]['page'])

    print('===========================================================')
    print('================== 뉴스 크롤링이 끝났습니다. ==================')
    print('===========================================================')


    tbl = pd.DataFrame(result, columns=('제목', '링크', '정보제공', '날짜'))
    tbl = tbl.applymap(lambda x: x.replace('\xa0',''))   # <<'cp949' codec can't encode character '\xa0' csv>> 오류 해결법
    tbl.to_csv('./%s_뉴스.csv'%company, encoding='cp949', mode='w', index=True)

if __name__ == '__main__':
    main()
