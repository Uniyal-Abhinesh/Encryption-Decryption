CXX = g++
CXXFLAGS = -std=c++17 -g -Wall -I. -Isrc/app/encryptDecrypt -Isrc/app/fileHandling -Isrc/app/processes
LDFLAGS = 

MAIN_TARGET = encrypt_decrypt
CRYPTION_TARGET = cryption

MAIN_SRC = main.cpp \
           src/app/processes/ProcessManagement.cpp \
           src/app/fileHandling/IO.cpp \
           src/app/fileHandling/ReadEnv.cpp \
           src/app/encryptDecrypt/Cryption.cpp

CRYPTION_SRC = src/app/encryptDecrypt/CryptionMain.cpp \
               src/app/encryptDecrypt/Cryption.cpp \
               src/app/fileHandling/IO.cpp \
               src/app/fileHandling/ReadEnv.cpp

COMPAT_SRC = compat.c
COMPAT_OBJ = compat.o

MAIN_OBJ = $(MAIN_SRC:.cpp=.o)
CRYPTION_OBJ = $(CRYPTION_SRC:.cpp=.o)

all: $(MAIN_TARGET) $(CRYPTION_TARGET)

$(MAIN_TARGET): $(MAIN_OBJ) $(COMPAT_OBJ)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@

$(CRYPTION_TARGET): $(CRYPTION_OBJ) $(COMPAT_OBJ)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(COMPAT_OBJ): $(COMPAT_SRC)
	gcc -c $(COMPAT_SRC) -o $(COMPAT_OBJ)

clean:
	rm -f $(MAIN_OBJ) $(CRYPTION_OBJ) $(COMPAT_OBJ) $(MAIN_TARGET) $(CRYPTION_TARGET)

.PHONY: clean all