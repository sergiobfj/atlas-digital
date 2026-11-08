"""Conteúdo editorial do painel de chuvas de Caruaru."""

METHODOLOGY_STEPS = (
    ("1", "Perfil da base", "Identificar a estrutura, a distribuição de CHUVA e as variáveis meteorológicas disponíveis."),
    ("2", "Pré-processamento", "Remover colunas não utilizadas, tratar ausências e imputar outliers pela moda quando aplicável."),
    ("3", "Preparação", "Codificar CHUVA, normalizar atributos numéricos e exportar a base processada."),
    ("4", "Balanceamento", "Aplicar under-sampling entre SIM e NAO para reduzir o desbalanceamento da classe-alvo."),
    ("5", "Seleção", "Calcular entropia e ganho de informação por coluna e por ponto de corte."),
    ("6", "Modelo", "Separar 80% para treino e 20% para teste e ajustar uma Árvore de Decisão."),
)
DATA_CONTRACT = ("data/processed/caruaru_chuvas.csv", "data_hora", "precipitacao_mm", "temperatura_c", "umidade_pct", "CHUVA")
PIPELINE_CONTRACTS = (
    ("Base preparada", "data/processed/caruaru_chuvas_preparada.csv", "Base após limpeza, codificação e transformações documentadas."),
    ("Base balanceada", "data/processed/caruaru_chuvas_balanceada.csv", "Base de treino balanceada; não usar para avaliar o teste."),
    ("Seleção de atributos", "data/artifacts/feature_selection.csv", "Atributo, método, ganho de informação e ponto de corte."),
    ("Avaliação", "data/artifacts/model_metrics.json", "Métricas, matriz de confusão e configuração de validação."),
)
