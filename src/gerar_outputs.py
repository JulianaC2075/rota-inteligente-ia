from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from astar import busca_a_estrela, criar_coordenadas
from bfs import busca_largura
from clustering import agrupar_entregas_kmeans
from dfs import busca_profundidade
from grafo import carregar_locais, carregar_rotas, construir_grafo
from metricas import calcular_distancia_caminho
from planejamento import planejar_rota_zona


PASTA_OUTPUTS = Path("outputs")


def preparar_pasta_outputs():
    PASTA_OUTPUTS.mkdir(
        parents=True,
        exist_ok=True
    )


def criar_networkx_grafo(locais, rotas):
    grafo_nx = nx.Graph()

    for _, local in locais.iterrows():
        grafo_nx.add_node(
            int(local["id"]),
            nome=local["nome"]
        )

    for _, rota in rotas.iterrows():
        grafo_nx.add_edge(
            int(rota["origem"]),
            int(rota["destino"]),
            distancia=float(rota["distancia_km"])
        )

    return grafo_nx


def obter_posicoes(locais):
    return {
        int(local["id"]): (
            float(local["x"]),
            float(local["y"])
        )
        for _, local in locais.iterrows()
    }


def obter_nomes(locais):
    return {
        int(local["id"]): local["nome"]
        for _, local in locais.iterrows()
    }


