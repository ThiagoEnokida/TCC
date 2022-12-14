#função para abrir o arquivo de texto para entrada e organização das variáveis#
def abertura():
    #abre-se o arquivo e busca os dados para alocalos para a maneira a se trabalhar
    arq= open ("entrada.txt","r")
    #inicia com o vetor inicial, que possui tamanho fixo
    vi=[0,0,0]
    inicial=arq.readline()
    valores=inicial.split()
    vi[0]=int(valores[0])
    vi[1]=int(valores[1])
    vi[2]=float(valores[2])
    #cria-se a matriz para alocar os valores dos nós
    mat_noz = []
    for i in range(0,(vi[0])):
        linha = []
        for j in range(7):
            linha.append(0)
        mat_noz.append(linha)
        #cria-se a matriz para alocar os valores dos elementos
    mat_element = []
    for i in range(0,(vi[1])):
        linha = []
        for j in range(10):
            linha.append(0)
        mat_element.append(linha)
    #insere a numeração na primeira coluna de cada matriz
    for i in range(0,vi[0]):
        mat_noz[i][0]=i+1
    for i in range(0,vi[1]):
        mat_element[i][0]=i+1
    cont=1
    #insere os valores da linha do arquivo em um vetor, que representa uma das linhas da matriz de nós
    for linha in arq:
        valores = linha.split()
        if cont<=vi[0]:
            v1=float(valores[1])
            v2=int(valores[2])
            v3=int(valores[3])
            v4=int(valores[4])
            v5=int(valores[5])
            v6=float(valores[6])
            mat_noz[cont-1][1]=v1
            mat_noz[cont-1][2]=v2
            mat_noz[cont-1][3]=v3
            mat_noz[cont-1][4]=v4
            mat_noz[cont-1][5]=v5
            mat_noz[cont-1][6]=v6
            cont+=1
        #insere os valores dos elementos em um vetor que representa a linha da matriz de elementos
        elif ((cont-vi[0])>=1 and (cont-vi[0])<=vi[1]):
            v1=int(valores[1])
            v2=int(valores[2])
            v3=mat_noz[v1-1][6]
            v4=mat_noz[v1][6]
            v5=float(valores[3])
            v6=float(valores[4])
            v7=int(valores[5])
            v8=float(valores[6])
            v9=mat_noz[v1][1]-mat_noz[v1-1][1]
            mat_element[cont-vi[0]-1][1]=v1
            mat_element[cont-vi[0]-1][2]=v2
            mat_element[cont-vi[0]-1][3]=v3
            mat_element[cont-vi[0]-1][4]=v4
            mat_element[cont-vi[0]-1][5]=v5
            mat_element[cont-vi[0]-1][6]=v6
            mat_element[cont-vi[0]-1][7]=v7
            mat_element[cont-vi[0]-1][8]=v8
            mat_element[cont-vi[0]-1][9]=v9
            cont+=1
    arq.close()    
    #retorna a matriz de nós, de elementos, e o coeficiente de detalhamento inserido
    return mat_noz,mat_element,vi[2]

