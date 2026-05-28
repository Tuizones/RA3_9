# Derivação LL(1) — Passo a Passo

| Passo | Pilha (topo →) | Entrada (→) | Ação |
|------:|---|---|---|
| 1 | `PROGRAM $` | `( START ) ( 10 3 + ) ( 8 …` | Expande: `PROGRAM` → `( start ) BODY` |
| 2 | `( start ) BODY $` | `( START ) ( 10 3 + ) ( 8 …` | Casa: `(` |
| 3 | `start ) BODY $` | `START ) ( 10 3 + ) ( 8 3 …` | Casa: `start` |
| 4 | `) BODY $` | `) ( 10 3 + ) ( 8 3 - …` | Casa: `)` |
| 5 | `BODY $` | `( 10 3 + ) ( 8 3 - ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 6 | `( BODY_TAIL $` | `( 10 3 + ) ( 8 3 - ) …` | Casa: `(` |
| 7 | `BODY_TAIL $` | `10 3 + ) ( 8 3 - ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 8 | `EXPR_BODY ) BODY $` | `10 3 + ) ( 8 3 - ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 9 | `ITEM REST1 ) BODY $` | `10 3 + ) ( 8 3 - ) ( …` | Expande: `ITEM` → `numero` |
| 10 | `numero REST1 ) BODY $` | `10 3 + ) ( 8 3 - ) ( …` | Casa: `numero` |
| 11 | `REST1 ) BODY $` | `3 + ) ( 8 3 - ) ( 4 …` | Expande: `REST1` → `ITEM REST2` |
| 12 | `ITEM REST2 ) BODY $` | `3 + ) ( 8 3 - ) ( 4 …` | Expande: `ITEM` → `numero` |
| 13 | `numero REST2 ) BODY $` | `3 + ) ( 8 3 - ) ( 4 …` | Casa: `numero` |
| 14 | `REST2 ) BODY $` | `+ ) ( 8 3 - ) ( 4 3 …` | Expande: `REST2` → `BINOP` |
| 15 | `BINOP ) BODY $` | `+ ) ( 8 3 - ) ( 4 3 …` | Expande: `BINOP` → `+` |
| 16 | `+ ) BODY $` | `+ ) ( 8 3 - ) ( 4 3 …` | Casa: `+` |
| 17 | `) BODY $` | `) ( 8 3 - ) ( 4 3 * …` | Casa: `)` |
| 18 | `BODY $` | `( 8 3 - ) ( 4 3 * ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 19 | `( BODY_TAIL $` | `( 8 3 - ) ( 4 3 * ) …` | Casa: `(` |
| 20 | `BODY_TAIL $` | `8 3 - ) ( 4 3 * ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 21 | `EXPR_BODY ) BODY $` | `8 3 - ) ( 4 3 * ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 22 | `ITEM REST1 ) BODY $` | `8 3 - ) ( 4 3 * ) ( …` | Expande: `ITEM` → `numero` |
| 23 | `numero REST1 ) BODY $` | `8 3 - ) ( 4 3 * ) ( …` | Casa: `numero` |
| 24 | `REST1 ) BODY $` | `3 - ) ( 4 3 * ) ( 10 …` | Expande: `REST1` → `ITEM REST2` |
| 25 | `ITEM REST2 ) BODY $` | `3 - ) ( 4 3 * ) ( 10 …` | Expande: `ITEM` → `numero` |
| 26 | `numero REST2 ) BODY $` | `3 - ) ( 4 3 * ) ( 10 …` | Casa: `numero` |
| 27 | `REST2 ) BODY $` | `- ) ( 4 3 * ) ( 10 2 …` | Expande: `REST2` → `BINOP` |
| 28 | `BINOP ) BODY $` | `- ) ( 4 3 * ) ( 10 2 …` | Expande: `BINOP` → `-` |
| 29 | `- ) BODY $` | `- ) ( 4 3 * ) ( 10 2 …` | Casa: `-` |
| 30 | `) BODY $` | `) ( 4 3 * ) ( 10 2 / …` | Casa: `)` |
| 31 | `BODY $` | `( 4 3 * ) ( 10 2 / ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 32 | `( BODY_TAIL $` | `( 4 3 * ) ( 10 2 / ) …` | Casa: `(` |
| 33 | `BODY_TAIL $` | `4 3 * ) ( 10 2 / ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 34 | `EXPR_BODY ) BODY $` | `4 3 * ) ( 10 2 / ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 35 | `ITEM REST1 ) BODY $` | `4 3 * ) ( 10 2 / ) ( …` | Expande: `ITEM` → `numero` |
| 36 | `numero REST1 ) BODY $` | `4 3 * ) ( 10 2 / ) ( …` | Casa: `numero` |
| 37 | `REST1 ) BODY $` | `3 * ) ( 10 2 / ) ( 10 …` | Expande: `REST1` → `ITEM REST2` |
| 38 | `ITEM REST2 ) BODY $` | `3 * ) ( 10 2 / ) ( 10 …` | Expande: `ITEM` → `numero` |
| 39 | `numero REST2 ) BODY $` | `3 * ) ( 10 2 / ) ( 10 …` | Casa: `numero` |
| 40 | `REST2 ) BODY $` | `* ) ( 10 2 / ) ( 10 3 …` | Expande: `REST2` → `BINOP` |
| 41 | `BINOP ) BODY $` | `* ) ( 10 2 / ) ( 10 3 …` | Expande: `BINOP` → `*` |
| 42 | `* ) BODY $` | `* ) ( 10 2 / ) ( 10 3 …` | Casa: `*` |
| 43 | `) BODY $` | `) ( 10 2 / ) ( 10 3 % …` | Casa: `)` |
| 44 | `BODY $` | `( 10 2 / ) ( 10 3 % ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 45 | `( BODY_TAIL $` | `( 10 2 / ) ( 10 3 % ) …` | Casa: `(` |
| 46 | `BODY_TAIL $` | `10 2 / ) ( 10 3 % ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 47 | `EXPR_BODY ) BODY $` | `10 2 / ) ( 10 3 % ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 48 | `ITEM REST1 ) BODY $` | `10 2 / ) ( 10 3 % ) ( …` | Expande: `ITEM` → `numero` |
| 49 | `numero REST1 ) BODY $` | `10 2 / ) ( 10 3 % ) ( …` | Casa: `numero` |
| 50 | `REST1 ) BODY $` | `2 / ) ( 10 3 % ) ( 2 …` | Expande: `REST1` → `ITEM REST2` |
| 51 | `ITEM REST2 ) BODY $` | `2 / ) ( 10 3 % ) ( 2 …` | Expande: `ITEM` → `numero` |
| 52 | `numero REST2 ) BODY $` | `2 / ) ( 10 3 % ) ( 2 …` | Casa: `numero` |
| 53 | `REST2 ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `REST2` → `BINOP` |
| 54 | `BINOP ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Expande: `BINOP` → `/` |
| 55 | `/ ) BODY $` | `/ ) ( 10 3 % ) ( 2 5 …` | Casa: `/` |
| 56 | `) BODY $` | `) ( 10 3 % ) ( 2 5 ^ …` | Casa: `)` |
| 57 | `BODY $` | `( 10 3 % ) ( 2 5 ^ ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 58 | `( BODY_TAIL $` | `( 10 3 % ) ( 2 5 ^ ) …` | Casa: `(` |
| 59 | `BODY_TAIL $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 60 | `EXPR_BODY ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 61 | `ITEM REST1 ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Expande: `ITEM` → `numero` |
| 62 | `numero REST1 ) BODY $` | `10 3 % ) ( 2 5 ^ ) ( …` | Casa: `numero` |
| 63 | `REST1 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 7.5 …` | Expande: `REST1` → `ITEM REST2` |
| 64 | `ITEM REST2 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 7.5 …` | Expande: `ITEM` → `numero` |
| 65 | `numero REST2 ) BODY $` | `3 % ) ( 2 5 ^ ) ( 7.5 …` | Casa: `numero` |
| 66 | `REST2 ) BODY $` | `% ) ( 2 5 ^ ) ( 7.5 2.5 …` | Expande: `REST2` → `BINOP` |
| 67 | `BINOP ) BODY $` | `% ) ( 2 5 ^ ) ( 7.5 2.5 …` | Expande: `BINOP` → `%` |
| 68 | `% ) BODY $` | `% ) ( 2 5 ^ ) ( 7.5 2.5 …` | Casa: `%` |
| 69 | `) BODY $` | `) ( 2 5 ^ ) ( 7.5 2.5 \| …` | Casa: `)` |
| 70 | `BODY $` | `( 2 5 ^ ) ( 7.5 2.5 \| ) …` | Expande: `BODY` → `( BODY_TAIL` |
| 71 | `( BODY_TAIL $` | `( 2 5 ^ ) ( 7.5 2.5 \| ) …` | Casa: `(` |
| 72 | `BODY_TAIL $` | `2 5 ^ ) ( 7.5 2.5 \| ) ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 73 | `EXPR_BODY ) BODY $` | `2 5 ^ ) ( 7.5 2.5 \| ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 74 | `ITEM REST1 ) BODY $` | `2 5 ^ ) ( 7.5 2.5 \| ) ( …` | Expande: `ITEM` → `numero` |
| 75 | `numero REST1 ) BODY $` | `2 5 ^ ) ( 7.5 2.5 \| ) ( …` | Casa: `numero` |
| 76 | `REST1 ) BODY $` | `5 ^ ) ( 7.5 2.5 \| ) ( 5 …` | Expande: `REST1` → `ITEM REST2` |
| 77 | `ITEM REST2 ) BODY $` | `5 ^ ) ( 7.5 2.5 \| ) ( 5 …` | Expande: `ITEM` → `numero` |
| 78 | `numero REST2 ) BODY $` | `5 ^ ) ( 7.5 2.5 \| ) ( 5 …` | Casa: `numero` |
| 79 | `REST2 ) BODY $` | `^ ) ( 7.5 2.5 \| ) ( 5 CONT …` | Expande: `REST2` → `BINOP` |
| 80 | `BINOP ) BODY $` | `^ ) ( 7.5 2.5 \| ) ( 5 CONT …` | Expande: `BINOP` → `^` |
| 81 | `^ ) BODY $` | `^ ) ( 7.5 2.5 \| ) ( 5 CONT …` | Casa: `^` |
| 82 | `) BODY $` | `) ( 7.5 2.5 \| ) ( 5 CONT ) …` | Casa: `)` |
| 83 | `BODY $` | `( 7.5 2.5 \| ) ( 5 CONT ) ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 84 | `( BODY_TAIL $` | `( 7.5 2.5 \| ) ( 5 CONT ) ( …` | Casa: `(` |
| 85 | `BODY_TAIL $` | `7.5 2.5 \| ) ( 5 CONT ) ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 86 | `EXPR_BODY ) BODY $` | `7.5 2.5 \| ) ( 5 CONT ) ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 87 | `ITEM REST1 ) BODY $` | `7.5 2.5 \| ) ( 5 CONT ) ( ( …` | Expande: `ITEM` → `numero` |
| 88 | `numero REST1 ) BODY $` | `7.5 2.5 \| ) ( 5 CONT ) ( ( …` | Casa: `numero` |
| 89 | `REST1 ) BODY $` | `2.5 \| ) ( 5 CONT ) ( ( CONT …` | Expande: `REST1` → `ITEM REST2` |
| 90 | `ITEM REST2 ) BODY $` | `2.5 \| ) ( 5 CONT ) ( ( CONT …` | Expande: `ITEM` → `numero` |
| 91 | `numero REST2 ) BODY $` | `2.5 \| ) ( 5 CONT ) ( ( CONT …` | Casa: `numero` |
| 92 | `REST2 ) BODY $` | `\| ) ( 5 CONT ) ( ( CONT ) …` | Expande: `REST2` → `BINOP` |
| 93 | `BINOP ) BODY $` | `\| ) ( 5 CONT ) ( ( CONT ) …` | Expande: `BINOP` → `\|` |
| 94 | `\| ) BODY $` | `\| ) ( 5 CONT ) ( ( CONT ) …` | Casa: `\|` |
| 95 | `) BODY $` | `) ( 5 CONT ) ( ( CONT ) 2 …` | Casa: `)` |
| 96 | `BODY $` | `( 5 CONT ) ( ( CONT ) 2 * …` | Expande: `BODY` → `( BODY_TAIL` |
| 97 | `( BODY_TAIL $` | `( 5 CONT ) ( ( CONT ) 2 * …` | Casa: `(` |
| 98 | `BODY_TAIL $` | `5 CONT ) ( ( CONT ) 2 * ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 99 | `EXPR_BODY ) BODY $` | `5 CONT ) ( ( CONT ) 2 * ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 100 | `ITEM REST1 ) BODY $` | `5 CONT ) ( ( CONT ) 2 * ) …` | Expande: `ITEM` → `numero` |
| 101 | `numero REST1 ) BODY $` | `5 CONT ) ( ( CONT ) 2 * ) …` | Casa: `numero` |
| 102 | `REST1 ) BODY $` | `CONT ) ( ( CONT ) 2 * ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 103 | `ITEM REST2 ) BODY $` | `CONT ) ( ( CONT ) 2 * ) ( …` | Expande: `ITEM` → `ident` |
| 104 | `ident REST2 ) BODY $` | `CONT ) ( ( CONT ) 2 * ) ( …` | Casa: `ident` |
| 105 | `REST2 ) BODY $` | `) ( ( CONT ) 2 * ) ( 1 …` | Expande: `REST2` → `ε` |
| 106 | `) BODY $` | `) ( ( CONT ) 2 * ) ( 1 …` | Casa: `)` |
| 107 | `BODY $` | `( ( CONT ) 2 * ) ( 1 RES …` | Expande: `BODY` → `( BODY_TAIL` |
| 108 | `( BODY_TAIL $` | `( ( CONT ) 2 * ) ( 1 RES …` | Casa: `(` |
| 109 | `BODY_TAIL $` | `( CONT ) 2 * ) ( 1 RES ) …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 110 | `EXPR_BODY ) BODY $` | `( CONT ) 2 * ) ( 1 RES ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 111 | `ITEM REST1 ) BODY $` | `( CONT ) 2 * ) ( 1 RES ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 112 | `( EXPR_BODY ) REST1 ) BODY $` | `( CONT ) 2 * ) ( 1 RES ) …` | Casa: `(` |
| 113 | `EXPR_BODY ) REST1 ) BODY $` | `CONT ) 2 * ) ( 1 RES ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 114 | `ITEM REST1 ) REST1 ) BODY $` | `CONT ) 2 * ) ( 1 RES ) ( …` | Expande: `ITEM` → `ident` |
| 115 | `ident REST1 ) REST1 ) BODY $` | `CONT ) 2 * ) ( 1 RES ) ( …` | Casa: `ident` |
| 116 | `REST1 ) REST1 ) BODY $` | `) 2 * ) ( 1 RES ) ( ( …` | Expande: `REST1` → `ε` |
| 117 | `) REST1 ) BODY $` | `) 2 * ) ( 1 RES ) ( ( …` | Casa: `)` |
| 118 | `REST1 ) BODY $` | `2 * ) ( 1 RES ) ( ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 119 | `ITEM REST2 ) BODY $` | `2 * ) ( 1 RES ) ( ( ( …` | Expande: `ITEM` → `numero` |
| 120 | `numero REST2 ) BODY $` | `2 * ) ( 1 RES ) ( ( ( …` | Casa: `numero` |
| 121 | `REST2 ) BODY $` | `* ) ( 1 RES ) ( ( ( CONT …` | Expande: `REST2` → `BINOP` |
| 122 | `BINOP ) BODY $` | `* ) ( 1 RES ) ( ( ( CONT …` | Expande: `BINOP` → `*` |
| 123 | `* ) BODY $` | `* ) ( 1 RES ) ( ( ( CONT …` | Casa: `*` |
| 124 | `) BODY $` | `) ( 1 RES ) ( ( ( CONT ) …` | Casa: `)` |
| 125 | `BODY $` | `( 1 RES ) ( ( ( CONT ) 0 …` | Expande: `BODY` → `( BODY_TAIL` |
| 126 | `( BODY_TAIL $` | `( 1 RES ) ( ( ( CONT ) 0 …` | Casa: `(` |
| 127 | `BODY_TAIL $` | `1 RES ) ( ( ( CONT ) 0 > …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 128 | `EXPR_BODY ) BODY $` | `1 RES ) ( ( ( CONT ) 0 > …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 129 | `ITEM REST1 ) BODY $` | `1 RES ) ( ( ( CONT ) 0 > …` | Expande: `ITEM` → `numero` |
| 130 | `numero REST1 ) BODY $` | `1 RES ) ( ( ( CONT ) 0 > …` | Casa: `numero` |
| 131 | `REST1 ) BODY $` | `RES ) ( ( ( CONT ) 0 > ) …` | Expande: `REST1` → `ITEM REST2` |
| 132 | `ITEM REST2 ) BODY $` | `RES ) ( ( ( CONT ) 0 > ) …` | Expande: `ITEM` → `res` |
| 133 | `res REST2 ) BODY $` | `RES ) ( ( ( CONT ) 0 > ) …` | Casa: `res` |
| 134 | `REST2 ) BODY $` | `) ( ( ( CONT ) 0 > ) ( …` | Expande: `REST2` → `ε` |
| 135 | `) BODY $` | `) ( ( ( CONT ) 0 > ) ( …` | Casa: `)` |
| 136 | `BODY $` | `( ( ( CONT ) 0 > ) ( ( …` | Expande: `BODY` → `( BODY_TAIL` |
| 137 | `( BODY_TAIL $` | `( ( ( CONT ) 0 > ) ( ( …` | Casa: `(` |
| 138 | `BODY_TAIL $` | `( ( CONT ) 0 > ) ( ( ( …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 139 | `EXPR_BODY ) BODY $` | `( ( CONT ) 0 > ) ( ( ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 140 | `ITEM REST1 ) BODY $` | `( ( CONT ) 0 > ) ( ( ( …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 141 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( CONT ) 0 > ) ( ( ( …` | Casa: `(` |
| 142 | `EXPR_BODY ) REST1 ) BODY $` | `( CONT ) 0 > ) ( ( ( CONT …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 143 | `ITEM REST1 ) REST1 ) BODY $` | `( CONT ) 0 > ) ( ( ( CONT …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 144 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( CONT ) 0 > ) ( ( ( CONT …` | Casa: `(` |
| 145 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `CONT ) 0 > ) ( ( ( CONT ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 146 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `CONT ) 0 > ) ( ( ( CONT ) …` | Expande: `ITEM` → `ident` |
| 147 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `CONT ) 0 > ) ( ( ( CONT ) …` | Casa: `ident` |
| 148 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 0 > ) ( ( ( CONT ) 1 …` | Expande: `REST1` → `ε` |
| 149 | `) REST1 ) REST1 ) BODY $` | `) 0 > ) ( ( ( CONT ) 1 …` | Casa: `)` |
| 150 | `REST1 ) REST1 ) BODY $` | `0 > ) ( ( ( CONT ) 1 - …` | Expande: `REST1` → `ITEM REST2` |
| 151 | `ITEM REST2 ) REST1 ) BODY $` | `0 > ) ( ( ( CONT ) 1 - …` | Expande: `ITEM` → `numero` |
| 152 | `numero REST2 ) REST1 ) BODY $` | `0 > ) ( ( ( CONT ) 1 - …` | Casa: `numero` |
| 153 | `REST2 ) REST1 ) BODY $` | `> ) ( ( ( CONT ) 1 - ) …` | Expande: `REST2` → `BINOP` |
| 154 | `BINOP ) REST1 ) BODY $` | `> ) ( ( ( CONT ) 1 - ) …` | Expande: `BINOP` → `>` |
| 155 | `> ) REST1 ) BODY $` | `> ) ( ( ( CONT ) 1 - ) …` | Casa: `>` |
| 156 | `) REST1 ) BODY $` | `) ( ( ( CONT ) 1 - ) CONT …` | Casa: `)` |
| 157 | `REST1 ) BODY $` | `( ( ( CONT ) 1 - ) CONT ) …` | Expande: `REST1` → `ITEM REST2` |
| 158 | `ITEM REST2 ) BODY $` | `( ( ( CONT ) 1 - ) CONT ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 159 | `( EXPR_BODY ) REST2 ) BODY $` | `( ( ( CONT ) 1 - ) CONT ) …` | Casa: `(` |
| 160 | `EXPR_BODY ) REST2 ) BODY $` | `( ( CONT ) 1 - ) CONT ) WHILE …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 161 | `ITEM REST1 ) REST2 ) BODY $` | `( ( CONT ) 1 - ) CONT ) WHILE …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 162 | `( EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( ( CONT ) 1 - ) CONT ) WHILE …` | Casa: `(` |
| 163 | `EXPR_BODY ) REST1 ) REST2 ) BODY $` | `( CONT ) 1 - ) CONT ) WHILE ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 164 | `ITEM REST1 ) REST1 ) REST2 ) BODY $` | `( CONT ) 1 - ) CONT ) WHILE ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 165 | `( EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `( CONT ) 1 - ) CONT ) WHILE ) …` | Casa: `(` |
| 166 | `EXPR_BODY ) REST1 ) REST1 ) REST2 ) BODY $` | `CONT ) 1 - ) CONT ) WHILE ) ( …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 167 | `ITEM REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `CONT ) 1 - ) CONT ) WHILE ) ( …` | Expande: `ITEM` → `ident` |
| 168 | `ident REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `CONT ) 1 - ) CONT ) WHILE ) ( …` | Casa: `ident` |
| 169 | `REST1 ) REST1 ) REST1 ) REST2 ) BODY $` | `) 1 - ) CONT ) WHILE ) ( ( …` | Expande: `REST1` → `ε` |
| 170 | `) REST1 ) REST1 ) REST2 ) BODY $` | `) 1 - ) CONT ) WHILE ) ( ( …` | Casa: `)` |
| 171 | `REST1 ) REST1 ) REST2 ) BODY $` | `1 - ) CONT ) WHILE ) ( ( ( …` | Expande: `REST1` → `ITEM REST2` |
| 172 | `ITEM REST2 ) REST1 ) REST2 ) BODY $` | `1 - ) CONT ) WHILE ) ( ( ( …` | Expande: `ITEM` → `numero` |
| 173 | `numero REST2 ) REST1 ) REST2 ) BODY $` | `1 - ) CONT ) WHILE ) ( ( ( …` | Casa: `numero` |
| 174 | `REST2 ) REST1 ) REST2 ) BODY $` | `- ) CONT ) WHILE ) ( ( ( CONT …` | Expande: `REST2` → `BINOP` |
| 175 | `BINOP ) REST1 ) REST2 ) BODY $` | `- ) CONT ) WHILE ) ( ( ( CONT …` | Expande: `BINOP` → `-` |
| 176 | `- ) REST1 ) REST2 ) BODY $` | `- ) CONT ) WHILE ) ( ( ( CONT …` | Casa: `-` |
| 177 | `) REST1 ) REST2 ) BODY $` | `) CONT ) WHILE ) ( ( ( CONT ) …` | Casa: `)` |
| 178 | `REST1 ) REST2 ) BODY $` | `CONT ) WHILE ) ( ( ( CONT ) 0 …` | Expande: `REST1` → `ITEM REST2` |
| 179 | `ITEM REST2 ) REST2 ) BODY $` | `CONT ) WHILE ) ( ( ( CONT ) 0 …` | Expande: `ITEM` → `ident` |
| 180 | `ident REST2 ) REST2 ) BODY $` | `CONT ) WHILE ) ( ( ( CONT ) 0 …` | Casa: `ident` |
| 181 | `REST2 ) REST2 ) BODY $` | `) WHILE ) ( ( ( CONT ) 0 == …` | Expande: `REST2` → `ε` |
| 182 | `) REST2 ) BODY $` | `) WHILE ) ( ( ( CONT ) 0 == …` | Casa: `)` |
| 183 | `REST2 ) BODY $` | `WHILE ) ( ( ( CONT ) 0 == ) …` | Expande: `REST2` → `KW_CTRL3` |
| 184 | `KW_CTRL3 ) BODY $` | `WHILE ) ( ( ( CONT ) 0 == ) …` | Expande: `KW_CTRL3` → `while` |
| 185 | `while ) BODY $` | `WHILE ) ( ( ( CONT ) 0 == ) …` | Casa: `while` |
| 186 | `) BODY $` | `) ( ( ( CONT ) 0 == ) ( …` | Casa: `)` |
| 187 | `BODY $` | `( ( ( CONT ) 0 == ) ( 42 …` | Expande: `BODY` → `( BODY_TAIL` |
| 188 | `( BODY_TAIL $` | `( ( ( CONT ) 0 == ) ( 42 …` | Casa: `(` |
| 189 | `BODY_TAIL $` | `( ( CONT ) 0 == ) ( 42 RESULT …` | Expande: `BODY_TAIL` → `EXPR_BODY ) BODY` |
| 190 | `EXPR_BODY ) BODY $` | `( ( CONT ) 0 == ) ( 42 RESULT …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 191 | `ITEM REST1 ) BODY $` | `( ( CONT ) 0 == ) ( 42 RESULT …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 192 | `( EXPR_BODY ) REST1 ) BODY $` | `( ( CONT ) 0 == ) ( 42 RESULT …` | Casa: `(` |
| 193 | `EXPR_BODY ) REST1 ) BODY $` | `( CONT ) 0 == ) ( 42 RESULT ) …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 194 | `ITEM REST1 ) REST1 ) BODY $` | `( CONT ) 0 == ) ( 42 RESULT ) …` | Expande: `ITEM` → `( EXPR_BODY )` |
| 195 | `( EXPR_BODY ) REST1 ) REST1 ) BODY $` | `( CONT ) 0 == ) ( 42 RESULT ) …` | Casa: `(` |
| 196 | `EXPR_BODY ) REST1 ) REST1 ) BODY $` | `CONT ) 0 == ) ( 42 RESULT ) IF …` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 197 | `ITEM REST1 ) REST1 ) REST1 ) BODY $` | `CONT ) 0 == ) ( 42 RESULT ) IF …` | Expande: `ITEM` → `ident` |
| 198 | `ident REST1 ) REST1 ) REST1 ) BODY $` | `CONT ) 0 == ) ( 42 RESULT ) IF …` | Casa: `ident` |
| 199 | `REST1 ) REST1 ) REST1 ) BODY $` | `) 0 == ) ( 42 RESULT ) IF ) …` | Expande: `REST1` → `ε` |
| 200 | `) REST1 ) REST1 ) BODY $` | `) 0 == ) ( 42 RESULT ) IF ) …` | Casa: `)` |
| 201 | `REST1 ) REST1 ) BODY $` | `0 == ) ( 42 RESULT ) IF ) ( …` | Expande: `REST1` → `ITEM REST2` |
| 202 | `ITEM REST2 ) REST1 ) BODY $` | `0 == ) ( 42 RESULT ) IF ) ( …` | Expande: `ITEM` → `numero` |
| 203 | `numero REST2 ) REST1 ) BODY $` | `0 == ) ( 42 RESULT ) IF ) ( …` | Casa: `numero` |
| 204 | `REST2 ) REST1 ) BODY $` | `== ) ( 42 RESULT ) IF ) ( END …` | Expande: `REST2` → `BINOP` |
| 205 | `BINOP ) REST1 ) BODY $` | `== ) ( 42 RESULT ) IF ) ( END …` | Expande: `BINOP` → `==` |
| 206 | `== ) REST1 ) BODY $` | `== ) ( 42 RESULT ) IF ) ( END …` | Casa: `==` |
| 207 | `) REST1 ) BODY $` | `) ( 42 RESULT ) IF ) ( END )` | Casa: `)` |
| 208 | `REST1 ) BODY $` | `( 42 RESULT ) IF ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 209 | `ITEM REST2 ) BODY $` | `( 42 RESULT ) IF ) ( END )` | Expande: `ITEM` → `( EXPR_BODY )` |
| 210 | `( EXPR_BODY ) REST2 ) BODY $` | `( 42 RESULT ) IF ) ( END )` | Casa: `(` |
| 211 | `EXPR_BODY ) REST2 ) BODY $` | `42 RESULT ) IF ) ( END )` | Expande: `EXPR_BODY` → `ITEM REST1` |
| 212 | `ITEM REST1 ) REST2 ) BODY $` | `42 RESULT ) IF ) ( END )` | Expande: `ITEM` → `numero` |
| 213 | `numero REST1 ) REST2 ) BODY $` | `42 RESULT ) IF ) ( END )` | Casa: `numero` |
| 214 | `REST1 ) REST2 ) BODY $` | `RESULT ) IF ) ( END )` | Expande: `REST1` → `ITEM REST2` |
| 215 | `ITEM REST2 ) REST2 ) BODY $` | `RESULT ) IF ) ( END )` | Expande: `ITEM` → `ident` |
| 216 | `ident REST2 ) REST2 ) BODY $` | `RESULT ) IF ) ( END )` | Casa: `ident` |
| 217 | `REST2 ) REST2 ) BODY $` | `) IF ) ( END )` | Expande: `REST2` → `ε` |
| 218 | `) REST2 ) BODY $` | `) IF ) ( END )` | Casa: `)` |
| 219 | `REST2 ) BODY $` | `IF ) ( END )` | Expande: `REST2` → `KW_CTRL3` |
| 220 | `KW_CTRL3 ) BODY $` | `IF ) ( END )` | Expande: `KW_CTRL3` → `if` |
| 221 | `if ) BODY $` | `IF ) ( END )` | Casa: `if` |
| 222 | `) BODY $` | `) ( END )` | Casa: `)` |
| 223 | `BODY $` | `( END )` | Expande: `BODY` → `( BODY_TAIL` |
| 224 | `( BODY_TAIL $` | `( END )` | Casa: `(` |
| 225 | `BODY_TAIL $` | `END )` | Expande: `BODY_TAIL` → `end )` |
| 226 | `end ) $` | `END )` | Casa: `end` |
| 227 | `) $` | `)` | Casa: `)` |
| 228 | `$` | `$` | Casa: `$` |
