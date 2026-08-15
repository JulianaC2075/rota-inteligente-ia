import pandas as pd

from grafo import carregar_locais, carregar_rotas, construir_grafo
from bfs import busca_largura


def obter_nome_local(locais, local_id):
    return locais.loc[
        locais["id"] == local_id,
        "nome"
    ].iloc[0]


def main():
    locais = carregar_locais()
    rotas = carregar_rotas()
    entregas = pd.read_csv("data/entregas.csv")

    grafo = construir_grafo(rotas)

    print("=== ROTA INTELIGENTE ===")
    print()

    print(f"Locais cadastrados: {len(locais)}")
    print(f"Rotas cadastradas: {len(rotas)}")
    print(f"Entregas cadastradas: {len(entregas)}")

    print()
    print("=== TESTE BFS ===")

    inicio = 0
    objetivo = 11

    caminho, visitados = busca_largura(
        grafo,
        inicio,
        objetivo
    )

    print(
        f"Origem: {obter_nome_local(locais, inicio)}"
    )

    print(
        f"Destino: {obter_nome_local(locais, objetivo)}"
    )

    print()

    if caminho:
        nomes_caminho = [
            obter_nome_local(locais, local_id)
            for local_id in caminho
        ]

        print(
            "Caminho encontrado: "
            + " -> ".join(nomes_caminho)
        )

        print(
            f"Quantidade de conexões: {len(caminho) - 1}"
        )

        print(
            f"Vértices analisados: {len(visitados)}"
        )
    else:
        print("Nenhum caminho encontrado.")


if __name__ == "__main__":
    main()