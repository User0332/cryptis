import math
from babystep_giantstep import babystep_giantstep, modinv

def factor(n: int) -> dict[int, int]:
	factors: dict[int, int] = {}

	for i in range(2, int(math.sqrt(n)) + 1):
		while n % i == 0:
			if i in factors:
				factors[i] += 1
			else:
				factors[i] = 1
			n //= i

	return factors

def pohlig_hellman(p: int, g: int, pubkey: int) -> int:
	# assume order is p-1
	N = p - 1
	h = pubkey

	factors = factor(N)

	congruences: list[tuple[int, int]] = [] # [(remainder, modulus), ...]

	for q, e in factors.items(): # q is prime factor, e is exponent
		g_i = pow(g, N//(q**e), p)
		h_i = pow(h, N//(q**e), p)

		# just use baby-step giant-step for now for each factor
		y_i = babystep_giantstep(p, g_i, h_i)
		congruences.append((y_i, q**e))

	# use CRT to combine congruences

	x = 0
	M = 1
	for _, modulus in congruences:
		M *= modulus

	for y_i, m_i in congruences:
		M_i = M // m_i
		inv = modinv(M_i, m_i)
		x += y_i * M_i * inv

	return x % M