#divide a matriz em N elementos, de acordo com o que é inserido no coeficiente de detalhamento
def detalhador(mat_noz,mat_element,det):
    newmat_noz=[]
    newmat_element=[]
    matposição=[]
    C=mat_noz[len(mat_noz)-1][1]
    #insere a primeira linha da nova matriz de elementos, e após isso, a apaga
    newmat_noz.append(mat_noz[0])
    matposição.append([mat_noz[0][0],mat_noz[0][1]])
    h1=mat_noz[0][6]
    h2=mat_noz[1][6]
    L=mat_noz[1][1]-mat_noz[0][1]
    memoria=mat_noz[0][1]
    mat_noz.pop(0)
    contador=0
    som=1
    #percorre por um contador detalhando e calculando novos nós, levando em conta de não sobrepor os nós da matriz original, e não pulando elementos
    while contador<(C/det):
        ver1=False
        ver2=False
        vet1=[0,0,0,0,0,0,0]
        if round(contador*det,2)>=mat_noz[0][1]:
            vet1=mat_noz[0]
            h1=mat_noz[0][6]
            h2=mat_noz[1][6]
            L=mat_noz[1][1]-mat_noz[0][1]
            memoria=mat_noz[0][1]
            mat_noz.pop(0)
            vet1[0]=contador+som
            newmat_noz.append(vet1)
            matposição.append([contador+som,vet1[1]])
            vet1=[0,0,0,0,0,0,0]
            ver1=True
        if round(contador*det,2)!=memoria:
            ver2=True
            xrel=(contador*det)-memoria
            if ver1==True and ver2==True:
                som+=1
            vet1[0]=(contador+som)
            vet1[1]=(round(contador*det,2))
            vet1[2]=(0)
            vet1[3]=(0)
            vet1[4]=(0)
            vet1[5]=(0)
            vet1[6]=(round(((((h2-h1)/L))*xrel)+h1,15))
            newmat_noz.append(vet1)
        contador+=1
    mat_noz[0][0]=contador+som
    newmat_noz.append(mat_noz[0])
    matposição.append([mat_noz[0][0],mat_noz[0][1]])
    posicionador=0
    #recria a matriz de elementos a partir dos novos nós inseridos no laço de repetição anterior
    for i in range(len(newmat_noz)-1):
        if i+1==matposição[posicionador][0]:
            q1=mat_element[posicionador][5]
            q2=mat_element[posicionador][6]
            E=mat_element[posicionador][7]
            b=mat_element[posicionador][8]
            L=mat_element[posicionador][9]
            posicionador+=1
            somador=0
        vet1=[]
        vet1.append(i+1)
        vet1.append(i+1)
        vet1.append(i+2)
        vet1.append(newmat_noz[i][6])
        vet1.append(newmat_noz[i+1][6])
        vet1.append((((q2-q1)/L)*somador)+q1)
        somador+=round(newmat_noz[i+1][1]-newmat_noz[i][1],14)
        vet1.append((((q2-q1)/L)*somador)+q1)
        vet1.append(E)
        vet1.append(b)
        vet1.append(round(newmat_noz[i+1][1]-newmat_noz[i][1],14))
        newmat_element.append(vet1)
    #retorna as novas matrizes que serão utilizadas, caso haja detalhamento
    return newmat_noz,newmat_element


#recebe as variaveis para criar a matriz de equações para o elemento finito
def processarmatlocal(v):
    #v=[E,b,L,h1,h2]
    #criação da matriz 4x4
    mat=[]
    for i in range(4):
        linha = []
        for j in range(4):
            linha.append(0)
        mat.append(linha)
    #inserção dos valores da matriz (previamente descrito no referencial teórico)
    mat[0][0]=((((21*v[3]**3)+(9*(v[3]**2)*v[4])+(9*v[3]*(v[4]**2))+(21*v[4]**3))*(v[0]*v[1]))/((v[2]**3)*60))
    mat[0][1]=((((15*v[3]**3)+(6*(v[3]**2)*v[4])+(3*v[3]*(v[4]**2))+(6*v[4]**3))*(v[0]*v[1]))/((v[2]**2)*60))
    mat[0][2]=((((-21*v[3]**3)+(-9*(v[3]**2)*v[4])+(-9*v[3]*(v[4]**2))+(-21*v[4]**3))*(v[0]*v[1]))/((v[2]**3)*60))
    mat[0][3]=((((6*v[3]**3)+(3*(v[3]**2)*v[4])+(6*v[3]*(v[4]**2))+(15*v[4]**3))*(v[0]*v[1]))/((v[2]**2)*60))
    mat[1][0]=mat[0][1]
    mat[1][1]=((((11*v[3]**3)+(5*(v[3]**2)*v[4])+(2*v[3]*(v[4]**2))+(2*v[4]**3))*(v[0]*v[1]))/((v[2])*60))
    mat[1][2]=((((-15*v[3]**3)+(-6*(v[3]**2)*v[4])+(-3*v[3]*(v[4]**2))+(-6*v[4]**3))*(v[0]*v[1]))/((v[2]**2)*60))
    mat[1][3]=((((4*v[3]**3)+(1*(v[3]**2)*v[4])+(1*v[3]*(v[4]**2))+(4*v[4]**3))*(v[0]*v[1]))/((v[2])*60))
    mat[2][0]=mat[0][2]
    mat[2][1]=mat[1][2]
    mat[2][2]=((((21*v[3]**3)+(9*(v[3]**2)*v[4])+(9*v[3]*(v[4]**2))+(21*v[4]**3))*(v[0]*v[1]))/((v[2]**3)*60))
    mat[2][3]=((((-6*v[3]**3)+(-3*(v[3]**2)*v[4])+(-6*v[3]*(v[4]**2))+(-15*v[4]**3))*(v[0]*v[1]))/((v[2]**2)*60))
    mat[3][0]=mat[0][3]
    mat[3][1]=mat[1][3]
    mat[3][2]=mat[2][3]
    mat[3][3]=((((2*v[3]**3)+(2*(v[3]**2)*v[4])+(5*v[3]*(v[4]**2))+(11*v[4]**3))*(v[0]*v[1]))/((v[2])*60))
    for i in range (len(mat)):
        print (mat[i])
    #for i in range (len(newmat_element)):
        #print (newmat_element[i])
    return mat

