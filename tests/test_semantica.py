# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA3 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara


import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.lexer_fsm import tokenizar_programa
from src.parser_ll1 import construirGramatica, parsear, gerarArvore
from src.semantica import (
    TIPO_BOOL,
    TIPO_INDEF,
    TIPO_INT,
    TIPO_REAL,
    TabelaSimbolos,
    construirTabelaSimbolos,
    formatarTabelaMarkdown,
    gerarArvoreAtribuida,
    inferir_tipo,
    salvarArvoreAtribuida,
    serializarArvoreAtribuidaJSON,
    serializarArvoreAtribuidaMarkdown,
    verificarTipos,
)


def _ast(fonte: str) -> dict:
    """Helper: tokeniza + parseia + devolve a AST de um programa fonte."""
    linhas = fonte.splitlines()
    tokens = tokenizar_programa(linhas)
    gram = construirGramatica()
    resultado = parsear(tokens, gram)
    return gerarArvore(resultado)


# --------------------------------------------------------------
# Casos felizes
# --------------------------------------------------------------


class TestTabelaSimbolosFelizes(unittest.TestCase):
    def test_declaracao_simples_seguida_de_uso(self):
        ast = _ast(
            "(START)\n"
            "(10 X)\n"
            "((X) 2 +)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(erros, [])
        self.assertIn("X", tabela)
        sim = tabela.obter("X")
        self.assertEqual(sim["tipo"], TIPO_INT)
        self.assertEqual(sim["linha_def"], 2)
        self.assertEqual(sim["linhas_uso"], [3])
        self.assertEqual(sim["escopo"], "global")

    def test_varias_variaveis_com_tipos_distintos(self):
        ast = _ast(
            "(START)\n"
            "(1 A)\n"
            "(2.5 B)\n"
            "((1 2 <) C)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(erros, [])
        self.assertEqual(tabela.obter("A")["tipo"], TIPO_INT)
        self.assertEqual(tabela.obter("B")["tipo"], TIPO_REAL)
        self.assertEqual(tabela.obter("C")["tipo"], TIPO_BOOL)
        # itens() devolve em ordem alfabética
        nomes = [s["nome"] for s in tabela.itens()]
        self.assertEqual(nomes, ["A", "B", "C"])

    def test_uso_dentro_de_estrutura_de_controle(self):
        ast = _ast(
            "(START)\n"
            "(0 I)\n"
            "(((I) 3 <) ((I) 1 +) WHILE)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(erros, [])
        sim = tabela.obter("I")
        self.assertEqual(sim["tipo"], TIPO_INT)
        # usado dentro de cond E body do WHILE (mesma linha → registrado uma vez)
        self.assertEqual(sim["linhas_uso"], [3])


# --------------------------------------------------------------
# Casos de erro
# --------------------------------------------------------------


class TestTabelaSimbolosErros(unittest.TestCase):
    def test_uso_sem_declaracao(self):
        ast = _ast(
            "(START)\n"
            "((X) 1 +)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(len(erros), 1)
        self.assertIn("'X'", erros[0].mensagem)
        self.assertIn("antes da declaração", erros[0].mensagem)
        self.assertEqual(erros[0].linha, 2)

    def test_redeclaracao_com_tipo_incompativel(self):
        ast = _ast(
            "(START)\n"
            "(10 X)\n"
            "(2.5 X)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(len(erros), 1)
        self.assertIn("'X'", erros[0].mensagem)
        self.assertIn("incompatível", erros[0].mensagem)
        self.assertEqual(erros[0].linha, 3)

    def test_redeclaracao_com_mesmo_tipo_eh_permitida(self):
        ast = _ast(
            "(START)\n"
            "(10 X)\n"
            "(20 X)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(erros, [])
        # mantém a primeira linha de declaração
        self.assertEqual(tabela.obter("X")["linha_def"], 2)

    def test_res_referencia_invalida(self):
        ast = _ast(
            "(START)\n"
            "(5 RES)\n"
            "(END)\n"
        )
        tabela, erros = construirTabelaSimbolos(ast)
        self.assertEqual(len(erros), 1)
        self.assertIn("5 linhas atrás", erros[0].mensagem)
        self.assertEqual(erros[0].linha, 2)

    def test_res_referencia_valida(self):
        ast = _ast(
            "(START)\n"
            "(1 2 +)\n"
            "(1 RES)\n"
            "(END)\n"
        )
        _, erros = construirTabelaSimbolos(ast)
        self.assertEqual(erros, [])


# --------------------------------------------------------------
# Inferência local + renderização
# --------------------------------------------------------------


class TestInferenciaERender(unittest.TestCase):
    def test_inferir_tipo_literais_e_relacional(self):
        tab = TabelaSimbolos()
        self.assertEqual(inferir_tipo({"tipo": "number", "valor": "42"}, tab), TIPO_INT)
        self.assertEqual(inferir_tipo({"tipo": "number", "valor": "3.14"}, tab), TIPO_REAL)
        rel = {
            "tipo": "binary",
            "op": ">=",
            "esq": {"tipo": "number", "valor": "1"},
            "dir": {"tipo": "number", "valor": "2"},
        }
        self.assertEqual(inferir_tipo(rel, tab), TIPO_BOOL)

    def test_formatar_tabela_markdown(self):
        ast = _ast(
            "(START)\n"
            "(10 X)\n"
            "((X) 2 +)\n"
            "(END)\n"
        )
        tabela, _ = construirTabelaSimbolos(ast)
        md = formatarTabelaMarkdown(tabela)
        self.assertIn("Tabela de Símbolos", md)
        self.assertIn("`X`", md)
        self.assertIn("int", md)
        self.assertIn("global", md)

    def test_formatar_tabela_vazia(self):
        ast = _ast("(START)\n(1 2 +)\n(END)\n")
        tabela, _ = construirTabelaSimbolos(ast)
        md = formatarTabelaMarkdown(tabela)
        self.assertIn("Nenhuma variável", md)


# --------------------------------------------------------------
# Verificação de Tipos (Sprint 3 / §4 do guia)
# --------------------------------------------------------------


def _check(fonte: str):
    """Helper: AST → tabela → verificarTipos; devolve (arvore, tabela, erros)."""
    arvore = _ast(fonte)
    tabela, _ = construirTabelaSimbolos(arvore)
    arvore, erros = verificarTipos(arvore, tabela)
    return arvore, tabela, erros


