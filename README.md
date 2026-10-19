# Atlas Digital de Desastres: falta x excesso de chuva

Classificacao supervisionada que identifica se um desastre registrado no Atlas Digital de Desastres no Brasil esta ligado a falta ou ao excesso de chuva, com os resultados apresentados em uma interface interativa feita em Streamlit.

## Resumo do projeto

**Qual e o problema?**
Os desastres registrados no Brasil reunem eventos de causas opostas, como secas e inundacoes. Entender quais caracteristicas de um registro diferenciam esses dois grupos ajuda a interpretar padroes e a apoiar acoes de prevencao.

**Qual e a variavel-alvo e como ela foi construida?**
A coluna `descricao_tipologia` foi agrupada em duas classes:

| Classe | Tipologias incluidas |
| --- | --- |
| **FALTA** | Estiagem e Seca |
| **EXCESSO** | Inundacoes, Enxurradas, Alagamentos |

As demais tipologias (Chuvas Intensas, Vendavais, Incendio Florestal, Granizo, Movimento de Massa, entre outras) ficam fora do recorte por nao se encaixarem diretamente na dicotomia falta/excesso de chuva.

**Qual e a proporcao entre as classes?**
51.921 registros para modelagem: **FALTA 33.493 (64,5%)** e **EXCESSO 18.428 (35,5%)**. Os 24.269 registros restantes (outras tipologias) ficam fora do escopo.

**Quais atributos serao usados e por que eles tem relacao com o alvo?**
O perfil de impacto de cada classe e diferente e mensuravel nos dados:

- **Danos humanos e moradias** (desalojados, desabrigados, feridos, obitos, moradias danificadas/destruidas): quase exclusivos de EXCESSO. Exemplo: desalojados aparecem em 44,5% dos registros de EXCESSO e apenas 0,6% dos de FALTA.
- **Prejuizos rurais e abastecimento** (agricultura, pecuaria, abastecimento de agua): predominam em FALTA. Agricultura tem prejuizo em 58,4% de FALTA contra 32,6% de EXCESSO.
- **Mes do evento**: EXCESSO concentra-se no verao (janeiro a marco); FALTA se distribui com pico em abril.
- **Regiao**: Nordeste tem 85% de FALTA; Norte e Centro-Oeste, mais de 60% de EXCESSO.

**O que foi excluido e por que?**

| Motivo | Colunas |
| --- | --- |
| Vazamento (revelam o tipo de desastre) | `descricao_tipologia`, `tipologia`, `Cod_Cobrade`, `grupo_de_desastre`, `DH_AFETADOS_SECA_ESTIAGEM` |
| Identificacao (sem poder preditivo) | `Protocolo_S2iD`, `Cod_IBGE_Mun` |
| Ausencia >= 80% | `DA_Polui/cont do ar`, `DA_Polui/cont do solo`, `DA_Polui/cont da agua`, `DA_Incendi parques/APAs/APPs`, `DA_Dimi/exauri hidrico` |

**Em que etapa o projeto esta?**
Notebooks 01 (analise exploratoria), 02 (selecao de variaveis) e 03 (graficos vs. alvo) concluidos. Proximos passos: pre-processamento, modelagem (tres algoritmos), avaliacao e interface Streamlit.

## Equipe

| Integrante | GitHub |
| --- | --- |
| Sergio Barbosa de Fontes Junior | [@sergiobfj](https://github.com/sergiobfj) |
| Gabriel de Lemos Cardim | [@gabelemos](https://github.com/gabelemos) |

## Dados

| Item | Detalhe |
| --- | --- |
| Fonte oficial | [Atlas Digital de Desastres no Brasil](https://atlasdigital.mdr.gov.br/paginas/downloads.xhtml) |
| Arquivo | `BD_Atlas_1991_2025_v1.1_2026.08.06_Consolidado.xlsx` (68,2 MB) |
| Versao | v1.1, de 06/08/2026 |
| Aba usada | `Atlas Valores Corrigidos` |
| Registros x atributos | 76.190 registros x 70 atributos |

Para baixar a base e o manual:

```bash
python scripts/baixar_base.py
```

## Metodologia

| Etapa | Notebook | O que e feito |
| --- | --- | --- |
| 1. Analise exploratoria | `01_analise_exploratoria.ipynb` | Estrutura, ausentes, outliers, duplicados, distribuicao das classes. |
| 2. Selecao de variaveis | `02_selecao_variaveis.ipynb` | Criacao do alvo, escolha dos preditores, remocao de vazamento. |
| 3. Graficos x alvo | `03_graficos_vs_alvo.ipynb` | Graficos de cada variavel vs. alvo, com leitura dos numeros. |
| 4. Pre-processamento | `04_preprocessamento.ipynb` | Ausentes, encoding, escalonamento, divisao estratificada, balanceamento. |
| 5. Modelagem | `05a`, `05b`, `05c` | Tres modelos com GridSearchCV e validacao cruzada estratificada. |
| 6. Avaliacao | `06_avaliacao.ipynb` | Comparacao com AUROC, F1, sensibilidade, especificidade, matriz de confusao, curva ROC. |

## Cronograma

| Sprint | Prazo | Entrega |
| --- | --- | --- |
| 1 | 11/10/2026 | Base de dados aprovada |
| 2 | 18/10/2026 | Analise exploratoria |
| 3 | 25/10/2026 | Selecao de variaveis e graficos |
| 4 | 01/11/2026 | Pre-processamento |
| 5 | 15/11/2026 | Modelagem |
| 6 | 22/11/2026 | Interface e relatorio |
| 7 | 29/11/2026 | Ensaio da apresentacao |
| Final | 30/11/2026 | Apresentacao |

---

## Para a equipe

### Como rodar

1. Clonar o repositorio e criar o ambiente virtual:

```bash
git clone https://github.com/sergiobfj/atlas-digital.git
cd atlas-digital
python -m venv .venv
```

2. Ativar o ambiente:

Windows (PowerShell): `.venv\Scripts\Activate.ps1`
Linux/Mac: `source .venv/bin/activate`

3. Instalar dependencias e configurar o nbstripout:

```bash
pip install -r requirements.txt
nbstripout --install
```

4. Baixar a base:

```bash
python scripts/baixar_base.py
```

### Como colaborar

- Tarefas no [quadro do Trello](https://trello.com/b/ff4K37em/topicos-de-big-data-em-python). Pegue um card, coloque seu nome e mova conforme o andamento.
- Uma branch por tarefa (`tipo/descricao-curta`), criada a partir da `main` atualizada.
- Commits no padrao [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/): `feat:`, `fix:`, `docs:`, `chore:`.
- Pull Request obrigatorio. Nunca faca push direto na `main`.
- Notebooks com um dono por vez para evitar conflitos.
- Nunca versionar a base (`data/` esta no `.gitignore`).

### Estrutura de pastas

```text
atlas-digital/
    app/                    interface Streamlit
    data/                   fora do Git
        raw/                base original
        processed/          base tratada
    docs/referencias/       manual do Atlas (fora do Git)
    notebooks/              um notebook por etapa
    reports/
        figures/            graficos exportados
        metrics/            metricas dos modelos
    scripts/
        baixar_base.py      baixa a base e o manual
    requirements.txt
    README.md
```
