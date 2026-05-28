# Árvore Sintática Atribuída

Cada nó traz `tipo_inferido` (Etapa 3) e `meta_asm` (Etapa 4).

```text
stmt #1
  binary  : tipo=int  [instr=ADD, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='10'
    │    ├─ valor:
    │    │  <'10'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='3'
    │    ├─ valor:
    │    │  <'3'>
stmt #2
  binary  : tipo=int  [instr=SUB, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='8'
    │    ├─ valor:
    │    │  <'8'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='3'
    │    ├─ valor:
    │    │  <'3'>
stmt #3
  binary  : tipo=int  [instr=MUL, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='4'
    │    ├─ valor:
    │    │  <'4'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='3'
    │    ├─ valor:
    │    │  <'3'>
stmt #4
  binary  : tipo=int  [instr=BL __op_idiv, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='10'
    │    ├─ valor:
    │    │  <'10'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='2'
    │    ├─ valor:
    │    │  <'2'>
stmt #5
  binary  : tipo=int  [instr=BL __op_mod, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='10'
    │    ├─ valor:
    │    │  <'10'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='3'
    │    ├─ valor:
    │    │  <'3'>
stmt #6
  binary  : tipo=int  [instr=BL __op_pow, reg=R0]
    ├─ esq:
    │  number  : tipo=int  [reg=R0]  valor='2'
    │    ├─ valor:
    │    │  <'2'>
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='5'
    │    ├─ valor:
    │    │  <'5'>
stmt #7
  binary  : tipo=real  [instr=VDIV.F64, reg=D0]
    ├─ esq:
    │  number  : tipo=real  [reg=D0]  valor='7.5'
    │    ├─ valor:
    │    │  <'7.5'>
    ├─ dir:
    │  number  : tipo=real  [reg=D0]  valor='2.5'
    │    ├─ valor:
    │    │  <'2.5'>
stmt #8
  mem_write  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    ├─ valor:
    │  number  : tipo=int  [reg=R0]  valor='5'
    │    ├─ valor:
    │    │  <'5'>
stmt #9
  binary  : tipo=int  [instr=MUL, reg=R0]
    ├─ esq:
    │  mem_read  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    ├─ dir:
    │  number  : tipo=int  [reg=R0]  valor='2'
    │    ├─ valor:
    │    │  <'2'>
stmt #10
  res_ref  : tipo=int  [reg=R0]  linhas_atras=1
stmt #11
  while  : tipo=indef  [reg=D0, L_ini=L_while_i_1, L_fim=L_while_f_2]
    ├─ cond:
    │  binary  : tipo=bool  [instr=CMP+MOV, reg=R0]
    │    ├─ esq:
    │    │  mem_read  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    │    ├─ dir:
    │    │  number  : tipo=int  [reg=R0]  valor='0'
    │    │    ├─ valor:
    │    │    │  <'0'>
    ├─ body:
    │  mem_write  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    │    ├─ valor:
    │    │  binary  : tipo=int  [instr=SUB, reg=R0]
    │    │    ├─ esq:
    │    │    │  mem_read  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    │    │    ├─ dir:
    │    │    │  number  : tipo=int  [reg=R0]  valor='1'
    │    │    │    ├─ valor:
    │    │    │    │  <'1'>
stmt #12
  if  : tipo=int  [reg=R0, L_fim=L_if_fim_3]
    ├─ cond:
    │  binary  : tipo=bool  [instr=CMP+MOV, reg=R0]
    │    ├─ esq:
    │    │  mem_read  : tipo=int  [reg=R0, mem=mem_cont]  nome='CONT'  → sim(tipo=int, def=22)
    │    ├─ dir:
    │    │  number  : tipo=int  [reg=R0]  valor='0'
    │    │    ├─ valor:
    │    │    │  <'0'>
    ├─ then_block:
    │  mem_write  : tipo=int  [reg=R0, mem=mem_result]  nome='RESULT'  → sim(tipo=int, def=30)
    │    ├─ valor:
    │    │  number  : tipo=int  [reg=R0]  valor='42'
    │    │    ├─ valor:
    │    │    │  <'42'>
```
