import BitVector
import constants

BLOCKSIZE = 8

f = open("encrypt.txt", "r")
hex = f.read()
bv_encrypt = BitVector.BitVector(hexstring = hex)
f.close()
tmp_ascii = bv_encrypt.get_bitvector_in_ascii()
max = 0
num = 0

for i in range(len(tmp_ascii)):
    tmp = tmp_ascii.count(tmp_ascii[i])
    if max < tmp:
        max = tmp
        num = i

max_letter = tmp_ascii[num]

list_char = [' ', 'e']
key_list = []

for char in list_char:
    tmp_list = []
    tmp = BitVector.BitVector(textstring = max_letter)
    for i in range(2**10):
        l = constants.decimal_to_bits(constants.decrypt_byte(i, constants.bits_to_decimal(tmp))).get_bitvector_in_ascii()
        if l == char:
            tmp_list.append(i)
    key_list.append(tmp_list)

max_i_c = 0
max_i_k = 0
max_i_a = 0
max_i_t = 0
for ch in range(len(key_list)):
    for k in range(len(key_list[ch])):
        bv_decrypt = BitVector.BitVector(size = 0)
        for i in range(len(bv_encrypt)//BLOCKSIZE):
            bv_read = bv_encrypt[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
            bv_decrypt += constants.decimal_to_bits(constants.decrypt_byte(key_list[ch][k], constants.bits_to_decimal(bv_read)))
        bv_decrypt_ascii = bv_decrypt.get_bitvector_in_ascii()
        temp_a = bv_decrypt_ascii.count("and")
        temp_t = bv_decrypt_ascii.count("the")
        if temp_a > max_i_a and temp_t > max_i_t:
            max_i_a = temp_a
            max_i_t = temp_t
            max_i_k = k
            max_i_c = ch

key = key_list[max_i_c][max_i_k]
sub_key = constants.key_generation(key)
bv_decrypt = BitVector.BitVector(size = 0)
for i in range(len(bv_encrypt)//BLOCKSIZE):
    bv_read = bv_encrypt[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
    bv_decrypt += constants.decimal_to_bits(constants.decrypt_byte(key, constants.bits_to_decimal(bv_read)))

f = open("recoveredtext.txt", 'w')
f.write(bv_decrypt.get_bitvector_in_ascii())
f.close()

key_bits = constants.decimal_to_bits_key(key)
sub_key_bits = [constants.decimal_to_bits(x) for x in sub_key]

print("Key: {0}\nSub_Key_1: {1}\nSub_Key_2: {2}".format(key_bits, sub_key_bits[0], sub_key_bits[1]))
