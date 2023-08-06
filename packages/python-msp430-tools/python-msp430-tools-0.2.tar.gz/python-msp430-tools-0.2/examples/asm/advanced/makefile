
PYTHONPATH = ../../..
export PYTHONPATH

#~ CPP = cpp
#~ CPPFLAGS = -E -w -I . -I /opt/mspgcc/msp430/include -D_GNU_ASSEMBLER_
CPP = python -m msp430.asm.cpp
CPPFLAGS = -I /opt/mspgcc/msp430/include -D_GNU_ASSEMBLER_

AS = python -m msp430.asm.as
ASFLAGS = -x -v -D

LD = python -m msp430.asm.ld
LDFLAGS = -v -D

.PHONY: clean all listing download

all: clean led.txt

led.o4: led.S
startup.o4: startup.S
intvec.o4: intvec.S

led.txt: startup.o4 led.o4 intvec.o4
	${LD} ${LDFLAGS} -o $@ --mapfile $@.map $^
	cat $@

led.a43: led.txt
	titext2ihex -o $@ $<

listing: led.a43
	msp430-objdump -D -m msp:11 $^

%o4: %S
	${CPP} ${CPPFLAGS} $< | ${AS} ${ASFLAGS} -o $@ -

download: led.txt
	msp430-jtag -e --no-close $^

clean:
	rm -f led.txt *.o4 led.a43
