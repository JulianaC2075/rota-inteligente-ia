import pandas as pd

from grafo import carregar_locais, carregar_rotas, construir_grafo
from bfs import busca_largura
from dfs import busca_profundidade
from astar import busca_a_estrela, criar_coordenadas
from metricas import calcular_distancia_caminho, medir_tempo_medio


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
    grafo,
    tempo_medio
):
    print()
    print(f"=== TESTE {algoritmo} ===")

    if caminho:
        nomes_caminho = [
            obter_nome_local(locais, local_id)
            for local_id in caminho
        ]

        distancia = calcular_distancia_caminho(
            grafo,
            caminho
        )

        print(
            "Caminho encontrado: "
            + " -> ".join(nomes_caminho)
        )

        print(
            f"Quantidade de conexões: {len(caminho) - 1}"
        )

        print(
            f"Distância total: {distancia:.1f} km"
        )

        print(
            f"Vértices analisados: {len(visitados)}"
        )

        print(
            f"Tempo médio: {tempo_medio:.4f} ms"
        )

        return {
            "algoritmo": algoritmo,
            "conexoes": len(caminho) - 1,
            "distancia": distancia,
            "vertices": len(visitados),
            "tempo": tempo_medio
        }

    print("Nenhum caminho encontrado.")

    return None


def main():
    locais = carregar_locais()
    rotas = carregar_rotas()
    entregas = pd.read_csv("data/entregas.csv")

    grafo = construir_grafo(rotas)
    coordenadas = criar_coordenadas(locais)

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

    (
        resultado_bfs,
        tempo_bfs
    ) = medir_tempo_medio(
        busca_largura,
        grafo,
        inicio,
        objetivo,
        repeticoes=1000
    )

    caminho_bfs, visitados_bfs = resultado_bfs

    (
        resultado_dfs,
        tempo_dfs
    ) = medir_tempo_medio(
        busca_profundidade,
        grafo,
        inicio,
        objetivo,
        repeticoes=1000
    )

    caminho_dfs, visitados_dfs = resultado_dfs

    (
        resultado_astar,
        tempo_astar
    ) = medir_tempo_medio(
        busca_a_estrela,
        grafo,
        coordenadas,
        inicio,
        objetivo,
        repeticoes=1000
    )

    (
        caminho_astar,
        visitados_astar,
        _
    ) = resultado_astar

    resultados = []

    resultados.append(
        exibir_resultado(
            "BFS",
            caminho_bfs,
            visitados_bfs,
            locais,
            grafo,
            tempo_bfs
        )
    )

    resultados.append(
        exibir_resultado(
            "DFS",
            caminho_dfs,
            visitados_dfs,
            locais,
            grafo,
            tempo_dfs
        )
    )

    resultados.append(
        exibir_resultado(
            "A*",
            caminho_astar,
            visitados_astar,
            locais,
            grafo,
            tempo_astar
        )
    )

    print()
    print("=== COMPARAÇÃO DOS ALGORITMOS ===")

    print(
        f"{'Algoritmo':<12}"
        f"{'Conexões':<12}"
        f"{'Distância':<15}"
        f"{'Vértices':<12}"
        f"{'Tempo (ms)':<12}"
    )

    print("-" * 63)

    for resultado in resultados:
        if resultado:
            print(
                f"{resultado['algoritmo']:<12}"
                f"{resultado['conexoes']:<12}"
                f"{resultado['distancia']:<15.1f}"
                f"{resultado['vertices']:<12}"
                f"{resultado['tempo']:<12.4f}"
            )


if __name__ == "__main__":
    main()