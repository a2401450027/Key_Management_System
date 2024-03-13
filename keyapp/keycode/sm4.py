from django.shortcuts import render

S_BOX = [
	[0xd6, 0x90, 0xe9, 0xfe, 0xcc, 0xe1, 0x3d, 0xb7, 0x16, 0xb6, 0x14, 0xc2, 0x28, 0xfb, 0x2c, 0x05],
	[0x2b, 0x67, 0x9a, 0x76, 0x2a, 0xbe, 0x04, 0xc3, 0xaa, 0x44, 0x13, 0x26, 0x49, 0x86, 0x06, 0x99],
	[0x9c, 0x42, 0x50, 0xf4, 0x91, 0xef, 0x98, 0x7a, 0x33, 0x54, 0x0b, 0x43, 0xed, 0xcf, 0xac, 0x62],
	[0xe4, 0xb3, 0x1c, 0xa9, 0xc9, 0x08, 0xe8, 0x95, 0x80, 0xdf, 0x94, 0xfa, 0x75, 0x8f, 0x3f, 0xa6],
	[0x47, 0x07, 0xa7, 0xfc, 0xf3, 0x73, 0x17, 0xba, 0x83, 0x59, 0x3c, 0x19, 0xe6, 0x85, 0x4f, 0xa8],
	[0x68, 0x6b, 0x81, 0xb2, 0x71, 0x64, 0xda, 0x8b, 0xf8, 0xeb, 0x0f, 0x4b, 0x70, 0x56, 0x9d, 0x35],
	[0x1e, 0x24, 0x0e, 0x5e, 0x63, 0x58, 0xd1, 0xa2, 0x25, 0x22, 0x7c, 0x3b, 0x01, 0x21, 0x78, 0x87],
	[0xd4, 0x00, 0x46, 0x57, 0x9f, 0xd3, 0x27, 0x52, 0x4c, 0x36, 0x02, 0xe7, 0xa0, 0xc4, 0xc8, 0x9e],
	[0xea, 0xbf, 0x8a, 0xd2, 0x40, 0xc7, 0x38, 0xb5, 0xa3, 0xf7, 0xf2, 0xce, 0xf9, 0x61, 0x15, 0xa1],
	[0xe0, 0xae, 0x5d, 0xa4, 0x9b, 0x34, 0x1a, 0x55, 0xad, 0x93, 0x32, 0x30, 0xf5, 0x8c, 0xb1, 0xe3],
	[0x1d, 0xf6, 0xe2, 0x2e, 0x82, 0x66, 0xca, 0x60, 0xc0, 0x29, 0x23, 0xab, 0x0d, 0x53, 0x4e, 0x6f],
	[0xd5, 0xdb, 0x37, 0x45, 0xde, 0xfd, 0x8e, 0x2f, 0x03, 0xff, 0x6a, 0x72, 0x6d, 0x6c, 0x5b, 0x51],
	[0x8d, 0x1b, 0xaf, 0x92, 0xbb, 0xdd, 0xbc, 0x7f, 0x11, 0xd9, 0x5c, 0x41, 0x1f, 0x10, 0x5a, 0xd8],
	[0x0a, 0xc1, 0x31, 0x88, 0xa5, 0xcd, 0x7b, 0xbd, 0x2d, 0x74, 0xd0, 0x12, 0xb8, 0xe5, 0xb4, 0xb0],
	[0x89, 0x69, 0x97, 0x4a, 0x0c, 0x96, 0x77, 0x7e, 0x65, 0xb9, 0xf1, 0x09, 0xc5, 0x6e, 0xc6, 0x84],
	[0x18, 0xf0, 0x7d, 0xec, 0x3a, 0xdc, 0x4d, 0x20, 0x79, 0xee, 0x5f, 0x3e, 0xd7, 0xcb, 0x39, 0x48]
]
CK = [
		'00070e15', '1c232a31', '383f464d', '545b6269',
		'70777e85', '8c939aa1', 'a8afb6bd', 'c4cbd2d9',
		'e0e7eef5', 'fc030a11', '181f262d', '343b4249',
		'50575e65', '6c737a81', '888f969d', 'a4abb2b9',
		'c0c7ced5', 'dce3eaf1', 'f8ff060d', '141b2229',
		'30373e45', '4c535a61', '686f767d', '848b9299',
		'a0a7aeb5', 'bcc3cad1', 'd8dfe6ed', 'f4fb0209',
		'10171e25', '2c333a41', '484f565d', '646b7279'
]
FK = [0xa3b1bac6, 0x56aa3350, 0x677d9197, 0xb27022dc]