def matglobal(mat_noz,mat_element):
    #criar vetor de entrada para função matglobal()
    ent=[0,0,0,0,0]
    #cria matriz quadrada com i e j igual a 2 vezes o numero de nós
    matglobal=[]
    for i in range((mat_noz[len(mat_noz)-1][0])*2):
        linha = []
        for j in range((mat_noz[len(mat_noz)-1][0])*2):
            linha.append(0)
        matglobal.append(linha)
    #cria a matriz local para processamento
    matlocal=[]
    for i in range(4):
        linha = []
        for j in range(4):
            linha.append(0)
        matlocal.append(linha)
    posicionador=0
    #processamento da matriz global
    for i in range(len(mat_element)):
        #aloca os dados necessarios no vetor de entrada
        ent=[mat_element[i][7],mat_element[i][8],mat_element[i][9],mat_element[i][3],mat_element[i][4]]
        #processa os dados do vetor de entrada na função matlocal
        matlocal=processarmatlocal(ent)
        #adiciona o valor da matlocal a sua reespectiva coordenada na matglobal
        #posicionador é um ponto de partida que avança de 2 em 2 a cada fim de laço para fixar um novo ponto de partida da matglobal
        for j in range(4):
            for k in range(4):
                if posicionador<(len(matglobal)):
                    matglobal[posicionador+j][posicionador+k]+=matlocal[j][k]
        posicionador+=2
    return matglobal

#calcula o vetor de forças, para levar em conta as forças distribuídas
def vetorforças(mat_noz,mat_element):
    vetforças=[]
    vetesf=[0,0,0,0]
    for i in range(mat_noz[len(mat_noz)-1][0]):
        vetforças.append("F")
        vetforças.append("M")
    for i in range(len(mat_noz)):
        vetforças[i*2]=mat_noz[i][4]
        vetforças[(i*2)+1]=mat_noz[i][5]
    for i in range(len(mat_element)):
        vetesf[0]=(((7*mat_element[i][9])/20)*(mat_element[i][5]))+(((3*mat_element[i][9])/20)*(mat_element[i][6]))
        vetesf[1]=(((mat_element[i][9]**2)/20)*(mat_element[i][5]))+((((mat_element[i][9])**2)/30)*(mat_element[i][6]))
        vetesf[2]=(((3*mat_element[i][9])/20)*(mat_element[i][5]))+(((7*mat_element[i][9])/20)*(mat_element[i][6]))
        vetesf[3]=((((mat_element[i][9]**2)/30)*(mat_element[i][5]))+((((mat_element[i][9])**2)/20)*(mat_element[i][6])))*-1
        vetforças[(mat_element[i][1]-1)*2]+=vetesf[0]
        vetforças[((mat_element[i][1]-1)*2)+1]+=vetesf[1]
        vetforças[(mat_element[i][2]-1)*2]+=vetesf[2]
        vetforças[((mat_element[i][2]-1)*2)+1]+=vetesf[3]
    return vetforças
    
#busca as condições de contorno e atribui zero a linha e as colunas onde ocorrem as condições
def contorno(matglobal,mat_noz,vet_trat):
    for i in range(len(mat_noz)):
        if mat_noz[i][2]==1:
            vet_trat[i*2]=0.00
            for coluna in range(len(matglobal)):
                for linha in range(len(matglobal[0])):
                    if coluna==2*i:
                        matglobal[coluna][linha]=0
                    if linha==2*i:
                        matglobal[coluna][linha]=0
                    if (2*i)==linha and (2*i)==coluna:
                        matglobal[coluna][linha]=1
        if mat_noz[i][3]==1:
            vet_trat[i*2+1]=0.00
            for coluna in range(len(matglobal)):
                for linha in range(len(matglobal[0])):
                    if coluna==(2*i)+1:
                        matglobal[coluna][linha]=0
                    if linha==(2*i)+1:
                        matglobal[coluna][linha]=0
                    if (2*i)+1==linha and (2*i)+1==coluna:
                        matglobal[coluna][linha]=1
    return matglobal,vet_trat
    
