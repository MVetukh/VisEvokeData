from random import randint


SPACE = '_'
STRAR = '*'


def toy(line):
    tmp = ''
    index = randint(0, len(line)-1)

    for i in range(len(line)):
        tmp += line[i] if i != index else 'o'

    return tmp


if __name__ == "__main__":
    rows = int(input())
    spaces = rows-1
    stars = 2

    for i in range(rows):
        print(
            (SPACE*spaces) +
            ((STRAR*stars) if (i % 2) != 0 else toy(STRAR*stars)) +
            (SPACE*spaces)
        )
        stars += 2
        spaces -= 1
print('С новым годом!!!!!')