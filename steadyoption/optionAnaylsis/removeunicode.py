import json
import re




def extract_trade_info(trade):
  trade_pattern = "(Buy to open|Buy to close|Sell to close|Sell to open)(.*?)(call|put)"
  action = trade[0]
  option_type = trade[2]
  message =""
  target=trade[1].lower()
  strike_pattern="(\d+\.?\d*\s*)$"
  strike = re.search(strike_pattern,target)
  print(strike)
  if not(strike):
      message+="strike"
  target =target[:strike.start()]

  Day_pattern ="(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december).\d+(.\d\d\d\d)?"

  #print(reminding)
  date = re.search(Day_pattern,target)
  if (date):
      target = target[:date.start()]
  else:
      message +="date "
      message +=target

  stock_symbol_pattern = "[a-zA-Z]+"
  stock_symbol = re.search(stock_symbol_pattern, target)
  if (stock_symbol):
      target = target[:stock_symbol.start()]
  else:
      message+="stock symbol, "

  number_of_contract_pattern ="\d+"
  number_of_contract = re.search(number_of_contract_pattern,target)
  if not (number_of_contract):
      number =1
  else:
      number = number_of_contract[0]

  print("number of contract: ",number )
  print("symbol: ",stock_symbol[0])
  print("date: ",date[0] )
  print("strike: ",strike[0])

  if (number_of_contract) and (stock_symbol) and (date) and (strike):
    return(action,number,stock_symbol[0],date[0],strike[0],option_type)
  else:
      #print("Error: ",message)
      return(("Error",message))



postexample ={
"Trade Name": "(TRADES) M November 2022 Straddle",
"Trade post": ["I opened M straddles. Buy to open 4 M Nov.18   21.5  put Buy to open 4  M Nov.18   21.5  call Price:  $2.41 debit per straddle Earnings date:   Thursday, November 17   Before Open Stock price:  $21.55 The number of contracts is per 10k portfolio and represents the closest number of contracts for 10% allocation. Please see more details in the discussion topic. Scroll down to the bottom of the page to see links to the last ten topics tagged with the same symbol. You need to follow this topic to get adjustment and close alerts. Please read about ﻿ our straddle strategy here . ﻿ ﻿ Disclaimer :  I am not a Financial Adviser and this is NOT trade recommendation. Please do your own homework and set your own entry and exit targets. Thanks Haha Upvote Downvote Like ×"]
}

article = postexample['Trade post'][0]
trade_pattern = "(Buy to open|Buy to close|Sell to close|Sell to open)(.*?)(call|put)"
strdecode = article.encode('ascii', errors='replace').decode().replace("?", " ")
#strdecode= re.sub(r'[^\x00-\x7f]', " ", article)
trade_detail = re.findall(trade_pattern,strdecode)

trade_list=[]
error_list=[]
if (trade_detail):
    trade_breakdown=[]
    error_breakdown=[]
    for t in trade_detail:
        result = extract_trade_info(t)
        if result[0]=="Error":
            error_list.append((t,result[1]))
        else:
            trade_breakdown.append(result)
    trade_list.append(trade_breakdown)


#print("trade")
#print(trade_list)
#print("Error")
#print(error_list)

'''
f = open('post.json', encoding="utf-8")

data = json.load(f)
print(len(data))

article_list =[]
for trade in data:

    for article in trade["Trade post"]:
        #encode() method
        strencode = article.encode("ascii", "ignore")
        #decode() method
        strdecode = strencode.decode()
        strdecode= re.sub(r'[^\x00-\x7f]', " ", article)

        article_list.append(strdecode)



with open('remove.json', 'w',encoding="utf-8") as file2:
    json.dump(article_list, file2)



f.close()
file2.close()
'''
