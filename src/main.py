import pandas as pd


def main():
    locais = pd.read_csv("data/locais.csv")
    rotas = pd.read_csv("data/rotas.csv")
    entregas = pd.read_csv("data/entregas.csv")

    print("=== ROTA INTELIGENTE ===")
    print()
    print(f"Locais cadastrados: {len(locais)}")
    print(f"Rotas cadastradas: {len(rotas)}")
    print(f"Entregas cadastradas: {len(entregas)}")


if __name__ == "__main__":
    main()