.text

# provide a default interrupt handler, assign all interrupts as weak labels to
# this one
.weak vector_0,  vector_2,  vector_4,  vector_6,  vector_8
.weak vector_10, vector_12, vector_14, vector_16, vector_18
.weak vector_20, vector_22, vector_24, vector_26, vector_28
__default_interrupt_handler:
        reti

# define the interrupt handler table
.section .vectors
        .word  vector_0
        .word  vector_2
        .word  vector_4
        .word  vector_6
        .word  vector_8
        .word  vector_10
        .word  vector_12
        .word  vector_14
        .word  vector_16
        .word  vector_18
        .word  vector_20
        .word  vector_22
        .word  vector_24
        .word  vector_26
        .word  vector_28
        .word  vector_30

