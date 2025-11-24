'''Para mostrar graficamente o vetor precisamos
do matplotlib'''
import numpy as np
import matplotlib.pyplot as plt

'''Abaixo utilizamos o método de "classe", que é uma forma de criar objetos com vários parâmetros e métodos específicos a ele, que é perfeito para vetores.'''
class Vetor:
    '''Nomes definidos fora do método construtor "__init__" são da classe que cria todos os objetos ou seja, são compartilhados entre todos os objetos existentes e que ainda não foram criados'''
    sempre_origem = True
    '''Verificado para até 3 dimensões'''
    def __init__(self, ponta=(0,1), pe=(0,0),nome='v'):
        '''Método que constrói o vetor. A notação que usaremos nos vetores será pe ---> ponta. Com a 'ponta' sendo o primeiro valor pedido podemos definir vetores na origem apenas com Vetor2D((posição_X, posição_Y)), se necessário usaremos o 'pe' para tira-lo da origem. Os nomes definidos no método __init__ são exclusivos do objeto que foi criado, i.e., se alterar no vetor 1, não influencia em nenhum outro vetor'''
        n=len(ponta)
        if n>2:
            aux = [0]*n
            pe = tuple(aux)
        self.pe = pe 
        self.ponta = ponta
        self.nome = nome
    
    def __str__(self):
        '''Faz com que, se é pedido o vetor diretamente (ex: print(vetor) ), o nome que foi dado ao vetor aparece ao invés do seu endereço ou a classe'''
        return "%s, origem: %s , fim: %s"%(self.nome,self.pe, self.ponta)
    
    def __add__(self, vetor):
        '''Permite a adição de dois vetores. Para garantir que some apenas vetores, precisamos de uma verificação.'''
        if type(vetor) == type(self):
            '''Para realizar a soma vetorial, a forma mais fácil é mover o segundo vetor de forma que a 'ponta' do primeiro conecta com o 'pe' do segundo'''
            #po1x, po1y = self.ponta
            #pe2x, pe2y = vetor.pe
            po1, pe2, po2 = [], [], []
            # nao da para fazer (1,2) + (1,2,3)
            self.ajustar_tamanho(vetor)
            for j in range(len(self.ponta)):
                po1.append(self.ponta[j])
                pe2.append(vetor.pe[j])
                po2.append(vetor.ponta[j])

            '''como vamos mudar a posição do vetor 2 para somar, vamos guardar a configuração inicial dele e usa-la depois'''
            #po2x, po2y = vetor.ponta 

            '''para saber o quanto mover o vetor 2 precisamos da diferença de coordenadas'''
            delta_x = pe2[0] - po1[0]
            if delta_x>0:
                '''pe do vetor 2 está a direita da ponta do vetor 1'''
                vetor.esquerda(delta_x)
            elif delta_x<0:
                '''pe do vetor 2 está a esquerda da ponta do vetor 1'''
                vetor.direita(delta_x)
            
            delta_y = pe2[1] - po1[1]
            if delta_y>0:
                '''pe do vetor 2 está acima da ponta do vetor 1'''
                vetor.baixo(delta_y)
            elif delta_y<0:
                '''pe do vetor 2 está abaixo da ponta do vetor 1'''
                vetor.cima(delta_y)

            if len(po2)>2:
                delta_z = pe2[2] - po1[2]
                if delta_z>0:
                    '''pe do vetor 2 está acima (em Z) da ponta do vetor 1'''
                    vetor.zminus(delta_z)
                elif delta_z<0:
                    '''pe do vetor 2 está abaixo (em Z) da ponta do vetor 1'''
                    vetor.zplus(delta_z)
                #para mais de 3 dimensoes, temos que generalizar os metodos zplus, zminus,cima,baixo,esquerda e direita em um unico

            '''As coordenadas do vetor 2 foram alteradas (sem modificar o vetor 2), agora o vetor soma será definido pelo 'pe' do vetor 1 ligado a 'ponta' do vetor 2'''
            self.sempre_origem = False
            #novopex, novopey = self.pe
            #novapontax, novapontay = vetor.ponta
            novo_pe , novo_ponta = [], []
            for j in range(len(self.pe)):
                novo_pe.append(self.pe[j])
                novo_ponta.append(vetor.ponta[j])

            novonome="%s+%s"%(self.nome,vetor.nome)
            #novo = Vetor(pe=(novopex,novopey),ponta=(novapontax,novapontay),nome=novonome)
            novo = Vetor(pe=tuple(novo_pe),ponta=tuple(novo_ponta),nome=novonome)
            #podemos ajustar o vetor 2 para a posição inicial
            vetor.pe = tuple(pe2)
            vetor.ponta = tuple(po2)
            return novo
        else:
            print(vetor, "Não pertence a classe Vetor!")

    def mover(self, sinal='+', coord=0,val=1):
        i = self.pe[coord]
        f = self.ponta[coord]
        aux_pe, aux_po = [], []
        for j in range(len(self.pe)):
            if j==coord:
                if sinal == '+':
                    pe = i+abs(val)
                    po = f+abs(val)
                else:
                    pe = i-abs(val)
                    po = f-abs(val)
                aux_pe.append(pe)
                aux_po.append(po)
            else:
                aux_pe.append(self.pe[j])
                aux_po.append(self.ponta[j])
        
        self.pe = aux_pe
        self.ponta = aux_po

    def zplus(self,val=1):
        self.mover('+',2,val)

    def zminus(self,val=1):
        self.mover('-',2,val)

    def direita(self,val=1):
        self.mover('+',0,val)

    def esquerda(self,val=1):
        self.mover('-',0,val)
        
    def cima(self,val=1):
        self.mover('+',1,val)
        
    def baixo(self,val=1):
        self.mover('-',1,val)
            
    def tamanho(self):
        '''Caso o vetor não seja paralelo a nenhuma eixo, pode ser útil saber seu tamanho. Para isso, basta considerar linhas que ligam os pontos (pe e ponta) diretamente aos eixos X e Y; escolher um dos triângulos formados com a hipotenusa entre o 'pe' e a 'ponta' e aplicar o teorema de Pitágoras'''
        #pex, pey = self.pe
        #pox, poy = self.ponta
        #hipotenusa = ( (pox-pex)**2 +(poy-pey)**2)**0.5
        hipotenusa2 = 0
        for j in range(len(self.pe)):
            auxpe, auxpo = self.pe[j], self.ponta[j] 
            hipotenusa2 += auxpo - auxpe

        return hipotenusa2**0.5
    
    def origem(self):
        '''Caso o vetor não comece na origem e você quer que ele comece, precisamos dos valores do pe para saber o quanto devemos move-lo'''
        #ix, iy = self.pe
        aux = self.pe
        #se uma das coordenadas já for zero não precisamos altera-la       
        #eixo X(j=0), Y(j=1), Z(j=3)
        for j in range(len(aux)):
            if aux[j]>0:
                # o vetor está a direita da origem
                self.esquerda(aux[j])
            elif aux[j]<0:
                # o vetor está a esquerda da origem
                self.direita(aux[j])
    def ajustar_tamanho(self,vetor):
        '''Força ambos vetores a manter o mesmo número de coordenadas para evitar erros'''
        n1, n2 = len(self.pe), len(vetor.pe)
        if n1 > n2:
            auxpe, auxpo = [], []
            for j in range(len(self.pe)):
                if j>=n2:
                    auxpe.append(0)
                    auxpo.append(0)
                else:
                    auxpe.append(vetor.pe[j])
                    auxpo.append(vetor.ponta[j])
            vetor.pe, vetor.ponta = auxpe, auxpo
        elif n2 > n1:
            auxpe, auxpo = [], []
            for j in range(len(vetor.pe)):
                if j>=n1:
                    auxpe.append(0)
                    auxpo.append(0)
                else:
                    auxpe.append(self.pe[j])
                    auxpo.append(self.ponta[j])
            self.pe, self.ponta = auxpe, auxpo

    def __rmul__(self,vetor):
        ''' Caso esteja por exemplo vet/escalar*vetor, colocamos para repetir o método de
         vetor * vet/escalar '''
        return self * vetor
    def __mul__(self,objeto):
        '''Entende como vetor * objeto'''
        if type(objeto) not in [int,float]:
            if type(objeto) == type(self):
                # Produto escalar
                self.ajustar_tamanho(objeto)
                #1: self, 2: objeto;  [[pe], [ponta]]
                # Produto escalar
                #  1*2 = sum_i: (1[1][i] - 1[0][i])*(2[1][i] - 2[0][i])
                prod = 0
                for j in range(len(self.pe)):
                    delt1 = self.ponta[j] - self.pe[j]
                    delt2 = objeto.ponta[j] - objeto.pe[j]
                    prod += delt1*delt2
                return prod
            else:
                print("Só aceitamos produto de vetor por um escalar ou outro vetor")
                return 404
        else:
            # Para o produto por escalar, basta multiplicar as coordenadas da ponta
            aux = []
            for j in range(len(self.ponta)):
                aux.append(self.ponta[j]*objeto)
            novo = Vetor(ponta=tuple(aux),pe=self.pe,nome="%.2f*%s"%(objeto,self.nome))
            return novo
        
    def produto_vetorial(self,vetor):
        #Colocar 2D e 3D como produto 3D
        for v in [self,vetor]:
            # fazer esse loop evita o caso de ambos serem 2D
            if len(v.pe) == 2:
                xpe, ype = v.pe
                xpo, ypo = v.ponta
                v.pe = (xpe, ype, 0)
                v.ponta = (xpo,ypo,0)
                break
            elif len(v.pe) == 1:
                # Por default, vou assumir sempre no eixo X
                xpe = v.pe
                xpo = v.ponta
                v.pe = (xpe, 0, 0)
                v.ponta = (xpo,0, 0)
                break

        self.ajustar_tamanho(vetor)
        # leitura dos vetores
        if len(self.pe) > 3:
            print("Não implementado produto de vetores com mais de 3 coordenadas")
            return 404
        auxs, auxv = [] , []
        for j in range(len(self.pe)):
            auxs.append(self.ponta[j] - self.pe[j])
            auxv.append(vetor.ponta[j] - vetor.pe[j])
        
        #       |i  j  k |
        # s^v = |sx sy sz| = (sy*vz-sz*vy)i +
        #       |vx vy vz|   (sz*vx-sx*vz)j +
        #                    (sx*vy-sy*vx)k
        novo_i = auxs[1]*auxv[2] - auxs[2]*auxv[1]
        novo_j = auxs[2]*auxv[0] - auxs[0]*auxv[2]
        novo_k = auxs[0]*auxv[1] - auxs[1]*auxv[0]
        # Por default, farei o produto ficar na origem
        novo = Vetor(ponta=(novo_i,novo_j,novo_k),pe=(0,0,0),nome="%s^%s"%(str(self.nome),str(vetor.nome)))
        return novo
        

