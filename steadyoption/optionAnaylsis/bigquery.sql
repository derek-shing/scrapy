select name, Trade.action
case
  when Trade.action like '%open' then 'open'
  when Trade.action like '%close' then 'close'
  else Trade.action
end as openclose
from Trade.post

Question :

How many completed/ open trade? (date can be the filter)

select name,count(*)as NumberOfPost,max(PostingDay) as closingDate
from Trade.post
group by name
order by closingDate desc

How much profit by money (date can be the filter)

Step1:Calculate COST
SELECT name,OpenClose, avg(t.Number*price*100) as cost ,max(PostingDay) as buyingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='open'
group by Name,OpenClose

SELECT name,OpenClose, avg(t.Number*price*100) as selling ,max(PostingDay) as sellingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='close'
group by Name,OpenClose




Average holding period

running accumlated acount value

what strategy ?

underlying stock
