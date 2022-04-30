SIC/XE ASSEMBLER THAT SUPPORTS PROGRAM RELOCATION AND SYMBOL DEFINING STATEMENTS

The Objective of the project is to implement a version of a two-pass SIC/XE assembler: Pass 1 and Pass 2. The Assembler we implemented includes 
all the SIC/XE instructions and supports all four formats viz. 1, 2, 3, 4 addressing modes as well as program relocation. It also support symbol 
defining statements.

Input to assembler- Assembler source program using the instruction set of SIC/XE. 
Output- Assembler will generate the following files as output-

1. Pass 1 will generate a Symbol Table (implemented using a Python Dictionary).
2. Pass 1 will also generate Intermediate File (text file) for the Pass 2.
3. Pass 2 will generate an object program including following types of record: Header (H), Text (T), Modification (M) and End (E).


Steps to compile and run the program:-
1. Open the terminal.
2. Change the directory to the SIC-XE-Assembler folder.
3. Run the command – python3 Assembler.py “input1.txt”.
4. Intermediate file will be generated in the directory as “Intermediate.txt” and object program will be generated as “Object_Program.txt”.

