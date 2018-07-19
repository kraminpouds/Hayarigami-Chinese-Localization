import png
import struct


class FontConvert:
    def __init__(self):
        pass

    def __savePng(self, path, width, height, palette, data):
        with open(path, 'wb') as f:
            w = png.Writer(width, height, palette=palette, bitdepth=4)
            w.write(f, data)
            f.close()

    def __getTiles(self, tile_width, tile_height, tile_data):
        tiles = list()
        tile_size = tile_width * tile_height / 2
        for _i in range(0, len(tile_data), tile_size):
            tile = list()
            for y in range(0, tile_size, tile_width / 2):
                tile_x = list()
                for x in range(tile_width / 2):
                    tile_x.append(tile_data[_i + y + x] & 0xf)
                    tile_x.append((tile_data[_i + y + x] >> 4) & 0xf)
                tile.append(tile_x)
            tiles.append(tile)
        return tiles

    def __tilesToImageData(self, xc, yc, yh, tiles):
        img_data = list()
        for y in range(0, xc * yc, xc):
            for h in range(yh):
                h_data = list()
                for x in range(xc):
                    h_data += tiles[y + x][h]
                img_data.append(h_data)
        return img_data

    def __imageDataToTiles(self, width, height, tile_width, tile_height, img_data):
        tiles = list()
        count = len(img_data) / (tile_width * tile_height / 2)
        for b in range(0, width * height / 2, width * tile_height / 2):
            for t in range(0, width / 2, tile_width / 2):
                t_data = list()
                for y in range(0, width * tile_height / 2, width / 2):
                    for x in range(tile_width / 2):
                        t_data.append(img_data[b + y + t + x])
                tiles.append(t_data)
                count -= 1
                if not count:
                    return tiles
        return tiles

    @classmethod
    def ftxToPng(cls, ftx_path, png_path):
        width_count = 16
        height_count = 197
        size = 0xDDA00
        conv = cls()
        with open(ftx_path, 'rb') as fs:
            fs.seek(0x10, 0)
            palette = [[byte & 0xff for byte in bytearray(fs.read(4))] for _ in range(16)]
            fs.seek(0x1f430, 0)
            img_data = [byte & 0xff for byte in bytearray(fs.read(size))]
            tiles = conv.__getTiles(24, 24, img_data)
            data = conv.__tilesToImageData(width_count, height_count, 24, tiles)
            conv.__savePng(png_path, width_count * 24, height_count * 24, palette, data)

    @classmethod
    def tm2InFtx(cls, ftx_path, tm2_path):
        size = 0xDDA00
        width_count = 16
        height_count = 197
        conv = cls()

        with open(tm2_path, 'rb') as fs:
            fs.seek(0x18, 0)
            d_size = struct.unpack('<l', fs.read(4))[0]
            fs.seek(0x40, 0)
            data = [byte & 0xff for byte in bytearray(fs.read(d_size))]
            fs.close()

        if len(data) > size or len(data) < 0x120:
            print 'font size too big or too small'
            return

        if len(data) % 0x120:
            print 'font size tile size error'
            return

        tiles = conv.__imageDataToTiles(width_count * 24, height_count * 24, 24, 24, data)

        with open(ftx_path, 'rb+') as fw:
            fw.seek(0x1f430, 0)
            for tile in tiles:
                fw.write(bytearray(tile))
            fw.close()


def test1():
    FontConvert.ftxToPng("files/fonta.ftx", "dist/fonta.png")


def test2():
    FontConvert.tm2InFtx("dist/fonta.ftx", "dist/fonta1.tm2")


test2()