def c8_2(s):
    t = []
    for i in range(4):
        t.append(s[i*2:i*2+2])
    return t

#字符串转二进制
def char_b(text):
    b_text = text.encode()
    list_b_text = list(b_text)
    re = []
    for num in list_b_text:
        re.append(bin(num)[2:].zfill(8))

    bin_str = ''.join(re)
    return bin_str

def bin_char(dec):
    list_bin = [dec[i:i + 8] for i in range(0, len(dec), 8)]
    list_int = []
    for bin_s in list_bin:
        list_int.append(int(bin_s, 2))
    try:
        ans = bytes(list_int).decode()
    except:
        ans = '秘钥错误'
    return ans

def change_16(a):
    str_en = []
    for i in range(int(len(a) / 4)):
        s = a[i * 4:i * 4 + 4]
        m = 8
        sum = 0
        for j in s:
            sum += (int(j) - 0) * m
            m = int(m / 2)
        r = hex(sum)[2:]
        str_en.append(r)
    str_en = ''.join(str_en)
    return str_en

def change_2(b):
    str_de = []
    for i in b:
        if i>='a':
            m = ord(i) - ord('a') + 10
        else:
            m = ord(i) - ord('0')
        str_de.append(bin(m)[2:].zfill(4))
    str_de = ''.join(str_de)
    return str_de

def dchangen_16(a):
    s = []
    for i in range(4):
        s.append(change_16(a[i*8:i*8+8]))
    return s

#4个16进制字符异或
def mo_r4(s1,s2):
    s = []
    for i in range(4):
        hex_1 = int(s1[i], base=16)
        hex_2 = int(s2[i], base=16)
        s.append(hex(hex_1 ^ hex_2)[2:].zfill(2))
    return s
#小S盒变换
def subbytes(s1,box):
    a = int(s1[0], base = 16)
    b = int(s1[1], base = 16)
    return hex(box[a][b])[2:].zfill(2)

def str_rol(s, k):
    tt = k % len(s)
    return s[tt:] + s[:tt]
#SM4轮函数
def SM4_LunF(x0,x1,x2,x3,rk,f):
    m = mo_r4(x1,x2)
    m = mo_r4(m,x3)
    if f == 1:
        m = mo_r4(m, c8_2(rk))  # 完成异或
    else:
        m = mo_r4(m,rk) #完成异或
    lin_m = []
    for i in m:
        lin_m.append(subbytes(i,S_BOX))#完成τ运算
    bin_c = []
    for i in lin_m:
        bin_c.append(change_2(i))
    bin_c = ''.join(bin_c)
    b0 = dchangen_16(bin_c)
    if f == 0:
        b1 = dchangen_16(str_rol(bin_c, 2))
        b2 = dchangen_16(str_rol(bin_c, 10))
        b3 = dchangen_16(str_rol(bin_c, 18))
        b4 = dchangen_16(str_rol(bin_c, 24))
        L = mo_r4(b1,mo_r4(b2,mo_r4(b3,mo_r4(b4,b0))))
    else:
        b1 = dchangen_16(str_rol(bin_c, 13))
        b2 = dchangen_16(str_rol(bin_c, 23))
        L = mo_r4(b1,mo_r4(b2,b0))
    return mo_r4(L,x0)

#SM4反序变换
def SM4_R(s):
    t = []
    for i in range(4):
        t.append(s[3-i])
    return t
