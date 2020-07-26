import BitVector
import constants

BLOCKSIZE = 8
key = input("Input in form of bits of size 10 (ex:1010010010):")
key = [int(x) for x in key]
key = constants.bits_to_decimal(key)

f = open("plaintext.txt", "r")
txt = f.read()
bv_plain = BitVector.BitVector(textstring = txt)
f.close()
bv_encrypt = BitVector.BitVector(size = 0)


for i in range(len(bv_plain)//BLOCKSIZE):
    bv_read = bv_plain[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
    bv_encrypt += constants.decimal_to_bits(constants.encrypt_byte(key, constants.bits_to_decimal(bv_read)))

hex = bv_encrypt.get_hex_string_from_bitvector()
f = open("encrypt.txt", "w")
f.write(hex)
f.close()
