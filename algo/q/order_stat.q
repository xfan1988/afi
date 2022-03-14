/Simulate a 10-minute markt data and order; run lj[] aj[] wj[]

/10：00 - 10：10
/100 quotes; 50 trades; order of 1000 shares spread over 10 executions

N:100

\S 100
bid:50.00+ sums 0.01*N?(0;1)
spread:0.01*N?(1;2)
quotetime:10:00:00,asc 10:00:01+(N-1)?600-1
quote:([]time:quotetime; bid; spread)
quote:update ask:bid+spread from quote

M:20
tradetime:asc 10:00:00+M?600
trade:([]time:tradetime)
trade:aj[`time; trade;select time:quotetime, bid, ask from quote]

\S 200

trade:update side:M?(1;-1), size:M?(100;200;300;400;500) from trade
trade:update price:?[side>0;bid;ask] from trade

/VWAP price within (10:00; 10:10): 50.29139 for 7200 shares
select market_volume:sum size, vwap_price:wavg[size;price] from trade

/Order to fill 1000 shares; select 10 of the above M executions as order filled time
\S 300

fill_id:asc neg[10]?til M

order_execution:select from trade where i in fill_id
order_execution:update size:100 from order_exeuction
select fill_cnt:count i, avg_px:wavg[size;price] from order_execution

/VWAP Slippage: side*1e-4*((avg_px%vwap_px)-1)
/7.2 bps
1e4 * ((exec wavg[size;price] from order_execution)%(exec wavg[size;price] from trade))-1

/Arrival Slippage: side*1e-4*((avg_px%p0)-1)
/61.5 bps
1e4 * ((exec wavg[size;price] from order_execution) %(exec first 0.5*bid+ask from `time xasc quote))-1

/Interval statistics lookup by wj[]
w:-5 5+\:trade.time     /5 seconds before and 5 seconds after
update range_5_second:ask-bid from wj[w; `time; select time, size, price from trade; (quote;(min;`bid);(max;`ask))]

/Group by minute; lj market volume with order filled quantity
(select exec_cnt:count i, fill_qty:sum size, fill_price:wavg[size;price] by `minute$time from order_execution)
    lj (select trade_cnt:count i, volume:sum size, vwap:wavg[size;price] by `minute$time from trade)


