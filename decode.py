import base64
from io import BytesIO
from typing import IO
"""
第1位：8（不明）
第2段：套牌ID，通常3位
第3位：18（不明）
第4位：套牌名称长度
后N位：套牌名称
后1位：所有佣兵数据位长度，超过128的算2位，数据量会小于位数
[佣兵信息循环]：[10 位长度 8 ID 16 装备 24 皮肤 32 金钻] 装备可省略
1位：40（不明）
1位：2或3（不明）
"""


def decode(deck_string: str):
    try:
        decoded = base64.b64decode(deck_string)
        data = BytesIO(decoded)

        # print('套牌代码：', end='')
        # print(deck_string)

        while True:
            try:
                print(_read_varint(data), end=' ')
            except Exception:
                break
        print()
        data = BytesIO(decoded)

        _read_varint(data)
        deck_id = _read_varint(data)
        print('套牌ID：', end='')
        print(deck_id)

        _read_varint(data)
        name_length = _read_varint(data)  # decoded[6]

        print('套牌名称：', end='')
        name = data.read(name_length)  # decoded[7:7+name_length]
        print(name.decode('utf-8'))

        _read_varint(data)
        _read_varint(data)
        _read_varint(data)

        print('佣兵信息：')
        m_len1 = _read_varint(data)
        m_int_list = None
        while m_len1 > 0:
            pos = _read_varint(data)
            if pos > 127:
                pos_len = 2
            else:
                pos_len = 1
            if pos == 10 and not m_int_list:
                if m_int_list:
                    mdata_print(m_int_list)
                m_int_list = []
            else:
                m_int_list.append(pos)
            m_len1 -= pos_len
        mdata_print(m_int_list)

        _read_varint(data)
        _read_varint(data)
        print()

    except Exception as e:
        print(e)
        return


def mdata_print(m_int_list):
    if m_int_list:
        for i in range(len(m_int_list) // 2):
            x = m_int_list[i * 2 + 1]
            y = m_int_list[i * 2 + 2]
            if x == 8:
                print(f'  ID {y}', end=' ')
            elif x == 16:
                print(f'装备 {y}', end=' ')
            elif x == 24:
                print(f'皮肤 {y}', end=' ')
            elif x == 32:
                print(f'金钻 {y}')


def _read_varint(stream: IO) -> int:
    shift = 0
    result = 0
    while True:
        c = stream.read(1)
        if c == "":
            raise EOFError("Unexpected EOF while reading varint")
        i = ord(c)
        result |= (i & 0x7f) << shift
        shift += 7
        if not (i & 0x80):
            break
    return result


if __name__ == '__main__':
    deckcodes = [
        'CIqf1AoSBERFQ0sYASIAKAI=',  # 空套牌
        # 'CIqf1AoSBERFQ0sYASIICgYIGhg4IAAoAg==',
        # 'CIqf1AoSBERFQ0sYASILCgkIGhDAARg4IAAoAg==',
        # 'CIqf1AoSBERFQ0sYASILCgkIGhDBARg4IAAoAg==',
        # 'CIqf1AoSBERFQ0sYASIKCggIGhAwGDggACgC',
        # 'CIqf1AoSBERFQ0sYASIJCgcIXxjLASAAKAI=',  # 罗姆爸 原画 原皮 无装备
        # 'CIqf1AoSBERFQ0sYASIJCgcIXxjLASABKAI=',  # 罗姆爸 原画 金皮 无装备
        # 'CIqf1AoSBERFQ0sYASIJCgcIXxjNASABKAI=',  # 罗姆爸 画1 金皮 无装备
        # 'CIqf1AoSBERFQ0sYASIJCgcIXxjMASABKAI=',  # 罗姆爸 画2 金皮 无装备
        'CPG81AoSBERFQ0sYASIICgYIEhggIAAoAg==',  # 小罗姆 原画 原皮 无装备
        # 'CJLF1AoSBERFQ0sYASILCgkIEhCMARggIAAoAw==',  # 小罗姆 原画 原皮 装备1
        # 'CPG81AoSBERFQ0sYASIRCgcIXxjLASAACgYIEhggIAAoAg==',  # 罗姆爸 原画 原皮 无装备，小罗姆 原画 原皮 无装备
        # 'CIKKxAoSBue7g+WFtRgBIk4KCwiwAhDDAhifBCAACgsItwIQhwMYrwQgAAoLCKoCEMoCGJIEIAAKCwj2AhCCAxiVBSAACgsI1QIQ5AIY2AQgAAoLCKQCENcCGIMEIAEoAQ==',  # 测试
        # 'CJLF1AoSBERFQ0sYASIiCggIAxAKGFYgAAoJCBIQjAEYICAACgsI1QIQ5AIY2gQgAigD',
    ]
    for deckcode in deckcodes:
        decode(deckcode)

    print('CPG81AoSBERFQ0sYASIICgYIEhggIAAoAg==')
    code = base64.b64decode('CPG81AoSBERFQ0sYASIICgYIEhggIAAoAg==')
    print(code)
    x = code[:18] + b'\x67' + code[19:]
    print(x)
    print(base64.b64encode(x))
    # dode = BytesIO(code)
    # dode[19] = b'1'
