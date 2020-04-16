import random
import numpy as np
import matplotlib.pyplot as plt

'''
- numpy: 
	pip install scipy --user
- matplot:
	pip3 install setuptools
	pip3 install scipy
	pip3 install matplotlib
'''

class MonteCarloIntegral:
	'''Numerical method to calculate definite integral:

int from 'a' to 'b' of f(x)  = (b-a)*<f>

<f> => means statistical average

integral_a-b [f(x)] ~ ((b-a)/N)* Sum_i f(x_i)

In this method, in order not to need an immense number of x_i's for the summation value to be close to the integral, a reasonable amount of random x_i's is used between the values of the interval [a, b].'''
	def __init__(self,function,aa,bb,factor):
		'''Integration range defined by attributes 'a' and 'b'. Factor indicates how many thousands of x_i's to use. '''
		self.a = aa
		self.b = bb
		self.func = function
		self.n = factor * 1000
		self.areas = []

	def fill_areas(self):
		'''Calculates this random integral thousands of times and stores the results in the 'areas' attribute. The final result can then be obtained by the expected value. '''
		for i in range(1000):
			x_r = np.zeros(self.n)
			random.seed()

			for j in range(len(x_r)):
				x_r[j] = random.uniform(self.a,self.b)

			integral = 0.

			for j in range(self.n):
				integral += self.func(x_r[j])

			answer = ( (self.b-self.a)/float(self.n))*integral
			self.areas.append(answer)	

	def plot_hist(self,title):
		'''Histogram's results. We should obtain a Gaussian indicating the correct value of the integral. '''
		plt.title(title)
		plt.hist(self.areas, bins = 30, ec = 'black')
		plt.xlabel("Areas")
		plt.show()


if __name__ == "__main__":
	inicio = 0.
	fim = np.pi
	fat = 2

	'''In this example, we calculate the sine integral between 0.0 e pi == (-cos(pi) + cos(0.0) = 2)'''
	def f(x):
		return np.sin(x)

	print("This may take a few seconds...")
	int_seno = MonteCarloIntegral(f,inicio,fim,fat)
	int_seno.fill_areas()
	int_seno.plot_hist("Sine integral (Range: [0.0,pi])")

