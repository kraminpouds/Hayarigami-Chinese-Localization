import struct
import os

f = open('files/LOGIC.dat', 'rb')
f.seek(0)
count = struct.unpack("<l", f.read(4))[0]
cur = 4
index_list = []
for num in range(0, count):
    f.seek(cur + num * 8)
    index_list.append([
        struct.unpack("<l", f.read(4))[0],
        struct.unpack("<l", f.read(4))[0]]
    )

f.seek(0, os.SEEK_END)
all_len = f.tell()
index_list.append([-1, all_len])

if not os.path.exists('dist/LOGIC/'):
    os.makedirs('dist/LOGIC/')

fw_log = open('dist/LOGIC.log', 'wb')
loop = 1
for item in index_list:
    if item[0] == -1:
        break

    next_item = index_list[loop]
    fw_log.write('{:d}'.format(item[0]))
    fw_log.write('\n')
    fw = open('dist/LOGIC/{0}.dat'.format(item[0]), 'wb')
    f.seek(item[1])
    fw.write(f.read(next_item[1]-item[1]))
    loop += 1

fw_log.close()

