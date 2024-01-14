# Project Title

## Description

This project uses the Message Passing Interface (MPI) for parallel computing. It is designed to [describe what your project does in detail, including the problems it solves and the methods it uses].

## Getting Started

### Dependencies

This project depends on the following libraries and tools:

- MPI: This is used for parallel computing. You can use any MPI implementation, such as OpenMPI or MPICH.
- C/C++ compiler: This is needed to compile the source code. GCC is recommended.

### Installing

Follow these steps to set up a development environment:

1. Install MPI. If you're using Ubuntu, you can do this with `sudo apt install mpich`.
2. Install a C/C++ compiler. If you're using Ubuntu, you can do this with `sudo apt install build-essential`.
3. Clone this repository with `git clone [your-repo-url]`.
4. Navigate to the project directory with `cd [your-project-directory]`.
5. Compile the source code with `mpicc -o output-file source-file.c`.

### Executing program

To run the program, use the following command:

```bash
mpirun -np 4 ./output-file