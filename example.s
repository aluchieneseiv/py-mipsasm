.data
a:
    .word 20
str:
    .asciiz "Hello world!"
.text
main:
    addu $a0, $0, $0
    li $s0, 0xffff
@0x20
my_loop:
    li $a2, 32800
    addi $a0, $a0, 1
    mov $a0, $a0
    mov $a1, 0($sp)
    mov 0($sp), $a1
    blt $a0, $s0, my_loop

@0x90
spim_test:
    lw $a0, 0($sp)
    addiu $a1, $sp, 4
    addiu $a2, $a1, 4
    sll $v0, $a0, 2
    addu $a2, $a2, $v0
    jal main
    la $ra, main
    nop