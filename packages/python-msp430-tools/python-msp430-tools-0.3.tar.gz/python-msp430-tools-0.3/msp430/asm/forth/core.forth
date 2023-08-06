( Core definitions for the cross compiler
  for Forth -> MSP430 assembler.

  vi:ft=forth 
)

INCLUDE _asm_snippets.forth

CODE ABORT
    ." \t mov \x23 .param_stack_end, TOS \n "
    ." \t mov \x23 .return_stack_end, RTOS \n "
    ." \t mov \x23 thread, IP \n "
    NEXT
END-CODE

CODE DOCOL
    ." \t decd RTOS       ; prepare to push on return stack \n "
    ." \t mov IP, 0(RTOS) ; save IP on return stack \n "
    ." \t mov -2(IP), IP  ; get where we are now \n "
    ." \t incd IP         ; jump over 'jmp DOCOL' \n "
    NEXT
END-CODE

CODE EXIT
    ." \t mov @RTOS+, IP  ; get last position from return stack \n "
    NEXT
END-CODE

( Get additional library functions )
INCLUDE _builtins.forth
INCLUDE _memory.forth
INCLUDE _helpers.forth


( Generate init code for forth runtime and core words )
: CROSS-COMPILE-CORE ( - )
    LINE
    HASH ." include < " MCU . ." .h> " NL
    NL
    LINE
    ." ; Assign registers. \n "
    DEFINE ." TOS R4 " NL
    DEFINE ." RTOS  R5 " NL
    DEFINE ." IP  R6 " NL
    DEFINE ." W  R7 " NL
    NL
    LINE
    ." ; Memory for the stacks. \n "
    ." .bss \n "
    ." param_stack: .skip 2*32 \n "
    ." .param_stack_end:\n "
    ." return_stack: .skip 2*16 \n "
    ." .return_stack_end: \n "
    NL
    LINE
    ." ; Main entry point. \n "
    ." .text \n "
    ." main: \n "
        ." \t mov \x23 WDTPW|WDTHOLD, &WDTCTL \n "
        ." \t jmp ABORT \n "
    NL
    LINE
    ." ; Initial thread that is run. Hardcoded init-main-loop. \n "
    ." thread: \n "
    ." \t .word INIT \n "
    ." \t .word MAIN \n "
    ." \t .word ABORT \n "
    NL

    ( output important runtime core parts )
    CROSS-COMPILE ABORT
    CROSS-COMPILE DOCOL
    CROSS-COMPILE EXIT
;

