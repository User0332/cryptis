def round_robin_single_round(n: int, k: int):
	assert 1 <= k <= n-1

	paired_j = set[int]()

	for i in range(1, n): # iterate through teams 1, 2, ..., n-1
		j = (k - i) % (n-1) # j satisfies the congruence i + j ≡ k (mod n-1)

		# this only happens when k == i, yielding 0, an invalid team number.
		# We can skip this pairing since it doesn't exist and will be handled by a later iteration.
		if j == 0: continue

		# if i == j, the same team facing is itself, which is a solution to the congruence.
		# However, this is not possible, so we instead look at the situation as i + i ≡ k (mod n-1) => 2i ≡ k (mod n-1).
		# Since gcd(2, n-1) = 1 (n is even so n-1 must be odd), we know that the linear congruence 2i ≡ k (mod n-1) has
		# a unique congruence class solution mod n-1. Since team numbers are from 0 to n, then the only solution to this congruence
		# must be the current team we are inspecting. Thus, we can we can pair this team with the Nth team, which is not represented
		# by the congruence.
		if j == i: yield (i, n)
		
		# else, we can just return the pair (i, j) which satisfies the congruence
		else:
			if i in paired_j: continue # don't dupe these pairings since the congruence can have solutions (x, y) AND (y, x)

			paired_j.add(j)

			yield (i, j)

	if k == n-1: # this is an edge case that doesn't get handled by the loop:
		yield (k, n)

def round_robin_scheduler(n: int):
	assert n % 2 == 0, "n must be even"

	for k in range(1, n):
		yield round_robin_single_round(n, k)

def all_permut(n: int):
	for i in range(1, n+1):
		for j in range(1, n+1):
			if i == j: continue

			yield (i, j)

seen_pairings = set[tuple[int, int]]()

N = 6

for i, round_gen in enumerate(round_robin_scheduler(N), start=1):
	print(f"Round {i}")

	for pairing in round_gen:
		print(f"  Team {pairing[0]} vs Team {pairing[1]}")

		if pairing in seen_pairings:
			assert False, f"Duplicate match found! ({pairing})"

		seen_pairings.add(pairing)

normalized_seen = set(tuple(sorted(pair)) for pair in seen_pairings)
normalized_all_permut = set(tuple(sorted(pair)) for pair in all_permut(N)) # test against known soln

assert normalized_seen == normalized_all_permut