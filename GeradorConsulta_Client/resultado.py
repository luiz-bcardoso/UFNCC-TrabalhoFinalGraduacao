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
        return f"Resultado(pergunta={self.pergunta}, tempo={self.tempo}, precisao={self.precisao}, consistencia={self.consistencia}, falhas={self.falhas}, qtd_execucoes={self.qtd_execucoes})"