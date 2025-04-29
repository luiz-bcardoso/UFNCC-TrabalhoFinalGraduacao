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
        return f"Resultado(pergunta={self.pergunta}, tempo={self.tempo:.4f}, precisao={self.precisao:.2f}, consistencia={self.consistencia:.2f}, falhas={self.falhas}, qtd_execucoes={self.qtd_execucoes})"