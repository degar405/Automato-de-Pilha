class Pilha:
    def __init__(self):
        self.itens = []

    def pilha_vazia(self):
        return self.itens == []

    def empilha(self, item):
        self.itens.append(item)

    def desempilha(self):
        return self.itens.pop()

    def topo(self):
        if self.pilha_vazia():
            return ''
        return self.itens[len(self.itens)-1]

    def tamanho(self):
        return len(self.itens)

    def copia(self,p_copiada):
        aux = Pilha()
        while not p_copiada.pilha_vazia():
            aux.empilha(p_copiada.desempilha())
        while not aux.pilha_vazia():
            a = aux.desempilha()
            self.empilha(a)
            p_copiada.empilha(a)
