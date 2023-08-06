/*
 * Test programm for msp430.asm.cpp, msp430.asm.as and msp430.asm.ld
 */
#include "msp430x11x1.h"

.data

var1:   .skip  2

.text

main:
        mov    #WDTPW|WDTHOLD, &WDTCTL
        bis.b  #BIT1, &P1DIR
        clr.b  &P1OUT

l1:     xor.b  #BIT1, &P1OUT
        mov    #0xdfff, R13
l2:     dec    R13
        jnz    l2
        jmp    l1