# Para mostrar graficamente os vetores
def Mostre_vetor(vetores=[], referencia = Vetor((0,0)), pontos=[], conjuntos_pontos=1):
    '''Apenas cria gráficos 2D.
    Argumentos:
    vetores: um objeto de Vetor ou uma listas destes
    referencia: caso seja usado alguma herança mudando o tipo do vetor, coloque um exemplo de objeto aqui
    pontos: para plotar pontos extras representando retas ou curvas, será esperado o formato [(x1,y1),...] para um tipo ou [[(xa1,ya1),...],[(xb1,yb1),...]] para vários
    conjuntos_pontos: facilita a verificação da lista de pontos, definindo quantos conjuntos será dado. Ex: para duas retas ou uma reta + uma curva espera-se o valor 2'''
    fig = plt.figure(dpi=100)
    if type(vetores) == type(referencia):
        '''O método recebeu só um vetor. Pela definição do método 'quiver' precisamos deixar no formato a seguir'''
        x, y = vetores.pe
        xp,yp = vetores.ponta
        o = [x], [y] #pe do vetor
        p = [xp-x], [yp-y] # quantas unidades na direção da ponta do vetor
        plt.quiver(*o,*p,angles='xy', scale_units='xy',scale=1)
        '''Por algum motivo o 'quiver' não encaixa corretamente no zoom inicial do gráfico. Então ajustamos os limites dos eixos para o tamanho do vetor e adicionamos um espaço extra de margem'''
        apenas_vetor = True
        if len(pontos)!=0:
            apenas_vetor = False
            for i in range(conjuntos_pontos):
                ax, ay = [], []
                teste = pontos[i]
                if i==0:
                    #pontos: [(x,y),...]
                    #pontos: [[(x,y),..],[...]]
                    if len(teste)==2:
                        teste = pontos
                for j in teste:
                    #teste: [(x,y),...]
                    ax.append(j[0])
                    ay.append(j[1])
                plt.plot(ax,ay,'o')
        plt.grid(True)
        if apenas_vetor:
            #margem
            mx, my = ((xp - x)/10.0, (yp - y)/10.0)
            #limites do eixo x
            plt.xlim(x-mx, xp+mx)
            #limites do eixo y
            plt.ylim(y-my, yp+my)
    elif type(vetores) == type([]):
        '''O método recebeu uma lista, então, serão mais de um vetor no mesmo gráfico. Aqui faremos o mesmo que no caso acima, porém devemos verificar cada membro da lista para garantir que todos são vetores. Quanto aos limites do gráfico teremos que procurar os vetores com as maiores coordenadas e os vetores com as menores. Para diferenciar cada vetor estamos trocando suas cores e adicionando uma legenda.'''
        '''limites do gráfico XY: assumimos valores de troca fácil - valores que devem ser pequenos ou negativos recebem inicialmente valores grandes, e valores que devem ser grandes recebem valores muito negativos. Assim quando verificarmos cada vetor, usaremos como mínimo do gráfico o menor valor entre um grande daqui e um pequeno do vetor (o do vetor será escolhido), com essa mesma ideia comparamos os valores de cada vetor. Ideia analoga pra os limites maiores do gráfico.'''
        xini, xfim = 1000, -1000
        yini, yfim = 1000, -1000
        '''Sequência de cores nos vetores: blue(b), green(g), red(r), cyan(c), magenta(m), yellow(y), black(k)'''
        cores =['b','g','r','c','m','y','k']
        indice_cor=0
        for i in vetores:
            if type(i)!= type(referencia):
                print(i, "Não é do tipo Vetor2D!")
                return 404
            x, y = i.pe
            xp,yp = i.ponta
            #modificando os limites dos eixos
            xini = min(x,xp,xini)
            xfim = max(x,xp,xfim)
            yini = min(y,yp,yini)
            yfim = max(y,yp,yfim)

            o = [x], [y]
            p = [xp-x], [yp-y] 
            plt.quiver(*o,*p,angles='xy', scale_units='xy',scale=1,color=cores[indice_cor],label=i)
            indice_cor +=1
            if indice_cor == len(cores):
                indice_cor = 0
        #para a legenda aparecer no topo esquerdo
        plt.legend(loc="upper left") 
        # sobre o conjunto de pontos extras 
        apenas_vetor = True
        if len(pontos)!=0:
            apenas_vetor = False
            for i in range(conjuntos_pontos):
                ax, ay = [], []
                teste = pontos[i]
                if i==0:
                    #pontos: [(x,y),...]
                    #pontos: [[(x,y),..],[...]]
                    if len(teste)==2:
                        teste = pontos
                for j in teste:
                    #teste: [(x,y),...]
                    ax.append(j[0])
                    ay.append(j[1])
                plt.plot(ax,ay,'o')
        if apenas_vetor:
            #margem
            margemx, margemy = ((xfim - xini)/10.0, (yfim - yini)/10.0)
            plt.xlim(xini-margemx, xfim+margemx)
            plt.ylim(yini-margemy, yfim+margemy)
        plt.grid(True)
    else:
        #não é um vetor ou uma lista de vetores
        print(vetores, "Não é do tipo Vetor ou uma lista de Vetor!")
        return 404
          
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.show() 

