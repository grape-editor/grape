from lib.algorithm import Algorithm

class Sample3(Algorithm):
    def __init__(self, graph):
        Algorithm.__init__(self, graph)

        self.category = "Examples"

    def run(self):



    PROCEDIMENTO busca(inicial);
        vars corrente, historico, não_tentados, item_de_estado, novo;
        corrente = inicial;
        histórico = [ ];
        nao_tentados = [ ];

        Até_que é_meta(corrente) faça
            Para_cada item_de_estado em adjacente(corrente) faça
                a_menos_que pertença(item_de_estado, histórico) fazer
                    novo = [^^historico ^corrente ^item_de_estado];
                    não_tentados = insere(novo, nao_tentados);
                FIM-a_menos_que;
            FIM-Para_cada;
            não_tentados UNIFICADA_COM [ [ ??histórico ?corrente ] ??não_tentados ];
        FIM-Até_que;
        pr('O caminho completo é: ' ); pr( [^^historico ^corrente] );
    FIM-PROCEDIMENTO;


    def search(first, goal):
        current = first
        history = []
        not_tried = []

        while current != goal:
            for adj in first.vertex_list:
                if not adj in history:
                    new = history + [current, adj]
                    not_tried.append(new)
            

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








