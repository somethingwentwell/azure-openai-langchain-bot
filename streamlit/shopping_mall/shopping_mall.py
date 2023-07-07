import streamlit as st
import requests
import json
import time
from PIL import Image

st.set_page_config(page_title="Shopping Mall", layout="wide", page_icon=":shopping_bags:")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

shop_list="""
Shop No.,Shop Name,Openning Hour: Mon - Thu,Openning Hour: Fri,Openning Hour: Sat & PH Eve,Openning Hour: Sun & PH
UB01,Parsons Music ,1100-2100,1100-2100,1100-2100,1100-2100
UB02,The White Box Creative Space by Little Prince Art ,1000-1900,1000-1900,1000-1900,1000-1900
UB03,YD Taekwondo ,1000-2200,1000-2200,1000-2200,1000-2200
UB04,ARTCO SUMO ,1000-1930,1000-1930,1000-1930,1000-1930
UB05,Shh Massage ,1100-2200,1100-2200,1100-2200,1100-2200
UB06,LOST ,1200-2100,1200-2100,1100-2100,1100-2100
UB07 & 08,The Monster Lab ,0930-1900,0930-1900,0930-1900,0930-1900
LB01 & 02,The Wonderful World of Whimsy ,1000-2200,1000-2200,1000-2200,1000-2200
LB03,LaserPlay ?? ,1130-2100,1130-2100,1130-2100,1130-2100
LB04,Art Art Land ,1100-2000,1100-2000,1100-2000,1100-2000
LB05,Little Scientists  ,1000-1930,1000-1930,1000-1930,1000-1930
LB06,0.9144m,1000-2200,1000-2200,1000-2200,1000-2200
LB07,YUM ME PLAY,1000-2000,1000-2000,1000-2000,1000-2000
LB08 & 09,Kiztopia,1000-2000,1000-2000,1000-2000,1000-2000
LB Carpark,Tesla,24 hours,24 hours,24 hours,24 hours
102,A-1 BAKERY ,0730-2200,0730-2200,0730-2200,0730-2200
103,GODIVA Belgium 1926,1030-2200,1030-2200,1030-2200,1030-2200
103A,Greyhound Café,1130-2200,1130-2300,1130-2300,1130-2300
105,Tsukada Nojo ,1130-2230,1130-2230,1130-2230,1130-2230
107,Toss Treasure of Semua Semua,1130-2200,1130-2200,1130-2200,1130-2200
108,Top Blade Steak Lab,1100-2230,1100-2230,1100-2230,1100-2230
110,Yaki ANA,1130-2200,1130-2200,1130-2200,1130-2200
112,Dab-pa Modern Chinese Cuisine,1130-2230,1130-2230,1130-2230,1130-2230
113,Hong Kong Wing Nin,0800-2230,0800-2230,0800-2230,0800-2230
115,Brass Spoon ,1130-2200,1130-2200,1130-2200,1130-2200
117,Parkview,1100-2230,1100-2230,1100-2230,1100-2230
119,Tasty Congee & Noodle Wantun shop,1100-2200,1100-2200,1000-2200,1000-2200
121,Pizza Express,0800-2200,0800-2200,0800-2200,0800-2200
126,Que Cafe ,1130-2200,1130-2200,1130-2200,1130-2200
127,Kikusan,0800-2200,0800-2200,0800-2200,0800-2200
128,Tristar Kitchen,1130-2200,1130-2200,1130-2200,1130-2200
129,simplylife ,0730-2300,0730-2300,0730-2300,0730-2300
153-154,Shake Shack,1100-2200,1100-2200,1000-2200,1000-2200
155,Starbucks Coffee,0700-2200,0700-2200,0800-2200,0800-2200
156,Cookies Quartet,1100-2100,1100-2100,1100-2100,1100-2100
157,ZAN CHEE,1100-2100,1100-2100,1100-2100,1100-2100
158,YiFang Taiwan Fruit Tea,1000-2200,1000-2200,1000-2200,1000-2200
159,Tempura Makino,1200-2200,1200-2200,1200-2200,1200-2200
165,Woofy,1130-2200,1130-2200,0900-2200,0900-2200
166,Din Tai Fung,1130-2200,1130-2200,1130-2200,1130-2200
167,Takano Ramen  ,1130-2200,1130-2200,1130-2200,1130-2200
202,Clinique,1100-2200,1100-2200,1100-2200,1100-2200
203,Jo Malone London,1100-2200,1100-2200,1100-2200,1100-2200
204a,Tea WG Boutique,1000-2200,1000-2200,1000-2200,1000-2200
204-214,Citysuper,1000-2200,1000-2200,1000-2200,1000-2200
214a,Enoteca,1100-2100,1100-2100,1100-2100,1100-2100
214b,Venchi,1100-2100,1100-2100,1100-2100,1100-2100
214c,Cova,1100-2000,1100-2000,1100-2030,1100-2030
215a,LAURA MERCIER,1030-2100,1030-2100,1030-2100,1030-2100
215b,Guerlain,1100-2100,1100-2100,1100-2100,1100-2100
216,"Mr Simms Olde Sweet Shoppe 
",1100-2100,1100-2100,1100-2100,1100-2100
217,IPSA,1030-2100,1030-2100,1030-2100,1030-2100
218,NARS,1030-2100,1030-2100,1030-2100,1030-2100
219,Clarins,1000-2200,1000-2200,1000-2200,1000-2200
220,ghd ,1000-2200,1000-2200,1000-2200,1000-2200
221,Good Mask,1000-2100,1000-2100,1000-2100,1000-2100
222-223,McDonald's / McCafé,0700-2300,0700-2300,0700-2300,0700-2300
225,Uniqlo,1100-2200,1100-2200,1100-2200,1100-2200
243,Charlotte Tilbury,1000-2200,1000-2200,1000-2200,1000-2200
245,XOVE ,1100-2100,1100-2100,1100-2100,1100-2100
246,BeyorgTM Beyond Organic,1000-2100,1000-2100,1000-2100,1000-2100
247,Sl...owood ,1100-2200,1100-2200,1100-2200,1100-2200
247A,Kapok ,1100-2030,1100-2030,1100-2030,1100-2030
"248,249",Cotton On,1000-2200,1000-2200,1000-2200,1000-2200
"250,359",Matsumoto Kiyoshi,1000-2200,1000-2200,1000-2200,1000-2200
250A,The Dog's Garden ,1000-2100,1000-2130,1000-2130,1000-2130
251,PICI Pasta Bar,1130-2230,1130-2230,1100-2230,1100-2230
252,Movie Town (Ticket Office),1015-2230,1015-2230,0815-2230,0815-2230
Portion of L1,Movie Town (House 1-6),1000-0030,1000-0030,0830-0030,0830-0030
Portion of L3,MovieTown (MX4D),1000-0030,1000-0030,0830-0030,0830-0030
301,Bally,1100-2030,1100-2030,1100-2030,1100-2030
302,Sandro,1100-2100,1100-2100,1100-2100,1100-2100
302A,MAX&Co.,1100-2000,1100-2100,1100-2100,1100-2000
303,BERACAMY,1100-2100,1100-2100,1100-2100,1100-2100
305,Fresh,1000-2130,1000-2130,1000-2130,1000-2130
307 & 307A,Mannings,0900-2200,0900-2200,0900-2200,0900-2200
308 & 308A,Rolex and Tudor,1100-2100,1100-2100,1100-2100,1100-2100
309,Ma Belle,1100-2100,1100-2100,1100-2100,1100-2100
309A,LADY M NEW YORK,1100-2100,1100-2200,1100-2200,1100-2100
310-311,Chow Sang Sang,1100-2100,1100-2100,1100-2100,1100-2100
312-313,Chow Tai Fook ,1030-2100,1030-2100,1030-2100,1030-2100
315 & 317,Luk Fook Jewellery ,1000-2130,1000-2130,1000-2130,1000-2130
318-319,TSL????,1100-2100,1100-2100,1100-2100,1100-2100
321,Masterpiece by King Fook,1100-2100,1100-2100,1100-2100,1100-2100
322,Sam Edelman ,1100-2100,1100-2100,1100-2100,1100-2100
323,SWAROVSKI,1100-2000,1100-2000,1100-2000,1100-2000
325,kate spade New York,1100-2100,1100-2200,1100-2200,1100-2100
326,Theory,1100-2000,1100-2000,1100-2000,1100-2000
328,Marc Jacobs,1100-2030,1100-2030,1100-2030,1100-2030
329,MCM,1100-2000,1100-2030,1100-2030,1100-2000
330,ESTÉE LAUDER,1000-2200,1000-2200,1000-2200,1000-2200
332,Dior Beauty,1000-2200,1000-2200,1000-2200,1000-2200
335,ZARA,1000-2200,1000-2200,1000-2200,1000-2200
357,Sa Sa,1030-2130,1030-2100,1030-2100,1030-2100
358,Initial ,1100-2100,1100-2200,1100-2200,1100-2200
365,Aerie ,1200-2100,1200-2100,1200-2100,1200-2100
366,Amercian Eagle Outfitters,1200-2100,1200-2100,1200-2100,1200-2100
367,Bath & Body Works,1100-2200,1100-2200,1100-2200,1100-2200
369A,SK-II,1000-2200,1000-2200,1000-2200,1000-2200
369B,POLA,1100-2100,1100-2100,1100-2100,1100-2100
369C,CASETiFY,1100-2130,1100-2130,1100-2130,1100-2130
369D,TOMMY HILFIGER ,1100-2100,1100-2100,1100-2100,1100-2100
369E,Dyson ,1000-2200,1000-2200,1000-2200,1000-2200
373,Shiseido,1030-2100,1030-2100,1030-2100,1030-2100
373A,Yves Saint Laurent,1000-2200,1000-2200,1000-2200,1000-2200
376,Chanel ,1100-2100,1100-2200,1100-2200,1100-2200
378,Lancôme,1000-2200,1000-2200,1000-2200,1000-2200
381,Longchamp,1100-2200,1100-2200,1100-2200,1100-2200
382,KENZO,1100-2030,1100-2030,1100-2030,1100-2030
383,POLO RALPH LAUREN,1100-2000,1100-2100,1100-2100,1100-2100
386,Alice and Olivia by Stacey Bendet,1100-2000,1100-2100,1100-2100,1100-2000
387,Weekend Max Mara,1100-2000,1100-2000,1100-2000,1100-2000
388,Furla,1100-2100,1100-2100,1100-2100,1100-2100
389,agnes b. ,1100-2030,1100-2100,1100-2100,1100-2030
390-391,COS,1100-2100,1100-2100,1100-2100,1100-2100
392,Monica Vinader,1000-2100,1000-2100,1000-2100,1000-2100
393,Moiselle ,1100-2030,1100-2030,1100-2030,1100-2030
395,Club Monaco,1100-2100,1100-2100,1100-2100,1100-2100
396,Pandora,1100-2100,1100-2130,1100-2130,1100-2100
397,Michael Kors,1100-2000,1100-2100,1100-2100,1100-2100
398 & 398A,Coach,1130-2000,1130-2000,,1130-2000
"""
event1 = "The Point「會員狂賞節 – 任務」"

