# coding=utf-8
import struct
import os
import glob
from os.path import basename
from os.path import splitext

fontPath = 'files/fonts0'
path = 'dist/OCCULTFILE'

fonts = {}
for f in glob.glob(os.path.join(fontPath, '*.txt')):
    with open(f, 'r') as fs:
        for line in fs:
            font = line.split('=')
            fonts[font[0]] = font[1].replace('\n', '')

index = []
with open('dist/OCCULTFILE.log', 'r') as fs:
    for line in fs:
        index.append(line.replace('\n', ''))

lines = []
for filename in index:
    text_line_index = 0
    with open(os.path.join(path, '{0}.dat'.format(filename)), 'rb') as f:
        str1 = ''
        code_len = 8
        while code_len:
            str1 += hex(ord(f.read(1))).replace('0x', '') + ' '
            code_len -= 1
        str1 = str1[:-1]
        lines.append("{0},{1:04d},{2}".format(filename, text_line_index, str1))
        text_line_index += 1

        str2 = ''
        while True:
            s = f.read(1)
            if ord(s) == 0:
                break
            elif (255 - ord(s)) >= 129:
                s += f.read(1)
                str2 += fonts[hex(struct.unpack(">H", s)[0]).replace('0x', '').upper()]
            else:
                str2 += chr(255 - ord(s))
        lines.append("{0},{1:04d},{2}".format(filename, text_line_index, str2))
        text_line_index += 1

        # 0 0 0 0 0 0 80 2 80 0 0 0 0 0 80 2 80 0 0 0
        # f.seek(0x48, os.SEEK_SET)
        # str1 = ''
        # code_len = 0x14
        # while code_len:
        #     str1 += hex(ord(f.read(1))).replace('0x', '') + ' '
        #     code_len -= 1
        # str1 = str1[:-1]
        # lines.append("{0},{1:04d},{2}".format(filename, text_line_index, str1))
        # text_line_index += 1

        f.seek(0x5c, os.SEEK_SET)
        str2 = ''
        s = f.read(1)
        while s:
            if ord(s) == 0:
                str2 += "{/}"
            elif (255 - ord(s)) >= 129:
                s += f.read(1)
                str2 += fonts[hex(struct.unpack(">H", s)[0]).replace('0x', '').upper()]
            else:
                str2 += chr(255 - ord(s))
            s = f.read(1)
        lines.append("{0},{1:04d},{2}".format(filename, text_line_index, str2))

with open('dist/OCCULTFILE' + '.txt', 'w') as fw:
    for line in lines:
        fw.write(line)
        fw.write('\n')
    fw.close()
