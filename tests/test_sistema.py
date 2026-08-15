import sys
import unittest
from pathlib import Path

import pandas as pd


RAIZ_PROJETO = Path(__file__).resolve().parents[1]
PASTA_SRC = RAIZ_PROJETO / "src"

if str(PASTA_SRC) not in sys.path:
    sys.path.insert(0, str(PASTA_SRC))


from astar import busca_a_estrela, criar_coordenadas
from bfs import busca_largura
from clustering import agrupar_entregas_kmeans
from dfs import busca_profundidade
from grafo import (
    aplicar_restricao_rota,
    carregar_locais,
    carregar_rotas,
    construir_grafo,
)
from planejamento import (
    planejar_rota_zona,
    planejar_rota_zona_otima,
)


class TestRotaInteligente(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.locais = carregar_locais()
        cls.rotas = carregar_rotas()

        cls.entregas = pd.read_csv(
            "data/entregas.csv"
        )

        cls.grafo = construir_grafo(
            cls.rotas
        )

        cls.coordenadas = criar_coordenadas(
            cls.locais
        )

    def test_01_quantidade_dados(self):
        self.assertEqual(
            len(self.locais),
            13
        )

        self.assertEqual(
            len(self.rotas),
            24
        )

        self.assertEqual(
            len(self.entregas),
            12
        )

    def test_02_bfs_encontra_caminho(self):
        caminho, visitados = busca_largura(
            self.grafo,
            0,
            11
        )

        self.assertIsNotNone(caminho)

        self.assertEqual(
            caminho[0],
            0
        )

        self.assertEqual(
            caminho[-1],
            11
        )

        self.assertEqual(
            len(caminho) - 1,
            2
        )

        self.assertGreater(
            len(visitados),
            0
        )

    def test_03_dfs_encontra_caminho(self):
        caminho, visitados = busca_profundidade(
            self.grafo,
            0,
            11
        )

        self.assertIsNotNone(caminho)

        self.assertEqual(
            caminho[0],
            0
        )

        self.assertEqual(
            caminho[-1],
            11
        )

        self.assertGreater(
            len(visitados),
            0
        )

    def test_04_astar_encontra_rota_otimizada(self):
        caminho, visitados, custo = busca_a_estrela(
            self.grafo,
            self.coordenadas,
            0,
            11
        )

        self.assertIsNotNone(caminho)

        self.assertEqual(
            caminho[0],
            0
        )

        self.assertEqual(
            caminho[-1],
            11
        )

        self.assertAlmostEqual(
            custo,
            5.6,
            places=1
        )

        self.assertEqual(
            len(caminho) - 1,
            2
        )

        self.assertLess(
            len(visitados),
            12
        )

    def test_05_restricao_urbana(self):
        grafo_restrito = aplicar_restricao_rota(
            self.grafo,
            0,
            9
        )

        caminho, _, custo = busca_a_estrela(
            grafo_restrito,
            self.coordenadas,
            0,
            11
        )

        self.assertIsNotNone(caminho)

        self.assertNotEqual(
            caminho,
            [0, 9, 11]
        )

        self.assertEqual(
            caminho,
            [0, 10, 11]
        )

        self.assertAlmostEqual(
            custo,
            5.6,
            places=1
        )

    def test_06_kmeans_cria_tres_zonas(self):
        dados, centroides = agrupar_entregas_kmeans(
            self.entregas,
            self.locais,
            quantidade_clusters=3
        )

        self.assertEqual(
            len(dados),
            12
        )

        self.assertEqual(
            dados["zona"].nunique(),
            3
        )

        self.assertEqual(
            len(centroides),
            3
        )

        self.assertFalse(
            dados["zona"].isnull().any()
        )

    def test_07_planejamento_atende_todas_entregas(self):
        dados, _ = agrupar_entregas_kmeans(
            self.entregas,
            self.locais,
            quantidade_clusters=3
        )

        entregas_planejadas = []

        for zona in sorted(
            dados["zona"].unique()
        ):
            dados_zona = dados[
                dados["zona"] == zona
            ]

            locais_zona = [
                int(local_id)
                for local_id
                in dados_zona["local_id"].tolist()
            ]

            planejamento = planejar_rota_zona(
                self.grafo,
                self.coordenadas,
                0,
                locais_zona
            )

            entregas_planejadas.extend(
                planejamento["ordem_entregas"]
            )

        locais_entregas = [
            int(local_id)
            for local_id
            in self.entregas["local_id"].tolist()
        ]

        self.assertEqual(
            len(entregas_planejadas),
            12
        )

        self.assertEqual(
            len(set(entregas_planejadas)),
            12
        )

        self.assertEqual(
            set(entregas_planejadas),
            set(locais_entregas)
        )

    def test_08_distancia_total_planejamento_heuristico(self):
        dados, _ = agrupar_entregas_kmeans(
            self.entregas,
            self.locais,
            quantidade_clusters=3
        )

        distancia_total = 0.0

        for zona in sorted(
            dados["zona"].unique()
        ):
            dados_zona = dados[
                dados["zona"] == zona
            ]

            locais_zona = [
                int(local_id)
                for local_id
                in dados_zona["local_id"].tolist()
            ]

            planejamento = planejar_rota_zona(
                self.grafo,
                self.coordenadas,
                0,
                locais_zona
            )

            distancia_total += planejamento[
                "distancia_total"
            ]

        self.assertAlmostEqual(
            distancia_total,
            33.7,
            places=1
        )

    def test_09_planejamento_otimizado(self):
        dados, _ = agrupar_entregas_kmeans(
            self.entregas,
            self.locais,
            quantidade_clusters=3
        )

        distancia_heuristica = 0.0
        distancia_otimizada = 0.0

        entregas_otimizadas = []

        for zona in sorted(
            dados["zona"].unique()
        ):
            dados_zona = dados[
                dados["zona"] == zona
            ]

            locais_zona = [
                int(local_id)
                for local_id
                in dados_zona["local_id"].tolist()
            ]

            planejamento_heuristico = planejar_rota_zona(
                self.grafo,
                self.coordenadas,
                0,
                locais_zona
            )

            planejamento_otimo = planejar_rota_zona_otima(
                self.grafo,
                self.coordenadas,
                0,
                locais_zona
            )

            distancia_heuristica += planejamento_heuristico[
                "distancia_total"
            ]

            distancia_otimizada += planejamento_otimo[
                "distancia_total"
            ]

            entregas_otimizadas.extend(
                planejamento_otimo["ordem_entregas"]
            )

        self.assertAlmostEqual(
            distancia_heuristica,
            33.7,
            places=1
        )

        self.assertAlmostEqual(
            distancia_otimizada,
            31.2,
            places=1
        )

        self.assertLess(
            distancia_otimizada,
            distancia_heuristica
        )

        economia = (
            distancia_heuristica
            - distancia_otimizada
        )

        self.assertAlmostEqual(
            economia,
            2.5,
            places=1
        )

        percentual_economia = (
            economia
            / distancia_heuristica
        ) * 100

        self.assertAlmostEqual(
            percentual_economia,
            7.4,
            places=1
        )

        locais_entregas = [
            int(local_id)
            for local_id
            in self.entregas["local_id"].tolist()
        ]

        self.assertEqual(
            len(entregas_otimizadas),
            12
        )

        self.assertEqual(
            len(set(entregas_otimizadas)),
            12
        )

        self.assertEqual(
            set(entregas_otimizadas),
            set(locais_entregas)
        )


if __name__ == "__main__":
    unittest.main()