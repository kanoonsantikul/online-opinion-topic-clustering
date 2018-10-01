import os
from pathlib import Path

directory = Path(__file__).parents[0]

with open('../posts.csv', 'r') as post_list:
    lst = post_list.readlines()
    for line in lst:
        url = line.split(',')[0]
        num_comments = int(line.split(',')[1])

        if num_comments >= 160 and num_comments <= 169:
            file_name = url.split('/')[-1] + '.txt'
            try:
                os.rename(directory + '/data/' + file_name, directory + '/data/160-169/' + file_name)
            except:
                print('can not move', file_name)
                continue
