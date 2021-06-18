import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
import matplotlib.pyplot as plt

driver = webdriver.Chrome()
token = 'jZZnuyrTrAdaO7HZPW6M5xxnFqO0LQVz9oEJmT5Eb4W' # Line Token

url_Gossiping="https://www.ptt.cc/bbs/Gossiping/index.html" # PTT八卦版
url_Beauty = "https://www.ptt.cc/bbs/Beauty/index.html" # PTT表特版

titles_and_links = [] # 存放title跟links
driver.get("https://www.ptt.cc/bbs/Gossiping/index.html") # 開啟PTT看板首頁
driver.maximize_window() # 最大化視窗
driver.find_element_by_xpath('/html/body/div[2]/form/div[1]/button').click() # 點選我已滿18歲，點一次就好
def get_all_href(url):
    my_headers = {'cookie': 'over18=1;'} # 設定Header與Cookie，是因為PTT有限制18歲
    r = requests.get(url, headers = my_headers) # 發送get 請求 到 ptt 指定看板
    soup = BeautifulSoup(r.text, "html.parser") # 把網頁程式碼(HTML)丟入bs4模組分析
    # 查找所有html元素過濾出標籤名稱為 'div' 同時class為 title,nrec
    title = soup.find_all('div','title') # 標題
    titles = []
    push = soup.find_all('div','nrec') # 推文數
    pushs = []
    for t in title:
        titles.append(t.text)
    for p in push:
        pushs.append(p.text)
    title_push = dict(zip(titles, pushs)) # 將標題及推文數做成dict
    msg = [] # 存放要推播到line的訊息
    XX = ['X1','X2','X3','X4','X5','X6','X7','X8','X9','XX'] # 噓文數
    # 印出推文數大於10的標題
    for key, value in title_push.items(): # key是標題，value是推文數
        if value=='爆': # 如果爆(推文數>99)
            msg.append(key) # 將符合條件的標題加到list
            #print(key, value)
        # 如果被噓(其形式有X1 X2 X3 X4 ... XX) 則忽略
        elif value in XX:
            ignore = 0 # 無意義，忽略 
        elif len(value)!=0 and int(value)>=80: # 如果不為空串且推文數大於80
            msg.append(key) # 將符合條件的標題加到list
            #print(key, value)
    
    title_results = soup.select("div.title") # 取div內class為title
    for item in title_results:
        a_item = item.select_one("a") #取div內class為title下的a標籤
        title = item.text # 取得其文字(標題)
        if a_item and title in msg: #確認a_item是有值的，才取href
            titles_and_links.append(title) # 插入標題 
            titles_and_links.append('https://www.ptt.cc'+ a_item.get('href')) # 插入連結
            url_ = 'https://www.ptt.cc'+ a_item.get('href') # 要開啟新分頁的網址
            driver.execute_script('window.open("' + url_ + '")') # 開新的分頁
            
print('Runing...')
titles_and_links.append('\n【八卦版】')
for page in range(1,15): # 找第1~15頁  文章數較多，可能來不及爆就被洗下去
    my_headers = {'cookie': 'over18=1;'} # 設定Header與Cookie，是因為PTT有限制18歲
    r = requests.get(url_Gossiping, headers = my_headers) # 發送get 請求 到 ptt 指定看板
    get_all_href(url = url_Gossiping) # 第一次先抓八卦首頁，接下來會抓下一頁
    soup = BeautifulSoup(r.text,"html.parser") # 把網頁程式碼(HTML)丟入bs4模組分析
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href 
    url_Gossiping = next_page_url # 下一頁的網址
    

titles_and_links.append('\n\n【表特版】')
for page in range(1,5): # 找第1~5頁  文章數較少且容易被推爆
    my_headers = {'cookie': 'over18=1;'} # 設定Header與Cookie，是因為PTT有限制18歲
    r = requests.get(url_Beauty, headers = my_headers) # 發送get 請求 到 ptt 指定看板
    get_all_href(url = url_Beauty) # 第一次先抓表特首頁，接下來會抓下一頁
    soup = BeautifulSoup(r.text,"html.parser") # 把網頁程式碼(HTML)丟入bs4模組分析
    btn = soup.select('div.btn-group > a')
    up_page_href = btn[3]['href']
    next_page_url = 'https://www.ptt.cc' + up_page_href 
    url_Beauty = next_page_url # 下一頁的網址
    

def show_boardPopularity():
    url_index = 'https://www.ptt.cc/bbs/index.html'
    # 設定Header與Cookie，是因為PTT有限制18歲
    my_headers = {'cookie': 'over18=1;'} # 設定Header與Cookie，是因為PTT有限制18歲
    r = requests.get(url_index, headers = my_headers) # 發送get 請求 到 ptt 指定看板
    soup = BeautifulSoup(r.text,"html.parser") # 把網頁程式碼(HTML)丟入bs4模組分析
    nuser = []
    board_name = []
    All_nuser = soup.select('div.b-ent  a.board div.board-nuser span') # 看板人氣
    # <span class="hl f6">19860</span>, <span class="hl f4">6361</span>, ...
    All_board_name = soup.select('div.b-ent  a.board div.board-name') # 看板名稱
    # <div class="board-name">Gossiping</div>, <div class="board-name">Stock</div>, ... 
    for index in range(0,5):
        nuser.append(int(All_nuser[index].get_text())) # 看板人氣
        # '20065', '5940', '4807', '3009', '2678', ...
        board_name.append(All_board_name[index].get_text()) # 看板名稱
        # 'Gossiping', 'Stock', 'C_Chat', 'NBA', 'Lifeismoney', ...
    plt.bar(board_name, nuser) # 繪製長條圖
    plt.title("Top 5 Board Bar Chart") # 設定圖表標題
    plt.ylabel("Board-Popularity") # 設定y軸標籤
    plt.xlabel("Board-Name") # 設定x軸標籤
    plt.savefig("Top5 Borad Bar Chart.png") # 將圖表存成圖片
    plt.show()
    
    #print(All_nuser, All_board_name)
    #print(nuser, board_name)
show_boardPopularity()

def lineNotifyMessage_image(token, msg, image_path):
    headers = {
        "Authorization":"Bearer " + token,
        #"Content-Type":"application/x-www-form-urlencoded"
    }
    payload = {'message':msg}
    files = {'imageFile':open(image_path, 'rb')}
    r = requests.post("https://notify-api.line.me/api/notify",
                     headers = headers, params=payload, files=files)
    print(r.status_code)
    return r.status_code        

image_path = r'./Top5 Borad Bar Chart.png' # 前五大看板人氣圖相對位置

# Line 通知標題及其連結並附上前五大看板人氣圖
lineNotifyMessage_image(token, titles_and_links, image_path) 
print('Done')