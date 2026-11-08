# Atlas Climático — Chuvas de Caruaru

Frontend em Streamlit para análise demonstrativa de precipitação, temperatura e umidade em Caruaru/PE durante 2025.

## Execução

```powershell
.venv\Scripts\streamlit run app\Home.py
```

## Dados e integração

Enquanto não houver base, o painel usa uma amostra sintética determinística e claramente identificada como **MODO DEMONSTRAÇÃO**. Nenhum número dessa amostra representa medição oficial ou métrica de modelo.

Para integrar a base real, adicione `data/processed/caruaru_chuvas.csv` com as colunas `data_hora`, `precipitacao_mm`, `temperatura_c`, `umidade_pct`, `CHUVA`. `CHUVA` deve usar somente as classes `SIM` e `NAO`.

O adaptador centralizado em `app/data_repository.py` converte tipos, remove da visualização linhas inválidas e faz fallback para a demonstração se o arquivo estiver ausente ou não atender ao contrato. As páginas não leem CSV diretamente.

## Escopo

- Indicadores e gráficos de chuva, temperatura e umidade;
- Correlações de precipitação com temperatura e umidade;
- Perfil, pré-processamento, under-sampling e ganho de informação;
- Preparação para Árvore de Decisão com divisão 80/20.

## Entrega do frontend (mock)

- Navegação: Home, Metodologia, Análise Gráfica e Preparação/Modelo.
- Os mocks são determinísticos e aparecem com aviso de demonstração.
- Para integrar: coloque `caruaru_chuvas.csv` em `data/processed/`, com as colunas do contrato.
- Os gráficos usam o CSV real automaticamente quando ele estiver presente; caso contrário, usam amostra simulada.
- Não publicar métricas de modelo como reais antes do treino e avaliação do backend.

## Contratos para o pipeline

Além do CSV de entrada, a interface reserva estes caminhos para substituição incremental pelo backend:

| Artefato | Caminho | Conteúdo mínimo |
| --- | --- | --- |
| Base preparada | `data/processed/caruaru_chuvas_preparada.csv` | Transformações e colunas finais documentadas. |
| Base balanceada | `data/processed/caruaru_chuvas_balanceada.csv` | Amostra de treino após balanceamento. |
| Seleção de atributos | `data/artifacts/feature_selection.csv` | Atributo, método, ganho e ponto de corte calculados. |
| Avaliação | `data/artifacts/model_metrics.json` | Métricas, matriz de confusão e configuração de validação. |

Enquanto os dois últimos artefatos não forem entregues, o painel mostra somente seu status; não cria valores de ganho, acurácia ou matriz de confusão.
