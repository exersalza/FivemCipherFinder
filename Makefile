CC = "g++"
CC_ARG = "-std=c++2a"

make:
	${CC} ${CC_ARG} src/main.cpp -o cipherfinder
	
rm:
	rm cipherfinder
	
install:
	sudo cp cipherfinder /bin/cipherfinder || echo "File can't be copied, did you run make?"