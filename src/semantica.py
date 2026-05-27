# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA3 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara


# Analisador semântico: construção da tabela de símbolos, verificação de tipos e geração
#
# Este módulo implementa a estrutura de dados responsável por rastrear
# todas as variáveis MEM declaradas e usadas no programa, além de uma
# função utilitária que percorre a AST gerada pelo parser LL(1) da
# Fase 2 e produz a tabela.
#
# Erros detectados nesta etapa (modo "best-effort", coletados em lista):
#   • uso de (MEM) antes de qualquer (v MEM) com o mesmo nome;
#   • redeclaração com tipo incompatível;
#   • (N RES) com N maior do que o número de statements anteriores.
#
# Tipos inferidos nesta fase (inferência completa virá na Sprint 4):
#   • número literal sem ponto  → "int"
#   • número literal com ponto  → "real"
#   • expressão relacional       → "bool"
#   • divisão real  ``|``        → "real"
#   • divisão inteira ``/`` ou ``%`` → "int"
#   • (MEM) referenciando variável conhecida → tipo da variável
#   • demais casos               → "indef"

from __future__ import annotations

from pathlib import Path


# --------------------------------------------------------------
# Tipos auxiliares
# --------------------------------------------------------------

TIPO_INT = "int"
TIPO_REAL = "real"
TIPO_BOOL = "bool"
TIPO_INDEF = "indef"

_OPS_RELACIONAIS = {">", "<", "==", "!=", ">=", "<="}
_OPS_INT = {"/", "%"}
_OPS_REAL = {"|"}


class ErroSemantico:
    """Erro semântico coletado durante a construção da tabela.

    Mantemos um objeto leve (e não uma exceção) porque a análise
    semântica adota recuperação de erros: queremos reportar todos os
    problemas de uma vez, igual ao parser em modo pânico da Fase 2.
    """

    __slots__ = ("mensagem", "linha")

    def __init__(self, mensagem: str, linha: int = 0) -> None:
        self.mensagem = mensagem
        self.linha = linha

    def __repr__(self) -> str:  # pragma: no cover - utilitário de debug
        return f"ErroSemantico(linha={self.linha}, msg={self.mensagem!r})"

    def __str__(self) -> str:
        prefixo = f"[semântico] (linha {self.linha}) " if self.linha else "[semântico] "
        return prefixo + self.mensagem


