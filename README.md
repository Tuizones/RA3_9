# RA3 9 — Análise Semântica (Fase 3)

> Trabalho da disciplina **Linguagens Formais e Compiladores** — PUC-PR.
> Integrantes: **Arthur Hoffmann Tuyzones**, **Emanuel Henrique Ricetto**,
> **Frederico Frutuoso**. Grupo Canvas: **RA3 9**.

Esta entrega estende o analisador léxico (Fase 1) e o analisador sintático
LL(1) (Fase 2) com a **análise semântica** completa: construção da tabela
de símbolos, verificação estática de tipos e geração de uma **árvore
sintática atribuída** pronta para a geração de código ARMv7.

## Sumário

1. [Visão geral](#vis%C3%A3o-geral)
2. [Estrutura do projeto](#estrutura-do-projeto)
3. [Pré-requisitos](#pr%C3%A9-requisitos)
4. [Instalação](#instala%C3%A7%C3%A3o)
5. [Como executar](#como-executar)
6. [Códigos de saída](#c%C3%B3digos-de-sa%C3%ADda)
7. [Testes automatizados](#testes-automatizados)

## Visão geral

A linguagem-fonte segue notação polonesa reversa (RPN) e expressa programas
como sequência de declarações `MEM` e expressões avaliadas pilha-acima. A
Fase 3 introduz:

- **Tabela de símbolos** com escopo único, mantendo nome, tipo, primeira
  declaração e contagem de usos por variável `MEM`.
- **Inferência de tipos** sobre números inteiros (`int`), reais (`real`) e
  resultados booleanos de operadores relacionais (`bool`).
- **Verificação estática** que rejeita operações entre tipos incompatíveis
  (por exemplo soma de `int` com `real` sem conversão explícita).
- **Árvore atribuída** que anota cada nó com seu tipo, rótulo ARMv7 e os
  metadados necessários para a geração de código.

## Estrutura do projeto

```
RA3_9/
├── AnalisadorSemantico.py        # CLI principal da Fase 3
├── README.md                     # este arquivo
├── gramatica.md                  # gramática livre de contexto (sem ações)
├── gramatica_atribuida.md        # gramática + ações semânticas
├── regras_tipos.md               # sistema de tipos em sequentes
├── docs/
│   └── diagramas.md              # diagramas Mermaid (pipeline, AST, tipos)
├── src/
│   ├── lexer_fsm.py              # analisador léxico (FSM)
│   ├── parser_ll1.py             # parser LL(1) descendente preditivo
│   ├── semantica.py              # tabela de símbolos + tipos + atribuição
│   ├── armv7_generator.py        # gerador de assembly ARMv7
│   └── pipeline.py               # orquestração das fases
├── tests/
│   ├── test_lexer.py
│   ├── test_pipeline.py
│   ├── test_semantica.py
│   └── test_arquivos_e2e.py
├── teste1.txt … teste3.txt       # programas válidos
├── teste_erro_lexico.txt         # programa com erro léxico
├── teste_erro_sintatico.txt      # programa com erro sintático
└── teste_erro_semantico.txt      # programa com erro semântico
```

## Pré-requisitos

- Python **3.10+** (usamos `match`/`case` e `tuple[…]` / `list[…]`).
- Nenhuma dependência externa: somente a biblioteca padrão.

## Instalação

```pwsh
git clone <repo>            # ou descompactar o ZIP da entrega
cd RA3_9
python --version            # confirme >= 3.10
```

Não há `requirements.txt` porque todo o código usa apenas a stdlib.

## Como executar

```pwsh
python AnalisadorSemantico.py teste1.txt
```

A CLI escreve todos os artefatos em `output/`:

| Arquivo                          | Descrição                                  |
| -------------------------------- | ------------------------------------------ |
| `tokens_ultima_execucao.txt`     | Lista linear de tokens produzidos          |
| `arvore_ultima_execucao.md`      | Árvore sintática (sem atribuições)         |
| `arvore_atribuida.md` / `.json`  | Árvore atribuída com tipos e rótulos       |
| `tabela_simbolos.md`             | Tabela de símbolos formatada               |
| `derivacao_ultima_execucao.md`   | Sequência de produções aplicadas           |
| `erros_lexsint.md`               | Diagnósticos das fases 1 e 2 (se houver)   |
| `erros_semanticos.md`            | Diagnósticos da fase 3 (se houver)         |
| `ultima_execucao.s`              | Assembly ARMv7 gerado (Cpulator DE1-SoC)   |

## Códigos de saída

| Código | Significado                                                       |
| -----: | ------------------------------------------------------------------|
|    `0` | Compilação concluída sem erros                                    |
|    `2` | Erros léxicos ou sintáticos (fases 1/2)                           |
|    `3` | Erros semânticos (fase 3)                                         |

## Testes automatizados

```pwsh
cd RA3_9
python -m unittest discover -s tests -v
```

Cobertura atual: **108 testes** distribuídos em 4 arquivos.
