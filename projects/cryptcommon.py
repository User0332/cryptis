import math
import random
from typing import Iterable

class CommunicationChannel:
	def __init__(self):
		self._messages: list[str | bytes | int | tuple[int, int]] = []

	def send(self, label: str, message: str | bytes | int | tuple[int, int]):
		self._messages.append((label, message))

	def peek(self) -> tuple[str, str | bytes | int | tuple[int, int]]:
		return self._messages[-1]
	
	def get_first(self, label: str) -> str | bytes | int | tuple[int, int] | None:
		for msg in self._messages:
			if msg[0] == label: return msg[1]

		return None
	
	def __str__(self):
		return "\n".join(f"{label}: {message}" for label, message in self._messages)

def xor_encrypt(message: str, key: int) -> bytes:
	return b''.join((ord(c) ^ key).to_bytes(4) for c in message)

def xor_decrypt(ciphertext: bytes, key: int) -> str:
	return ''.join(chr(int.from_bytes(ciphertext[i:i+4]) ^ key) for i in range(0, len(ciphertext), 4))

MAX_KEY = 2**32 - 1
MIN_KEY = 0

assert xor_decrypt(xor_encrypt("Hello, World!", MAX_KEY), MAX_KEY) == "Hello, World!" # sanity check


def gcd(a: int, b: int) -> int:
	"""Fast GCD using Euclidean Algorithm."""

	greater, lesser = max(a, b), min(a, b)

	while lesser != 0: # lesser = remainder
		temp = lesser

		# greater = q*lesser + r
		# then set greater = lesser, lesser = r
		lesser = greater % lesser
		greater = temp

	return greater


def factor_twos(n : int):
	"""Decomposes n into 2^k * q"""

	k = 0

	while (res := divmod(n, 2))[1] == 0:
		n = res[0]
		k+=1

	return (k, n)

def generate_possible_witnesses(n: int, length: int) -> Iterable[int]:
	possible_witnesses: list[int] = []

	while len(possible_witnesses) != length:
		possible_witness = random.randint(1, n-1)

		if possible_witness in possible_witnesses: continue # ensure uniqueness

		possible_witnesses.append(possible_witness)

	return possible_witnesses

def miller_rabin(n: int, iter: int=100) -> bool:
	"""Returns true if n is (probably) prime"""
	k, q = factor_twos(n-1)

	if k == 0: return False # n is even bru

	possible_witnesses = generate_possible_witnesses(n, iter)

	for a in possible_witnesses:
		if gcd(a, n) > 1: return False # don't even test witness, this number is composite as it shares divisor with a

		a = pow(a, q, n)

		if a == 1: continue # one witness passed (a^q ≡ 1 (mod n))

		for i in range(k):
			if a == n-1: break # one witness passsed (a^(2^i)q ≡ -1 (mod n))

			a = pow(a, 2, n)
		else: # no passing tests
			return False
		
	return True # all possible witnesses were witnesses!


def generate_prime(a: int=2**16, b: int=2**256):
	"""Uses Miller-Rabin test to probabilistically generate a prime between a and b (ends inclusive)"""

	while not miller_rabin(num := random.randint(a, b)): pass

	return num

def exp_encrypt(msg: str, e: int, n: int) -> int: # returns m^e (mod n)
	m = int.from_bytes(msg.encode())

	return pow(m, e, n)

def exp_decrypt(cipher: int, e: int, p: int, q: int) -> str:
	n = p*q

	# solve for d in ed ≡ 1 (mod (p-1)(q-1)) [modular inverse of e mod ...]
	mod = (p-1)*(q-1)

	d = pow(e, -1, mod) # we could solve with extd Euclidean alg or just use the builtin for now

	# undo the encryption
	msg_int = pow(cipher, d, n)

	return integer_to_str(msg_int)

def integer_to_str(msg_int: int) -> str:
	bytelength = (msg_int.bit_length() + 7) // 8

	return int.to_bytes(msg_int, length=bytelength).decode(errors="ignore")