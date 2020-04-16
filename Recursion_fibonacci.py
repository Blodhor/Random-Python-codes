'''Using fibonacci sequence to show two forms of recursion'''


'''If you draw the recursion tree, you'll easly see how bad the recursion in fibo_lento is (exponential complexity).'''
def fibo_lento(n): #starts from 'n'
	if n ==0 or n==1:
		temp = 1
	else:
		temp = fibo_lento(n-2) + fibo_lento(n-1)
	return temp

'''In fibo_rapido, it's used dynamic programming, which makes the complexity linear (a much faster, but memory costing, way to do a recursion).'''
def fibo_rapido(n, l = []): #saves what it already made to avoid redundancies
	l = [-1]*(n+1)
	if l[n] == -1:
		vet = checar_fib(n,l) #if it knows the answer it'll just returns the answer, else it'll calculate through the fibonnaci formula
	return vet

def checar_fib(n, vetor):
	if vetor[n] == -1:
		if n == 0:
			vetor[n] = 1
		elif n == 1:
			checar_fib(0,vetor)
			vetor[n] =1
		else:
			checar_fib(n-2,vetor)
			checar_fib(n-1,vetor) 
			vetor[n] = vetor[n-1] + vetor[n-2] #fibonnaci formula
		return vetor   


if __name__ == "__main__":
	import sys
	if sys.argv[1] == 'slow':
		print(fibo_lento(int(sys.argv[2])))
	elif sys.argv[1] == 'fast':
		print(fibo_rapido(int(sys.argv[2])))
