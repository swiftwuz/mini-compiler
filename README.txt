//NAME: NANA KOJO EWUSIE
//INDEX NUMBER: 040118156

To execute the compiler, open your terminal and go the compiler's path.
To allow file access and run the executable, type 'chmod a+x 341fe'.

The compiler takes four flags:

	-h > prints a list of the flags available and the syntax for running the program. 

	-s > prints the line number and token type. 

	-r > prints in readable format the intermediate representation.    
 
	-p > reports either a success or failure on the intermediate representation and lists all the errors in the input file. 

	-q > quits the command line

	./341fe [flag] filename.txt << is the command you type to run the program. 

Replace '[flag]' with any of the available flags. 
Replace <filename.txt> with the input file. 

I added an ILOC that is handled correctly by the compiler. 
Run {./341fe [flag] ILOC_fail.txt} or {./341fe [flag] ILOC_pass.txt} for fail and pass respectively. 

As an alternative to running the source code, you can type 'python3 341fe.py [flag] filename.txt' 

NB: depending on your python version, you can omit the [version number] in the command if python2.7 is your default python version. However, I strongly recommend you update your python as 2.7 is out of production. 

Also, the shell script (or unix executable) can be changed to '341fe.sh' but then you'd have to run the syntax like this {./341fe.sh [flag] filename.txt} after giving the file permission. 