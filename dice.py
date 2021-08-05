import random

def dice():
    a = random.randrange(1,7)
    b = random.randrange(1,7)

    if a > b:
        return "패배"
    elif a == b:
        return "무승부"
    elif a < b:
        return "승리"
