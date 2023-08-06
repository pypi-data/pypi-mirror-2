( vi:ft=forth

  Some assembler snippets that are commonly used.

  Copyright [C] 2011 Chris Liechti <cliechti@gmx.net>
  All Rights Reserved.
  Simplified BSD License [see LICENSE.txt for full text]
)

: BS     8 EMIT ;
: LF    10 EMIT ;
: CR    13 EMIT ;
: SPACE 32 EMIT ;
: HASH  35 EMIT ;

: DEFINE HASH ." define " SPACE ;

: ASM-NEXT ." \t br @IP+ \t; NEXT \n " ;
: ASM-DROP ." \t incd SP \t; DROP \n " ;

: TOS->R15 ." \t pop  R15 \n " ;
: TOS->R14 ." \t pop  R14 \n " ;
: R15->TOS ." \t push R15 \n " ;

: TOS->W   ." \t pop  W \n " ;
: W->TOS   ." \t push W \n " ;


