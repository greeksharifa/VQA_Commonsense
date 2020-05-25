import random

in_file = open('conceptnet_english.csv', 'r', encoding='utf-8')
# in_file = open('conceptnet-assertions-5.7.0.csv', 'r', encoding='utf-8')


# with open('conceptnet.csv', 'w', encoding='utf-8') as out_file:
with open('brief_conceptnet.csv', 'w', encoding='utf-8') as out_file:
    cnt = 0
    line_number = 0
    while True:

        line = in_file.readline()
        if not line:
            break
        splited = line.split(',')
        if random.randint(0, 3000) == 1:
        # if len(splited) >= 3 and splited[1].startswith('/c/en/') and splited[2].startswith('/c/en/'):
            out_file.write(line)
            cnt += 1

        line_number += 1
        if line_number % 1000 == 0:
            print('\r{:<10d} / {}'.format(cnt, line_number), end='')

print('done')