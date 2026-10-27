# Organização da interface

## Onde cada pessoa mexe

| Se você precisa... | Arquivo certo |
| --- | --- |
| Alterar a tela inicial | `Home.py` |
| Alterar textos, etapas ou gráficos da análise | `content.py` |
| Alterar a estrutura visual de uma página | `pages/` |
| Alterar cores, espaçamentos e componentes visuais comuns | `ui.py` |
| Integrar os resultados reais do backend | `results_repository.py` e `../reports/metrics/README.md` |

## Regra simples

As páginas em `pages/` devem apenas montar a tela. Não coloque nelas textos longos, valores mockados ou leitura direta de CSV/JSON. Isso fica, respectivamente, em `content.py` e `results_repository.py`.

## Para desmockar os resultados

Consulte [`reports/metrics/README.md`](../reports/metrics/README.md). O backend grava três arquivos em `reports/metrics/` e a tela Resultados passa a usá-los automaticamente. Não é preciso modificar nenhuma página.
