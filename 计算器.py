#计算器最后写出来长这样
x=1#给计算次数赋值1
while True:#开始大循环
    num1 = input('请输入数字（按q键退出）：')

    if num1.upper() != 'Q':#第1,2类：如果按的不是Q
        try:#第1类：能换成小数
            num1 = float(num1)
            while input('按任意键开始或继续（按q键退出）：').upper() != 'Q':
                print(f'这是第{x}次计算')
                op = input('请输入运算符（按q键退出）：')
                num2 = float(input('请输入数字（按q键退出）：'))
                if op == '+':
                    num1 = num1 + num2
                    print(num1)

                elif op == '-':
                    num1 = num1 - num2
                    print(num1)

                elif op == '*':
                    num1 = num1 * num2
                    print(num1)

                elif op == '/':
                    while True:
                        try:
                            num1 = num1 / num2
                            print(num1)
                            break
                        except ZeroDivisionError:
                            print('0不能作除数，请重新输入')
                            break
                elif op == '^':
                    num1 = num1 ** num2
                    print(num1)

                elif op.upper() == 'Q':

                    break
                else:
                    print('输入有误')
                    continue
                x += 1
        except ValueError:#第2类不能换成小数
            print('输入有误')
            continue

    elif num1.upper() == 'Q':#第3类：按Q退出大循环
        print('计算结束')
        break

