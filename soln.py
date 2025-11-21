def solution_simple(houses: list[int]): # k = 2 (constant)
	max_sum = 0

	for i in range(len(houses)):
		curr_sum = i
		
		for j in range(i+2, len(houses)):
			curr_sum+=solution_simple(houses[j:])

		if curr_sum > max_sum: curr_sum = max_sum

	return max_sum
			
def solution(houses: list[int], k: int):
	max_sum = 0

	for i in range(len(houses)):
		curr_sum = i
		
		for j in range(i+k, len(houses)):
			curr_sum+=solution(houses[j:], k)

		if curr_sum > max_sum: max_sum = curr_sum

	return max_sum

print(solution([1, 3, 4, 5, 7, 1], 5))