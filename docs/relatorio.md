# Relatório — Atlas Climático: Chuvas de Caruaru

## Entrega do frontend

O painel Streamlit contempla Home, metodologia, análise gráfica e preparação/modelo. A versão atual é demonstrativa: os gráficos meteorológicos são gerados por dados sintéticos determinísticos quando a base real não está disponível. Nenhum valor simulado deve ser interpretado como medição oficial.

## Análises previstas

- Dias chuvosos por mês e proporção de dias com/sem chuva.
- Proporção de horas com/sem chuva.
- Temperatura média mensal e distribuição da temperatura.
- Distribuição e boxplot da precipitação.
- Relações entre precipitação e temperatura/umidade nas horas chuvosas.

## Pipeline de modelagem (a executar pelo backend)

1. Perfil da base e variável `CHUVA`.
2. Pré-processamento: seleção de colunas, tratamento de ausências e outliers.
3. Codificação e normalização dos atributos.
4. Balanceamento da classe (preferencialmente aplicado apenas ao conjunto de treino).
5. Entropia, ganho de informação e pontos de corte.
6. Divisão estratificada 80/20 e treinamento de Árvore de Decisão.
7. Avaliação no teste: métricas e matriz de confusão.

## Contrato de dados

Arquivo: `data/processed/caruaru_chuvas.csv`

Colunas: `data_hora`, `precipitacao_mm`, `temperatura_c`, `umidade_pct`, `CHUVA` (SIM/NAO).

O frontend concentra a leitura e a validação em `app/data_repository.py`. Caso o CSV esteja ausente, ilegível ou sem colunas obrigatórias, a interface informa o problema e usa dados sintéticos determinísticos apenas para manter a navegação demonstrável. Linhas inválidas de um CSV válido são ocultadas e comunicadas na tela.

## Contratos de artefatos futuros

| Artefato | Caminho previsto | Responsável |
| --- | --- | --- |
| Base preparada | `data/processed/caruaru_chuvas_preparada.csv` | Pré-processamento |
| Base balanceada | `data/processed/caruaru_chuvas_balanceada.csv` | Balanceamento |
| Seleção de atributos | `data/artifacts/feature_selection.csv` | Seleção/ganho de informação |
| Avaliação do modelo | `data/artifacts/model_metrics.json` | Treinamento e validação |

O painel de Preparação/Modelo apresenta a disponibilidade desses arquivos, mas não exibe métricas sintéticas como se fossem resultados do pipeline.

## Pendências do backend

- Entregar CSV real e confirmar unidades/frequência das observações.
- Exportar artefatos do pré-processamento e balanceamento.
- Calcular ganho de informação e treinar/avaliar o modelo.
- Substituir placeholders por métricas reais e registrar metodologia de validação.
