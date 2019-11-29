import AP as ap

simp = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def get_delta(linha):
    conj_transicoes = ap.cria_tuplas_delta(linha)
    linha = linha[linha.find('(')+1:]
    pv = linha.find(',')
    estado = linha[0:pv]
    if 'epsilon' in linha[0:linha.find('=')]:
        simbp = linha[pv+9]
        return ((estado,'epsilon',simbp),conj_transicoes)
    simb = linha[pv+1]
    simbp = linha[pv+3]
    return ((estado,simb,simbp),conj_transicoes)

def cria_lista(Q,sigma,simbp,estado_inicial,simbolo_inicial,F,delta):
    arquivo = ['AP\n']
    #cria linha Q
    linha = 'Q = {' + Q[0]
    for n in range(1,len(Q)):
        linha = linha + ',' + Q[n]
    linha = linha + '}\n'
    arquivo.append(linha)
    #cria linha sigma
    linha = 'sigma = {' + sigma[0]
    for n in range(1,len(sigma)):
        linha = linha + ',' + sigma[n]
    linha = linha + '}\n'
    arquivo.append(linha)
    #cria linha simbp
    linha = 'simbp = {' + simbp[0]
    for n in range(1,len(simbp)):
        linha = linha + ',' + simbp[n]
    linha = linha + '}\n'
    arquivo.append(linha)
    #cria linha estado_inicial
    linha = estado_inicial + ': estado_inicial\n'
    arquivo.append(linha)
    #cria linha simbolo_inicial
    linha = simbolo_inicial + ': simbolo_de_pilha_inicial\n'
    arquivo.append(linha)
    #cria linha F
    if len(F)>0:
        linha = 'F = {' + F[0]
        for n in range(1,len(F)):
            linha = linha + ',' + F[n]
        linha = linha + '}\n'
    else:
        linha = 'F = {}\n'
    arquivo.append(linha)
    #cria linhas delta
    for n in range(0,len(delta)):
        ((e1,label,topo),conj_duplas) = delta[n]
        (e2,st) = conj_duplas[0]
        linha = 'delta('+e1+','+label+','+topo+') = {('+e2+','+st+')'
        for n in range(1,len(conj_duplas)):
            (e2,st) = conj_duplas[n]
            linha = linha + ',(' + e2 + ',' + st + ')'
        linha = linha + '}\n'
        if n == len(delta)-1:
            linha = linha[0:len(linha)-1]
        arquivo.append(linha)
    #retorna o arquivo
    return arquivo
        

def pv_ef(nome_arquivo):
    r = open(nome_arquivo,'r')
    lines_list = r.readlines()
    #lê arquivo e pega dados
    Q = ap.cria_Q(lines_list)
    sigma = ap.cria_sigma(lines_list)
    simbp = ap.cria_simbp(lines_list)
    estado_inicial = ap.get_estadoinicial(lines_list)
    simbolo_inicial = ap.get_simboloinicial(lines_list)
    deltas = []
    for n in range(7,len(lines_list)):
        deltas.append(get_delta(lines_list[n]))
    #cria e confere se são válidos os novos estados inicial e final
    estado_i = 'qi'
    estado_f = 'qf'
    while estado_i in Q:
        estado_i = estado_i + 'i'
    while estado_f in Q:
        estado_f = estado_f + 'f'
    #cria e confere se é válido o novo símbolo de pilha inicial
    simbolo_i = 'A'
    i = 1
    while (simbolo_i in simbp) and (i<26):
        simbolo_i = simp[i]
    if simbolo_i in simbp:
        return False
    #cria as novas transições do autômato e as adiciona a deltas
    novo_delta = ((estado_i,'epsilon',simbolo_i),[(estado_inicial,simbolo_inicial+simbolo_i)])
    deltas.append(novo_delta)
    for n in range(0,len(Q)):
        novo_delta = ((Q[n],'epsilon',simbolo_i),[(estado_f,'epsilon')])
        deltas.append(novo_delta)
    #atualiza Q, simbp
    Q.append(estado_i)
    Q.append(estado_f)
    simbp.append(simbolo_i)
    #cria a lista com as linhas pro arquivo
    lista = cria_lista(Q,sigma,simbp,estado_i,simbolo_i,[estado_f],deltas)
    arquivo = open(nome_arquivo+' ef','w')
    for n in range(0,len(lista)):
        arquivo.write(lista[n])
        print(lista[n])
    return nome_arquivo+' ef'
    
def ef_pv(nome_arquivo):
    r = open(nome_arquivo,'r')
    lines_list = r.readlines()
    #lê arquivo e pega dados
    Q = ap.cria_Q(lines_list)
    F = ap.cria_F(lines_list)
    sigma = ap.cria_sigma(lines_list)
    simbp = ap.cria_simbp(lines_list)
    estado_inicial = ap.get_estadoinicial(lines_list)
    simbolo_inicial = ap.get_simboloinicial(lines_list)
    deltas = []
    for n in range(7,len(lines_list)):
        deltas.append(get_delta(lines_list[n]))
    #cria e confere se são válidos os novos estados inicial e de desempilhamento
    estado_i = 'qi'
    estado_d = 'qd'
    while estado_i in Q:
        estado_i = estado_i + 'i'
    while estado_d in Q:
        estado_f = estado_f + 'd'
    #cria e confere se é válido o novo símbolo de pilha inicial
    simbolo_i = 'A'
    i = 1
    while (simbolo_i in simbp) and (i<26):
        simbolo_i = simp[i]
    if simbolo_i in simbp:
        return False
    #atualiza simbp e Q
    simbp.append(simbolo_i)
    Q.append(estado_i)
    Q.append(estado_d)
    #cria as novas transições do autômato e as adiciona a deltas
    novo_delta = ((estado_i,'epsilon',simbolo_i),[(estado_inicial,simbolo_inicial+simbolo_i)])
    deltas.append(novo_delta)
    F.append(estado_d)
    for n in range(0,len(F)):
        for o in range(0,len(simbp)):
            novo_delta = ((F[n],'epsilon',simbp[o]),[(estado_d,'epsilon')])
            deltas.append(novo_delta)
    #cria a lista com as linhas pro arquivo
    lista = cria_lista(Q,sigma,simbp,estado_i,simbolo_i,[],deltas)
    arquivo = open(nome_arquivo+' pv','w')
    for n in range(0,len(lista)):
        print(lista[n])
        arquivo.write(lista[n])
    return nome_arquivo+' pv'
