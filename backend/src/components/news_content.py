import requests
from bs4 import BeautifulSoup


def get_news_contents():
    print("start")
    main_response = requests.get("https://news.sbs.co.kr/news/newsPlusList.do?themeId=10000000134&plink=SITEMAP&cooper=SBSNEWS")
    main_response.raise_for_status()
    html = main_response.text
    soup = BeautifulSoup(html, "html.parser")
    articles = soup.select("a.news")
    
    if not articles:
        print("No articles found")
        return "error"
    for article in articles:
        print(article["href"])
        sub_response = requests.get(f"https://news.sbs.co.kr{article['href']}")
        soup = BeautifulSoup(sub_response.text, "html.parser")
        news_box = soup.find('div', attrs={"class": "text_area"})
        if news_box.find('span'):
            news_box.find('span').decompose()
            print('span tag removed')

        news = news_box.text.replace("\n\n", "").replace("\n", "").replace("   ", "").replace("  ","").strip()

        #! 뉴스 맨처음 기사만 가져오는 모듈임 따라서 이미 저장된 기사라면 다음 컨텐츠를 가져와야함
        
        if len(news)<2000 and len(news)>500:
            index = news.rfind("(사진")
             
            contents = news[:index]
            
            print(news[:index])
            return contents
            
        else:
            print("2000자 이상이거나 500자 이하임!!")
            
    
    return "error"
        
    
# get_news_contents()
#container > div > div.w_news_list.type_issue2 > ul > li:nth-child(1) > a
#container > div > div.w_news_list.type_issue2 > ul > li:nth-child(2) > a
