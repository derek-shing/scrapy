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

how many trade have more than 2 post ?

With NOP as(
select name, max(postingday)as day, count(*) as numberofpost from  Trade.post
where postingday>'2022-01-01'
group by name
)

select * from NOP where numberofpost>2 order by day desc


How many open trade?


#select count(*) from Trade.post where OpenClose ='open'

#2553

#select count(*) from Trade.post where OpenClose ='close'

#2642

With NOP as(
select name, max(postingday)as day, count(*) as numberofpost from  Trade.post
where postingday>'2022-01-01'
group by name
)

select * from NOP where numberofpost>2 order by day desc

How man close trade?

#select count(*) from Trade.post where OpenClose ='close'

#2642

How many open but not closed?

list each profit , click to see the complete

Total Profit

How much profit by money (date can be the filter)

Step1:Calculate COST
WITH
costtable as(
SELECT name,OpenClose, avg(t.Number*price*100) as cost ,max(PostingDay) as buyingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='open'
group by Name,OpenClose),

sellingtable as(
SELECT name,OpenClose, avg(t.Number*price*100) as selling ,max(PostingDay) as sellingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='close'
group by Name,OpenClose)

select costtable.name, cost, selling, (selling - cost) as profit, buyingday, sellingday
from
costtable,sellingtable
where costtable.name = sellingtable.name
order by profit desc



Total Profits

costtable as(
SELECT name,OpenClose, avg(t.Number*price*100) as cost ,max(PostingDay) as buyingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='open'
group by Name,OpenClose),

sellingtable as(
SELECT name,OpenClose, avg(t.Number*price*100) as selling ,max(PostingDay) as sellingday FROM `optiontrader2.Trade.post`,unnest(Trade) as t
where Price is not null and PostingDay>"2022-01-01" and OpenClose='close'
group by Name,OpenClose)

select  sum((selling - cost)) as profit
from
costtable,sellingtable
where costtable.name = sellingtable.name






Average holding period

running accumlated acount value

what strategy ? Number of strategy ?

1.Straddle
2.Weekly Combo
3.calendar
4.Strangle
5.Hedged Strangle
6.Fly
7.Call Fly
8.Iron Fly
9.Hedged Straddle
10.Put Diagonal
11.Hedged Fly
12.Hold Through Earnings Combo
13.Non-Earnings Hedged Strangle
14.Call Fly
15.Hedged Call Vertical


underlying stock




array(['Weekly Combo', 'Straddle', 'calendar', 'Strangle', 'strangle',
       'Hedged Strangle', 'Fly', 'SPY fly', 'Call Fly', 'Iron Fly', '',
       'Hedged Straddle', 'Put Diagonal', 'Hold Through Earnings Combo',
       'Hedged Fly', 'Non-Earnings Hedged Strangle',
       'Hedged Call Vertical', 'ratio diagonal', 'Hedged Call Ratio',
       'straddle', 'Call Ratio', 'RIC', 'Reverse Call Butterfly',
       'hedged straddle', 'Put Ratio', 'diagonal', 'Double Call Ratio',
       'Hedged Put Ratio', 'fly', 'Reverse Iron Fly', 'hedged strangle',
       'put ratio', 'Ratio Diagonal', 'Iron Condor', 'backspread',
       'butterfly', 'Hedged Ratio', 'Iron butterfly', 'Ratio', 'Calendar',
       'iron butterfly', 'Unbalanced Butterfly', 'BWB', 'Iron Butterfly',
       'Butterfly', 'IC', 'call ratio', 'Put Ratio Spread',
       'Call Butterfly', 'Double Calendar', 'iron condor',
       'Broken Wing Condor', 'put credit spread', 'diagonal spread',
       'Risk Reversal', 'trade', 'put', 'Riks Reversal',
       'calendar strangle', 'reverse iron condor', 'Reverse Iron Condor',
       'Reverse iron Condor', 'Diagonal', 'Calendar strangle',
       'back ratio', 'call spread', 'Combo', 'call calendar',
       'put calendar', 'Put credit spread', 'call backspread',
       'call vertical', 'weekly calendar', 'double calendar',
       'Diagonal spread', 'strangle/calendar combo', 'backspread trade',
       'Calendar spread'], dtype=object)



Set Strategy base on name:

update Trade.post
set strategy = case
  when lower(name) like '%hedged strangle%' then 'Hedged Strangle'
  when lower(name) like '%calendar strangle%' then 'Calendar Strangle'
  when lower(name) like '%strangle%' then 'Strangle'
  when lower(name) like '%hedged straddle%' then 'Hedged Straddle'
  when lower(name) like '%straddle%' then 'Straddle'
  when lower(name) like '%weekly combo%' then 'Weekly Combo'

  when lower(name) like '%reverse call butterfly%' then 'Reverse Call Butterfly'
  when lower(name) like '%unbalanced butterfly%' then 'Unbalanced Butterfly'
  when lower(name) like '%iron butterfly%' then 'Iron Butterfly'
  when lower(name) like '%call butterfly%' then 'Call Butterfly'
  when lower(name) like '%butterfly%' then 'Butterfly'

  when lower(name) like '%calendar spread%' then 'Calendar Spread'
  when lower(name) like '%double calendar%' then 'Double Calendar'
  when lower(name) like '%call calendar%' then 'Call Calendar'
  when lower(name) like '%put calendar%' then 'Put Calendar'
  when lower(name) like '%calendar%' then 'Calendar'

  when lower(name) like '%reverse iron fly%' then 'Reverse Iron Fly'
  when lower(name) like '%hedged fly%' then 'Hedged Fly'
  when lower(name) like '%spy fly%' then 'SPY fly'
  when lower(name) like '%call fly%' then 'Call Flyo'
  when lower(name) like '%iron fly%' then 'Iron Fly'
  when lower(name) like '%fly%' then 'Fly'

  when lower(name) like '%hedged call ratio%' then 'Hedged Call Ratio'
  when lower(name) like '%double call ratio%' then 'Double Call Ratio'
  when lower(name) like '%hedged put ratio%' then 'Hedged Put Ratio'
  when lower(name) like '%put ratio spread%' then 'Put Ratio Spread'
  when lower(name) like '%call ratio%' then 'Call Ratio'
  when lower(name) like '%put ratio%' then 'Put Ratio'
  when lower(name) like '%back ratio%' then 'Back Ratio'

  when lower(name) like '%put diagonal%' then 'Put Diagonal'
  when lower(name) like '%ratio diagonal%' then 'Ratio Diagonal'
  when lower(name) like '%diagonal spread%' then 'Diagonal Spread'
  when lower(name) like '%diagonal%' then 'Diagonal'

  when lower(name) like '%hold through earnings combo%' then 'Hold Through Earnings Combo'

  when lower(name) like '%hedged call vertical%' then 'Hedged Call Vertical'
  when lower(name) like '%call vertical%' then 'Call Vertical'
  when lower(name) like '%ric%' then 'RIC'


  when lower(name) like '%reverse iron condor%' then 'Reverse Iron Condor'
  when lower(name) like '%broken wing condor%' then 'Broken Wing Condor'
  when lower(name) like '%iron condor%' then 'Iron Condor'

  when lower(name) like '%call backspread%' then 'Call Backspread'
  when lower(name) like '%put credit spread%' then 'Put Credit Spread'
  when lower(name) like '%backspread%' then 'Backspread'
  when lower(name) like '%call spread%' then 'Call Spread'


  when lower(name) like '%BWB%' then 'BWB'

where
  TRUE
