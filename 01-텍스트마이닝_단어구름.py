from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par

keyword = input("키워드 입력 >> ")
encoded = par.quote(keyword) # 한글 -> 특수한 문자

page_num = 1
output_total = ""
while True:
    url = f"https://www.joongang.co.kr/_CP/496?keyword={encoded}&sort%20=&pageItemId=439&page={page_num}"
    code = req.urlopen(url)
    soup = BeautifulSoup(code, "html.parser")
    title = soup.select("h2.headline a")
    if len(title) == 0: # 끝 페이지까지 크롤링 완료했으면?
        break
    for i in title:
        print("제목 :", i.text.strip())
        print("링크 :", i.attrs["href"])
        code_news = req.urlopen(i.attrs["href"])
        soup_news = BeautifulSoup(code_news, "html.parser")
        content = soup_news.select_one("div#article_body")
        result = content.text.strip().replace("     ", " ").replace("   ", "")
        output_total += result
        print(result)
        print()
    if page_num == 1:
        break
    page_num += 1

# 명사들만 추출
print("[알림] 명사들만 추출합니다.")
from konlpy.tag import Okt
okt = Okt()
nouns_list = okt.nouns(output_total)
# print(nouns_list)

# 불용어 제거
print("[알림] 불용어를 제거합니다.")
nouns_without_stopwords = []
for i in nouns_list:
    if len(i) != 1:
        nouns_without_stopwords.append(i)

# 단어빈도수 카운트
print("[알림] 단어 빈도수를 카운트합니다.")
from collections import Counter
count_result = Counter(nouns_without_stopwords)
# print(count_result)

# 단어구름 그리기
print("[알림] 단어구름을 만듭니다.")
from wordcloud import WordCloud
wc = WordCloud(background_color="white", font_path="./NanumMyeongjoBold.ttf")
wc = wc.generate_from_frequencies(count_result)

# 이미지 띄우기
import matplotlib.pyplot as plt
plt.figure() # 창을 만듦
plt.imshow(wc, interpolation="bilinear") # 창에 이미지를 넣음.
plt.axis("off") # x축, y축을 없앰
plt.show() # 창을 화면에 띄움