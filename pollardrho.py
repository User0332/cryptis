import random
from typing import Callable

# Euclidean algorithm to compute gcd

def gcd(a: int, b: int) -> int:
	greater, lesser = max(a, b), min(a, b)

	while lesser != 0: # lesser = remainder
		temp = lesser

		# greater = q*lesser + r
		# then set greater = lesser, lesser = r
		lesser = greater % lesser
		greater = temp

	return greater


def x_squared_plus_one(x: int) -> int:
	return x*x + 1

def yield_x(n: int, x0: int=2, f:Callable[[int], int]=x_squared_plus_one) -> int:
	x_last = x0

	while 1:
		x = f(x_last) % n
		yield x
		
		x_last = x