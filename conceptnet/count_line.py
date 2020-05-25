'''
brief.csv
line_number: 110
English line_number: 110

english.csv
line_number: 3422860
English line_number: 3422860

conceptnet-assertions-5.7.0.csv
line_number: 34074917
English line_number: 3422860
'''


FILES = [
    'brief_conceptnet.csv',
    'conceptnet_english.csv',
    'conceptnet-assertions-5.7.0.csv'
         ]
for FILE in FILES:


    with open(FILE, 'r', encoding='utf-8') as in_file:
        cnt = 0
        line_number = 0
        english = 0
        while True:
            line = in_file.readline()
            if not line:
                break
            cnt += 1
            line_number += 1
            splited = line.split(',')
            if len(splited) >= 3 and splited[1].startswith('/c/en/') and splited[2].startswith('/c/en/'):
                english += 1

            if line_number % 1000 == 0:
                print('\r{:<10d} / {}'.format(cnt, line_number), end='')

    print(FILE)
    print('line_number:', line_number)
    print('English line_number:', english)