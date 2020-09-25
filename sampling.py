import random
import numpy as np
import matplotlib.pyplot as plt

class Sampling:
	def __init__(self, a=0, b=20, fator=10.):
		self.a = a
		self.b = b
		self.nome = "Amostragem aleatória"

		#desta maneira aumenta o numero de pontos, sem alterar o intervalo
		X = [x/fator for x in range(int(self.a*fator),int(self.b*fator))]
		Y = self.samples(X)

		Ind = np.zeros(len(X))
		for i in range(len(X)):
			Ind[i] = int(X[i]*fator)

		self.plot(Ind,Y)

	def plot(self, X, Y):

		plt.plot(X,Y)
		plt.title(self.nome)
		plt.ylabel("Amostra")
		plt.xlabel("Indice")
		plt.show()

	def samples(self, x_r = [1,2,3,4]):
		random.seed()
		samp = np.zeros(len(x_r))

		for j in range(len(x_r)):
			samp[j] = random.uniform(self.a,self.b)

		return samp

from scipy.stats import norm

def pgauss(esperanca, desv_pad):
	return lambda x: (np.e**(-( ((x-esperanca)/desv_pad)**2 )/2))

class MCMC_sampling(Sampling):
	def plot(self, X, Y):
		Ypai = Sampling.samples(self,X)
		fig, axs = plt.subplots(2, sharex=True, sharey=True)
		axs[0].plot(X,Ypai)
		axs[0].set_title("Amostragem aleatória")
		axs[1].plot(X,Y)
		axs[1].set_title("Amostragem de Metropolis")
		for ax in axs.flat:
			ax.set(xlabel='Indice', ylabel='Amostra')

		#como sao os mesmo eixos, o comando abaixo esconde as redundancias
		for ax in axs.flat:
			ax.label_outer()

		plt.show()

	def samples(self, x_r = [1,2,3,4]):
		self.nome = "Amostragem MCMC"
		#random.seed()
		samp = np.zeros(len(x_r))
		#ruido muito pequeno gera uma amostragem ruim
		ruido = abs(self.a -self.b)/5.

		#valor inicial
		samp[0] = 1.
		#definindo a pdf no centro do intervalo
		esperanca = (self.a + self.b)/2.
		desv_pad = abs(self.a -self.b)/4.
		pdf = pgauss(esperanca,desv_pad)
		
		for i in range(1,len(x_r)):
			prop = self.proposta(samp[i-1],ruido)
			#criterio de Metropolis
			razao_pdf = pdf(prop)/pdf(samp[i-1])
			if razao_pdf > random.uniform(0,1):
				samp[i] = prop
			else:
				samp[i] = samp[i-1]

		return samp

	def proposta(self, anterior, ruido):
		t = True
		Ab = False
		if self.a > self.b:
			Ab = True
		while t:
			#norm.rvs faz uma amostragem de tamanho 'size' numa dist. normal centrada em 'loc' com desvio 'scale'
			novo = anterior + norm.rvs(loc=0,scale=ruido,size=1)
			if Ab:
				#se 'novo' estiver no intervalo, retorne ele
				if novo >=self.b and novo <=self.a:
					t = False
			else:
				if novo >=self.a and novo <=self.b:
					t = False

		return novo

if __name__ == "__main__":
	ob2 = MCMC_sampling(fator=5.)
