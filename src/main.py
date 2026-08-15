import pandas as pd

from grafo import carregar_locais, carregar_rotas, construir_grafo
from bfs import busca_largura
from dfs import busca_profundidade
from astar import busca_a_estrela


def obter_nome_local(locais, local_id):
    return locais.loc[
        locais["id"] == local_id,
        "nome"
    ].iloc[0]


def exibir_resultado(
    algoritmo,
    caminho,
    visitados,
    locais,
    custo=None
):
    print()
    print(f"=== TESTE {algoritmo} ===")

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

        if custo is not None:
            print(
                f"Distância total: {custo:.1f} km"
            )

        print(
            f"Vértices analisados: {len(visitados)}"
        )
    else:
        print("Nenhum caminho encontrado.")


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

    inicio = 0
    objetivo = 11

    print()
    print(
        f"Origem: {obter_nome_local(locais, inicio)}"
    )

    print(
        f"Destino: {obter_nome_local(locais, objetivo)}"
    )

    caminho_bfs, visitados_bfs = busca_largura(
        grafo,
        inicio,
        objetivo
    )

    caminho_dfs, visitados_dfs = busca_profundidade(
        grafo,
        inicio,
        objetivo
    )

    (
        caminho_astar,
        visitados_astar,
        custo_astar
    ) = busca_a_estrela(
        grafo,
        locais,
        inicio,
        objetivo
    )

    exibir_resultado(
        "BFS",
        caminho_bfs,
        visitados_bfs,
        locais
    )

    exibir_resultado(
        "DFS",
        caminho_dfs,
        visitados_dfs,
        locais
    )

    exibir_resultado(
        "A*",
        caminho_astar,
        visitados_astar,
        locais,
        custo_astar
    )


if __name__ == "__main__":
    main()