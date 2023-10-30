'''Maquina de rotor baseada no RC4'''
def Help():
	'''Função simples de ajuda quando identifica algum erro'''
	print("O argumento deve seguir o formato a seguir:\n")
	print("python3 Cifra_Rotor.py modo n f1 f2 fn k1 l1 k2 l2 kn ln entrada saida\n")
	print("modo: 'C' ou 'D', para cifrar ou decifrar\n")
	print("n: Número de rotores de 1 a 5\n")
	print("f1/.../fn: Frases usadas para inicializar os respectivos rotores\n")
	print("k1/.../kn: A cada ki simbolos os rotores de movem\n")
	print("l1/.../ln: Quantas posições os rotores se movem\n")
	print("entrada/saida: Nomes dos arquivos de entrada e saida\n")

def Args_rotor(arg=['rotor.py','C','2','fra1','fra2','k1','l1','k2','l2','ent','out']):
	'''Leitura dos argumentos'''
	if arg[2].isdigit():
		if len(arg)== (int(arg[2])*3)+5:
			mode = arg[1]
			n = int(arg[2])
			keys = []
			for i in range(n):
				keys.append({})
				keys[i]['f']= arg[3+i]
				keys[i]['k']= int(arg[3+(i+1)*n])
				keys[i]['l']= int(arg[3+(i+1)*n+1])
			ent=arg[3+3*n]
			out=arg[3+3*n+1]#arg[-1]
			return (mode,keys,ent,out)
		else:
			Help()
	else:
		Help()

def Lendo_entrada(inpt='inpt.txt',modo='D', byte_tam = 3):
	'''Auto explicativo não?'''

	#caso a entrada nao seja um arquivo texto legivel
	from_binario = False
	try:
		#Assumindo que o arquivo é tipo um txt comum
		f = open(inpt,'r')
		p = f.readlines()
		f.close()

		#convertendo texto de entrada numa lista de simbolos
		plain=[]
		if modo.upper()=='C':
			for i in p:
				for j in i:
					'''if j == '\n':
					j=' ' '''
					plain.append(j)
		elif modo.upper()=='D':
			for i in p:
				plain.extend(i.split())
				#plain.append([])
	except UnicodeDecodeError:
		#Caso seja um binario
		from_binario = True
		f = open(inpt,'rb')
		p = f.read(byte_tam)
		plain = []
		while p:
			plain.append(int.from_bytes(p,'big')%256)
			p= f.read(byte_tam)
		f.close()

	return from_binario, plain

def S(modo='C',key_ini={'f':'BAUNILHA','k':1,'l':1},rotnum=1):
	'''Inicialização do rotor''' 
	temp=[]
	for i in range(256):
		temp.append(i)

	j=0
	for i in range(256):
		j= (j+ temp[i] + ord(key_ini['f'][i%len(key_ini['f'])])) % 256
		temp[i],temp[j] = temp[j],temp[i]

	Print_rot(mode=modo,rotnum=rotnum,key=key_ini,rot=temp)	
	return temp

def Rotor_girou(mdir='d',rotor=[1,2,3],l=1):
	'''Girando o rotor utilizando apenas os indices evita de criar rotores novos,
	mas como o rotor é pequeno (tamanho 256), a execução extra não faz muita diferença na velocidade.'''
	temp =[]
	if mdir=='d':
		move= l
	else:
		#'e'
		move= -l
	for i in range(len(rotor)):
		temp.append( rotor[(i+move)%len(rotor)] )
	del rotor
	return temp

def Cifra_rot(k=1,l=1,plaintext=['P','l','a'],rotor=[1,2,3],hexa=False,from_bin=False,cifrar_cifra=False):
	'''Modificação por símbolo lido para inteiro com a função ord e cifragem disso com o rotor'''
	cifra=''
	for i in range(len(plaintext)):
		if from_bin:
			indice = plaintext[i]
		elif cifrar_cifra:
			indice = int(plaintext[i])
		else:
			indice = ord(plaintext[i])
		c=rotor[indice]
		
    if hexa:
			if c<16:
				cifra += "%3s"%('0'+hex(c)[2:])	
			else:
				cifra += "%3s"%hex(c)[2:]
		else:
			cifra += "%3s "%c
		if (i+1)%k==0:
			rotor = Rotor_girou(rotor=rotor,l=l)
	return cifra

