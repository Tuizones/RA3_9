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


# --------------------------------------------------------------
# Tabela de símbolos
# --------------------------------------------------------------


class TabelaSimbolos:
    """Tabela de símbolos do programa (escopo único: ``global``).

    Cada entrada é um ``dict`` com as chaves:
      ``nome``        — identificador da variável MEM;
      ``tipo``        — tipo inferido na primeira declaração;
      ``linha_def``   — linha da primeira ``(v MEM)``;
      ``linhas_uso``  — lista de linhas onde ``(MEM)`` aparece;
      ``escopo``      — sempre ``"global"`` nesta linguagem.
    """

    def __init__(self) -> None:
        self._tab: dict[str, dict] = {}

    # ---- operações principais -----------------------------------

    def declarar(self, nome: str, tipo: str, linha: int) -> list[ErroSemantico]:
        """Registra ``(v MEM)``. Devolve lista de erros (vazia se ok)."""
        erros: list[ErroSemantico] = []
        if nome in self._tab:
            existente = self._tab[nome]
            tipo_atual = existente["tipo"]
            if tipo_atual == TIPO_INDEF and tipo != TIPO_INDEF:
                # promove de indef para o tipo concreto
                existente["tipo"] = tipo
            elif tipo == TIPO_INDEF:
                # nada a fazer: mantém o tipo conhecido
                pass
            elif tipo_atual != tipo:
                erros.append(
                    ErroSemantico(
                        f"redeclaração da variável '{nome}' com tipo "
                        f"incompatível: era '{tipo_atual}', recebeu '{tipo}'",
                        linha,
                    )
                )
            # mesmo se houver erro, registramos a linha como uma "nova def"
            # para que análises subsequentes funcionem
            return erros
        self._tab[nome] = {
            "nome": nome,
            "tipo": tipo,
            "linha_def": linha,
            "linhas_uso": [],
            "escopo": "global",
        }
        return erros

    def usar(self, nome: str, linha: int) -> tuple[dict | None, list[ErroSemantico]]:
        """Registra ``(MEM)``. Devolve (símbolo|None, erros)."""
        if nome not in self._tab:
            return None, [
                ErroSemantico(
                    f"uso da variável '{nome}' antes da declaração (faltou '(v MEM)')",
                    linha,
                )
            ]
        sim = self._tab[nome]
        if linha and linha not in sim["linhas_uso"]:
            sim["linhas_uso"].append(linha)
        return sim, []

    # ---- acesso somente-leitura ---------------------------------

    def obter(self, nome: str) -> dict | None:
        return self._tab.get(nome)

    def itens(self) -> list[dict]:
        return [self._tab[n] for n in sorted(self._tab)]

    def __contains__(self, nome: str) -> bool:  # pragma: no cover - trivial
        return nome in self._tab

    def __len__(self) -> int:  # pragma: no cover - trivial
        return len(self._tab)


# --------------------------------------------------------------
# Inferência de tipos (versão leve da Sprint 2)
# --------------------------------------------------------------


def _tipo_de_numero(valor: str) -> str:
    return TIPO_REAL if "." in valor else TIPO_INT


def inferir_tipo(no: dict | None, tabela: TabelaSimbolos) -> str:
    """Inferência de tipo *best-effort* a partir da AST.

    Esta versão é minimalista; a Sprint 4 (verificarTipos) fará a
    verificação completa com erros e promoções. Aqui basta o suficiente
    para registrar o tipo declarado nas variáveis MEM.
    """
    if no is None:
        return TIPO_INDEF
    tipo = no.get("tipo")
    if tipo == "number":
        return _tipo_de_numero(no.get("valor", ""))
    if tipo == "binary":
        op = no.get("op", "")
        if op in _OPS_RELACIONAIS:
            return TIPO_BOOL
        if op in _OPS_REAL:
            return TIPO_REAL
        if op in _OPS_INT:
            return TIPO_INT
        # +, -, *, ^  → herdamos o tipo dos operandos (regra simples)
        t_esq = inferir_tipo(no.get("esq"), tabela)
        t_dir = inferir_tipo(no.get("dir"), tabela)
        if t_esq == t_dir and t_esq in (TIPO_INT, TIPO_REAL):
            return t_esq
        if TIPO_REAL in (t_esq, t_dir):
            return TIPO_REAL
        if TIPO_INT in (t_esq, t_dir):
            return TIPO_INT
        return TIPO_INDEF
    if tipo == "mem_read":
        sim = tabela.obter(no.get("nome", ""))
        return sim["tipo"] if sim else TIPO_INDEF
    if tipo == "mem_write":
        # uma escrita não devolve valor utilizável aqui
        return TIPO_INDEF
    if tipo == "res_ref":
        return TIPO_INDEF  # depende do statement referenciado
    if tipo == "if":
        return inferir_tipo(no.get("then_block"), tabela)
    if tipo == "ifelse":
        t1 = inferir_tipo(no.get("then_block"), tabela)
        t2 = inferir_tipo(no.get("else_block"), tabela)
        return t1 if t1 == t2 else TIPO_INDEF
    if tipo == "while":
        return TIPO_INDEF
    return TIPO_INDEF


