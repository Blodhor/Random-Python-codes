'''In this file is written the following operations:
	*List summation {'for_vectors': sum_1d, 'for_matrix': sum}
	*1d-vector product
'''

class Vector_1d:
	'''There are very simple  - but useful in physics - methods defined here'''
	def __init__(self, vect1 = [], vect2 = []):
		if len(vect1) == 0 or len(vect2) == 0 or not len(vect1) == len(vect2):
			print("The vectors don't have the same length or both are null vectors\n")
			self.v1 = [] #object attribute
			self.v2 = [] #object attribute
		else:
			self.v1 = vect1 #object attribute
			self.v2 = vect2 #object attribute

	def sum_1d(self, op = '+'):
		'''
a=[a1,a2,...,an]; b=[b1,b2,...,bn]

if op == +
sum_1d =[a1+b1,a2+b2,...,an+bn]
else
sum_1d =[a1-b1,a2-b2,...,an-bn]'''
		summ = []
		if op == '+':
			for i in range(len(self.v1)):
				summ.append(self.v1[i]+self.v2[i])
		else:
			for i in range(len(self.v1)):
				summ.append(self.v1[i]-self.v2[i])
		
		return summ

	def dot_prod(self):
		'''
a=[a1,a2,...,an]; b=[b1,b2,...,bn]

sum_1d = a1*b1 + a2*b2 +...+ an*bn'''
		dot = 0
		for i in range(len(self.v1)):
			dot += self.v1[i]*self.v2[i]
		
		return dot

	def ext_prod(self):
		if len(self.v1) == 3:
			Ext = [self.v1[1]*self.v2[2] - self.v1[2]*self.v2[1], self.v1[2]*self.v2[0] - self.v1[0]*self.v2[2], self.v1[0]*self.v2[1] - self.v1[1]*self.v2[0]] 
		else:
			print("Sorry, this product was defined only for 3d vectors!\n")

		return Ext

class Matrix(Vector_1d):
	m1 = [[1,4],
	 	  [2,5]] #class attribute
	m2 = [[5,3],
	 	  [1,0]] #class attribute

	def __init__(self):
		'''This method is here just to show the polymorphism possibility and to stop the printing from Vector_1d'''

	def sum(self, op ='+'):
		if len(self.m1) != len(self.m2) or len(self.m1[0]) != len(self.m1[0]):
			'''We want only the traditional mathematical form of a matrix and not some random computational bullsh**!!'''
			print("Error in the format") #i'm still not too familiar with rasing exceptions :(
			return -1  
		msum = []
		if op == '+':
			for i in range(len(self.m1)):
				msum.append([])
				for j in range(len(self.m1[i])):
					msum[i].append( self.m1[i][j] + self.m2[i][j])
		else:
			for i in range(len(self.m1)):
				msum.append([])
				for j in range(len(self.m1[i])):
					msum[i].append( self.m1[i][j] - self.m2[i][j])

		return msum