#utiliza-se a função numpy para resolver o sistema de equações com as devidas condições de contorno já aplicadas
def solução(vettrat,matglobtrat):
    A = np.array(matglobtrat)
    b = np.array(vettrat)
    x = np.linalg.solve(A, b)
    return x

#utiliza-se do vetor de deslocamento e a matriz global para o calculo dos valores dos apoios
def retorno(matglobal,vetsol):
    vetapoio=[]
    for i in range(len(vetsol)):
        vetapoio.append(0)
    for i in range(len(matglobal)):
        for j in range(len(matglobal[0])):
            vetapoio[i]+=matglobal[i][j]*vetsol[j]
    return(vetapoio)

#subtrai a parcela da força distribuída do vetor que representa as forças atuantes, assim tendo o vetor de apoio
def distribuida(vetini,vetfin):
    for i in range(len(vetini)):
        vetfin[i]-=vetini[i]
    return vetfin

           
        
#calcula os esforços internos e os plota com a função numpy.plot
def esforçosinternos(vetdes,mat_element,mat_noz):
    vetlocal=[[0,0,0,0],[0,0,0,0]]
    vetres=[]
    vetlinha=[]
    #cria uma matriz 4x4 da matriz de rigidez e aplica os valores das soluções, assim extraindo os valores da força cortante e momento fletor em cada nó do elemento
    for element in range(len(mat_element)):
        vetres.append([])
        ent=[mat_element[element][7],mat_element[element][8],mat_element[element][9],mat_element[element][3],mat_element[element][4]]
        matlocal=processarmatlocal(ent)
        vetlocal[0][0]=vetdes[((mat_element[element][1]-1)*2)]
        vetlocal[0][1]=vetdes[((mat_element[element][1]-1)*2)+1]
        vetlocal[0][2]=vetdes[((mat_element[element][2]-1)*2)]
        vetlocal[0][3]=vetdes[((mat_element[element][2]-1)*2)+1]
        vetlocal[1][0]=(((7*mat_element[element][9])/20)*(mat_element[element][5]))+(((3*mat_element[element][9])/20)*(mat_element[element][6]))
        vetlocal[1][1]=(((mat_element[element][9]**2)/20)*(mat_element[element][5]))+((((mat_element[element][9])**2)/30)*(mat_element[element][6]))
        vetlocal[1][2]=(((3*mat_element[element][9])/20)*(mat_element[element][5]))+(((7*mat_element[element][9])/20)*(mat_element[element][6]))
        vetlocal[1][3]=((((mat_element[element][9]**2)/30)*(mat_element[element][5]))+((((mat_element[element][9])**2)/20)*(mat_element[element][6])))*-1
        vetres[element].append(element)
        for i in range(4):
            a=0
            a+=matlocal[i][0]*vetlocal[0][0]
            a+=matlocal[i][1]*vetlocal[0][1]
            a+=matlocal[i][2]*vetlocal[0][2]
            a+=matlocal[i][3]*vetlocal[0][3]
            a-=vetlocal[1][i]
            vetres[element].append(a)
        vetres[element].append(mat_noz[element][1])
        vetres[element].append(mat_noz[element+1][1]-0.0000001)
    for i in range(len(vetres)):
        vetres[i][4]=vetres[i][4]*-1
        vetres[i][3]=vetres[i][3]*-1
    vetplotx=[]
    vetplotyM=[]
    vetplotyC=[]
    for i in range(len(vetres)):
        vetlinha.append(0)
        vetlinha.append(0)
        vetplotx.append(vetres[i][5])
        vetplotx.append(vetres[i][6])
        vetplotyM.append(vetres[i][2])
        vetplotyM.append(vetres[i][4])
        vetplotyC.append(vetres[i][1])
        vetplotyC.append(vetres[i][3])
    vet_coord=[]
    vetlinha2=[]
    for i in range(len(mat_noz)):
        vet_coord.append(mat_noz[i][1])
        vetlinha2.append(0)
    vet_des=[]
    for i in range(len(vetdes)):
        if i%2==0:
            vet_des.append(vetdes[i])
    vetplotx.insert(1,0.0000001)
    vetplotx.insert(len(vetplotx),mat_noz[len(mat_noz)-1][1])
    vetplotyM.insert(0,0)
    vetplotyM.insert(len(vetplotyM),0)
    vetplotyC.insert(0,0)
    vetplotyC.insert(len(vetplotyC),0)
    vetlinha.insert(0,0)
    vetlinha.insert(0,0)
    return vet_coord,vet_des,vetlinha2,vetplotx,vetplotyM,vetlinha,vetplotyC