# --------------------------------------------------------------
# Construção da tabela a partir da AST
# --------------------------------------------------------------


def construirTabelaSimbolos(arvore: dict) -> tuple[TabelaSimbolos, list[ErroSemantico]]:
    """Percorre a AST do programa e devolve ``(tabela, erros)``.

    O percurso é pré-ordem; para ``mem_write`` registramos a declaração
    ANTES de descer no valor (uma definição numa expressão imbricada
    passa a valer a partir daquele ponto). Para ``mem_read`` registramos
    o uso. Para ``res_ref`` validamos o N contra o índice do statement
    de topo atual.
    """
    tabela = TabelaSimbolos()
    erros: list[ErroSemantico] = []
    if not arvore or arvore.get("tipo") != "program":
        return tabela, erros

    stmts: list[dict] = arvore.get("stmts", [])

    def visitar(no: dict | None, idx_stmt_topo: int) -> None:
        if not isinstance(no, dict):
            return
        tipo = no.get("tipo")
        linha = no.get("linha", 0) or 0

        if tipo == "mem_write":
            # primeiro descemos no valor (ele não pode usar a própria
            # MEM antes de ela existir — mas pode usar OUTRAS MEMs já
            # declaradas anteriormente)
            visitar(no.get("valor"), idx_stmt_topo)
            tipo_inferido = inferir_tipo(no.get("valor"), tabela)
            erros.extend(tabela.declarar(no.get("nome", ""), tipo_inferido, linha))
            return

        if tipo == "mem_read":
            _, errs = tabela.usar(no.get("nome", ""), linha)
            erros.extend(errs)
            return

        if tipo == "res_ref":
            n = no.get("linhas_atras", 0)
            if n > idx_stmt_topo:
                erros.append(
                    ErroSemantico(
                        f"(N RES) referencia {n} linhas atrás, mas só existem "
                        f"{idx_stmt_topo} statement(s) anterior(es)",
                        linha,
                    )
                )
            return

        if tipo == "binary":
            visitar(no.get("esq"), idx_stmt_topo)
            visitar(no.get("dir"), idx_stmt_topo)
            return

        if tipo == "if":
            visitar(no.get("cond"), idx_stmt_topo)
            visitar(no.get("then_block"), idx_stmt_topo)
            return

        if tipo == "ifelse":
            visitar(no.get("cond"), idx_stmt_topo)
            visitar(no.get("then_block"), idx_stmt_topo)
            visitar(no.get("else_block"), idx_stmt_topo)
            return

        if tipo == "while":
            visitar(no.get("cond"), idx_stmt_topo)
            visitar(no.get("body"), idx_stmt_topo)
            return

        # number, ident, keyword: folhas sem efeito sobre a tabela

    for i, stmt in enumerate(stmts):
        # idx_stmt_topo = i  → quantos statements existem ANTES deste
        visitar(stmt, i)

    return tabela, erros


# --------------------------------------------------------------
# Renderização: tabela em Markdown
# --------------------------------------------------------------


def formatarTabelaMarkdown(tabela: TabelaSimbolos) -> str:
    """Devolve uma representação Markdown da tabela de símbolos."""
    linhas: list[str] = []
    linhas.append("# Tabela de Símbolos\n")
    if len(tabela) == 0:
        linhas.append("_Nenhuma variável MEM declarada._\n")
        return "\n".join(linhas)
    linhas.append("| Nome | Tipo | Escopo | Linha def. | Linhas de uso |")
    linhas.append("|------|------|--------|-----------:|---------------|")
    for sim in tabela.itens():
        usos = ", ".join(str(u) for u in sim["linhas_uso"]) or "—"
        linhas.append(
            f"| `{sim['nome']}` | {sim['tipo']} | {sim['escopo']} | "
            f"{sim['linha_def']} | {usos} |"
        )
    return "\n".join(linhas) + "\n"


def salvarTabelaSimbolos(
    tabela: TabelaSimbolos, caminho: str | Path = "output/tabela_simbolos.md"
) -> Path:
    p = Path(caminho)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(formatarTabelaMarkdown(tabela), encoding="utf-8")
    return p

