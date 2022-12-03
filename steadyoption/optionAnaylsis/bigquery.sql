select name, Trade.action
case
  when Trade.action like '%open' then 'open'
  when Trade.action like '%close' then 'close'
  else Trade.action
end as openclose
from Trade.post
