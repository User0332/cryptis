import math

def modinv(a: int, p: int):
	return pow(a, -1, p)


def find_match(g_power_list: list[int], inv_power_list: list[int]) -> tuple[int, int]:
	for i, babystep in enumerate(g_power_list): # yeah ik this is slow but its just for concept cause the finding part doesn't really matter here
		for j, giantstep in enumerate(inv_power_list):
			if babystep == giantstep:
				return i, j

	raise ValueError("this shouldn't be possible...")


def babystep_giantstep(p: int, g: int, pubkey: int) -> int:
	# g is of order N or less (g^N = e, so then g^N = 1 for the first positive N)
	N = p-1

	h = pubkey

	n = math.floor(math.sqrt(N)) + 1

	g_power_list = [pow(g, i, p) for i in range(0, n+1)] # generators won't be useful for sort

	u = modinv(g, p)
	inv_power_list = [(h * pow(u, j*n, p)) % p for j in range(0, n+1)]

	i, j = find_match(g_power_list, inv_power_list)

	# g^i = hg^(-jn) [mod p]
	# g^i * g^jn = h [mod p]
	# g^(i+jn) = h [mod p]
	# x = i + jn (g^x = h)

	privkey =  i+j*n

	return privkey