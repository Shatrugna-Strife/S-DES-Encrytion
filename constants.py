import BitVector

KeyLength = 10
SubKeyLength = 8
DataLength = 8
FLength = 4


IP_list = (2, 6, 3, 1, 4, 8, 5, 7)
FP_list = (4, 1, 3, 5, 7, 2, 8, 6)


P10_list = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8_list = (6, 3, 7, 4, 8, 5, 10, 9)


EP_list = (4, 1, 2, 3, 2, 3, 4, 1)
S0_list = (1, 0, 3, 2, 3, 2, 1, 0, 0, 2, 1, 3, 3, 1, 3, 2)
S1_list = (0, 1, 2, 3, 2, 0, 1, 3, 3, 0, 1, 0, 2, 1, 0, 3)
P4_list = (2, 4, 3, 1)

def permutate(input_byte, perm_table):
    output_byte = 0
    for index, elem in enumerate(perm_table):
        if index >= elem:
            output_byte |= (input_byte & (128 >> (elem - 1))) >> (index - (elem - 1))
        else:
            output_byte |= (input_byte & (128 >> (elem - 1))) << ((elem - 1) - index)
    return output_byte

def ip_generation(input_byte):
    return permutate(input_byte, IP_list)

def fp_generation(input_byte):
    return permutate(input_byte, FP_list)

def swap_nibbles(input_byte):
    return (input_byte << 4 | input_byte >> 4) & 0xff

def key_generation(key):

    def leftShift(keyBitList):
        shiftedKey = [None] * KeyLength
        shiftedKey[0:9] = keyBitList[1:10]
        shiftedKey[4] = keyBitList[0]
        shiftedKey[9] = keyBitList[5]
        return shiftedKey

    keyList = [(key & 1 << i) >> i for i in reversed(range(KeyLength))]
    permKeyList = [None] * KeyLength
    for index, elem in enumerate(P10_list):
        permKeyList[index] = keyList[elem - 1]
    shifted_once_key = leftShift(permKeyList)
    shifted_twice_key = leftShift(leftShift(shifted_once_key))
    sub_key_1 = sub_key_2 = 0
    for index, elem in enumerate(P8_list):
        sub_key_1 += (128 >> index) * shifted_once_key[elem - 1]
        sub_key_2 += (128 >> index) * shifted_twice_key[elem - 1]
    return (sub_key_1, sub_key_2)

def fk_generation(sub_key, input_data):
    def fiestal(sKey, right_nibble):
        aux = sKey ^ permutate(swap_nibbles(right_nibble), EP_list)
        index1 = ((aux & 0x80) >> 4) + ((aux & 0x40) >> 5) + \
                 ((aux & 0x20) >> 5) + ((aux & 0x10) >> 2)
        index2 = ((aux & 0x08) >> 0) + ((aux & 0x04) >> 1) + \
                 ((aux & 0x02) >> 1) + ((aux & 0x01) << 2)
        sboxOutputs = swap_nibbles((S0_list[index1] << 2) + S1_list[index2])
        return permutate(sboxOutputs, P4_list)

    left_nibble, right_nibble = input_data & 0xf0, input_data & 0x0f
    return (left_nibble ^ fiestal(sub_key, right_nibble)) | right_nibble

def encrypt_byte(key, plaintext):
    data = fk_generation(key_generation(key)[0], ip_generation(plaintext))
    return fp_generation(fk_generation(key_generation(key)[1], swap_nibbles(data)))

def decrypt_byte(key, ciphertext):
    data = fk_generation(key_generation(key)[1], ip_generation(ciphertext))
    return fp_generation(fk_generation(key_generation(key)[0], swap_nibbles(data)))


def bits_to_decimal(bits):
    res = 0
    for ele in bits:
        res = (res << 1) | ele
    return res

def decimal_to_bits(decimal):
    res = [int(i) for i in list('{0:0b}'.format(decimal))]
    if len(res)!=8:
        for _ in range(8 - len(res)):
            res.insert(0, 0)
    return BitVector.BitVector(bitlist = res)

def decimal_to_bits_key(decimal):
    res = [int(i) for i in list('{0:0b}'.format(decimal))]
    if len(res)!=10:
        for _ in range(10 - len(res)):
            res.insert(0, 0)
    return BitVector.BitVector(bitlist = res)

# for i in range(2**10):
#     encrypt_byte(0b1110001110, 0b10101010)
# print(0b10101010, 0b1110001110, encrypt_byte(910, 170), decrypt_byte(910, 202))
