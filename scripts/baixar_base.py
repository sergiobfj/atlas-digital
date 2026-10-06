"""Baixa a base do Atlas Digital de Desastres no Brasil e o manual de aplicação.

A base vai para data/raw/ e o manual para docs/referencias/. Nenhum dos dois é
versionado no Git, então cada integrante roda este script uma vez depois de
clonar o repositório.

Uso:
    python scripts/baixar_base.py            baixa só o que ainda não existe
    python scripts/baixar_base.py --force    baixa tudo de novo

Usa apenas a biblioteca padrão (urllib), sem dependências extras.
"""

import argparse
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

PAGINA_DOWNLOADS = "https://atlasdigital.mdr.gov.br/paginas/downloads.xhtml"

DOWNLOADS = [
    (
        "https://atlasdigital.mdr.gov.br/arquivos/2026/BD_Atlas_1991_2025_v1.1_2026.08.06_Consolidado.xlsx",
        RAIZ / "data" / "raw",
    ),
    (
        "https://atlasdigital.mdr.gov.br/arquivos/Atlas_Digital_Desastres_Manual_Aplicacao.pdf",
        RAIZ / "docs" / "referencias",
    ),
]

TAMANHO_BLOCO = 256 * 1024
TIMEOUT_SEGUNDOS = 60


def formatar_tamanho(n_bytes):
    tamanho = float(n_bytes)
    for unidade in ("B", "KB", "MB"):
        if tamanho < 1024:
            return f"{tamanho:.1f} {unidade}"
        tamanho /= 1024
    return f"{tamanho:.1f} GB"


def mostrar_progresso(baixado, total):
    if total:
        texto = f"{baixado / total:6.1%} ({formatar_tamanho(baixado)} de {formatar_tamanho(total)})"
    else:
        texto = formatar_tamanho(baixado)
    print(f"\r  {texto}", end="", flush=True)


def baixar(url, pasta, force=False):
    """Baixa url para pasta, mantendo o nome do arquivo. Retorna o caminho final."""
    destino = pasta / url.rsplit("/", 1)[-1]
    nome = destino.relative_to(RAIZ).as_posix()

    if destino.exists() and not force:
        tamanho = formatar_tamanho(destino.stat().st_size)
        print(f"{nome} já existe ({tamanho}), pulando. Use --force para baixar de novo.")
        return destino

    pasta.mkdir(parents=True, exist_ok=True)
    # Baixa para um arquivo .part e só renomeia no fim, assim um download
    # interrompido não fica parecendo um arquivo completo.
    parcial = destino.with_name(destino.name + ".part")
    print(f"Baixando {nome}")
    pedido = urllib.request.Request(url, headers={"User-Agent": "atlas-digital/baixar_base.py"})
    try:
        with urllib.request.urlopen(pedido, timeout=TIMEOUT_SEGUNDOS) as resposta, parcial.open("wb") as saida:
            total = int(resposta.headers.get("Content-Length") or 0)
            baixado = 0
            while bloco := resposta.read(TAMANHO_BLOCO):
                saida.write(bloco)
                baixado += len(bloco)
                mostrar_progresso(baixado, total)
            print()
        if total and baixado != total:
            raise OSError(f"download incompleto ({baixado} de {total} bytes)")
        parcial.replace(destino)
    except BaseException:
        parcial.unlink(missing_ok=True)
        raise

    print(f"  Salvo em {nome} ({formatar_tamanho(destino.stat().st_size)})")
    return destino


def main():
    parser = argparse.ArgumentParser(
        description="Baixa a base do Atlas Digital de Desastres no Brasil e o manual de aplicação."
    )
    parser.add_argument("--force", action="store_true", help="baixa de novo mesmo se o arquivo já existir")
    args = parser.parse_args()

    falhas = 0
    for url, pasta in DOWNLOADS:
        try:
            baixar(url, pasta, force=args.force)
        except OSError as erro:
            print(f"\n  Falha ao baixar {url}: {erro}", file=sys.stderr)
            print(f"  Se o link mudou, confira a página oficial: {PAGINA_DOWNLOADS}", file=sys.stderr)
            falhas += 1
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
