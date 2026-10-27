"""Conteúdo editorial das páginas do Streamlit.

EDIÇÃO DE CONTEÚDO: altere textos, títulos e a lista de gráficos somente neste
arquivo. As páginas em ``app/pages`` ficam responsáveis apenas por exibir esse
conteúdo, o que deixa a revisão mais simples.
"""


# METODOLOGIA — cada item cria uma aba. Para incluir uma etapa, adicione outro
# dicionário seguindo o mesmo formato. ``detail`` é opcional.
METHODOLOGY_STEPS = (
    {
        "number": "1",
        "title": "Recorte do problema",
        "description": "Selecionamos registros ligados à estiagem/seca (FALTA) e a inundações, enxurradas e alagamentos (EXCESSO).",
    },
    {
        "number": "2",
        "title": "Seleção de variáveis",
        "description": "Mantemos indicadores de impactos humanos, materiais, rurais, mês e região; removemos identificadores e campos que revelariam a resposta.",
        "detail": "**Proteção contra vazamento:** tipologia, códigos de desastre e identificadores não entram como preditores, pois poderiam entregar a classe ao modelo.",
    },
    {
        "number": "3",
        "title": "Preparação",
        "description": "Tratamos ausências, codificamos categorias e separamos treino e teste de forma estratificada para preservar a proporção entre as classes.",
        "detail": "**Por que separar treino e teste?** Para testar o modelo em casos que ele ainda não viu, simulando o uso em novos registros.",
    },
    {
        "number": "4",
        "title": "Modelagem",
        "description": "Comparamos regressão logística, random forest e XGBoost, com validação cruzada e ajuste de hiperparâmetros.",
    },
    {
        "number": "5",
        "title": "Avaliação",
        "description": "Avaliamos AUROC, F1, sensibilidade, especificidade, matrizes de confusão e curvas ROC.",
        "detail": "**Como ler:** valores mais altos indicam melhor capacidade de separar FALTA e EXCESSO, sempre considerando o equilíbrio entre os erros possíveis.",
    },
)


# DESCRIÇÃO DAS CLASSES — texto exibido no final da página Metodologia.
CLASS_DESCRIPTIONS = (
    ("FALTA", "Estiagem e seca, geralmente associadas a prejuízos na agricultura, pecuária e abastecimento de água."),
    ("EXCESSO", "Inundações, enxurradas e alagamentos, associados a danos humanos, moradias e infraestrutura."),
)


# ANÁLISE GRÁFICA — para trocar ou adicionar um gráfico, atualize ``figure``
# com o nome do PNG que está em reports/figures e revise título e leitura.
GRAPH_ANALYSES = (
    {
        "title": "Danos humanos e moradias",
        "figure": "grafico1_danos_humanos_moradias.png",
        "insight": "Ocorrências de EXCESSO apresentam percentuais muito maiores de desalojados, desabrigados e danos a moradias. Isso evidencia impactos súbitos e concentrados.",
    },
    {
        "title": "Prejuízos econômicos",
        "figure": "grafico2_prejuizos_economicos.png",
        "insight": "Em FALTA, agricultura, pecuária e abastecimento de água aparecem com mais frequência, mostrando um impacto prolongado sobre atividades rurais e serviços.",
    },
    {
        "title": "Registros por mês",
        "figure": "grafico3_registros_por_mes.png",
        "insight": "A sazonalidade ajuda a contextualizar os eventos: o excesso de chuva se concentra em períodos chuvosos, enquanto a falta tem uma distribuição própria no ano.",
    },
    {
        "title": "Classe por região",
        "figure": "grafico4_classe_por_regiao.png",
        "insight": "A composição muda entre as regiões brasileiras. Essa diferença regional é um sinal útil, mas não substitui os indicadores de impacto no modelo.",
    },
)
