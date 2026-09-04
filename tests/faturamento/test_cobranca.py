import time
import pytest
from app.faturamento.cobranca import processar_cobranca

@pytest.mark.parametrize(
    "valor_base, plano, dias_atraso, esperado",
    [
        (0, "BRONZE", 0, -1.0),
        (-100, "PRATA", 0, -1.0),
        (100, "OURO", -1, -1.0),

        (100, "DIAMANTE", 0, -2.0),
        (100, "", 0, -2.0),
        (100, None, 0, -2.0),

        (100, "BRONZE", 0, 100.00),
        (100, "PRATA", 0, 85.00),
        (100, "OURO", 0, 75.00),

        (100, " bronze ", 0, 100.00),
        (100, " prata ", 0, 85.00),
        (100, "ouro", 0, 75.00),

        (100, "BRONZE", 1, 108.40),

        (100, "BRONZE", 20, 116.00),

        (100, "BRONZE", 21, 146.80),
    ],
)
def test_processar_cobranca_cenarios(
    valor_base, plano, dias_atraso, esperado
):
    resultado = processar_cobranca(
        valor_base,
        plano,
        dias_atraso,
    )

    assert resultado == esperado

@pytest.mark.parametrize(
    "plano, desconto",
    [
        ("BRONZE", 0.00),
        ("PRATA", 0.15),
        ("OURO", 0.25),
    ],
)
def test_desconto_por_plano(plano, desconto):
    valor_base = 200.00

    resultado = processar_cobranca(
        valor_base,
        plano,
        0,
    )

    esperado = round(valor_base * (1 - desconto), 2)
    assert resultado == esperado


def test_atraso_moderado():
    valor_base = 200.00

    resultado = processar_cobranca(
        valor_base,
        "PRATA",
        10,
    )
    assert resultado == 184.80


def test_atraso_severo():
    valor_base = 200.00

    resultado = processar_cobranca(
        valor_base,
        "OURO",
        30,
    )
    assert resultado == 216.00


def test_arredondamento_duas_casas():
    resultado = processar_cobranca(
        123.45,
        "PRATA",
        7,
    )
    assert resultado == round(resultado, 2)


def test_desempenho_processar_cobranca():
    inicio = time.perf_counter()

    processar_cobranca(
        100.00,
        "OURO",
        10,
    )
    fim = time.perf_counter()

    tempo_decorrido = fim - inicio
    assert tempo_decorrido <= 0.08