def derot(rot=[1,2,3]):
	'''Rotor inverso'''
	t = [0]*len(rot)
	for i in range(len(rot)):
		t[rot[i]]=i
	return t

def Decifra_rot(k=1,l=1,cifra=['28','157','226'],rotor=[1,2,3],hexa=False,decifra2cifra=False,debug=False):
	'''Inverso da função 'Cifra_rot'.'''
	decifra=''
	inv_rot= derot(rotor)
	for i in range(len(cifra)):
		if hexa:
			cc = int(cifra[i], 16)
		elif type(cifra[i])== int:
			cc = cifra[i]
		else:
			cc = int(cifra[i])
		d=inv_rot[cc]
		if decifra2cifra:
			decifra += "%3s "%str(d)
		else:
			decifra += chr(d)
		if debug:
			print("dentro do decifra: ", cc, d, decifra)

		if (i+1)%k==0:
			rotor = Rotor_girou(rotor=rotor,l=l,mdir='d')
			inv_rot= derot(rotor)
	return decifra

def Print_rot(mode='C',rotnum=1,key={'f':'GIROSCOPIO','k':1,'l':1},rot=[89,99,188,232,'...']):
	'''Impressão do rotor inicial'''
	print(mode, rotnum, key['f'], key['k'], key['l'])
	if mode.upper()=='D':
		rot = derot(rot)
	
	for i in range(16):
		s='%3d'%rot[16*i]	
		for j in range(1,16):
			s+= ' %3d'%rot[16*i+j]
		print(s)

def Processamento(modo='D',chaves=[{'f':'GIROSCOPIO','k':1,'l':1}],plain=['p','l','a'],from_binario=False,debug=False):
	'''Se tiver mais de uma chave, (de)cifro a cifra do primeiro rotor com o próximo rotor.'''
	tout = []
	rot_cnt=0
	cifrar_cifra=False
	tam_c = len(chaves)
	for i in range(tam_c):
		#print(i)
		rot_cnt+=1
		if modo.upper() == 'D':
			r = S(modo=modo,key_ini=chaves[tam_c-1-i],rotnum=rot_cnt)
			bool_dec = not cifrar_cifra
			tout = Decifra_rot(k=chaves[tam_c-1-i]['k'],l=chaves[tam_c-1-i]['l'],cifra=plain,rotor=r,hexa=hexadecimal,decifra2cifra=bool_dec,debug=Debug)
		else:
			r = S(modo=modo,key_ini=chaves[i],rotnum=rot_cnt)
			# cifra no formato string
			tout = Cifra_rot(k=chaves[i]['k'],l=chaves[i]['l'],plaintext=plain,rotor=r,hexa=hexadecimal,cifrar_cifra=cifrar_cifra,from_bin=from_binario)
		
		# para (de)cifrar a cifra com o proximo rotor
		plain = tout.split()
		if debug:
			print("\n plain:", plain)
		cifrar_cifra=True

	if debug:
		print("\n final:", tout)
		exit(0)
	return tout		

if __name__ == "__main__":
	import sys
	
	Debug = [False,True][0]
	hexadecimal = False #se 'True', transforma a cifra para hexadecimal# nao implementei direito essa parte, entao, deixe em False
	
	#Leitura dos argumentos
	try:
		modo,chaves,inpt,out = Args_rotor(arg=sys.argv)
	except:
		Help()
		exit()

	from_binario, plain = Lendo_entrada(inpt=inpt,modo=modo)
	
	tout = Processamento(modo=modo,chaves=chaves,plain=plain,from_binario=from_binario,debug=Debug)
	
	if modo.upper()=='C':
		f = open(out,'w')
		for i in tout:
			f.write(i)
	elif modo.upper()=='D':
		if tout.isnumeric():
			#decifrou e so tem numero na saida==entao deve ser binario em formato texto
			f = open(out,'wb')
			tempor = tout.split()
			by_arr = []
			for i in tempor:
				by_arr.append(int(i))
			f.write(bytearray(by_arr))
		elif not (tout.isalnum() and tout.isalpha()):
			f = open(out,'wb')
			f.write(tout.encode())
		else:
			f = open(out,'w')
			f.write(tout)
	f.close()
