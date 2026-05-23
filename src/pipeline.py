# Integrantes:
#   Arthur Felipe Bach Biancolini (Tuizones)
#   Emanuel Riceto da Silva (emanuelriceto)
#   Frederico Virmond Fruet (fredfruet)
# Grupo Canvas: RA3 9
# Instituição: Pontifícia Universidade Católica do Paraná
# Disciplina: Linguagens Formais e Compiladores
# Professor: Frank Coelho de Alcantara

# Pipeline da Fase 2 — aqui ficam as funções obrigatórias do enunciado.
# Todas as partes do projeto passam por aqui antes de chegar no main.
#
#   lerArquivo(nomeArquivo, linhas)   — abre o .txt e carrega as linhas
#   lerTokens(nomeArquivoTokens)      — lê o arquivo de tokens (integração Fase 1)
#   construirGramatica()              — apenas re-exporta de parser_ll1
#   parsear(tokens, tabela_ll1)       — idem
#   gerarArvore(resultado_parse)      — idem
#   gerarAssembly(arvore)             — chama o gerador ARMv7
#   exibirResultados(resultados)      — imprime resumo no terminal
#
# As funções parseExpressao e executarExpressao são da Fase 1 e ficam
# aqui apenas para compatibilidade com os testes existentes.

from __future__ import annotations

import os
from pathlib import Path

from .lexer_fsm import (
    Token,
    Erros,
    TIPO_ABRE,
    TIPO_FECHA,
    TIPO_KEYWORD,
    tokenizar_linha,
)
from .parser_ll1 import (
    construirGramatica,
    parsear,
    gerarArvore,
)
from .armv7_generator import gerar_assembly_arvore


# --------------------------------------------------------------
# lerArquivo — leitura do código-fonte
# --------------------------------------------------------------


