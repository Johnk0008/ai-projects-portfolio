CC = gcc
CFLAGS = -Wall -Wextra -std=c99
TARGET = calculator
SOURCE = calculator.c

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCE)

clean:
	rm -f $(TARGET)

run: $(TARGET)
	./$(TARGET)

.PHONY: all clean run