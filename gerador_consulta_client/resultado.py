class Resultado:
    # resultado possui uma pergunta, seu tempo (segundos), precisao (double), consistencia (double), falhas (int) e qtd. de execucoes (int)
    def __init__(self, pergunta, tempo, precisao, consistencia, falhas, qtd_execucoes):
        self.pergunta = pergunta
        self.tempo = tempo
        self.precisao = precisao
        self.consistencia = consistencia
        self.falhas = falhas
        self.qtd_execucoes = qtd_execucoes
        
    def __str__(self):
        return (
            "-" * 50 + "\n"
            f"Pergunta: {self.pergunta}\n"
            f"Tempo: {self.tempo}\n"
            f"Precisão: {self.precisao}\n"
            f"Consistência: {self.consistencia*100:.2f}%\n"
            f"Falhas: {self.falhas}\n"
            f"Quantidade de execuções: {self.qtd_execucoes}\n"
            + "-" * 50
        )