import pilha as pi
from tkinter import *
from functools import partial
'''
def uniao(a,b):
    for n in range(0,len(b)):
        if(b[n] not in a):
            a.append(b[n])
    return a
'''
def cria_estados(linha):
    estados = []
    estado = ''
    for n in range(linha.find('{')+1,len(linha)):
        if(linha[n]==',' or linha[n]=='}'):
            estados.append(estado)
            estado = ''
        else:
            estado = estado + linha[n]
    if estados == ['']:
        estados = []
    return estados

def cria_Q(lines_list):
    return cria_estados(lines_list[1])

def cria_F(lines_list):
    return cria_estados(lines_list[6])

def cria_alfabeto(linha):
    #tanto os simbolos de pilha quanto os do alfabeto são unitários
    alfabeto = []
    for n in range (9,len(linha)-1,2):
        alfabeto.append(linha[n])
    return alfabeto

def cria_sigma(lines_list):
    return cria_alfabeto(lines_list[2])

def cria_simbp(lines_list):
    return cria_alfabeto(lines_list[3])

def get_estadoinicial(lines_list):
    return lines_list[4][0:lines_list[4].find(':')]

def get_simboloinicial(lines_list):
    simbolo = lines_list[5][0:lines_list[5].find(':')]
    if(len(simbolo)>1):
        return 'erro1'
    return simbolo

def cria_tuplas_delta(linha):
    tuplas = []
    l = linha[linha.find('{')+1:]
    cond = True
    while cond:
        pv = l.find(',')
        fp = l.find(')')
        estado = l[1:pv]
        string = l[pv+1:fp]
        tuplas.append((estado,string))
        if(l[fp+1]=='}'):
            return tuplas
        l = l[fp+2:]

def delta(estado,simbolo,simbolop,lines_list):
    if simbolop=='':
        if(simbolo != ''):
            return []
    resultado = []
    for n in range(7,len(lines_list)):
        pv = lines_list[n].find(',')
        if simbolo != 'epsilon':
            if (estado == lines_list[n][6:pv])and(simbolo == lines_list[n][pv+1])and(simbolop == lines_list[n][pv+3]):
                resultado = cria_tuplas_delta(lines_list[n])
        else:
            if (estado == lines_list[n][6:pv])and(simbolo == lines_list[n][pv+1:pv+8])and(simbolop == lines_list[n][pv+9]):
                resultado = cria_tuplas_delta(lines_list[n])
    return resultado

