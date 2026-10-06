# Atlas Digital de Desastres: falta x excesso de chuva

Classificação supervisionada que identifica se um desastre registrado no Atlas Digital de Desastres no Brasil está ligado à falta de chuva (estiagem ou seca) ou ao excesso de chuva (inundação, enxurrada ou alagamento), com os resultados apresentados em uma interface interativa feita em Streamlit.

## Sobre o projeto

| Item | Descrição |
| --- | --- |
| Disciplina | WYD6399 Tópicos em Big Data em Python, UNIFAVIP Wyden |
| Professor | Prof. MSc. Flávio Morais |
| Problema | Os desastres registrados no Brasil reúnem eventos de causas opostas, como secas e inundações. Entender quais características de um registro diferenciam esses dois grupos ajuda a interpretar padrões e a apoiar ações de prevenção. |
| Objetivo | Treinar e avaliar modelos de classificação que separem desastres por falta e por excesso de chuva, e apresentar o resultado ao público em um app Streamlit. |
| Base de dados | [Atlas Digital de Desastres no Brasil](https://atlasdigital.mdr.gov.br) (Sedec/MIDR e Ceped/UFSC) |
| Registros x atributos | 76.190 registros x 70 atributos (aba `Atlas Valores Corrigidos`) |
| Variável-alvo | **Proposta, aguardando aprovação do professor.** Tipo de desastre agrupado em duas classes: **FALTA** de chuva (estiagem, seca) e **EXCESSO** de chuva (inundação, enxurrada, alagamento). Os demais tipos ficam fora do recorte. Proporção entre as classes: TODO |
| App publicado | TODO |
| Apresentação final | 30/11/2026 |

## Equipe

| Integrante | GitHub |
| --- | --- |
| Sergio Barbosa de Fontes Júnior | [@sergiobfj](https://github.com/sergiobfj) |
| A Adicionar | A Adicionar |
| A Adicionar | A Adicionar |
| A Adicionar | A Adicionar |
| A Adicionar | A Adicionar |

## Dados

| Item | Detalhe |
| --- | --- |
| Fonte oficial | [Página de downloads do Atlas Digital](https://atlasdigital.mdr.gov.br/paginas/downloads.xhtml) |
| Arquivo | `BD_Atlas_1991_2025_v1.1_2026.08.06_Consolidado.xlsx` (68,2 MB) |
| Versão | v1.1, de 06/08/2026 |
| Aba usada | `Atlas Valores Corrigidos` |
| Manual | `Atlas_Digital_Desastres_Manual_Aplicacao.pdf`, salvo em `docs/referencias/` |

O xlsx tem quatro abas:

| Aba | Conteúdo |
| --- | --- |
| `Atlas Valores Originais` | Registros com os valores monetários do ano de registro |
| `Cálculo Correção` | Fatores de correção pelo IGP-DI. O cabeçalho da aba fala em dezembro de 2024, mas as fórmulas usam o índice de dezembro de 2025 |
| `Atlas Valores Corrigidos` | Registros com os valores monetários corrigidos pelo IGP-DI para reais de dezembro de 2025, conforme o ano do evento. **É a aba usada no projeto.** |
| `Grupos de Desastres` | Tabela de apoio que relaciona código Cobrade, tipologia e grupo de desastre |

Para baixar a base e o manual:

```bash
python scripts/baixar_base.py
```

O script usa só a biblioteca padrão do Python. Se um arquivo já existir, ele não baixa de novo, a menos que receba `--force`. A base e o manual ficam fora do Git.

## Como rodar

### Pré-requisitos

- Python 3 (TODO: definir a versão usada pela equipe)
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/sergiobfj/atlas-digital.git
cd atlas-digital
```

### 2. Criar e ativar o ambiente virtual

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Se o PowerShell bloquear a execução do script, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` e ative de novo.

Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar o nbstripout

```bash
nbstripout --install
```

Rode uma vez em cada clone, com o ambiente ativado. O comando registra um filtro no Git que remove as saídas dos notebooks no `git add`, o que deixa os diffs menores e reduz conflitos.

### 5. Baixar a base

```bash
python scripts/baixar_base.py
```

A base vai para `data/raw/` e o manual para `docs/referencias/`. As duas pastas ficam fora do Git. Nunca faça commit da base.

### 6. Rodar a interface

```bash
streamlit run app/Home.py
```

O app abre no navegador, por padrão em http://localhost:8501.

## Estrutura de pastas prevista

```text
atlas-digital/
    app/                                interface Streamlit
        Home.py                         página inicial do app
    data/                               fora do Git
        raw/                            base original baixada do Atlas
        processed/                      base tratada, gerada pelos notebooks
    docs/                               relatório e material da apresentação
        referencias/                    manual do Atlas (fora do Git)
    notebooks/                          um notebook por tarefa do Trello
        01_analise_exploratoria.ipynb
        02_selecao_variaveis.ipynb
        03_graficos_vs_alvo.ipynb
        04_preprocessamento.ipynb
        05a_modelo1.ipynb
        05b_modelo2.ipynb
        05c_modelo3.ipynb
        06_avaliacao.ipynb
    reports/
        figures/                        gráficos exportados
        metrics/                        métricas dos modelos
    scripts/
        baixar_base.py                  baixa a base e o manual
    src/                                funções reutilizadas pelos notebooks e pelo app
    requirements.txt
    README.md
```

## Metodologia

| Etapa | Notebook | O que é feito |
| --- | --- | --- |
| 1. Análise exploratória | `01_analise_exploratoria.ipynb` | Estrutura da base, tipos de dados, valores ausentes, outliers, duplicados e distribuição das classes e dos atributos no tempo e no território. |
| 2. Seleção de variáveis | `02_selecao_variaveis.ipynb` | Recorte dos tipos de desastre das duas classes, criação da variável-alvo, escolha justificada dos atributos preditores (selecionados e descartados) e remoção de colunas que revelem diretamente o tipo de desastre (vazamento de informação). |
| 3. Gráficos x alvo | `03_graficos_vs_alvo.ipynb` | Gráfico de cada variável selecionada em relação à variável-alvo, com o tipo de gráfico escolhido conforme a natureza de cada variável (item 7 da diretriz). |
| 4. Pré-processamento | `04_preprocessamento.ipynb` | Tratamento de valores ausentes, codificação de variáveis categóricas, escalonamento e divisão estratificada em treino e teste. Se as classes estiverem desbalanceadas, balanceamento com imbalanced-learn aplicado somente aos dados de treino. |
| 5. Modelagem | `05a_modelo1.ipynb`, `05b_modelo2.ipynb`, `05c_modelo3.ipynb` | Um modelo por notebook, cada um com um responsável (TODO: definir os algoritmos). Grid Search (`GridSearchCV`) com validação cruzada estratificada, só nos dados de treino e dentro de pipelines para evitar vazamento entre os folds. |
| 6. Avaliação | `06_avaliacao.ipynb` | Avaliação no conjunto de teste e comparação dos três modelos com AUROC, F1, sensibilidade, especificidade, precisão, acurácia, matriz de confusão e curva ROC. Gráficos salvos em `reports/figures/` e métricas em `reports/metrics/`. |

Classe positiva usada no cálculo de sensibilidade e especificidade: TODO (FALTA ou EXCESSO).

## Cronograma

As tarefas de cada sprint estão no [quadro do Trello](https://trello.com/b/ff4K37em/topicos-de-big-data-em-python).

| Sprint | Prazo | Entrega |
| --- | --- | --- |
| 1 | 11/10/2026 | Base de dados aprovada |
| 2 | 18/10/2026 | Análise exploratória |
| 3 | 25/10/2026 | Seleção de variáveis e gráficos |
| 4 | 01/11/2026 | Pré-processamento |
| 5 | 15/11/2026 | Modelagem |
| 6 | 22/11/2026 | Interface e relatório |
| 7 | 29/11/2026 | Ensaio da apresentação |
| Final | 30/11/2026 | Apresentação |

## Como colaborar

1. **Tarefas no Trello.** Toda tarefa vira um card no [quadro da equipe](https://trello.com/b/ff4K37em/topicos-de-big-data-em-python). Pegue um card, coloque seu nome e mova conforme o andamento.
2. **Uma branch por tarefa**, criada a partir da `main` atualizada. Padrão de nome: `tipo/descricao-curta`, por exemplo `feat/analise-exploratoria`.
3. **Commits no padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/):**

   | Prefixo | Uso | Exemplo |
   | --- | --- | --- |
   | `feat:` | nova funcionalidade, análise ou gráfico | `feat: adiciona matriz de confusão na avaliação` |
   | `fix:` | correção de erro | `fix: corrige leitura de datas da base` |
   | `docs:` | documentação | `docs: atualiza cronograma no README` |
   | `chore:` | configuração, dependências e manutenção | `chore: adiciona seaborn ao requirements` |

4. **Pull Request obrigatório.** Todo código entra na `main` por PR. Nunca faça push direto na `main`.
5. **Notebooks com um dono por vez.** Só uma pessoa edita cada notebook de cada vez, para evitar conflitos no `.ipynb`. Indique o dono no card do Trello. A modelagem já vem dividida em `05a`, `05b` e `05c` para que cada modelo tenha o seu responsável.
6. **Nunca versionar a base.** Nenhum arquivo de `data/` entra em commit. Confira o `git status` antes de cada commit.

Fluxo de uma tarefa:

```bash
git checkout main
git pull
git checkout -b feat/analise-exploratoria
# faça as alterações
git add notebooks/01_analise_exploratoria.ipynb
git commit -m "feat: adiciona análise de valores ausentes"
git push -u origin feat/analise-exploratoria
```

Depois, abra o Pull Request para a `main` no GitHub.
