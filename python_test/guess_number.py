import random

dist = random.randint(1, 100)

guess = int(input("请输入你猜的数字："))
while guess != dist:
    guess = int(input("请输入你猜的数字："))
    if guess > dist:
        print("你猜的数字太大了")
    else:
        print("你猜的数字太小了")
    if guess == dist:
        print("恭喜你猜对了")