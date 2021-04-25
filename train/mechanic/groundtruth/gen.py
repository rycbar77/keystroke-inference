import os
pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(pwd)
pwd = os.path.join(pwd, '../')
for root, dirs, files in os.walk(pwd):
    for f in files:
        if f.split('.')[-1] == 'wav':
            content = f.split('.')[0]
            with open(content+'.txt', 'w') as fs:
                if len(content) == 1:
                    for i in range(20):
                        fs.write(content+'\n')
                elif content == 'space':
                    for i in range(20):
                        fs.write('<space>\n')
                else:
                    for i in content:
                        tmp_char = i
                        if tmp_char == '_':
                            tmp_char = '<space>'
                        fs.write(tmp_char+'\n')
