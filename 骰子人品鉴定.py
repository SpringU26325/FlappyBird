import random
result = random.randint(1,6)
print(f'你掷出来的是{result}')
if result == 6:
    print("人品鉴定为：运气值爆棚10000+")
elif 2<=result <=5:
    print('人品鉴定为：Not Bad')
else:
    print('人品鉴定为：Bad Luck')