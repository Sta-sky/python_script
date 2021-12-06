"""
修改图片后缀名

"""

import os
base_path = "G:\\img\image\\{}"
filename = "G:\\img\\"

file = os.listdir(filename)
count = 0
for i in file:
    count +=1
    names = str(count) + '.jpg'
    filenames = base_path.format(names)
    filenamess = "G:\\img\\{}".format(i)
    print(filenamess)
    with open(filenamess,'rb') as f1:
        with open(filenames, 'wb') as f2:
            while True:
                s_bate = f1.read(1024)
                if s_bate == b'':
                    break

                f2.write(s_bate)


