from sklearn.cluster import KMeans


def preparar_dados_entregas(entregas, locais):
    dados = entregas.merge(
        locais[
            [
                "id",
                "nome",
                "x",
                "y"
            ]
        ],
        left_on="local_id",
        right_on="id",
        how="left"
    )

    if dados[["x", "y"]].isnull().any().any():
        raise ValueError(
            "Existem entregas sem coordenadas cadastradas."
        )

    dados = dados.drop(columns=["id"])

    return dados


def agrupar_entregas_kmeans(
    entregas,
    locais,
    quantidade_clusters=3
):
    dados = preparar_dados_entregas(
        entregas,
        locais
    )

    coordenadas = dados[
        ["x", "y"]
    ]

    modelo = KMeans(
        n_clusters=quantidade_clusters,
        random_state=42,
        n_init=10
    )

    dados["cluster"] = modelo.fit_predict(
        coordenadas
    )

    dados["zona"] = dados["cluster"] + 1

    centroides = modelo.cluster_centers_

    return dados, centroides