import pytest

from app.credito.credito import classificar_credito


@pytest.mark.parametrize(
    "renda_mensal, score_credito, restrito, esperado",
    [
        (0, 500, False, "renda invalida"),
        (-100, 500, False, "renda invalida"),

        (-100, -1, False, "renda invalida"),

        (1000, -1, False, "score invalido"),
        (1000, 1001, False, "score invalido"),

        (1000, 500, True, "reprovado"),

        (1000, 0, False, "reprovado"),
        (1000, 200, False, "reprovado"),
        (1000, 399, False, "reprovado"),

        (1000, 400, False, "aprovado padrao"),
        (1000, 500, False, "aprovado padrao"),
        (1000, 699, False, "aprovado padrao"),

        (1000, 700, False, "aprovado premium"),
        (1000, 850, False, "aprovado premium"),
        (1000, 1000, False, "aprovado premium"),
    ],
)
def test_classificar_credito_tabela_decisao(
    renda_mensal, score_credito, restrito, esperado
):
    resultado = classificar_credito(
        renda_mensal, score_credito, restrito
    )

    assert resultado == esperado


@pytest.mark.parametrize(
    "renda_mensal, score_credito, restrito, esperado",
    [
        (0, 700, False, "renda invalida"),
        (0.01, 700, False, "aprovado premium"),

        (1000, -1, False, "score invalido"),
        (1000, 0, False, "reprovado"),

        (1000, 399, False, "reprovado"),
        (1000, 400, False, "aprovado padrao"),

        (1000, 699, False, "aprovado padrao"),
        (1000, 700, False, "aprovado premium"),

        (1000, 1000, False, "aprovado premium"),
        (1000, 1001, False, "score invalido"),
    ],
)
def test_classificar_credito_valores_fronteira(
    renda_mensal, score_credito, restrito, esperado
):
    resultado = classificar_credito(
        renda_mensal, score_credito, restrito
    )

    assert resultado == esperado
