# Euclidean algorithm to compute gcd

def gcd(a: int, b: int) -> int:
	"""Fast GCD using euclidean algorithm."""

	greater, lesser = max(a, b), min(a, b)

	while lesser != 0: # lesser = remainder
		temp = lesser

		# greater = q*lesser + r
		# then set greater = lesser, lesser = r
		lesser = greater % lesser
		greater = temp

	return greater

def rrsm(n: int):
	"""Yields a reduced residue system modulo n."""

	for i in range(1, n):
		if gcd(i, n) == 1: # i and n are relatively prime, i is in the set
			yield i


def φ(n: int) -> int:
	"""Euler's totient function"""

	count = 0

	for i in range(1, n):
		if gcd(i, n) == 1: count+=1

	return count


def solve_linear_congruence(a: int, b: int, m: int):
	"""
	Solves the linear congruence ax ≡ b (mod m) using Euler's theorem.

	If a' is the modular inverse of a mod m, then the solution is given by:
		x ≡ b(a') (mod m)


	The inverse of a mod m only exists if (a, m) = 1, so we verify that first.

	Euler's theorem states that if (a, m) = 1, then:
		a^φ(m) ≡ 1 (mod m)

		Since (a, m) = 1, we can multiply both sides by the a' to get:
		a^(φ(m)-1) * a * a' ≡ a' (mod m)
		a^(φ(m)-1) ≡ a' (mod m)
		a' ≡ a^(φ(m)-1) (mod m)

		then multiply both sides of the original congruence by a^(φ(m)-1) to get:
		x ≡ b * a^(φ(m)-1) (mod m)


	This function returns ((b * a^(φ(m)-1)) mod m), which is congruent to x modulo m.
	"""

	if gcd(a, m) != 1:
		raise ValueError("a and m must be relatively prime")
	
	return (b * a**(φ(m)-1)) % m

print(list(rrsm(8)))
print(solve_linear_congruence(3, 4, 7)) # 3x ≡ 4 (mod 7) -> x ≡ 6 (mod 7)
print(solve_linear_congruence(2, 3, 5)) # 2x ≡ 3 (mod 5) -> x ≡ 4 (mod 5)
print(solve_linear_congruence(4, 5, 9)) # 4x ≡ 5 (mod 9) -> x ≡ 8 (mod 9)
