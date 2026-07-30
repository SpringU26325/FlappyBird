import datetime
date0=int(datetime.datetime.now().strftime('%Y%m%d'))
date1=date0**0.5
date2=date1-int(date1)
date3=date2*100
luck_value=int(date3)
print(luck_value)
if luck_value>=99:
    print(f'你今天的人品值为{luck_value}','你今天的运气爆棚')
elif 50<=luck_value<100:
    print(f'你今天的人品值为{luck_value}',"还不错")
elif 0<luck_value<50:
    print(f'你今天的人品值为{luck_value}',"今天的人品似乎不太好")
else:
    print(f'你今天的人品值为{luck_value}','WOW，中奖了')
