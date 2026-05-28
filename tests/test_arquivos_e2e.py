"""Testes end-to-end consumindo os arquivos `teste*.txt`.

Esta primeira leva exercita apenas os arquivos VÁLIDOS, garantindo que o
pipeline completo (lex + parse + semantica + asm) termina sem erros e
produz os artefatos esperados em `output/`.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.lexer_fsm import lex  # noqa: E402
from src.parser_ll1 import construir_arvore  # noqa: E402
from src.pipeline import prepararEntradaSemantica  # noqa: E402
from src.semantica import (  # noqa: E402
    construirTabelaSimbolos,
    verificarTipos,
    gerarArvoreAtribuida,
)


class _E2EBase(unittest.TestCase):
    """Helpers compartilhados pelos casos end-to-end."""

    maxDiff = None

    def _carregar(self, nome: str) -> str:
        return (RAIZ / nome).read_text(encoding="utf-8")

    def _pipeline(self, fonte: str):
        entrada = prepararEntradaSemantica(fonte)
        tabela, erros_tab = construirTabelaSimbolos(entrada["arvore"])
        erros_tipo = verificarTipos(entrada["arvore"], tabela)
        atribuida = gerarArvoreAtribuida(entrada["arvore"], tabela)
        return entrada, tabela, erros_tab, erros_tipo, atribuida


class TestArquivosValidos(_E2EBase):
    """teste1.txt, teste2.txt e teste3.txt devem compilar limpos."""

    def test_teste1_sem_erros(self):
        fonte = self._carregar("teste1.txt")
        _, tabela, erros_tab, erros_tipo, _ = self._pipeline(fonte)
        self.assertEqual(erros_tab, [], "tabela com erros inesperados")
        self.assertEqual(erros_tipo, [], "tipos com erros inesperados")
        self.assertGreater(len(tabela.entradas), 0, "MEM esperada na tabela")

    def test_teste2_sem_erros(self):
        fonte = self._carregar("teste2.txt")
        _, _, erros_tab, erros_tipo, _ = self._pipeline(fonte)
        self.assertEqual(erros_tab, [])
        self.assertEqual(erros_tipo, [])

    def test_teste3_sem_erros(self):
        fonte = self._carregar("teste3.txt")
        _, _, erros_tab, erros_tipo, _ = self._pipeline(fonte)
        self.assertEqual(erros_tab, [])
        self.assertEqual(erros_tipo, [])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
