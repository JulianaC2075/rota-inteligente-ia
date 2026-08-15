import pandas as pd

from grafo import carregar_locais, carregar_rotas, construir_grafo


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
    print("=== GRAFO DA CIDADE ===")
    print(f"Vértices: {len(grafo)}")
    print(f"Arestas: {len(rotas)}")

    print()
    print("Vizinhos da Sabor Express:")

    for vizinho in grafo[0]:
        destino_id = vizinho["destino"]

        nome_destino = locais.loc[
            locais["id"] == destino_id,
            "nome"
        ].iloc[0]

        print(
            f"- {nome_destino}: "
            f"{vizinho['distancia_km']} km, "
            f"{vizinho['tempo_min']} min"
        )


if __name__ == "__main__":
    main()