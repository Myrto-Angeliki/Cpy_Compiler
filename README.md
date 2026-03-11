# Cpy_Compiler
A Compiler written in Python that converts a program written in a custom language to RISC-V assembly.<br>

### In /docs 
there are:
- images of the **FSM** of the language
- images of the **class diagram** of the *symbols table* classes
- a **.txt** file of the RARS output after assembling and running the **/assembly/final.asm** (produced after compiling **/cpy_programs/default_test.cpy**)
- a **.txt** file that contains the grammar of the language
<br><br>

### In /cpy_programs 
there are different programs written in **Cpy**. Some have names based on the compiler errors they produce.
<br><br>

### In **/src** 
there is the source code of the compiler. After compiling a program, two additional files are produced besides the the assembly file, that contain a visiual representation of the intermediate code and the symbols table. Those are **/src/intermediate/intermediate.int** and **/src/sym_table/symbols_table.sym**
<br><br><br>

## Requirements

- **Python 3.10 | Other Python versions could also work but 3.10 was used here**
- **RARS 1.5 or other RISC-V assembler and runtime simulator**

## To run the project
  1. Clone the repository:<br>
    ```
    git clone https://github.com/Myrto-Angeliki/Cpy_Compiler.git
    ```<br><br>
  2. Change directory to **/src**. <br><br>
  3. If you want to compile the default **.cpy** file, open a terminal and then type the following command:<br>
  ```> python parser.py``` <br><br>
  4. If you want to compile one of the other files inside **/cpy_programs**, type the following while stiil being inside the **/src** directory:<br>
  ```> python parser.py ..\cpy_programs\another_file.cpy``` <br>
  or <br>
  ```> python parser.py ../cpy_programs/another_file.cpy``` <br> depending on yous operating system,
  where *another_file.cpy* could be any of the files found inside **/cpy_programs**. <br><br>
5. To compile a different file than the ones provided inside **/cpy_programs**, open a terminal and then type the following command:<br>
 ```> python parser.py absolute_or_relative_file_path``` <br>
  or <br>
  ```> python parser.py absolute_or_relative_file_path``` <br> depending on yous operating system. <br><br>
