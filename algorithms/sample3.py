from lib.algorithm import Algorithm

class Sample3(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):


        """    
        PROCEDIMENTO busca(inicial);
            vars corrente, historico, nao_tentados, item_de_estado, novo;
            corrente = inicial;
            historico = [];
            nao_tentados = [];

            Ate_que e_meta(corrente) faca
                Para_cada item_de_estado em adjacente(corrente) faca
                    a_menos_que pertenca(item_de_estado, historico) fazer
                        novo = [^^historico ^corrente ^item_de_estado];
                        nao_tentados = insere(novo, nao_tentados);
                    FIM-a_menos_que;
                FIM-Para_cada;
                nao_tentados UNIFICADA_COM [ [ ??historico ?corrente ] ??nao_tentados ];
            FIM-Ate_que;
            pr('O caminho completo e: ' ); pr( [^^historico ^corrente] );
        FIM-PROCEDIMENTO;
        """

    def search(first, goal):
        current = first
        history = []
        not_tried = []

        while current != goal:
            for adj in first.vertex_list:
                if not adj in history:
                    new = history + [current, adj]
                    not_tried.append(new)
            

"""
                                    a
                    b                               c
            d               e               f               g
        h       i       j       k       l       m       n       o
----------------------------------------------------------------------
goal = o        |
first = a       |
current = a     |
history = []    | 
not_tried = []  | [[a,b], [a,c]] | [[a], [a,b], [a,c]]

"""