def lerArquivo(nomeArquivo: str, linhas: list[str]) -> None:
    # Lê o arquivo-fonte ignorando linhas em branco e comentários com #.
    # Se não encontrar o arquivo direto, tenta a pasta 'exemplos/' também.
    if not os.path.isfile(nomeArquivo):
        alternativo = os.path.join("exemplos", nomeArquivo)
        if os.path.isfile(alternativo):
            nomeArquivo = alternativo
    with open(nomeArquivo, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            texto = linha.strip()
            if texto and not texto.startswith("#"):
                linhas.append(texto)


# --------------------------------------------------------------
# parseExpressao (compat. Fase 1) e lerTokens (Fase 2)
# --------------------------------------------------------------


def parseExpressao(linha: str, tokens_saida: list[str]) -> list[Token]:
    # Compat. Fase 1: tokeniza uma linha e devolve os Tokens.
    tokens = tokenizar_linha(linha)
    tokens_saida.extend(token.valor for token in tokens)
    return tokens


def salvarTokens(caminho: str | Path, tokens_por_linha: list[list[Token]]) -> None:
    # Salva no formato que a lerTokens sabe ler:
    # cada linha do arquivo = linha_N;TIPO:valor,TIPO:valor,...
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", encoding="utf-8") as f:
        for i, tokens in enumerate(tokens_por_linha, start=1):
            pares = [f"{t.tipo}:{t.valor}" for t in tokens]
            f.write(f"linha_{i};" + ",".join(pares) + "\n")


def lerTokens(nomeArquivo: str) -> list[Token]:
    # Lê o arquivo de tokens gerado pelo lexer da Fase 1.
    # Formato esperado por linha:
    #   linha_<N>;TIPO:valor,TIPO:valor,...
    # Reconstrói objetos Token com linha e coluna preservados.
    tokens: list[Token] = []
    if not os.path.isfile(nomeArquivo):
        raise Erros(f"Arquivo de tokens não encontrado: {nomeArquivo}")
    with open(nomeArquivo, "r", encoding="utf-8") as f:
        for bruta in f:
            linha = bruta.strip()
            if not linha or linha.startswith("#"):
                continue
            if ";" not in linha:
                raise Erros(f"Linha sem separador ';' no arquivo de tokens: {linha!r}")
            cabecalho, corpo = linha.split(";", 1)
            try:
                numero_linha = int(cabecalho.replace("linha_", "").strip())
            except ValueError:
                numero_linha = 0
            if not corpo:
                continue
            for i, par in enumerate(corpo.split(",")):
                if ":" not in par:
                    raise Erros(f"Par inválido no arquivo de tokens: {par!r}")
                tipo, valor = par.split(":", 1)
                tokens.append(
                    Token(tipo=tipo, valor=valor, linha=numero_linha, coluna=i + 1)
                )
    return tokens


# --------------------------------------------------------------
# executarExpressao (compat Fase 1) + validação semântica básica
# --------------------------------------------------------------


def executarExpressao(tokens: list[Token], contexto: dict) -> dict:
    # Compat. Fase 1: valida uma linha isolada sem precisar de arquivo.
    # Envolvemos a linha em (START)...(END) para poder usar o parser da Fase 2.
    envelope = [
        Token(TIPO_ABRE, "(", 0, 0),
        Token(TIPO_KEYWORD, "START", 0, 0),
        Token(TIPO_FECHA, ")", 0, 0),
        *tokens,
        Token(TIPO_ABRE, "(", 0, 0),
        Token(TIPO_KEYWORD, "END", 0, 0),
        Token(TIPO_FECHA, ")", 0, 0),
    ]
    gram = construirGramatica()
    resultado = parsear(envelope, gram)
    arvore = gerarArvore(resultado)
    stmts = arvore["stmts"]
    if not stmts:
        raise Erros("Expressão vazia")
    no = stmts[0]

    contexto.setdefault("memoria", {})
    contexto.setdefault("resultados", [])

    descricao = "expressão válida"
    if no["tipo"] == "mem_write":
        contexto["memoria"][no["nome"]] = "definida"
        descricao = f"memória {no['nome']} marcada como definida"
    elif no["tipo"] == "mem_read":
        if no["nome"] not in contexto["memoria"]:
            contexto["memoria"][no["nome"]] = "não inicializada"
        descricao = f"leitura da memória {no['nome']}"
    elif no["tipo"] == "res_ref":
        n = no["linhas_atras"]
        if n > len(contexto["resultados"]):
            raise Erros(f"RES inválido: {n} linhas atrás não disponível")
        descricao = f"referência ao resultado de {n} linhas atrás"

    contexto["resultados"].append("gerado_em_assembly")
    return {"ok": True, "descricao": descricao, "arvore": no}


# --------------------------------------------------------------
# gerarAssembly — agora a partir da AST "program"
# --------------------------------------------------------------


def gerarAssembly(arvore_programa: dict) -> str:
    # Simplesmente delega para o gerador ARMv7.
    # Função separada para manter a interface do enunciado.
    return gerar_assembly_arvore(arvore_programa)


# --------------------------------------------------------------
# Exibição
# --------------------------------------------------------------


def exibirResultados(resultados: list[dict]) -> None:
    for i, resultado in enumerate(resultados, start=1):
        print(f"Linha {i}: {resultado['descricao']}")


# --------------------------------------------------------------
# Helpers de alto nível usados pelo main
# --------------------------------------------------------------


def executar_fase2(
    caminho_fonte: str,
    caminho_tokens: str,
    caminho_asm: str,
    caminho_arvore: str,
) -> dict:
    # Orquestrador: chama todas as etapas em ordem e retorna tudo num dict.
    # Esse dict é usado pelo AnalisadorSintatico.py para salvar os artefatos e exibir resultados.
    # 1) leitura do fonte
    linhas: list[str] = []
    lerArquivo(caminho_fonte, linhas)

    # 2) tokenização e salva o arquivo de tokens
    tokens_por_linha = [tokenizar_linha(ln, numero_linha=i + 1) for i, ln in enumerate(linhas)]
    salvarTokens(caminho_tokens, tokens_por_linha)

    # 3) relê os tokens do arquivo (simula integração com a Fase 1)
    tokens_flat = lerTokens(caminho_tokens)

    # 4) constrói a gramática LL(1) (produções + FIRST + FOLLOW + tabela)
    gram = construirGramatica()

    # 5) roda o parser com pilha
    resultado = parsear(tokens_flat, gram)

    # 6) constrói a AST semântica
    arvore = gerarArvore(resultado)

    # 7) salva a árvore apenas em JSON
    Path(caminho_arvore).parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(caminho_arvore, "w", encoding="utf-8") as f:
        json.dump(arvore, f, ensure_ascii=False, indent=2)

    # 8) gera o Assembly ARMv7
    asm = gerarAssembly(arvore)
    Path(caminho_asm).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho_asm).write_text(asm, encoding="utf-8")

    return {
        "linhas": linhas,
        "tokens": tokens_flat,
        "gramatica": gram,
        "derivacao": resultado["derivacao"],
        "passos": resultado["passos"],
        "arvore": arvore,
        "assembly": asm,
    }
