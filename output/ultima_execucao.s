@ =====================================================
@  Assembly gerado a partir da ÁRVORE SINTÁTICA ATRIBUÍDA
@  (Fase 3 — Etapa 5)
@  Tipos inferidos por statement de topo:
@    stmt #1: int
@    stmt #2: int
@    stmt #3: int
@    stmt #4: int
@    stmt #5: int
@    stmt #6: int
@    stmt #7: real
@    stmt #8: int
@    stmt #9: int
@    stmt #10: int
@    stmt #11: indef
@    stmt #12: int
@ =====================================================
.syntax unified
.cpu cortex-a9
.fpu vfpv3
.global _start

.text
_start:
    @ Expressão 1
    LDR r0, =const_0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=int + → ADD (ARM inteiro)
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    ADD r0, r0, r1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_0
    VSTR.F64 d0, [r0]
    @ Exibir resultado 1 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 2
    LDR r0, =const_2
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=int - → SUB (ARM inteiro)
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    SUB r0, r0, r1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_1
    VSTR.F64 d0, [r0]
    @ Exibir resultado 2 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 3
    LDR r0, =const_3
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=int * → MUL (ARM inteiro)
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    MUL r0, r0, r1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_2
    VSTR.F64 d0, [r0]
    @ Exibir resultado 3 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 4
    LDR r0, =const_0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ divisão inteira → BL __op_idiv
    BL __op_idiv
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_3
    VSTR.F64 d0, [r0]
    @ Exibir resultado 4 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 5
    LDR r0, =const_0
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_1
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ módulo inteiro → BL __op_mod
    BL __op_mod
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_4
    VSTR.F64 d0, [r0]
    @ Exibir resultado 5 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 6
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ potência (expoente int) → BL __op_pow
    BL __op_pow
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_5
    VSTR.F64 d0, [r0]
    @ Exibir resultado 6 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 7
    LDR r0, =const_6
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_7
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ divisão real → VDIV.F64
    VDIV.F64 d0, d0, d1
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_6
    VSTR.F64 d0, [r0]
    @ Exibir resultado 7 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 8
    LDR r0, =const_5
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =mem_cont
    VSTR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_7
    VSTR.F64 d0, [r0]
    @ Exibir resultado 8 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 9
    LDR r0, =mem_cont
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_4
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=int * → MUL (ARM inteiro)
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    MUL r0, r0, r1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_8
    VSTR.F64 d0, [r0]
    @ Exibir resultado 9 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 10
    LDR r0, =resultado_8
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_9
    VSTR.F64 d0, [r0]
    @ Exibir resultado 10 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 11
L_while_i_1:
    LDR r0, =mem_cont
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_8
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=bool (> int) → CMP + MOVGT
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    CMP r0, r1
    MOV r0, #0
    MOVGT r0, #1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =const_zero
    VLDR.F64 d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ L_while_f_2
    LDR r0, =mem_cont
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_9
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=int - → SUB (ARM inteiro)
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    SUB r0, r0, r1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =mem_cont
    VSTR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    B L_while_i_1
L_while_f_2:
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_10
    VSTR.F64 d0, [r0]
    @ Exibir resultado 11 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex
    @ Expressão 12
    LDR r0, =mem_cont
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    LDR r0, =const_8
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d1, r4, r5
    POP {r4, r5}
    VMOV d0, r4, r5
    @ tipo=bool (== int) → CMP + MOVEQ
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    CMP r0, r1
    MOV r0, #0
    MOVEQ r0, #1
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =const_zero
    VLDR.F64 d1, [r0]
    VCMP.F64 d0, d1
    VMRS APSR_nzcv, FPSCR
    BEQ L_if_fim_3
    LDR r0, =const_10
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =mem_result
    VSTR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
L_if_fim_3:
    LDR r0, =const_zero
    VLDR.F64 d0, [r0]
    VMOV r4, r5, d0
    PUSH {r4, r5}
    POP {r4, r5}
    VMOV d0, r4, r5
    LDR r0, =resultado_11
    VSTR.F64 d0, [r0]
    @ Exibir resultado 12 nos HEX displays
    VCVT.S32.F64 s0, d0
    VMOV r0, s0
    BL __exibir_hex

loop_final:
    B loop_final

__op_idiv:
    PUSH {lr}
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r0, s0
    VMOV r1, s2
    BL __sdiv32
    VMOV s0, r0
    VCVT.F64.S32 d0, s0
    POP {lr}
    BX lr