#行列转置
def changelr(s):
    t = []
    for i in range(4):
        for j in range(4):
            t.append(s[i*2+j*8:i*2+j*8+2])
    return ''.join(t)

#轮秘钥
def SM4_key(x0,x1,x2,x3,FK):
    k = ['0'] * 36
    k[0] = mo_r4(x0, c8_2(hex(FK[0])[2:].zfill(8)))
    k[1] = mo_r4(x1, c8_2(hex(FK[1])[2:].zfill(8)))
    k[2] = mo_r4(x2, c8_2(hex(FK[2])[2:].zfill(8)))
    k[3] = mo_r4(x3, c8_2(hex(FK[3])[2:].zfill(8)))
    rk = []
    for i in range(32):
        k[i+4] = SM4_LunF(k[i],k[i+1],k[i+2],k[i+3],CK[i],1)
        rk.append(k[i+4])
    return rk

def SM4_Encrypt(text,cyber,rk):
    clen = int(len(text) / 32)
    print(text)
    if len(text) % 32 == 0:
        clen -= 1
    enc = []
    length = 0
    while length <= clen:
        x = ['0'] * 36
        encry_s = []
        st = text[32 * length:32 * length + 32]
        if len(st)<32:
            st = st.zfill(32)
        # st = changelr(st)
        text1 = []
        str_c = []
        slen = 0
        for i in range(16):
            slen += 1
            text1.append(st[i*2:i*2+2])
            if slen == 4:
                str_c.append(text1)
                text1 = []
                slen = 0
        x[0] = str_c[0]
        x[1] = str_c[1]
        x[2] = str_c[2]
        x[3] = str_c[3]
        for i in range(32):
            x[i+4] = SM4_LunF(x[i],x[i+1],x[i+2],x[i+3],rk[i],0)
            encry_s.append(''.join(x[i+4]))

        enc.append(''.join(SM4_R(encry_s[28:32])))
        length += 1
    return enc


def SM4_Decrypt(text,cyber,rk):
    clen = int(len(text) / 32)
    if len(text) % 32 == 0:
        clen -= 1
    enc = []
    length = 0

    while length <= clen:
        x = ['0'] * 36
        encry_s = []
        st = text[32 * length:32 * length + 32]
        text1 = []
        str_c = []
        slen = 0
        for i in range(16):
            slen += 1
            text1.append(st[i * 2:i * 2 + 2])
            if slen == 4:
                str_c.append(text1)
                text1 = []
                slen = 0
        x[0] = str_c[0]
        x[1] = str_c[1]
        x[2] = str_c[2]
        x[3] = str_c[3]
        for i in range(32):
            x[i + 4] = SM4_LunF(x[i], x[i + 1], x[i + 2], x[i + 3], rk[i], 0)
            encry_s.append(''.join(x[i + 4]))
        lin_enc = ''.join(SM4_R(encry_s[28:32]))
        while lin_enc[0:2] == '00':
            lin_enc = lin_enc[2:]
        enc.append(lin_enc)
        length += 1
    return enc

#SM4
def SM4(text,cyber,dec):
    if len(cyber)<16:
        cyber = cyber.zfill(16)
    elif len(cyber)>16:
        cyber = cyber[0:16]
    cyber = change_16(char_b(cyber))
    # cyber = changelr(cyber)
    text1 = []
    str_c = []
    slen = 0
    for i in range(16):
        slen += 1
        text1.append(cyber[i * 2:i * 2 + 2])
        if slen == 4:
            str_c.append(text1)
            text1 = []
            slen = 0
    x0 = str_c[0]
    x1 = str_c[1]
    x2 = str_c[2]
    x3 = str_c[3]
    rk = SM4_key(x0,x1,x2,x3,FK)
    if dec == '1':
        bin_str = change_16(char_b(text))
        aa = SM4_Encrypt(bin_str,cyber,rk)
        aa = ''.join(aa)

    else:
        rk = rk[::-1]
        aa = SM4_Decrypt(text,cyber,rk)
        aa = ''.join(aa)
        aa = change_2(aa)
        aa = bin_char(aa)
    return aa