def gerar_grafo_cidade(
    locais,
    rotas
):
    grafo_nx = criar_networkx_grafo(
        locais,
        rotas
    )

    posicoes = obter_posicoes(locais)
    nomes = obter_nomes(locais)

    plt.figure(
        figsize=(14, 10)
    )

    nx.draw_networkx_nodes(
        grafo_nx,
        posicoes,
        node_size=1300
    )

    nx.draw_networkx_edges(
        grafo_nx,
        posicoes,
        width=1.5
    )

    nx.draw_networkx_labels(
        grafo_nx,
        posicoes,
        labels=nomes,
        font_size=8
    )

    pesos = {
        (origem, destino):
        f"{dados['distancia']:.1f} km"
        for origem, destino, dados
        in grafo_nx.edges(data=True)
    }

    nx.draw_networkx_edge_labels(
        grafo_nx,
        posicoes,
        edge_labels=pesos,
        font_size=7
    )

    plt.title(
        "Grafo da Cidade - Sabor Express"
    )

    plt.axis("off")
    plt.tight_layout()

    caminho = (
        PASTA_OUTPUTS
        / "grafo_cidade.png"
    )

    plt.savefig(
        caminho,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


def gerar_clusters(
    locais,
    entregas
):
    dados, centroides = agrupar_entregas_kmeans(
        entregas,
        locais,
        quantidade_clusters=3
    )

    plt.figure(
        figsize=(12, 8)
    )

    zonas = sorted(
        dados["zona"].unique()
    )

    for zona in zonas:
        dados_zona = dados[
            dados["zona"] == zona
        ]

        plt.scatter(
            dados_zona["x"],
            dados_zona["y"],
            s=130,
            label=f"Zona {zona}"
        )

        for _, entrega in dados_zona.iterrows():
            plt.annotate(
                entrega["nome"],
                (
                    entrega["x"],
                    entrega["y"]
                ),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8
            )

    restaurante = locais[
        locais["tipo"] == "restaurante"
    ].iloc[0]

    plt.scatter(
        restaurante["x"],
        restaurante["y"],
        marker="*",
        s=350,
        label="Sabor Express"
    )

    for indice, centroide in enumerate(
        centroides,
        start=1
    ):
        plt.scatter(
            centroide[0],
            centroide[1],
            marker="X",
            s=220
        )

        plt.annotate(
            f"Centroide Zona {indice}",
            (
                centroide[0],
                centroide[1]
            ),
            xytext=(7, -12),
            textcoords="offset points",
            fontsize=8
        )

    plt.title(
        "Agrupamento das Entregas com K-Means"
    )

    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")

    plt.grid(
        alpha=0.3
    )

    plt.legend()

    plt.tight_layout()

    caminho = (
        PASTA_OUTPUTS
        / "clusters.png"
    )

    plt.savefig(
        caminho,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


def gerar_comparacao_algoritmos(
    grafo,
    locais,
    coordenadas
):
    inicio = 0
    objetivo = 11

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
        _
    ) = busca_a_estrela(
        grafo,
        coordenadas,
        inicio,
        objetivo
    )

    algoritmos = [
        "BFS",
        "DFS",
        "A*"
    ]

    distancias = [
        calcular_distancia_caminho(
            grafo,
            caminho_bfs
        ),
        calcular_distancia_caminho(
            grafo,
            caminho_dfs
        ),
        calcular_distancia_caminho(
            grafo,
            caminho_astar
        )
    ]

    vertices = [
        len(visitados_bfs),
        len(visitados_dfs),
        len(visitados_astar)
    ]

    conexoes = [
        len(caminho_bfs) - 1,
        len(caminho_dfs) - 1,
        len(caminho_astar) - 1
    ]

    figura, eixos = plt.subplots(
        1,
        3,
        figsize=(15, 5)
    )

    eixos[0].bar(
        algoritmos,
        distancias
    )

    eixos[0].set_title(
        "Distância"
    )

    eixos[0].set_ylabel(
        "Quilômetros"
    )

    eixos[1].bar(
        algoritmos,
        vertices
    )

    eixos[1].set_title(
        "Vértices analisados"
    )

    eixos[1].set_ylabel(
        "Quantidade"
    )

    eixos[2].bar(
        algoritmos,
        conexoes
    )

    eixos[2].set_title(
        "Quantidade de conexões"
    )

    eixos[2].set_ylabel(
        "Quantidade"
    )

    figura.suptitle(
        "Comparação entre BFS, DFS e A*"
    )

    figura.tight_layout()

    caminho = (
        PASTA_OUTPUTS
        / "comparacao_algoritmos.png"
    )

    figura.savefig(
        caminho,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(figura)


def gerar_rotas_por_zona(
    locais,
    rotas,
    entregas,
    grafo,
    coordenadas
):
    dados, _ = agrupar_entregas_kmeans(
        entregas,
        locais,
        quantidade_clusters=3
    )

    grafo_nx = criar_networkx_grafo(
        locais,
        rotas
    )

    posicoes = obter_posicoes(
        locais
    )

    nomes = obter_nomes(
        locais
    )

    plt.figure(
        figsize=(14, 10)
    )

    nx.draw_networkx_edges(
        grafo_nx,
        posicoes,
        width=1,
        alpha=0.25
    )

    nx.draw_networkx_nodes(
        grafo_nx,
        posicoes,
        node_size=1000
    )

    nx.draw_networkx_labels(
        grafo_nx,
        posicoes,
        labels=nomes,
        font_size=8
    )

    zonas = sorted(
        dados["zona"].unique()
    )

    cores = [
        "tab:blue",
        "tab:orange",
        "tab:green"
    ]

    for indice, zona in enumerate(zonas):
        dados_zona = dados[
            dados["zona"] == zona
        ]

        locais_zona = [
            int(local_id)
            for local_id
            in dados_zona["local_id"].tolist()
        ]

        planejamento = planejar_rota_zona(
            grafo,
            coordenadas,
            0,
            locais_zona
        )

        arestas_rota = []

        for trecho in planejamento["trechos"]:
            caminho = trecho["caminho"]

            arestas_rota.extend(
                zip(
                    caminho,
                    caminho[1:]
                )
            )

        nx.draw_networkx_edges(
            grafo_nx,
            posicoes,
            edgelist=arestas_rota,
            width=4,
            edge_color=cores[indice],
            label=f"Zona {zona}"
        )

    plt.title(
        "Rotas Planejadas por Zona"
    )

    plt.legend()

    plt.axis("off")
    plt.tight_layout()

    caminho = (
        PASTA_OUTPUTS
        / "rotas_por_zona.png"
    )

    plt.savefig(
        caminho,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


def main():
    preparar_pasta_outputs()

    locais = carregar_locais()
    rotas = carregar_rotas()

    entregas = pd.read_csv(
        "data/entregas.csv"
    )

    grafo = construir_grafo(
        rotas
    )

    coordenadas = criar_coordenadas(
        locais
    )

    print(
        "Gerando grafo da cidade..."
    )

    gerar_grafo_cidade(
        locais,
        rotas
    )

    print(
        "Gerando clusters..."
    )

    gerar_clusters(
        locais,
        entregas
    )

    print(
        "Gerando comparação dos algoritmos..."
    )

    gerar_comparacao_algoritmos(
        grafo,
        locais,
        coordenadas
    )

    print(
        "Gerando planejamento das rotas..."
    )

    gerar_rotas_por_zona(
        locais,
        rotas,
        entregas,
        grafo,
        coordenadas
    )

    print()
    print(
        "Outputs gerados com sucesso."
    )


if __name__ == "__main__":
    main()