CC=gcc
CFLAGS=-g -Wall -Werror -pedantic -std=gnu99
TARGET=etovucca
SRCDIR=src
LIBDIR=lib
DEPS=Database.o libsqlite3.so

.PHONY: all clean initdb cgi

all: $(TARGET)

cgi: etovucca
		python3 -m http.server --cgi

etovucca: $(DEPS) $(SRCDIR)/RTBB.c
		$(CC) $(CFLAGS) -I $(LIBDIR) -o $@ $^ -L./ -lsqlite3

Database.o: $(SRCDIR)/Database.c 
		$(CC) $(CFLAGS) -I $(LIBDIR) -o $@ -c $^

libsqlite3.so: $(LIBDIR)/sqlite3.c
		$(CC) -shared -o $@ -fPIC $^ -ldl -pthread
		$(CC) -o sqlite3 $^ $(LIBDIR)/shell.c -ldl -pthread

clean:
		$(RM) $(TARGET) $(DEPS) sqlite3 *.o

initdb:
		echo .quit | ./sqlite3 -init setup.sql rtbb.sqlite3
