; startup code. it initializes:
; - .data and .bss sections
; - stack pointer

.text

RESET:      mov    #_stack, SP

.init_data:
            mov     #_data_init_end-_data_init_start, R15
            tst     R15
            jz      .init_bss
.data_loop: dec     R15
            mov     _data_init_start(R15), _data_start(R15)
            jnz     .data_loop

.init_bss:
            mov     #_bss_end-_bss_start, R15
            tst     R15
            jz      .run
.bss_loop:  dec     R15
            clr     _bss_start(R15)
            jnz     .bss_loop

.run:       br     #main