# reta: r(x,y) = (x0,y0) + c*Vetor(vx(ponta-pe),vy(ponta-pe))
#      x = x0 + c*vx(ponta-pe)
#      y = y0 + c*vy(ponta-pe)
#  (x-x0)/vx(ponta-pe) = (y-y0)/vy(ponta-pe)
# y = y0 + vy(ponta-pe) * (x-x0)/vx(ponta-pe)
def reta2D(X=[-5+i for i in range(11)], ref=(0,0), vetor= Vetor((1,0))):
    vx = vetor.ponta[0] - vetor.pe[0]
    if vx==0:
        print("Componente x do Vetor é zero")
        vx=X[-1]/100 # para evitar divisao por zero
        print("Foi utilizado:", vx, 'no lugar')
    vy = vetor.ponta[1] - vetor.pe[1]
    lista = []
    for j in X:
        y = ref[1] + vy*(j-ref[0])/vx
        lista.append((j,y))
    return lista

def Mostre_vetor3D(vetores=[], referencia = Vetor((0,0,0)), pontos=[], conjuntos_pontos=1):
    # a fazer
    return 0

if __name__ == "__main__":
    a = Vetor((1,2),nome='a')
    b = Vetor((1,-2),nome='b')
    c = a+b
    r = reta2D(X=[-3+i for i in range(7)], vetor=a)
    s = reta2D(X=[-3+i for i in range(7)], vetor=b)
    #Mostre_vetor(vetores=a,pontos=r)
    #print(r)
    #print(s)
    Mostre_vetor(vetores=[a,b],pontos=[r,s],conjuntos_pontos=2)
    '''x = Vetor((1,0,0), nome='x')
    y = Vetor((0,1,0), nome='y')
    z = x.produto_vetorial(y)
    print(x,'\n',y)
    print(z)
    print("x^y*(-z)=", z*Vetor((0,0,-1))) # LI !=0
    print("x^y*(-x)=", z*Vetor((-1,0,0))) # LD == 0'''
    #print(a, b, "\nProduto escalar: ", a*b)
    #d = Vetor((1,2,3))
    #print(type(a)==type(d))# True ;D
    #Mostre_vetor([a,b,c])
    
