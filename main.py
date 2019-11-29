from tkinter import *
from functools import partial
import AP as ap
import conversao_ap as cvs

def apfunc1a():
    arq = arquivo1a.get()
    string = cadeia1a.get()
    r = open(arq,'r')
    l = r.readlines()
    alfa = ap.cria_sigma(l)
    for n in range(0,len(string)):
        if string[n] not in alfa:
            result1a['bg'] = 'red'
            result1a['text'] = 'Existe na cadeia símbolo não pertencente ao alfabeto!! ERRO!!'
            return -1
    resultado = ap.descins('',string,'inicio',l)
    print(resultado)
    if resultado[0:4] == 'erro':
        result1a['bg'] = 'red'
        if resultado[4]=='1':
            result1a['text'] = 'Símbolo de pilha inicial é não unitário!! ERRO!!'
        if resultado[4]=='3':
            result1a['text'] = 'Erro no autômato! Existem erros nas definições dos deltas!'
        return -1
    (boolean, pilha) = resultado
    if not boolean:
        result1a['bg'] = 'red'
        result1a['text'] = 'Cadeia não pertence à linguagem!'
        return False
    result1a['bg'] = 'green'
    result1a['text'] = 'Cadeia aceita!'
    while not pilha.pilha_vazia():
        print(pilha.desempilha())
    return True

def apfunc1b():
    arq = arquivo1b.get()
    string = cadeia1b.get()
    r = open(arq,'r')
    l = r.readlines()
    alfa = ap.cria_sigma(l)
    for n in range(0,len(string)):
        if string[n] not in alfa:
            result1b['bg'] = 'red'
            result1b['text'] = 'Existe na cadeia símbolo não pertencente ao alfabeto!! ERRO!!'
            return -1
    resultado = ap.descins('',string,'inicio',l)
    print(resultado)
    if resultado[0:4] == 'erro':
        result1b['bg'] = 'red'
        if resultado[4]=='1':
            result1b['text'] = 'Símbolo de pilha inicial é não unitário!! ERRO!!'
        if resultado[4]=='3':
            result1b['text'] = 'Erro no autômato! Existem erros nas definições dos deltas!'
        return -1
    (boolean, pilha) = resultado
    if not boolean:
        result1b['bg'] = 'red'
        result1b['text'] = 'Cadeia não pertence à linguagem!'
        return False
    result1b['bg'] = 'green'
    result1b['text'] = 'Cadeia aceita!'
    while not pilha.pilha_vazia():
        print(pilha.desempilha())
    return True

def apfunc2():
    arq = arquivo2.get()
    r = open(arq,'r')
    l = r.readlines()
    if ap.cria_F(l)==[]:
        nome_arq = cvs.pv_ef(arq)
        i = 0
    else:
        nome_arq = cvs.ef_pv(arq)
        i = 1
    if nome_arq == False:
        result2['bg'] = 'red'
        result2['text'] = 'Houve um erro na conversão. Não há símbolos de pilha disponíveis.'
    texto = 'O autômato ' + arq
    if i==0:
        texto = texto + ' de aceitação por pilha vazia foi convertido com sucesso para o automato ' + nome_arq +' com aceitação por estado final'
    if i==1:
        texto = texto + ' de aceitação por estado final foi convertido com sucesso para o automato ' + nome_arq +' com aceitação por pilha vazia'
    result2['bg'] = 'green'
    result2['text'] = texto
    return True

menu = Tk()
menu.title('TRABALHO 4 DE LFA')
menu.geometry('1000x800')

conteudo1 = Frame(menu)
conteudo1.pack(side=TOP,fill=BOTH,expand=1)

conteudo1a = Frame(conteudo1)
conteudo1a.pack(side=LEFT,fill=BOTH,expand=1)
titulo1a = Label(conteudo1a,text='Implementação de autômato de pilha',bg='white')
titulo1a.pack(side=TOP,fill=BOTH,expand=1)
div1a = Frame(conteudo1a)
div1a.pack(side=TOP,fill=BOTH,expand=1)
req_arquivo1a = Label(div1a,text='Digite o nome do arquivo:',bg='white')
req_arquivo1a.pack(side=TOP,fill=BOTH,expand=1)
arquivo1a = Entry(div1a)
arquivo1a.pack(side=TOP,fill=BOTH,expand=1)
req_cadeia1a = Label(div1a,text='Digite a cadeia:',bg='white')
req_cadeia1a.pack(side=TOP,fill=BOTH,expand=1)
cadeia1a = Entry(div1a)
cadeia1a.pack(side=TOP,fill=BOTH,expand=1)
submeter1a = Button(div1a,width=10,text='Submeter',command=apfunc1a)
submeter1a.pack(side=TOP,fill=BOTH,expand=1)
result1a = Label(div1a,text='',bg='yellow')
result1a.pack(side=TOP,fill=BOTH,expand=1)

conteudo1b = Frame(conteudo1)
conteudo1b.pack(side=LEFT,fill=BOTH,expand=1)
titulo1b = Label(conteudo1b,text='Implementação de autômato de pilha',bg='white')
titulo1b.pack(side=TOP,fill=BOTH,expand=1)
div1b = Frame(conteudo1b)
div1b.pack(side=TOP,fill=BOTH,expand=1)
req_arquivo1b = Label(div1b,text='Digite o nome do arquivo:',bg='white')
req_arquivo1b.pack(side=TOP,fill=BOTH,expand=1)
arquivo1b = Entry(div1b)
arquivo1b.pack(side=TOP,fill=BOTH,expand=1)
req_cadeia1b = Label(div1b,text='Digite a cadeia:',bg='white')
req_cadeia1b.pack(side=TOP,fill=BOTH,expand=1)
cadeia1b = Entry(div1b)
cadeia1b.pack(side=TOP,fill=BOTH,expand=1)
submeter1b = Button(div1b,width=10,text='Submeter',command=apfunc1b)
submeter1b.pack(side=TOP,fill=BOTH,expand=1)
result1b = Label(div1b,text='',bg='yellow')
result1b.pack(side=TOP,fill=BOTH,expand=1)

conteudo2 = Frame(menu)
conteudo2.pack(side=TOP,fill=BOTH,expand=1)
titulo2 = Label(conteudo2,text='Conversão de autômato de pilha',bg='white')
titulo2.pack(side=TOP,fill=BOTH,expand=1)
div2 = Frame(conteudo2)
div2.pack(side=TOP,fill=BOTH,expand=1)
req_arquivo2 = Label(div2,text='Digite o nome do arquivo:',bg='white')
req_arquivo2.pack(side=TOP,fill=BOTH,expand=1)
arquivo2 = Entry(div2)
arquivo2.pack(side=TOP,fill=BOTH,expand=1)
submeter2 = Button(div2,width=10,text='Submeter',command=apfunc2)
submeter2.pack(side=TOP,fill=BOTH,expand=1)
result2 = Label(div2,text='',bg='yellow')
result2.pack(side=TOP,fill=BOTH,expand=1)
