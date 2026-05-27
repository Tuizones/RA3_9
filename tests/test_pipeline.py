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
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lexer_fsm import Erros, tokenizar_linha, tokenizar_programa
from src.parser_ll1 import (
    construirGramatica,
    parsear,
    gerarArvore,
)
from src.pipeline import (
    lerArquivo,
    lerTokens,
    salvarTokens,
    executar_fase2,
    gerarAssembly,
)


def _programa(linhas):
    tokens = tokenizar_programa(["(START)"] + list(linhas) + ["(END)"])
    return tokens


class TestGramaticaLL1(unittest.TestCase):
    def test_construirGramatica_sem_conflitos(self):
        g = construirGramatica()
        self.assertIn("PROGRAM", g["nao_terminais"])
        self.assertGreater(len(g["tabela"]), 0)
        # PROGRAM é o símbolo inicial
        self.assertEqual(g["inicial"], "PROGRAM")

    def test_first_follow_contem_basicos(self):
        g = construirGramatica()
        self.assertIn("(", g["first"]["PROGRAM"])
        self.assertIn("(", g["first"]["ITEM"])
        self.assertIn(")", g["follow"]["ITEM"])

    def test_tabela_resolve_item(self):
        g = construirGramatica()
        self.assertIn(("ITEM", "numero"), g["tabela"])
        self.assertIn(("ITEM", "("), g["tabela"])


class TestParser(unittest.TestCase):
    def setUp(self):
        self.g = construirGramatica()

    def test_programa_minimo(self):
        toks = _programa([])
        res = parsear(toks, self.g)
        arv = gerarArvore(res)
        self.assertEqual(arv["tipo"], "program")
        self.assertEqual(arv["stmts"], [])

    def test_binaria_simples(self):
        toks = _programa(["(3.0 2.0 +)"])
        res = parsear(toks, self.g)
        arv = gerarArvore(res)
        self.assertEqual(arv["stmts"][0]["tipo"], "binary")
        self.assertEqual(arv["stmts"][0]["op"], "+")

    def test_aninhamento(self):
        toks = _programa(["((3 2 +) (4 1 -) *)"])
        arv = gerarArvore(parsear(toks, self.g))
        no = arv["stmts"][0]
        self.assertEqual(no["tipo"], "binary")
        self.assertEqual(no["op"], "*")
        self.assertEqual(no["esq"]["op"], "+")
        self.assertEqual(no["dir"]["op"], "-")

    def test_mem_write_e_read(self):
        toks = _programa(["(10 MEM)", "(MEM)"])
        arv = gerarArvore(parsear(toks, self.g))
        self.assertEqual(arv["stmts"][0]["tipo"], "mem_write")
        self.assertEqual(arv["stmts"][1]["tipo"], "mem_read")

    def test_res_ref(self):
        toks = _programa(["(3 2 +)", "(1 RES)"])
        arv = gerarArvore(parsear(toks, self.g))
        self.assertEqual(arv["stmts"][1]["tipo"], "res_ref")
        self.assertEqual(arv["stmts"][1]["linhas_atras"], 1)

    def test_if(self):
        toks = _programa(["((A) 0 >) (1 B) IF"])
        # ajusta para sintaxe correta com parens extras
        toks = _programa(["(((A) 0 >) (1 B) IF)"])
        arv = gerarArvore(parsear(toks, self.g))
        self.assertEqual(arv["stmts"][0]["tipo"], "if")

    def test_ifelse(self):
        toks = _programa(["(((A) 0 >) (1 B) (0 B) IFELSE)"])
        arv = gerarArvore(parsear(toks, self.g))
        self.assertEqual(arv["stmts"][0]["tipo"], "ifelse")

    def test_while(self):
        toks = _programa(["(((C) 0 >) ((C) 1 -) WHILE)"])
        arv = gerarArvore(parsear(toks, self.g))
        self.assertEqual(arv["stmts"][0]["tipo"], "while")

    def test_erro_sintatico_token_extra(self):
        toks = _programa(["(3 2 + 5)"])
        with self.assertRaises(Erros):
            parsear(toks, self.g)

    def test_erro_sem_start(self):
        toks = tokenizar_programa(["(3 2 +)", "(END)"])
        with self.assertRaises(Erros):
            parsear(toks, self.g)

    def test_erro_sem_end(self):
        toks = tokenizar_programa(["(START)", "(3 2 +)"])
        with self.assertRaises(Erros):
            parsear(toks, self.g)

    def test_recuperacao_panico_multi_erros(self):
        # Modo panico: o parser deve continuar apos o primeiro erro e
        # reportar varios erros em uma unica execucao. Aqui ha 3 problemas
        # sintaticos distintos no mesmo programa.
        toks = tokenizar_programa([
            "(START)",
            "(3 2 + 5)",          # token extra antes do ')'
            "(1 RES MEM)",        # 3 itens sem IFELSE
            "(((1 2 +) 3 4 -) WHILE)",  # itens demais antes de WHILE
            "(END)",
        ])
        try:
            parsear(toks, self.g)
        except Erros as erro:
            mensagem = str(erro)
        else:  # pragma: no cover - so deveria executar se nao houver erro
            self.fail("parsear() deveria ter levantado Erros")
        # A mensagem deve conter o cabecalho de modo panico e pelo menos
        # 3 erros distintos (um por linha problematica).
        self.assertIn("modo panico", mensagem)
        contagem = mensagem.count("Erro sintatico")
        self.assertGreaterEqual(contagem, 3, f"esperava >=3 erros, veio: {mensagem}")


