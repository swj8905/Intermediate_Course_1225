from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller # 터미널 창에 pip install chromedriver_autoinstaller 입력하여 모듈 설치!

# chromedriver_autoinstaller 를 사용하여 코드를 아래처럼 작성하면,
# 굳이 chromedriver 파일을 별도로 다운로드 받지 않아도 됩니다.
# browser = webdriver.Chrome("./chromedriver") # 삭제
chrome_path = chromedriver_autoinstaller.install() # 추가
browser = webdriver.Chrome(chrome_path) # 추가
browser.get("https://www.youtube.com/watch?v=dI4Fb0qmJ90")
time.sleep(5)

# 스크롤 살짝 내려서 댓글 생성시키기
browser.find_element_by_css_selector("html").send_keys(Keys.PAGE_DOWN)
# # 스크롤 끝까지 내려서 댓글 생성시키기
# browser.find_element_by_css_selector("html").send_keys(Keys.END)
time.sleep(4)
comments = browser.find_elements_by_css_selector("#content-text")
idx = 0
output_total = ""
while True:
    try:
        print(comments[idx].text)
        output_total += comments[idx].text
    except:
        print("===== 크롤링 완료! =====")
        break # break를 추가해야 무한 루프(while True)를 탈출할 수 있습니다.
    idx += 1
    if idx % 20 == 0:  # idx 가 20의 배수라면?
        browser.find_element_by_css_selector("html").send_keys(Keys.END)
        time.sleep(4)
        comments = browser.find_elements_by_css_selector("#content-text")
        break


#명사들만 추출
print("[알림] 명사들만 추출함")
from konlpy.tag import Okt
okt = Okt()
nouns_list=okt.nouns(output_total)
#print(nouns_list) 한번만 테스트하고 주석처리해도 됨

#불용어 제거
nouns_without_stopwords = []
for i in nouns_list:
    if len(i) != 1:
        nouns_without_stopwords.append(i)

#단어빈도수 카운트
print("[알림] 단어 빈도수를 카운트함")
from collections import Counter
count_result = Counter(nouns_without_stopwords)

#단어구름 그리기
print("[알림] 단어구름 생성")
from wordcloud import WordCloud
wc = WordCloud(background_color= "white", font_path= "./NanumMyeongjoBold.ttf")
wc = wc.generate_from_frequencies(count_result)

#이미지 띄우기
import matplotlib.pyplot as plt
plt.figure()#창을 만듦
plt.imshow(wc, interpolation= "bilinear")#창에 이미지를 넣음; bilinear 이미지에 화소를 높여줌
plt.axis("off")#x,y 축 없앰
plt.show()#창을 화면에 띄움