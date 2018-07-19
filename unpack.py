import struct
import os

f = open('files/story.dat', 'rb')
f.seek(0)
ds = struct.unpack("<l", f.read(4))[0]
len = struct.unpack("<l", f.read(4))[0]
cur = 8
index_list = []
for num in range(0, len):
    f.seek(cur + num * 8)
    id = struct.unpack("<l", f.read(4))[0]
    seek = struct.unpack("<l", f.read(4))[0]
    index_list.append([id, seek])

f.seek(0, os.SEEK_END)
all_len = f.tell()
index_list.append([-1, all_len])

if not os.path.exists('dist/story/'):
    os.makedirs('dist/story/')

fw_log = open('dist/story.log', 'wb')
loop = 1
for item in index_list:
    if item[0] == -1:
        break

    next_item = index_list[loop]
    fw_log.write('{:d}'.format(item[0]))
    fw_log.write('\n')
    fw = open('dist/story/{0}.dat'.format(item[0]), 'wb')
    f.seek(item[1])
    fw.write(f.read(next_item[1]-item[1]))
    loop += 1

fw_log.close()

