def encrypt(message: str, key: int) -> bytes:
	return b''.join((ord(c) ^ key).to_bytes(4) for c in message)

def decrypt(ciphertext: bytes, key: int) -> str:
	return ''.join(chr(int.from_bytes(ciphertext[i:i+4]) ^ key) for i in range(0, len(ciphertext), 4))


MAX_KEY = 2**32 - 1
MIN_KEY = 0

assert decrypt(encrypt("Hello, World!", MAX_KEY), MAX_KEY) == "Hello, World!" # sanity check