# coding=utf-8
# date: 2016年7月22日 16:41:23
# name: Krad
# description: export TEXT from story.dat and convert old style to current style

import struct
import os
import glob
import shutil
import codecs
import re
from io import StringIO


class StoryParse(object):
    def __init__(self):
        self.story_index = []
        self.path = ""
        self.basename = ""
        self.data_offset = 0
        self.block_count = 0
        self.story_size = 0
        self.is_inline = 0
        self.buf_win_no = 0
        self.buf_win = StringIO()
        self.fw_code = None
        self.fw_text = None

        self.text_old = {}
        self.text_new = {}
        self.text_path = ""

    @staticmethod
    def _getBlockName(_block_id):
        _block_str = ""
        if _block_id in [8001, 8010, 8020, 8030, 8040, 8002, 8011, 8021, 8031, 8003, 8012, 8022, 8032, 8004, 8013, 8023,
                         8014, 8024, 8018, 8009, 8019, 9901, 8999, 1, 2, 20, 21, 30, 40]:
            _block_str = u"1-序章"
        elif _block_id in [10001, 10002, 10020, 10040, 10047, 10060, 10069, 10070, 10079, 10080, 10111, 18001, 18002,
                           10021, 10041, 10061, 10071, 10081, 10401, 10022, 10023, 10042, 10062, 10072, 10411, 10412,
                           10025, 10043, 10063, 10073, 10421, 10026, 10027, 10028, 10044, 10064, 10074, 10501, 10502,
                           10503, 10029, 10045, 10065, 10075, 10601, 10602, 10046, 10066, 10611, 10701, 10702, 10801,
                           10802, 10803, 17001, 10901, 10902, 10903, 17011, 10911, 17012, 17013, 10003, 11001, 17014,
                           17015, 17016, 17017, 10004, 11011, 11012, 11013, 11014, 17018, 17019, 10005, 11022, 11021,
                           11023, 16001, 17020, 11031, 11032, 16011, 16012, 11061, 16021, 17002, 11092, 15011, 16031,
                           17021, 12001, 15031, 16041, 17022, 17023, 12011, 12012, 15041, 16051, 17024, 17025, 12021,
                           15042, 15043, 16061, 17026, 17027, 12022, 12023, 12024, 15051, 16071, 17028, 12025, 15052,
                           15053, 15054, 16072, 16073, 16074, 12051, 12052, 15055, 16075, 15081, 15082, 16081, 16082,
                           101]:
            _block_str = u"2-零章"
        elif _block_id in [20001, 20002, 20003, 29000, 29100, 29200, 29300, 29400, 20011, 20004, 29001, 29101, 29201,
                           29301, 29401, 20021, 29011, 29012, 29111, 29112, 29211, 29212, 29311, 29312, 29411, 29412,
                           20031, 20032, 29021, 29022, 29121, 29122, 29221, 29222, 29321, 29322, 29421, 29422, 20041,
                           20042, 29131, 29132, 29231, 29331, 29332, 29431, 29432, 20043, 20044, 29133, 29241, 29341,
                           29342, 20051, 29351, 20061, 20071, 20072, 20073, 20081, 20091, 20101, 20111, 20121, 20122,
                           20123, 20131, 20132, 20133, 20141, 20142, 20143, 20151, 20161, 20171, 20181, 20191, 20192,
                           20201, 20202, 20211, 20212, 20213, 20221, 20231, 20241, 20261, 21001, 20271, 21011, 20281,
                           21021, 20291, 21031, 20301, 21041, 20311, 20312, 20313, 21051, 21052, 20321, 21061, 20331,
                           20332, 20333, 21071, 21072, 20341, 20342, 21081, 20351, 21091, 20361, 20362, 21101, 20371,
                           21112, 21122, 20381, 21131, 20391, 20392, 21141, 20401, 20402, 21151, 21161, 20411, 20412,
                           21171, 20421, 21181, 21182, 21183, 20431, 20432, 20433, 21191, 20441, 21201, 20451, 20452,
                           20453, 21211, 20461, 20462, 20463, 21221, 20471, 20472, 20473, 21231, 20481, 20482, 21241,
                           21242, 20491, 20492, 20493, 21251, 21252, 20501, 21261, 21262, 20511, 21271, 21272, 20521,
                           21281, 20531, 20532, 21291, 21294, 21295, 21296, 21297, 20541, 20542, 21301, 21302, 20551,
                           20552, 20561, 20562, 20571, 20572, 20581, 20582, 20583, 20591, 20592, 20593, 20601, 20604,
                           20605, 20606, 20607, 20611, 20612, 29999]:
            _block_str = u"3-一章"
        elif _block_id in [30001, 30002, 30102, 30030, 30201, 30010, 30301, 30020, 30311, 30313, 30040, 30041, 30321,
                           30401, 30411, 30412, 30501, 30521, 39000, 39001, 39002, 39004, 30522, 30533, 39003, 39005,
                           30602, 30603, 30701, 30711, 30712, 30901, 31001, 31301, 31311, 31312, 31331, 31401, 31451,
                           31452, 31453, 31601, 39102, 39104, 31643, 31642, 39100, 39101, 39103, 39106, 39105, 31644,
                           31701, 39107, 39108, 31901, 32101, 32201, 32221, 32222, 32401, 39300, 39330, 39331, 39333,
                           39335, 39336, 39339, 39340, 39342, 32501, 39332, 39334, 39337, 39341, 32601, 39338, 32611,
                           32612, 39400, 39410, 39420, 39440, 32613, 32614, 39421, 39430, 39450, 39461, 32615, 32616,
                           39441, 39460, 39470, 32701, 32702, 39431, 39442, 39471, 32801, 39443, 32901, 33101, 33111,
                           33112, 33121, 33201, 33211, 33212, 39575, 39578, 33301, 39500, 39570, 39571, 39573, 39574,
                           39576, 33401, 39572, 39577, 39580, 39582, 36101, 33501, 39583, 36201, 33601, 36221, 36222,
                           33621, 39600, 39610, 39601, 39603, 39604, 39607, 36301, 34001, 39602, 39605, 39608, 39625,
                           36321, 34101, 39620, 39606, 36331, 39800, 39870, 39871, 39873, 34111, 34112, 34113, 39621,
                           39622, 39624, 36411, 39872, 39874, 34321, 34322, 39623, 36501, 34331, 36611, 34401, 36621,
                           35101, 39700, 39710, 39758, 36701, 35211, 39754, 39756, 39759, 36711, 35301, 39755, 39757,
                           36801, 36802, 36803, 36804, 36805, 35311, 39761, 39763, 39766, 36901, 36902, 35321, 39762,
                           39764, 39767, 39768, 35401, 39765, 39769, 35421, 35441, 35442, 35443, 35444, 35445, 35501,
                           35502, 35521, 35601]:
            _block_str = u"4-二章"
        elif _block_id in [40001, 40002, 40011, 49000, 49001, 40021, 49010, 49012, 40031, 49020, 49021, 40041, 49030,
                           40051, 49040, 40061, 49050, 40071, 49060, 40081, 40091, 40092, 40093, 40094, 40101, 40111,
                           40112, 40121, 40141, 40151, 49200, 49201, 49208, 40161, 41001, 49202, 49203, 40171, 41011,
                           41012, 41013, 49204, 49205, 40172, 40173, 41021, 41022, 41023, 49206, 49207, 40181, 41031,
                           41032, 41033, 40200, 40201, 40202, 40203, 41041, 41042, 40182, 41051, 41100, 41101, 41102,
                           41103, 42000, 41052]:
            _block_str = u"5-最终话"
        elif _block_id in [50001, 50002, 50003, 50101, 50201, 50301, 50401, 50501, 50601, 50701, 50801, 50110, 50113,
                           50115, 50117, 50119, 50901, 50111, 50112, 50114, 50116, 50118, 51001, 51101, 50310, 50313,
                           50315, 50317, 50319, 51201, 50311, 50312, 50314, 50316, 50318, 51301, 51401, 51501, 51601,
                           51701, 51702, 51703, 51704, 51801, 51901, 51902, 51903, 50511, 50513, 50515, 50517, 50519,
                           52001, 50510, 50512, 50514, 50516, 50518, 52101, 52201, 50611, 50613, 50615, 50617, 50619,
                           52301, 50610, 50612, 50614, 50616, 50618, 52401, 52502, 52501, 52503, 52601, 52701, 50911,
                           50913, 50917, 50919, 52801, 50910, 50912, 50916, 50918, 52901, 51011, 51015, 51017, 51019,
                           53001, 51010, 51014, 51016, 51018, 53101, 54001, 54002, 54003, 54004, 53102, 53103, 53201,
                           53202, 53301, 53401]:
            _block_str = u"6-雾崎篇"
        elif _block_id in [60001, 60002, 60011, 60103, 60012, 60022, 60023, 60131, 60133, 60021, 60132, 60135, 60031,
                           60032, 60033, 60036, 60134, 60137, 60034, 60136, 60139, 60035, 60138, 60041, 60042, 60043,
                           60104, 60106, 60044, 60141, 60143, 60161, 60163, 60045, 60142, 60145, 60162, 60165, 60051,
                           60052, 60053, 60144, 60147, 60164, 60166, 60054, 60146, 60149, 60167, 60169, 60055, 60148,
                           60168, 60061, 60062, 60063, 60064, 60107, 60065, 60171, 60173, 60071, 60072, 60073, 60172,
                           60175, 60074, 60174, 60177, 60075, 60176, 60179, 60076, 60178, 60081, 60082, 60083, 60084,
                           60202, 60203, 60092, 60093, 60221, 60223, 60231, 60233, 60091, 60222, 60225, 60232, 60235,
                           60224, 60227, 60234, 60237, 60095, 60226, 60236, 60239, 69901, 69902, 69903, 69904, 60238,
                           60096, 60098, 60097, 69001, 69002, 69003, 69004]:
            _block_str = u"7-人见篇"
        elif _block_id in [70001, 70002, 70003, 70011, 70004, 71000, 71002, 71004, 71006, 71008, 71099, 70005, 71001,
                           71003, 71005, 71007, 71009, 70021, 70022, 70032, 70041, 70042, 70043, 70051, 70052, 70121,
                           70142, 71199, 71100, 70131, 70062, 70063, 71200, 71202, 71204, 71206, 71208, 70141, 71299,
                           70073, 70074, 71201, 71203, 71205, 71207, 70086, 70087, 70093, 70094, 70098, 70103, 70132,
                           70114, 70113, 70124, 70126, 70123, 70135, 70134, 70137, 71399, 70136, 70145, 70144, 70171,
                           70156, 70165, 70162, 70166, 70167, 70168, 70163, 70177, 70176, 70191, 70184, 70164, 70301,
                           70194, 70195, 70186, 70185, 70302, 70204, 70187, 70226, 70227, 70214, 70215, 70188, 70238,
                           71700, 70225, 72710, 71701, 71703, 71702, 71705, 71400, 71704, 71707, 71401, 71403, 71706,
                           71402, 71405, 71708, 71709, 71404, 71407, 71406, 71409, 70303, 71408, 70304, 71499, 72000,
                           70236, 72001, 72003, 72711, 72002, 72005, 72004, 72007, 72006, 72008, 72009, 70306, 70201,
                           70224, 70099, 79901, 79902, 79903, 79904, 70100, 70101]:
            _block_str = u"8-裕香篇"
        elif _block_id in [80001, 80002, 80003, 80004, 80011, 80021, 80031, 80041, 80051, 80061, 80071, 80081, 80091]:
            _block_str = u"9-退魔篇"

        return _block_str

    @staticmethod
    def _decryptCode(string):
        ns = ""
        for s in string:
            if ord(s):
                ns += chr(ord(s) ^ 0xff)
        return ns

    def _readOldStyle(self, old_style_path):
        style = re.compile("^[0-9A-F]{8},\\d+,")
        for f in glob.glob(os.path.join(old_style_path, '*.txt')):
            lines = codecs.open(f, "rb", "utf-16").readlines()
            for v in lines:
                if style.match(v) and len(v.split(",")) >= 3:
                    _offset = int(v.split(",")[0], 16)
                    # _len = int(v.split(",")[1], 10) # not use
                    string = ",".join(v.split(",")[2:])
                    string = string.replace("\r", "")
                    string = string.replace("\n", "")
                    self.text_old[_offset] = string
                else:
                    print "error:", v

    def _readNewStyle(self, new_style_path):
        style = re.compile("^\\d+,\\d+,")
        for f in glob.glob(os.path.join(new_style_path, '*.txt')):
            lines = codecs.open(f, "rb", "utf-16").readlines()
            for v in lines:
                if style.match(v) and len(v.split(",")) == 3:
                    _bid = int(v.split(",")[0], 10)
                    _num = int(v.split(",")[1], 10)
                    string = v.split(",")[2]
                    string = string.replace("\r", "")
                    string = string.replace("\n", "")
                    self.text_new[(_bid, _num)] = string
                else:
                    print "error:", v

    def _getStoryIndex(self, fn):
        fp = open(fn, "rb")
        self.data_offset = struct.unpack("I", fp.read(4))[0]
        self.block_count = struct.unpack("I", fp.read(4))[0]
        for i in xrange(self.block_count):
            _cnt_id, _cnt_offset = struct.unpack("2I", fp.read(8))
            self.story_index.append((_cnt_id, _cnt_offset))
        fp.close()
        for i in xrange(self.block_count):
            self.story_index[i] = (self.story_index[i][0], self.story_index[i][1],
                                   self.story_index[i + 1][1] if i + 1 < self.block_count else self.story_size)

    def unpack(self, story_fn, old_style_path=None, new_style_path=None):
        self.basename = os.path.basename(story_fn)
        self.story_size = os.path.getsize(story_fn)
        self.path = os.path.dirname(story_fn)
        old_style_path and self._readOldStyle(old_style_path)
        new_style_path and self._readNewStyle(new_style_path)

        os.path.exists("dist/story/code.txt") and os.remove("dist/story/code.txt")
        self.text_path = "dist/story/old_cn_text" if len(self.text_old) or len(self.text_new) else "dist/story/jp_text"
        os.path.exists(self.text_path) and shutil.rmtree(self.text_path)
        os.makedirs(self.text_path)

        self._getStoryIndex(story_fn)
        fp = open(story_fn, "rb")
        for index in self.story_index:
            self._parseBlock(index, fp)
        fp.close()

    def _parseBlock(self, index, fp):
        bid, offset, size = index
        b_name = self._getBlockName(bid)
        print bid, b_name, "%02x" % offset, "%02x" % size

        if not os.path.exists("dist/story/code.txt"):
            self.fw_code = codecs.open("dist/story/code.txt", "wb", 'utf-16')
            self.fw_code.write(u"")
        else:
            self.fw_code = codecs.open("dist/story/code.txt", "ab", 'utf-16-le')

        if not os.path.exists(os.path.join(self.text_path, "%s.txt" % b_name)):
            self.fw_text = codecs.open(os.path.join(self.text_path, "%s.txt" % b_name), "wb", 'utf-16')
            self.fw_text.write(u"")
        else:
            self.fw_text = codecs.open(os.path.join(self.text_path, "%s.txt" % b_name), "ab", 'utf-16-le')

        fp.seek(offset, os.SEEK_SET)
        pos = offset
        num = 0
        while pos < size:
            code = fp.read(1)
            if ord(code) == 0xff:
                code_len = ord(fp.read(1))
                fp.seek(-2, os.SEEK_CUR)
                code_data = fp.read(code_len)
                (code_len % 4) and fp.seek(4 - code_len % 4, os.SEEK_CUR)
                self._parseCode(code_data, (bid, pos, num))
            elif ord(code) == 0:
                # pos = fp.tell()
                # continue
                while code:
                    if ord(code) == 0xff:
                        fp.seek(-1, os.SEEK_CUR)
                        break
                    code = fp.read(1)
            else:
                text = ""
                # text
                while code:
                    if ord(code) == 0xff:
                        fp.seek(-1, os.SEEK_CUR)
                        break
                    elif ord(code) == 0x0:
                        pass
                    else:
                        text += code
                    code = fp.read(1)
                if len(text) == 1:
                    self._parseCode(text, (bid, pos, num))
                else:
                    self._parseText(text, (bid, pos, num))

            pos = fp.tell()
            num += 1
        self._clear_buf_win(bid, num)
        self.fw_code.close()
        self.fw_text.close()

    def _clear_buf_win(self, bid, num):
        if not self.buf_win.tell():
            return
        if self.is_inline == 2 and self.fw_text:
            self.fw_text.write("####%d,%04d####\r\n" % (bid, self.buf_win_no))
            self.fw_text.write(
                self.buf_win.getvalue()
                    .replace(u'㊧', u'♡')
                    .replace(u'㊨', u'廆')
                    .replace(u'㊤', u'㊧')
                    .replace(u'㊦', u'㊨'))
            self.fw_text.write('\r\n')
        elif self.fw_code:
            self.fw_code.write("%d,%04d," % (bid, self.buf_win_no))
            self.fw_code.write(self.buf_win.getvalue())
            self.fw_code.write('\r\n')
        else:
            raise Exception("should never reach here")

        self.is_inline = 0
        self.buf_win_no = num
        self.buf_win = StringIO()

    def _parseCode(self, data, info):
        bid, pos, num = info
        if ord(data[0]) != 0xff:
            if len(data) == 1:
                self._clear_buf_win(bid, num)
                self.buf_win.write(u"%s" % ":".join(["%02x" % ord(v) for v in data]))
                return
            else:
                print " ".join(["%02x" % ord(v) for v in data])
                raise Exception("should never reach here")
        code_type = struct.unpack("H", data[2:4])[0]
        if code_type == 0x00cc and self.is_inline == 2:
            if ord(data[4]) == 0x00:
                # 自动
                self.buf_win.write(u"{/}\r\n")
            elif ord(data[4]) == 0x01 and ord(data[5]) == 0x00:
                # 等待
                self.buf_win.write(u"\r\n")
            elif ord(data[4]) == 0x01 and ord(data[5]) == 0x03:
                # 段落
                self.buf_win.write(u"\r\n\r\n")
            else:
                raise "should never reach here - %04x" % 0x00cc
        elif code_type == 0x00ca and self.is_inline == 2:
            # 未知操作
            # 00 00 00 00 时候出现同行箭头等待按键
            var = struct.unpack("%dB" % len(data[2:]), data[2:])
            self.buf_win.write(u"{%s}" % ":".join(["%02x" % v for v in var]))
        elif code_type == 0x00c9:
            if not self.is_inline:
                self._clear_buf_win(bid, num)
                self.is_inline = 1
            # 延时
            if len(data) != 6:
                raise Exception("should never reach here")
            var = struct.unpack("H", data[4:6])[0]
            self.buf_win.write(u"{d:%d}" % var)
        elif code_type == 0x00d0 and self.is_inline == 2:
            # 假名起始 汉化不需要
            pass
        elif code_type == 0x00d1 and self.is_inline == 2:
            # 假名结束 汉化不需要
            pass
        elif code_type == 0x00d5:
            if not self.is_inline:
                self._clear_buf_win(bid, num)
                self.is_inline = 1
            # 玩家姓名
            if len(data) != 6:
                raise Exception("should never reach here")
            var = struct.unpack("H", data[4:6])[0]
            if var == 8:
                self.buf_win.write(u"{x}")  # 姓
            elif var == 9:
                self.buf_win.write(u"{m}")  # 名
            else:
                raise Exception("should never reach here")
        elif code_type == 0x00cf:
            if not self.is_inline:
                self._clear_buf_win(bid, num)
                self.is_inline = 1
            # 延时
            if len(data) != 6:
                raise Exception("should never reach here")
            var = struct.unpack("H", data[4:6])[0]
            self.buf_win.write(u"{s:%d}" % var)
        elif code_type == 0x00d9:
            if not self.is_inline:
                self._clear_buf_win(bid, num)
                self.is_inline = 1
            # 按钮
            if len(data) != 6:
                raise Exception("should never reach here")
            var = struct.unpack("H", data[4:6])[0]
            self.buf_win.write(u"{b:%d}" % var)
        elif code_type == 0x0323:
            self._clear_buf_win(bid, num)
            # 设定姓名
            self.buf_win.write(u"{sxm:")
            self.buf_win.write(u"%d:" % ord(data[4]))
            if pos + 4 in self.text_old:
                string = self.text_old[pos + 4]
            else:
                string = self._decryptCode(data[5:]).decode("cp932")
            self.buf_win.write(string)
            self.buf_win.write(u"}")
            self.is_inline = 2
        elif code_type == 0x0579:
            self._clear_buf_win(bid, num)
            # 登录词条
            var = struct.unpack("I", data[4:8])[0]
            self.buf_win.write(u"{word:%d:" % var)
            if pos + 8 in self.text_old:
                string = self.text_old[pos + 8]
            else:
                string = self._decryptCode(data[8:]).decode("cp932")
            self.buf_win.write(string)
            self.buf_win.write(u"}")
            self.is_inline = 2
        elif code_type == 0x03e9:
            self._clear_buf_win(bid, num)
            # 标签
            self.buf_win.write(u"{label:%s:" % ":".join(["%02x" % ord(v) for v in data[4:0xc]]))
            if pos + 0xc in self.text_old:
                string = self.text_old[pos + 0xc]
            else:
                string = self._decryptCode(data[0xc:]).decode("cp932")
            self.buf_win.write(string)
            self.buf_win.write(u"}")
            self.is_inline = 2
        else:
            self._clear_buf_win(bid, num)
            self.buf_win.write(u"%s" % ":".join(["%02x" % ord(v) for v in data]))

    def _parseText(self, text, info):
        bid, pos, num = info
        not self.is_inline and self._clear_buf_win(bid, num)
        if (bid, num) in self.text_new:
            string = self.text_new[(bid, num)]
            string \
                .replace(u"{r}", u"\r\n") \
                .replace(u"{/}", u"{/}\r\n") \
                .replace(u'㊧', u'㊤') \
                .replace(u'㊨', u'㊦') \
                .replace(u'♡', u'㊧') \
                .replace(u'廆', u'㊨')

        elif pos in self.text_old:
            string = self.text_old[pos]
        else:
            # 此处是正常逻辑
            string = self._decryptCode(text).decode("cp932")
        self.buf_win.write(string)
        self.is_inline = 2


sp = StoryParse()
sp.unpack("files/STORY.DAT")
# sp.unpack("files/STORY.DAT", "old", "new")

