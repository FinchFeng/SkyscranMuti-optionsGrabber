from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

lowersPriceList = []
def getPrice(startDate,startPlace):
    cheapestPrice = 19999
    #这里添加不同的返回日期
    for timeLongth in range(6,8):
        driver = webdriver.Chrome()
        endDate = startDate + timeLongth
        # WebDriverWait(driver,20)
        # driver.implicitly_wait(30)
        driver.get("https://www.tianxun.com/intl-round-" + startPlace + "-tyoa.html?depdate=2019-08-"+str(startDate)+"&rtndate=2019-08-"+str(endDate)+"&cabin=Economy&adult=6&child=0&infant=0")
        sleep(10)
        # print("wake up")
        html_source = driver.page_source
        soup = BeautifulSoup(html_source,features="html.parser")
        tickets = soup.find_all(class_="fly_int_re")
        thisDatesResult = []
        for div in tickets:
            changeFilghtTimes = len(div.find_all(class_="z"))
            needToChangeFilght = changeFilghtTimes != 0
            companyList = getAllText(div.find_all(class_="clearfix"))
            timePointList = getAllText(div.find_all(class_="time-color"))
            durationTimeList = getAllText(div.find_all(class_="timeBox"))
            price = div.find("p",class_="price-black").find("b").get_text()
            #组织信息
            result = price
            priceNumber = int(price[1:])
            # print(priceNumber)
            if (needToChangeFilght):
                result += "[转机 " + str(changeFilghtTimes) + "次]"
            result += "{去程} 起飞时间 2019-08-"+str(startDate) + " " + timePointList[0] + " " + companyList[0] + " 航班 " + "到达时间 2019-08-"+str(startDate) + " "+ timePointList[1] + " 飞行时长" + durationTimeList[0] + ""
            result += "{回程} 起飞时间 2019-08-"+str(endDate) + " "  + timePointList[2] + " " + companyList[len(companyList)-1] + " 航班 "  + "到达时间 2019-08-"+str(endDate) + " " + timePointList[3] + "飞行时长" + durationTimeList[1] + "   "
            #检查是否是最便宜的
            if cheapestPrice > priceNumber and changeFilghtTimes == 0:
                cheapestPrice = priceNumber
            #添加result
            if (len(thisDatesResult)<=5):
                thisDatesResult.append(result)
            else:
                driver.close()
                break
        print("出发日期 08-"+str(startDate))
        print("返回日期 08-"+str(endDate))
        for string in thisDatesResult:
            print(string)
        #价钱排序
        lowersPriceList.append(cheapestPrice)
        lowersPriceList.sort()
    return cheapestPrice
def getAllText(dic):
    result = []
    for element in dic:
        result.append(element.getText())
    return result


def checkPriceStartAt(city):
    cheapestPrice = 19999
    lowersPriceList.clear()
    #这里添加不同的出发日期
    for startDate in range(15,25):
        price = getPrice(startDate,city)
        if cheapestPrice > price:
            cheapestPrice = price
    print("------------------------------------------")
    print("从" + city + "最便宜的直飞价钱 ")
    print(cheapestPrice)
    print("从" + city + "所有日期的直飞价格排序")
    print(lowersPriceList)
    print("------------------------------------------")

if __name__ == "__main__":
    #在这里添加不同的目的地
    checkPriceStartAt("cxmn")
    checkPriceStartAt("hkga")
    checkPriceStartAt("csha")