def descins(estado,string,pilha,lines_list):
    #primeira iteração
    if pilha == 'inicio':
        estado = get_estadoinicial(lines_list)
        simbp = get_simboloinicial(lines_list)
        if simbp == 'erro1':
            return 'erro1'
        pilha = pi.Pilha()
        pilha.empilha(simbp)
    #caso base
    if string == '':
        F = cria_F(lines_list)
        if F == []:
            if pilha.pilha_vazia():
                print('ACEITO POR PILHA VAZIA!!')
                piprint = pi.Pilha()
                piprint.empilha((estado,'',''))
                return (True,piprint)
            else: #ldeltase ...
                l_deltase = delta(estado,'epsilon',pilha.topo(),lines_list)
                for n in range(0,len(l_deltase)):
                    (estado_n,str_pilha) = l_deltase[n]
                    p1 = pi.Pilha()
                    p1.copia(pilha)
                    if len(str_pilha) > 1:
                        teste = p1.desempilha()
                        if str_pilha != 'epsilon':
                            if teste != str_pilha[len(str_pilha)-1]:
                                return 'erro3'
                            for n in range(len(str_pilha)-1,-1,-1):
                                p1.empilha(str_pilha[n])
                    else:
                        if str_pilha != p1.topo():
                            return 'erro3'
                    resultado = descins(estado_n,string,p1,lines_list)
                    if resultado[0:4] == 'erro':
                        return resultado
                    (boolean,piprint) = resultado
                    if boolean:
                        piprint.empilha((estado,string,pilha.topo()))
                        return(boolean,piprint)
                return(False,False)
        if estado in F:
            print('ACEITO POR ESTADO FINAL!!')
            piprint = pi.Pilha()
            piprint.empilha((estado,'',pilha.topo()))
            return(True,piprint)
        else:#verifica se pode-se chegar nesse estado
            l_deltase = delta(estado,'epsilon',pilha.topo(),lines_list)
            for n in range(0,len(l_deltase)):
                (estado_n,str_pilha) = l_deltase[n]
                p1 = pi.Pilha()
                p1.copia(pilha)
                if len(str_pilha) > 1:
                    teste = p1.desempilha()
                    if str_pilha != 'epsilon':
                        if teste != str_pilha[len(str_pilha)-1]:
                            return 'erro3'
                        for n in range(len(str_pilha)-1,-1,-1):
                            p1.empilha(str_pilha[n])
                else:
                    if str_pilha != p1.topo():
                        return 'erro3'
                resultado = descins(estado_n,string,p1,lines_list)
                if resultado[0:4] == 'erro':
                    return resultado
                (boolean,piprint) = resultado
                if boolean:
                    piprint.empilha((estado,string,pilha.topo()))
                    return(boolean,piprint)
            return(False,False)
        return (False,False)
    #deltas
    l_deltas = delta(estado,string[0],pilha.topo(),lines_list)
    l_deltase = delta(estado,'epsilon',pilha.topo(),lines_list)
    if l_deltas==[] and l_deltase==[]:#caso base 2
        return (False,False)
    #chamadas recursivas das:
    #transições "normais"
    string1 = string [1:]
    for n in range(0,len(l_deltas)):
        (estado_n,str_pilha) = l_deltas[n]
        p1 = pi.Pilha()
        p1.copia(pilha)
        if len(str_pilha) > 1:
            teste = p1.desempilha()
            if str_pilha != 'epsilon':
                if teste != str_pilha[len(str_pilha)-1]:
                    return 'erro3'
                for n in range(len(str_pilha)-1,-1,-1):
                    p1.empilha(str_pilha[n])
        else:
            if str_pilha != p1.topo():
                return 'erro3'
        resultado = descins(estado_n,string1,p1,lines_list)
        if resultado[0:4] == 'erro':
            return resultado
        (boolean,piprint) = resultado
        if boolean:
            piprint.empilha((estado,string,pilha.topo()))
            return(boolean,piprint)
    #epsilon transições
    for n in range(0,len(l_deltase)):
        (estado_n,str_pilha) = l_deltase[n]
        p1 = pi.Pilha()
        p1.copia(pilha)
        if len(str_pilha) > 1:
            teste = p1.desempilha()
            if str_pilha != 'epsilon':
                if teste != str_pilha[len(str_pilha)-1]:
                    return 'erro3'
                for n in range(len(str_pilha)-1,-1,-1):
                    p1.empilha(str_pilha[n])
        else:
            if str_pilha != p1.topo():
                return 'erro3'
        resultado = descins(estado_n,string,p1,lines_list)
        if resultado[0:4] == 'erro':
            return resultado
        (boolean,piprint) = resultado
        if boolean:
            piprint.empilha((estado,string,pilha.topo()))
            return(boolean,piprint)
    #em caso de nenhum retornar erro ou chegar em um resultado aceitável
    return (False,False)

def apfunc():
    arq = arquivo.get()
    string = cadeia.get()
    r = open(arq,'r')
    l = r.readlines()
    alfa = cria_sigma(l)
    for n in range(0,len(string)):
        if string[n] not in alfa:
            result['bg'] = 'red'
            result['text'] = 'Existe na cadeia símbolo não pertencente ao alfabeto!! ERRO!!'
            return -1
    resultado = descins('',string,'inicio',l)
    print(resultado)
    if resultado[0:4] == 'erro':
        result['bg'] = 'red'
        if resultado[4]=='1':
            result['text'] = 'Símbolo de pilha inicial é não unitário!! ERRO!!'
        if resultado[4]=='3':
            result['text'] = 'Erro no autômato! Existem erros nas definições dos deltas!'
        return -1
    (boolean, pilha) = resultado
    if not boolean:
        result['bg'] = 'red'
        result['text'] = 'Cadeia não pertence à linguagem!'
        return False
    result['bg'] = 'green'
    result['text'] = 'Cadeia aceita!'
    while not pilha.pilha_vazia():
        print(pilha.desempilha())
    return True
        
'''
menu = Tk()
menu.title('TRABALHO 3 DE LFA')
menu.geometry('1000x800')
conteudo = Frame(menu)
conteudo.pack(side=TOP,fill=BOTH,expand=1)
titulo = Label(conteudo,text='Implementação de autômato de pilha!',bg='white')
titulo.pack(side=TOP,fill=BOTH,expand=1)
div = Frame(conteudo)
div.pack(side=TOP,fill=BOTH,expand=1)
req_arquivo = Label(div,text='Digite o nome do arquivo:',bg='white')
req_arquivo.pack(side=TOP,fill=BOTH,expand=1)
arquivo = Entry(div)
arquivo.pack(side=TOP,fill=BOTH,expand=1)
req_cadeia = Label(div,text='Digite a cadeia:',bg='white')
req_cadeia.pack(side=TOP,fill=BOTH,expand=1)
cadeia = Entry(div)
cadeia.pack(side=TOP,fill=BOTH,expand=1)
submeter = Button(div,width=10,text='Submeter',command=apfunc)
submeter.pack(side=TOP,fill=BOTH,expand=1)
result = Label(div,text='',bg='yellow')
result.pack(side=TOP,fill=BOTH,expand=1)
'''