__op_mod:
    PUSH {r4, lr}
    VCVT.S32.F64 s0, d0
    VCVT.S32.F64 s2, d1
    VMOV r2, s0
    VMOV r3, s2
    MOV r0, r2
    MOV r1, r3
    BL __sdiv32
    MUL r4, r0, r3
    SUB r2, r2, r4
    VMOV s0, r2
    VCVT.F64.S32 d0, s0
    POP {r4, lr}
    BX lr

__op_pow:
    PUSH {lr}
    VCVT.S32.F64 s2, d1
    VMOV r3, s2
    CMP r3, #0
    BLE __pow_zero_ou_negativo
    VMOV.F64 d2, d0
    SUB r3, r3, #1
__pow_loop:
    CMP r3, #0
    BEQ __pow_done
    VMUL.F64 d2, d2, d0
    SUB r3, r3, #1
    B __pow_loop
__pow_done:
    VMOV.F64 d0, d2
    POP {lr}
    BX lr
__pow_zero_ou_negativo:
    LDR r0, =const_one
    VLDR.F64 d0, [r0]
    POP {lr}
    BX lr

__sdiv32:
    PUSH {r2, r3, r4, lr}
    CMP r1, #0
    BEQ __sdiv32_divzero
    MOV r2, #0
    CMP r0, #0
    RSBMI r0, r0, #0
    EORMI r2, r2, #1
    CMP r1, #0
    RSBMI r1, r1, #0
    EORMI r2, r2, #1
    MOV r3, #0
__sdiv32_loop:
    CMP r0, r1
    BLT __sdiv32_done
    SUB r0, r0, r1
    ADD r3, r3, #1
    B __sdiv32_loop
__sdiv32_done:
    CMP r2, #0
    RSBNE r3, r3, #0
    MOV r0, r3
    POP {r2, r3, r4, lr}
    BX lr
__sdiv32_divzero:
    MOV r0, #0
    POP {r2, r3, r4, lr}
    BX lr

__exibir_hex:
    PUSH {r1, r2, r3, r4, r5, r6, lr}
    LDR r1, =__hex_tabela
    LDR r6, =0xFF200020
    MOV r5, #0
    CMP r0, #0
    RSBMI r0, r0, #0
    MOVMI r5, #1
    MOV r4, #0
    MOV r2, #10
    BL __udiv_simples
    LDRB r3, [r1, r3]
    ORR r4, r4, r3
    MOV r2, #10
    BL __udiv_simples
    LDRB r3, [r1, r3]
    ORR r4, r4, r3, LSL #8
    MOV r2, #10
    BL __udiv_simples
    LDRB r3, [r1, r3]
    ORR r4, r4, r3, LSL #16
    CMP r5, #1
    MOVEQ r3, #0x40
    BEQ __exibir_hex_store
    MOV r2, #10
    BL __udiv_simples
    LDRB r3, [r1, r3]
    ORR r4, r4, r3, LSL #24
    B __exibir_hex_fim
__exibir_hex_store:
    ORR r4, r4, r3, LSL #24
__exibir_hex_fim:
    STR r4, [r6]
    POP {r1, r2, r3, r4, r5, r6, lr}
    BX lr

__udiv_simples:
    MOV r3, #0
__udiv_simples_loop:
    CMP r0, r2
    BLT __udiv_simples_done
    SUB r0, r0, r2
    ADD r3, r3, #1
    B __udiv_simples_loop
__udiv_simples_done:
    MOV r12, r0
    MOV r0, r3
    MOV r3, r12
    BX lr

.data
const_0: .double 10
const_1: .double 3
const_2: .double 8
const_3: .double 4
const_4: .double 2
const_5: .double 5
const_6: .double 7.5
const_7: .double 2.5
const_8: .double 0
const_9: .double 1
const_10: .double 42
const_zero: .double 0.0
const_one:  .double 1.0
mem_cont: .double 0.0
mem_result: .double 0.0
resultado_0: .double 0.0
resultado_1: .double 0.0
resultado_2: .double 0.0
resultado_3: .double 0.0
resultado_4: .double 0.0
resultado_5: .double 0.0
resultado_6: .double 0.0
resultado_7: .double 0.0
resultado_8: .double 0.0
resultado_9: .double 0.0
resultado_10: .double 0.0
resultado_11: .double 0.0

@ Tabela 7-segmentos (0-9) para display HEX
__hex_tabela:
    .byte 0x3F  @ 0
    .byte 0x06  @ 1
    .byte 0x5B  @ 2
    .byte 0x4F  @ 3
    .byte 0x66  @ 4
    .byte 0x6D  @ 5
    .byte 0x7D  @ 6
    .byte 0x07  @ 7
    .byte 0x7F  @ 8
    .byte 0x6F  @ 9
