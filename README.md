# rayTrace

To make necessary input files: run make_inputfile.py \n
Edits can be made to the variables in lines 44-53 of this script to change input files. \n

To run python version of rayTrace: run rt_run.py [inputfile] [outputfile] \n
You can also just run on default inputs: run rt_run.py \n

rt_run.py run functions in rt_function.  These must be in the same foulder. \n

To run fortran version first move .inc and .h files into include folder. \n
Then compile: make or make all \n
Then ./rayTrace [inputfile] \n
