from __future__ import unicode_literals
import json
import re

#!/usr/bin/env python
#coding=utf-8

f = open('post.json', encoding="utf-8")

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

  Day_pattern ="(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december)(.+)\d+(s+\d\d\d\d)?"

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

  '''
  number_of_contract_pattern ="\d+"
  number_of_contract = re.search(number_of_contract_pattern,trade[1])
  if (number_of_contract):
      reminding = trade[1][number_of_contract.end():]
  else:
      message+="Number of contract,"

  stock_symbol_pattern = "\w+"
  stock_symbol = re.search(stock_symbol_pattern, reminding)
  if (stock_symbol):
      reminding = reminding[stock_symbol.end():]
  else:
      message+="stock symbol, "

  reminding2 = reminding.lower()
  #Day_pattern ="[A-Z]\w\w\.\d+"
  Day_pattern ="(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|february|march|april|june|july|august|september|october|november|december).\d+(.\d\d\d\d)?"

  #print(reminding)
  date = re.search(Day_pattern,reminding2)
  if (date):
      reminding = reminding[date.end():]
  else:
      print(date, " ", reminding)
      message +="date "
      message +=reminding2


  strike_pattern="(?s:.*)\d+\.?\d*"
  strike = re.search(strike_pattern,reminding)
  if not(strike):
      message+="strike"

      '''

  if (number) and (stock_symbol) and (date) and (strike):
    return(action,number,stock_symbol[0].upper().strip(),date[0].strip(),strike[0].strip(),option_type)
  else:
      return(("Error",message))

history=[]
Error =[]

for trade in data:
    name = trade['Trade Name']
    post = trade['Trade post']
    if "(TRADES)" in name:
        trade_list=[]
        error_list=[]
        for article in post:
            trade_pattern = "(Buy to open|Buy to close|Sell to close|Sell to open)(.*?)(call|put)"
            strdecode = article.encode('ascii', errors='replace').decode().replace("?", " ")
            #strdecode= re.sub(r'[^\x00-\x7f]', " ", article)
            trade_detail = re.findall(trade_pattern,strdecode)
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
                #error_list.append(error_breakdown)
        #temp = {'Trade Name':name,'Trade':trade_list}
        temp = {'Trade Name':name,'Trade':trade_list}
        history.append(temp)
        if len(error_list)>0:
            temp2 ={'Trade Name':name, 'Error_parse':error_list}
            Error.append(temp2)

with open('error2.json', 'w',encoding="utf-8") as file:
    json.dump(Error, file)

file.close()

with open('data2.json', 'w',encoding="utf-8") as file2:
    json.dump(history, file2)

file2.close()
f.close()

#[(Jan)(Feb)(Mar)(Apr)(May)(Jun)(Jul)(Aug)(Sep)(Oct)(Nov)(Dec)]*\d\d
#January|February|March|April|May|June|July|August|September|October|November|December
