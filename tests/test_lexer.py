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

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer_fsm import (
    Erros,
    TIPO_IDENT,
    TIPO_KEYWORD,
    TIPO_OPERADOR,
    tokenizar_linha,
)


class TestLexerFase2(unittest.TestCase):

    # ---------- operadores aritméticos (Fase 2) ----------
    def test_div_real_pipe(self):
        tokens = tokenizar_linha("(8.0 2.0 |)")
        valores = [t.valor for t in tokens]
        self.assertEqual(valores, ["(", "8.0", "2.0", "|", ")"])
        self.assertEqual(tokens[3].tipo, TIPO_OPERADOR)

    def test_div_inteira_barra_simples(self):
        tokens = tokenizar_linha("(10 3 /)")
        self.assertEqual([t.valor for t in tokens], ["(", "10", "3", "/", ")"])
        self.assertEqual(tokens[3].valor, "/")
        self.assertEqual(tokens[3].tipo, TIPO_OPERADOR)

    def test_potencia(self):
        tokens = tokenizar_linha("(2 8 ^)")
        self.assertEqual(tokens[3].valor, "^")

    # ---------- operadores relacionais ----------
    def test_maior_menor_simples(self):
        toks = [t.valor for t in tokenizar_linha("(3 2 >)")]
        self.assertEqual(toks, ["(", "3", "2", ">", ")"])
        toks = [t.valor for t in tokenizar_linha("(3 2 <)")]
        self.assertEqual(toks, ["(", "3", "2", "<", ")"])

    def test_maior_igual_menor_igual(self):
        self.assertEqual(
            [t.valor for t in tokenizar_linha("(A 2 >=)")],
            ["(", "A", "2", ">=", ")"],
        )
        self.assertEqual(
            [t.valor for t in tokenizar_linha("(A 2 <=)")],
            ["(", "A", "2", "<=", ")"],
        )

    def test_igualdade_e_diferente(self):
        self.assertEqual(
            [t.valor for t in tokenizar_linha("(A 2 ==)")],
            ["(", "A", "2", "==", ")"],
        )
        self.assertEqual(
            [t.valor for t in tokenizar_linha("(A 2 !=)")],
            ["(", "A", "2", "!=", ")"],
        )

    def test_igual_solitario_eh_erro(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(A 2 =)")

    def test_exclamacao_solitaria_eh_erro(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(A 2 !)")

    # ---------- palavras reservadas ----------
    def test_keywords_novas(self):
        for palavra in ("START", "END", "IF", "IFELSE", "WHILE", "RES"):
            toks = tokenizar_linha(f"({palavra})")
            self.assertEqual(toks[1].tipo, TIPO_KEYWORD)
            self.assertEqual(toks[1].valor, palavra)

    def test_identificador_comum(self):
        toks = tokenizar_linha("(MEM)")
        self.assertEqual(toks[1].tipo, TIPO_IDENT)

    # ---------- erros léxicos ----------
    def test_caractere_invalido(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(3 2 &)")

    def test_parentese_extra(self):
        with self.assertRaises(Erros):
            tokenizar_linha("3 2 +)")

    def test_parentese_faltando(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(3 2 +")

    def test_numero_dois_pontos(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(3.14.5 +)")

    def test_identificador_com_minuscula(self):
        with self.assertRaises(Erros):
            tokenizar_linha("(Mem)")


if __name__ == "__main__":
    unittest.main()
