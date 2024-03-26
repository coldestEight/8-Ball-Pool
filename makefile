all: libphylib.so _phylib.so

phylib.o: phylib.c
	clang -Wall -pedantic -std=c99 -fPIC -c phylib.c -o phylib.o

libphylib.so: phylib.o
	clang -shared -o libphylib.so phylib.o -lm

phylib_wrap.c: phylib.i
	swig -python phylib.i

phylib_wrap.o: phylib_wrap.c
	clang -Wall -pedantic -std=c99 -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so: phylib_wrap.o
	clang -Wall -pedantic -std=c99 -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so

clean:
	rm *.o *.so phylib_wrap.c

svg:
	rm *.svg