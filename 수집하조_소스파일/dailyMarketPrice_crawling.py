import requests
from bs4 import BeautifulSoup
import pandas as pd

def dailyMarketPriceCrawling(result,code):
    dailyMarketPriceURL = 'https://finance.naver.com/item/sise_day.naver?code=%s&page=1' % code
    response = requests.get(dailyMarketPriceURL, headers={'User-agent': 'Mozilla/5.0'})
    soupData = BeautifulSoup(response.text, 'html.parser')

    pgrr = soupData.find('td', attrs={'class': 'pgRR'})
    endPage = int(pgrr.a['href'].split('=')[-1])

    for idx in range(1,endPage+1):
        dailyMarketPriceURL = 'https://finance.naver.com/item/sise_day.naver?code=%s&page=%s' % (code,idx)
        response = requests.get(dailyMarketPriceURL, headers={'User-agent': 'Mozilla/5.0'})
        soupData = BeautifulSoup(response.text, 'html.parser')

        tr=soupData.find_all("tr")

        for i in range(1,len(tr)-1):
            if(tr[i].span!=None):
                date=tr[i].find('td',attrs={'align':'center'}).string
                closingPrice=tr[i].findAll('td',attrs={'class':'num'})[0].string
                absoluteComparePrice=tr[i].findAll('td',attrs={'class':'num'})[1].find('span').string.strip()

                if(tr[i].find('img')!=None):
                    if(tr[i].find('img').get('src').split('/')[-1]=='ico_down.gif'):
                        comparePrice='-'+absoluteComparePrice
                    if(tr[i].find('img').get('src').split('/')[-1]=='ico_up.gif'):
                        comparePrice = '+' +absoluteComparePrice
                else:
                    comparePrice='0'

                openingPrice=tr[i].findAll('td', attrs={'class': 'num'})[2].string
                highestPrice=tr[i].findAll('td', attrs={'class': 'num'})[3].string
                lowestPrice=tr[i].findAll('td', attrs={'class': 'num'})[4].string
                volume=tr[i].findAll('td', attrs={'class': 'num'})[5].string

                result.append([date]+[closingPrice]+[comparePrice]+[openingPrice]+[highestPrice]+[lowestPrice]+[volume])


        print("[%s page] 완료 !" % idx)


def main():
    result = []

    company = input("기업의 이름을 정확히 입력하세요 : ")
    data = {
            '카카오': {
                'code': '035720'
            },
            '카카오게임즈':{
                'code':'293490'
            },
            '카카오뱅크': {
                'code': '323410'
            },
            '카카오페이': {
                'code': '377300'
            }
        }

    print('===============================================================')
    print('================== 일별 시세 크롤링을 시작합니다. ==================')
    print('===============================================================')

    dailyMarketPriceCrawling(result,data[company]['code'])

    print('===============================================================')
    print('================== 일별 시세 크롤링이 끝났습니다. ==================')
    print('===============================================================')


    tbl = pd.DataFrame(result, columns=('날짜', '종가', '전일비', '시가','고가','저가','거래량'))
    tbl.to_csv('./%s_일별시세.csv'%company, encoding='cp949', mode='w', index=True)


if __name__ == '__main__':
    main()