class TestGeracaoAssembly(unittest.TestCase):
    def setUp(self):
        self.g = construirGramatica()

    def _gerar(self, linhas):
        arv = gerarArvore(parsear(_programa(linhas), self.g))
        return gerarAssembly(arv)

    def test_instrucoes_basicas(self):
        asm = self._gerar(["(3.0 2.0 +)", "(5.0 1.0 -)", "(2.0 3.0 *)", "(6.0 2.0 |)"])
        self.assertIn("VADD.F64", asm)
        self.assertIn("VSUB.F64", asm)
        self.assertIn("VMUL.F64", asm)
        self.assertIn("VDIV.F64", asm)

    def test_rotinas_idiv_mod_pow(self):
        asm = self._gerar(["(10 3 /)", "(10 3 %)", "(2 5 ^)"])
        self.assertIn("__op_idiv", asm)
        self.assertIn("__op_mod", asm)
        self.assertIn("__op_pow", asm)

    def test_assembly_com_while(self):
        asm = self._gerar(["(10 C)", "(((C) 0 >) ((C) 1 -) WHILE)"])
        self.assertIn("L_while_i", asm)
        self.assertIn("L_while_f", asm)

    def test_assembly_com_ifelse(self):
        asm = self._gerar(["(((A) 0 >) (1 B) (0 B) IFELSE)"])
        self.assertIn("L_else", asm)
        self.assertIn("L_ife_fim", asm)

    def test_ieee754_double(self):
        asm = self._gerar(["(3.14 2.0 +)"])
        self.assertIn(".double", asm)
        self.assertIn("F64", asm)


class TestLerTokens(unittest.TestCase):
    def test_ciclo_tokens(self):
        linhas = [[t for t in tokenizar_linha("(3 2 +)", numero_linha=1)]]
        with tempfile.TemporaryDirectory() as d:
            caminho = os.path.join(d, "toks.txt")
            salvarTokens(caminho, linhas)
            recuperados = lerTokens(caminho)
        self.assertEqual([t.valor for t in recuperados], ["(", "3", "2", "+", ")"])


class TestLerArquivoEFluxo(unittest.TestCase):
    def test_ler_arquivo_ignora_comentarios(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("# comentario\n(START)\n\n(1 2 +)\n(END)\n")
            nome = f.name
        try:
            linhas = []
            lerArquivo(nome, linhas)
            self.assertEqual(linhas, ["(START)", "(1 2 +)", "(END)"])
        finally:
            os.unlink(nome)

    def test_pipeline_fim_a_fim(self):
        conteudo = "(START)\n(3 2 +)\n(1 RES)\n(END)\n"
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "p.txt")
            with open(src, "w", encoding="utf-8") as f:
                f.write(conteudo)
            r = executar_fase2(
                caminho_fonte=src,
                caminho_tokens=os.path.join(d, "tk.txt"),
                caminho_asm=os.path.join(d, "o.s"),
                caminho_arvore=os.path.join(d, "a.txt"),
            )
            self.assertIn("VADD.F64", r["assembly"])
            self.assertEqual(r["arvore"]["stmts"][1]["tipo"], "res_ref")


if __name__ == "__main__":
    unittest.main()
