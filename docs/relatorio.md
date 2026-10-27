# Relatório — Atlas Digital de Desastres

## Metodologia

O projeto classifica registros do Atlas Digital de Desastres em duas classes: **FALTA** (estiagem e seca) e **EXCESSO** (inundações, enxurradas e alagamentos). O recorte reúne 51.921 registros: 33.493 de FALTA (64,5%) e 18.428 de EXCESSO (35,5%).

Foram selecionadas variáveis relacionadas a impactos humanos, danos materiais, prejuízos rurais e ao abastecimento, além de mês e região. Campos que identificam diretamente a tipologia do desastre, códigos e identificadores foram excluídos para evitar vazamento de informação.

Os dados passam por tratamento de ausências, codificação de categorias e divisão estratificada entre treino e teste. São comparados regressão logística, random forest e XGBoost, usando validação cruzada e ajuste de hiperparâmetros. A avaliação utiliza AUROC, F1, sensibilidade, especificidade, matrizes de confusão e curvas ROC.

## Análise gráfica

Os gráficos exploratórios mostram que eventos de EXCESSO apresentam mais frequentemente desalojados, desabrigados e danos a moradias e infraestrutura. Já FALTA se associa mais a prejuízos na agricultura, pecuária e no abastecimento de água. Também há diferenças de sazonalidade e de composição entre as regiões brasileiras. Essas leituras orientam a seleção de variáveis, mas não substituem a avaliação do modelo.

## Resultados

> **Status: dados mockados.** Os valores a seguir existem para validar a interface e serão substituídos pelas saídas do backend. Não representam desempenho real.

| Modelo | AUROC | F1 | Sensibilidade | Especificidade |
| --- | ---: | ---: | ---: | ---: |
| Regressão logística | 0,842 | 0,781 | 0,770 | 0,851 |
| Random forest | 0,901 | 0,842 | 0,818 | 0,912 |
| XGBoost | 0,918 | 0,861 | 0,852 | 0,924 |

Nos dados mockados, o XGBoost é o melhor modelo, pois apresenta o maior AUROC (0,918) e F1 (0,861). As matrizes de confusão e as curvas ROC exibidas na interface seguem essa mesma demonstração: a diagonal da matriz mostra acertos, e curvas mais próximas do canto superior esquerdo indicam melhor separação entre FALTA e EXCESSO.

Quando estiverem prontos, o backend deve gravar `reports/metrics/comparacao.csv`, `matrizes_confusao.json` e `curvas_roc.csv`. A interface prioriza esses arquivos e deixa de usar os mocks automaticamente.