def plotagem(vet_coord,vet_des,vetlinha2,vetplotx,vetplotyM,vetlinha,vetplotyC):
    for i in range(len(vet_des)):
        vet_des[i]=vet_des[i]*1000
    plt.plot(vet_coord,vet_des)
    plt.plot(vet_coord,vetlinha2)
    annot_maxD(vet_coord,vet_des)
    annot_minD(vet_coord,vet_des)
    plt.ylabel('Deslocamento')
    plt.xlabel('Comprimento')
    plt.savefig('deslocamento.jpeg', format='jpeg')
    plt.show()
    plt.plot(vetplotx,vetplotyM)
    plt.plot(vetplotx,vetlinha)
    annot_maxM(vetplotx,vetplotyM)
    annot_minM(vetplotx,vetplotyM)
    plt.ylabel('Momento')
    plt.xlabel('Comprimento')
    plt.savefig('momento fletor.jpeg', format='jpeg')
    plt.show()
    annot_maxC(vetplotx,vetplotyC)
    annot_minC(vetplotx,vetplotyC)
    plt.plot(vetplotx,vetplotyC)
    plt.plot(vetplotx,vetlinha)
    plt.ylabel('Cortante')
    plt.xlabel('Comprimento')
    plt.savefig('força cortante.jpeg', format='jpeg')
    plt.show()
    
def annot_maxM(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = max(y)
    text= "x={:.2f} m, Momento max={:.3f} kN.m".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(1.1,1.1), **kw)
    
def annot_minM(x,y, ax=None):
    xmin = x[np.argmin(y)]
    ymin = min(y)
    text= "x={:.2f} m, Momento min={:.3f} kN.m".format(xmin, ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax.annotate(text, xy=(xmin, ymin), xytext=(-0.1,-0.1), **kw)
    
def annot_maxC(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = max(y)
    text= "x={:.2f} m, Cortante max={:.3f} kN".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(1.1,1.1), **kw)
    
def annot_minC(x,y, ax=None):
    xmin = x[np.argmin(y)]
    ymin = min(y)
    text= "x={:.2f} m, Cortante min={:.3f} kN".format(xmin, ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax.annotate(text, xy=(xmin, ymin), xytext=(-0.1,-0.1), **kw)
    
def annot_maxD(x,y, ax=None):
    xmax = x[np.argmax(y)]
    ymax = max(y)
    text= "x={:.2f} m, Deslocamento max positivo={:.8f} mm".format(xmax, ymax)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")
    ax.annotate(text, xy=(xmax, ymax), xytext=(1.1,1.1), **kw)
    
def annot_minD(x,y, ax=None):
    xmin = x[np.argmin(y)]
    ymin = min(y)
    text= "x={:.2f} m, Deslocamento max negativo={:.8f} mm".format(xmin, ymin)
    if not ax:
        ax=plt.gca()
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=60")
    kw = dict(xycoords='data',textcoords="axes fraction",
              arrowprops=arrowprops, bbox=bbox_props, ha="left", va="top")
    ax.annotate(text, xy=(xmin, ymin), xytext=(-0.1,-0.1), **kw)
    

import numpy as np
import matplotlib.pyplot as plt
M1,M2,det=abertura()
if det!=0:
    M1,M2=detalhador(M1,M2,det)
M3=matglobal(M1,M2)
V1=vetorforças(M1,M2)
V2,M4=contorno(M3,M1,V1)
V3=solução(M4,V2)
M3=matglobal(M1,M2)
V4=retorno(M3,V3)
V1=vetorforças(M1,M2)
V4=distribuida(V1,V4)
V5,V6,V7,V8,V9,V10,V11=esforçosinternos(V3,M2,M1)
plotagem(V5,V6,V7,V8,V9,V10,V11)

#    Código elaborado para o trabalho de conclusão de curso de Engenharia Civil
#    Copyright (C) 2021  Thiago Seiji Enokida
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