event1details = """1. 「The Point 會員狂賞節」（「活動」）適用於所有The Point會員（「會員」）。
2. 活動之推廣期由2023年4月1日至4月27日，包括首尾兩日（「推廣期」）。
3. 活動只適用於新鴻基地產代理有限公司（「新鴻基地產」）旗下25家參與商場，包括
觀塘apm、屯門卓爾廣場、薄扶林置富南區廣場、將軍澳東港城、北角匯、沙田
HomeSquare、屯門錦薈坊、上水廣場、葵芳新都會廣場、上水新都廣場、新蒲崗
Mikiki、旺角MOKO新世紀廣場、柴灣新翠商場、沙田新城市廣場、將軍澳中心、將軍
澳 PopWalk 天晉滙、大埔超級城、荃灣荃錦中心、荃灣廣場、大埔新達廣場、屯門V 
city、南昌V Walk、銅鑼灣wwwtc mall、元朗YOHO MALL形點及元朗廣場（「參與商
場」）。如有更新，恕不另行通知，請瀏覽www.thepoint.com.hk。
4. 會員於推廣期內於參與商場以電子貨幣累積消費滿指定金額，並於消費交易日起計14天
內透過手機應用程式、微信官方帳號或經消費商場之禮賓櫃檯／顧客服務中心上載或出
示有效之消費單據登記積分，或透過「自動賺取The Point積分」功能 (不適用於透過網
上付款繳付優惠價的獎賞換領賺取積分)、The Point手機應用程式外賣自取服務賺取積
分，成功批核後，除基本積分外，可獲取額外積分（「獎賞」）。2023年4月27日之消
費單據最遲登記積分日期為2023年4月27日。每完成一項指定「狂賞任務」（「任務」）
後，會員須在任務頁面換領積分獎賞。換領積分後，系統將按完成的任務發放獎賞，會
員最多可於每項任務享積分獎賞一次。任務詳情如下：
a) 任務一： 累積消費滿HK$500或以上並成功登分及經核實後，即賞額外250積分。
b) 任務二：累積消費滿HK$2,000或以上並成功登分及經核實後，即賞額外1,250積分。
c) 任務三：累積消費滿HK$5,000或以上並成功登分及經核實後，即賞額外4,500積分。
d) 任務四：累積消費滿HK$8,000或以上並成功登分及經核實後，即賞額外9,000積分。
e) 任務五：累積消費滿HK$15,000或以上並成功登分及經核實後，即賞額外15,000積
分。
5. 整個推廣期內 ，每位會員可從活動中獲取最多30,000積分。
6. 只計算實際消費金額，即只計算折扣後或使用優惠券／現金券／電子券後之剩餘金額。
7. 每組合資格之消費單據 ，系統將根據消費單據批核日期之先後次序發放額外積分。
8. 獎賞數量有限，先到先得，換完即止。
9. The Point積分獎賞將於確認換領後經系統即時存入The Point會員之帳戶，會員亦可自行
瀏覽「積分紀錄」以了解積分狀況。
10. 換領獎賞一經確認，有關積分獎賞不可轉換、更改、取消或兌換現金。
11. 會員須於2023年5月4日晚上11:59或之前（「換領期」），透過手機應用程式於活動頁
面兌換完成任務的獎賞，逾期無效。已逾期而未有兌換的獎賞，將於換領期完結後全數自
動作廢。
12. The Point積分之登記及使用須受其他條款及細則約束，詳情請瀏覽
www.thepoint.com.hk、手機應用程式、微信官方帳號或向參與商場之禮賓專櫃／顧客服務
中心查詢。
13. 登記活動之消費單據可同時兌換參與商場之常設泊車優惠（視乎參與商場之泊車優惠消
費條款），亦可與個別商場其他優惠及推廣活動同時使用，詳情請留意個別商場之條款及
細則。
14. 如有任何舞弊或欺詐行為，新鴻基地產及參與商場將即時取消The Point會員有關的積
分及獎賞換領資格，並保留追究之權利。
15. 新鴻基地產及參與商場有權更改活動條款及細則而毋須另行通知。
16. 如有任何爭議，新鴻基地產及參與商場保留最終決定權。
17. 本條款及細則的中文及英文版本若有任何差異，一概以英文版本為準。

推廣期: 2023年4月1日至4月27日，包括首尾兩日
參與商場: 
觀塘apm、屯門卓爾廣場、薄扶林置富南區廣場、將軍澳東港城、北角匯、沙田HomeSquare、屯門錦薈坊、上水廣場、葵芳新都會廣場、
上水新都廣場、新蒲崗Mikiki、旺角MOKO新世紀廣場、柴灣新翠商場、沙田新城市廣場、將軍澳中心、將軍澳 PopWalk 天晉滙、大埔超級城、荃灣荃錦中心、荃灣廣場、大埔新達廣場、屯門V city、南昌V Walk、銅鑼灣wwwtc mall、元朗YOHO MALL形點及元朗廣場
目標客戶: 全部會員
活動內容:
本活動包括了5項任務，於推廣期內以任何電子貨幣於新地商場累積消費滿指定金額，並透過The Point App或微信官方帳號或親臨消費之
商場禮賓櫃檯／顧客服務中心登記積分以完成下任務 (不適用於透過網上付款繳付優惠價的獎賞換領賺取積分:
任務一：累積消費滿$500或以上
任務二：累積消費滿$2,000或以上
任務三：累積消費滿$5,000或以上
任務四：累積消費滿$8,000或以上
任務五：累積消費滿$15,000或以上
"""
def insource_reply_shoplist(question ,shop_list):
    response_text = f"""
    You are an shopping mall customer service that help to reply consummer questions. You must follow the Rules below: 
    <Rules> 
    Rule 1: The reply must refer to the shoplist provided below. 
    Rule 2: Do not any question that not related to the shoplist below and reply 'I don't have information on this question'.
    Rule 3: If the question in Chinese, you must reply in Chinese.
    <Rules> 

    T & C: 
    {shop_list}

    Question from consummer:
    {question}
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": "2",  
      "text": response_text
    }
    response = requests.post(url, json=payload)  
    return response.json()

def insource_reply_event1(question ,event1details):
    response_text = f"""
    You are an shopping mall customer service that help to reply consummer questions. You must follow the Rules below: 
    <Rules> 
    Rule 1: The reply must refer to the event details provided below. 
    Rule 2: Do not any question that not related to the event details below and reply 'I don't have information on this question'.
    Rule 3: If the question in Chinese, you must reply in Chinese.
    <Rules> 

    T & C: 
    {event1details}

    Question from consummer:
    {question}
    """
    url = "http://insource-test-015.southeastasia.cloudapp.azure.com:8000/run"  
    payload = {  
      "id": "2",  
      "text": response_text
    }
    response = requests.post(url, json=payload)  
    return response.json()

topics = ["Shop List", event1]

# image = Image.open("shopping_mall_banner.jpg")
# st.image(image, caption='Sunrise by the mountains')
st.write("Hello there! How can I assist you today?")
topic = st.selectbox("",topics)

def chatbot():
  # Initialize chat history
  if "messages" not in st.session_state:
      st.session_state.messages = []

  # Display chat messages from history on app rerun
  for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

  # Accept user input
  if question := st.chat_input("Enter enquiries"):
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": question})
      # Display user message in chat message container
      with st.chat_message("user"):
          st.markdown(question)

      # Display assistant response in chat message container
      with st.chat_message("assistant"):
          message_placeholder = st.empty()
          full_response = ""
          assistant_response = ""

          if topic == "Shop List":
             assistant_response = insource_reply_shoplist(question ,shop_list)['result']
          elif topic == event1:
             assistant_response = insource_reply_event1(question ,event1details)['result']
          # elif topic == "Event Overview":
          #    assistant_response = insource_reply_event2(question ,event2details)['result']

          # Simulate stream of response with milliseconds delay
          for chunk in assistant_response.split():
              full_response += chunk + " "
              time.sleep(0.05)
              # Add a blinking cursor to simulate typing
              message_placeholder.markdown(full_response + "▌")
          message_placeholder.markdown(full_response)
      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": full_response})

chatbot()