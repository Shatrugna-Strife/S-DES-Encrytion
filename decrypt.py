import BitVector
import constants

BLOCKSIZE = 8
key = input("Input in form of bits of size 10 (ex:1010010010):")
key = [int(x) for x in key]
key = constants.bits_to_decimal(key)

f = open("encrypt.txt", "r")
hex = f.read()
bv_encrypt = BitVector.BitVector(hexstring = hex)
f.close()
bv_decrypt = BitVector.BitVector(size = 0)

for i in range(len(bv_encrypt)//BLOCKSIZE):
    bv_read = bv_encrypt[i*BLOCKSIZE:(i+1)*BLOCKSIZE]
    bv_decrypt += constants.decimal_to_bits(constants.decrypt_byte(key, constants.bits_to_decimal(bv_read)))

print(bv_decrypt.get_bitvector_in_ascii())
