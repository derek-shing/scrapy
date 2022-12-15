from __future__ import unicode_literals
import json
import re

test = {"Trade Name": "(TRADES) GM October 2022 Straddle",
"Trade post": ["I opened GM straddles. Buy to open 5  GM  Oct.28   34.5  put Buy to open 5  GM  Oct.28   34.5  call Price:  $2.24  debit per straddle Earnings date:   Tuesday, October 25   Before Open Stock price:  $34.50 The number of contracts is per 10k portfolio and represents the closest number of contracts for 10% allocation. Please see more details in the discussion topic. Scroll down to the bottom of the page to see links to the last ten topics tagged with the same symbol. You need to follow this topic to get adjustment and close alerts. Please read about ﻿ our straddle strategy here . ﻿ ﻿ Disclaimer :  I am not a Financial Adviser and this is NOT trade recommendation. Please do your own homework and set your own entry and exit targets. Thanks Haha Upvote Downvote Like ×",
"I closed GM straddles. Sell to close 5  GM  Oct.28   34.5  put Sell to close 5  GM  Oct.28   34.5  call Price:  $2.47  credit per straddle, Gain +10.27% Earnings date:   Tuesday, October 25   Before Open Stock price:  $35.75 The number of contracts is per 10k portfolio and represents the closest number of contracts for 10% allocation. Please see more details in the discussion topic. Scroll down to the bottom of the page to see links to the last ten topics tagged with the same symbol. You need to follow this topic to get adjustment and close alerts. Please read about ﻿ our straddle strategy here . ﻿ ﻿ Disclaimer : I am not a Financial ﻿ Adviser and this is NOT trade recommendation. Please do your own homework and set your own entry and exit targets. 1 1 Pascal and ParadigmAU reacted to this Thanks Haha Upvote Downvote Like ×"]}


def extract_price(post):
    pattern="price:\s+\$(\d*\.?\d*)\s+(credit|debit)"
    price = re.search(pattern , post)
    if price:
        return (price.group(1))
    else:
        return (None)

def testisprofit(post,startposition, endposition):
    targetrange = post[startposition-10:endposition +10]
    if ("profit" in targetrange or "gain" in targetrange or "loss" in targetrange):
        return True
    else:
        return False

def extract_PL(post):
    pattern ="(\+|-)?\d+\.?\d*%"
    pl = re.search(pattern, post)
    if pl and testisprofit(post,pl.start(),pl.end()):
        return pl[0]
    else:
        return (None)

def extract_earningday(post):

    pattern = "(earnings date:.*)(jan|feb|mar|apr|arp|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december)\s+(\d+)(\s+\d\d\d\d)?"
    day = re.search(pattern, post)
    if (day):
        return (day.group(2)+day.group(3))
    else:
        return (None)



#!/usr/bin/env python
#coding=utf-8

f = open('post2.json', encoding="utf-8")

data = json.load(f)
print(len(data))

#for post in data:
#    assert type(post['Trade post']) is unicode

def extract_trade_info(trade):
  trade_pattern = "(Buy to open|Buy to close|Sell to close|Sell to open)(.*?)(call|put)"
  action = trade[0]
  option_type = trade[2]
  message =""
  target=trade[1].lower()
  strike_pattern="(\d+\.?\d*\s*)$"
  strike = re.search(strike_pattern,target)
  if not(strike):
      message+="strike :"+f" Can't find {strike} in {target}"
  else:
      target =target[:strike.start()]

  Day_pattern ="(jan|feb|mar|apr|arp|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december)(.+)\d+(s+\d\d\d\d)?"

  #print(reminding)
  date = re.search(Day_pattern,target)
  if (date):
      target = target[:date.start()]
  else:
      print(date, " ", target)
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
      message+="Number of contract,"



  if (number) and (stock_symbol) and (date) and (strike):
    return(action,number,stock_symbol[0].upper().strip(),date[0].strip(),strike[0].strip(),option_type)
  else:
      return("Error",message)



################## Main ##################################

#print(test['Trade post'][0].lower())

#print(extract_earningday(test['Trade post'][1].lower()))
#print(extract_price(test['Trade post'][1].lower()))
#print(extract_PL(test['Trade post'][1].lower()))



history=[]
Error =[]

for trade in data:
    name = trade['Trade Name']
    articles = trade['Trade post']
    if "(TRADES)" in name:
        for article in articles:
            writer = article['Writer']
            postdateorg = article['Date']
            postdate = re.search('\d\d/\d\d/\d\d\d\d',postdateorg)[0]
            trade_list=[]
            error_list=[]
            trade_pattern = "(buy to open|buy to close|sell to close|sell to open)(.*?)(call|put)"
            strdecode = article['Post'].encode('ascii', errors='replace').decode().replace("?", " ")
            #strdecode= re.sub(r'[^\x00-\x7f]', " ", article)
            openclose=''
            trade_detail = re.findall(trade_pattern,strdecode.lower())
            if (trade_detail):
                trade_breakdown=[]
                error_breakdown=[]
                for t in trade_detail:
                    result = extract_trade_info(t)
                    if result[0]=="Error":
                        error_list.append((t,result[1]))
                    else:
                        tradeobject={"Action":result[0],"Number":result[1],"Symbol":result[2],"Date":result[3],"Strike":result[4],"Type":result[5]}
                        #(action,number,stock_symbol[0].upper().strip(),date[0].strip(),strike[0].strip(),option_type)
                        trade_breakdown.append(tradeobject)
                        if 'open' in result[0]:
                            openclose = 'open'
                        elif 'close' in result[0]:
                            openclose ='close'
                #trade_list.append(trade_breakdown)
                #error_list.append(error_breakdown)
                price = extract_price(strdecode.lower())
                earning_day = extract_earningday(strdecode.lower())
                pl = extract_PL(strdecode.lower())
                temp = {'Name': name,'Trade':trade_breakdown,'OpenClose':openclose, 'EarningDay':earning_day,'Price':price,'Profit':pl,'Writer':writer,'PostingDay':postdate,'Original':strdecode}
                history.append(temp)
                if len(error_list)>0:
                    temp2 ={'Trade Name':name, 'Error_parse':error_list}
                    Error.append(temp2)

with open('error2.json', 'w',encoding="utf-8") as file:
    for entry in Error:
        json.dump(entry, file)
        file.write('\n')

file.close()

with open('data3.json', 'w',encoding="utf-8") as file2:
    for entry in history:
        json.dump(entry, file2)
        file2.write('\n')
    #json.dump(history, file2)

file2.close()
f.close()




#[(Jan)(Feb)(Mar)(Apr)(May)(Jun)(Jul)(Aug)(Sep)(Oct)(Nov)(Dec)]*\d\d
#January|February|March|April|May|June|July|August|September|October|November|December
