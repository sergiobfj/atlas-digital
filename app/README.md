# Como substituir os dados mockados

Não é preciso alterar nenhuma página do Streamlit.

Quando o backend estiver pronto, gere estes três arquivos na pasta `reports/metrics/`:

1. `comparacao.csv`
2. `matrizes_confusao.json`
3. `curvas_roc.csv`

A tela **Resultados** detecta esses arquivos automaticamente e deixa de usar os mocks.

Os formatos e exemplos de cada arquivo estão em [`reports/metrics/README.md`](../reports/metrics/README.md).
