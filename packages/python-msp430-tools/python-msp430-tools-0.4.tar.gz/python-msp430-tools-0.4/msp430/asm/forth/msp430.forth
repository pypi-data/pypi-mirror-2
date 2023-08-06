( vi:ft=forth

  MSP430 specific low level operations.

  Copyright [C] 2011 Chris Liechti <cliechti@gmx.net>
  All Rights Reserved.
  Simplified BSD License [see LICENSE.txt for full text]
)

INCLUDE _interrupts.forth

( - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - )
( 8 bit memory operations )

CODE CRESET ( n adr - )
    TOS->R15
    TOS->R14
    ." \t bic.b R14, 0(R15) \n "
    ASM-NEXT
END-CODE

CODE CSET ( n adr - )
    TOS->R15
    TOS->R14
    ." \t bis.b R14, 0(R15) \n "
    ASM-NEXT
END-CODE

CODE CTOGGLE ( n adr - )
    TOS->R15
    TOS->R14
    ." \t xor.b R14, 0(R15) \n "
    ASM-NEXT
END-CODE

CODE CTESTBIT ( mask adr - bool )
    TOS->W
    ." \t bit.b @W, 0(SP) \n "
    ." \t jz  .cbit0 \n "
    ." \t mov \x23 -1, 0(SP) \n "       ( replace TOS w/ result )
    ." \t jmp .cbit2 \n "
    ." .cbit0:\n "
    ." \t mov \x23 0, 0(SP) \n "        ( replace TOS w/ result )
    ." .cbit2:\n "
    ASM-NEXT
END-CODE

( - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - )
( 16 bit memory operations )

CODE RESET ( n adr - )
    TOS->W
    ." \t bic @SP+, 0(W) \n "
    ASM-NEXT
END-CODE

CODE SET ( n adr - )
    TOS->W
    ." \t bis @SP+, 0(W) \n "
    ASM-NEXT
END-CODE

CODE TOGGLE ( n adr - )
    TOS->W
    ." \t xor @SP+, 0(W) \n "
    ASM-NEXT
END-CODE

CODE TESTBIT ( mask adr - bool )
    TOS->W
    ." \t bit @W, 0(SP) \n "
    ." \t jz  .bit0 \n "
    ." \t mov \x23 -1, 0(SP) \n "       ( replace TOS w/ result )
    ." \t jmp .bit2 \n "
    ." .bit0:\n"
    ." \t mov \x23 0, 0(SP) \n "        ( replace TOS w/ result )
    ." .bit2:\n"
    ASM-NEXT
END-CODE

( - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - )

CODE 1+ ( n - n )
    ." \t inc 0(SP) \n "
    ASM-NEXT
END-CODE

CODE 2+ ( n - n )
    ." \t incd 0(SP) \n "
    ASM-NEXT
END-CODE

CODE 4+ ( n - n )
    ." \t add \x23 4, 0(SP) \n "
    ASM-NEXT
END-CODE


CODE 1- ( n - n )
    ." \t dec 0(SP) \n "
    ASM-NEXT
END-CODE

CODE 2- ( n - n )
    ." \t decd 0(SP) \n "
    ASM-NEXT
END-CODE

CODE 4- ( n - n )
    ." \t sub \x23 4, 0(SP) \n "
    ASM-NEXT
END-CODE

( - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - )
( Miscellaneous functions )

( Simple busy-wait type delay. 3 cycles/loop. )
CODE DELAY ( n - )
    TOS->W
    ." .loop: \t dec W \n "
    ." \t jnz .loop \n "
    ASM-NEXT
END-CODE

( - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - )
( custom extensions )


( Swap high/low byte )
CODE SWPB ( n - n )
    ." \t swpb 0(SP) \n "
    ASM-NEXT
END-CODE

( Sign extend )
CODE SIGN-EXTEND ( n - n )
    ." \t sxt 0(SP) \n "
    ASM-NEXT
END-CODE

( Move byte from memory to memory )
CODE C@! ( src-adr dst-adr - )
    TOS->R15                        ( pop destination address )
    TOS->R14                        ( pop source address )
    ." \t mov.b @R14, 0(R15) \n "   ( copy value from src to dst )
    ASM-NEXT
END-CODE

( Move word from memory to memory )
CODE @! ( src-adr dst-adr - )
    TOS->R15                        ( pop destination address )
    TOS->R14                        ( pop source address )
    ." \t mov @R14, 0(R15) \n "     ( copy value from src to dst )
    ASM-NEXT
END-CODE


( NOP )
CODE NOP ( - )
    ." \t nop\n "
    ASM-NEXT
END-CODE

( Enable interrupts )
CODE EINT ( - )
    ." \t eint\n "
    ASM-NEXT
END-CODE

( Disable interrupts )
CODE DINT ( - )
    ." \t dint\n "
    ASM-NEXT
END-CODE

( Enter low-power mode. )
CODE ENTER-LPM0 ( n - )
    ." \t bis \x23 LPM0, SR\n "
    ASM-NEXT
END-CODE

( Enter low-power mode LPM1. )
CODE ENTER-LPM1 ( n - )
    ." \t bis \x23 LPM2, SR\n "
    ASM-NEXT
END-CODE

( Enter low-power mode LMP2. )
CODE ENTER-LPM2 ( n - )
    ." \t bis \x23 LPM3, SR\n "
    ASM-NEXT
END-CODE

( Enter low-power mode LPM3. )
CODE ENTER-LPM3 ( n - )
    ." \t bis \x23 LPM3, SR\n "
    ASM-NEXT
END-CODE

( Enter low-power mode LPM4. )
CODE ENTER-LPM4 ( n - )
    ." \t bis \x23 LPM4, SR\n "
    ASM-NEXT
END-CODE

