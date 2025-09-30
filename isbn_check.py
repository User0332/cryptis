def isbn10_is_valid(isbn: str):
	assert len(isbn) == 10

	# we must satisfy the congruence Σ[i=1 to 10](i*x(i)) ≡ 0 (mod 11)

	lhs = 0

	for i, digit in enumerate(isbn, start=1):
		lhs+= i * (10 if digit == 'X' else int(digit))

	return lhs % 11 == 0 # validate congruence

def attach_checksum(isbn_stripped: str):
	# the check digit we choose must satisfy the congruence Σ[i=1 to 10](i*x(i)) ≡ 0 (mod 11)
	# this is equivalent to saying Σ[i=1 to 9](i*x(i)) ≡ x(10) (mod 11)

	lhs = 0

	for i, digit in enumerate(isbn_stripped, start=1):
		lhs+= i * int(digit)

	check_digit = lhs % 11 # this gives x(10) (RHS) of the congruence

	return isbn_stripped + ('X' if check_digit == 10 else str(check_digit)) # append check digit


def isbn13_is_valid(isbn: str):
	assert len(isbn) == 13

	raise NotImplementedError()

	# we must satisfy

print(isbn10_is_valid("1982156899"))
print(attach_checksum("198215689"))
