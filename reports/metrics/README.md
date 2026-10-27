# Contrato de métricas para a interface

As páginas do Streamlit usam mocks apenas enquanto os arquivos reais abaixo não existem. Para integrar o backend, grave os arquivos em `reports/metrics/` com estes nomes exatos. Não é necessário alterar as páginas em `app/pages/`.

## 1. Comparação dos modelos

Arquivo: `comparacao.csv`

| Coluna | Tipo | Exemplo |
| --- | --- | --- |
| `Modelo` | texto | `XGBoost` |
| `AUROC` | decimal entre 0 e 1 | `0.918` |
| `F1` | decimal entre 0 e 1 | `0.861` |
| `Sensibilidade` | decimal entre 0 e 1 | `0.852` |
| `Especificidade` | decimal entre 0 e 1 | `0.924` |

Exemplo:

```csv
Modelo,AUROC,F1,Sensibilidade,Especificidade
Regressão logística,0.842,0.781,0.770,0.851
Random forest,0.901,0.842,0.818,0.912
XGBoost,0.918,0.861,0.852,0.924
```

O modelo com maior `AUROC` é exibido como melhor modelo. Para mudar esse critério, altere somente a função `best_model` em `app/mock_data.py`.

## 2. Matrizes de confusão

Arquivo: `matrizes_confusao.json`

Cada chave é o nome de um modelo. A matriz tem duas linhas (classe real FALTA, EXCESSO) e duas colunas (classe prevista FALTA, EXCESSO).

```json
{
  "Regressão logística": [[5700, 998], [848, 2840]],
  "Random forest": [[6020, 678], [670, 3018]],
  "XGBoost": [[6105, 593], [632, 3056]]
}
```

## 3. Curvas ROC

Arquivo: `curvas_roc.csv`

| Coluna | Tipo | Descrição |
| --- | --- | --- |
| `modelo` | texto | Nome do modelo, igual ao usado nos outros arquivos. |
| `fpr` | decimal entre 0 e 1 | Taxa de falsos positivos. |
| `tpr` | decimal entre 0 e 1 | Taxa de verdadeiros positivos. |

Exemplo:

```csv
modelo,fpr,tpr
XGBoost,0.0,0.0
XGBoost,0.1,0.63
XGBoost,1.0,1.0
```

## Como confirmar a integração

1. Grave os três arquivos reais.
2. Rode `streamlit run app/Home.py`.
3. Abra **Resultados**. O aviso amarelo de “MODO DEMONSTRAÇÃO” deve ser substituído pela confirmação de dados do backend.

Os arquivos mockados não precisam ser apagados: eles são úteis para desenvolvimento local e só são lidos quando não houver uma saída real.
