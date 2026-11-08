"""Estilos compartilhados do painel."""
import streamlit as st


def apply_atlas_style() -> None:
    st.markdown("""<style>
    .block-container { max-width: 1200px; padding-top: 4rem; padding-bottom: 3rem; }
    .atlas-kicker { color:#18794E; font-size:.78rem; font-weight:700; letter-spacing:.08em; margin-bottom:.35rem; }
    .atlas-title { color:#123D2B; font-size:clamp(2rem,4vw,3rem); line-height:1.08; margin:0 0 .55rem; }
    .atlas-intro { color:#466052; font-size:1.08rem; max-width:780px; margin-bottom:1.8rem; }
    .reading { border-left:4px solid #78B995; background:#F0F7F1; border-radius:0 10px 10px 0; color:#234A35; padding:.9rem 1rem; margin-top:.7rem; }
    div[data-testid="stMetric"] { background:white; border:1px solid #DCE7DE; padding:.85rem; border-radius:12px; min-height:104px; }
    div[data-testid="stVegaLiteChart"], div[data-testid="stDataFrame"] { border:1px solid #DCE7DE; border-radius:10px; padding:8px; }
    div[data-testid="stTabs"] button { font-weight:600; }
    @media (max-width: 700px) {
      .block-container { padding: 2rem 1rem; }
      .atlas-intro { font-size:1rem; }
    }
    </style>""", unsafe_allow_html=True)


def header(title: str, intro: str, kicker: str = "ATLAS CLIMÁTICO") -> None:
    st.markdown(f'<div class="atlas-kicker">{kicker}</div><h1 class="atlas-title">{title}</h1><p class="atlas-intro">{intro}</p>', unsafe_allow_html=True)


def reading(text: str) -> None:
    st.markdown(f'<div class="reading"><strong>Leitura</strong><br>{text}</div>', unsafe_allow_html=True)


def data_source_notice(source: str, notices: tuple[str, ...] = ()) -> None:
    """Mantém explícita a origem dos números em todas as páginas."""
    if source == "mock":
        st.info(
            "MODO DEMONSTRAÇÃO — os números e gráficos usam dados sintéticos "
            "reproduzíveis; não representam medições oficiais nem resultados do modelo."
        )
    else:
        st.success("CSV oficial carregado. Os gráficos usam a base disponível localmente.")
    for notice in notices:
        st.warning(notice)
