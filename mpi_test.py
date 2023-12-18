import time
from mpi4py import MPI

#Initilazing MPI environment
# mpiexec -n 2 python mpi_test.py

comm = MPI.COMM_WORLD


size = comm.Get_size()
rank = comm.Get_rank()

data = [3,6,9]
if rank == 0:
    data_0 = data[0]
    comm.send(data_0, dest = 1)
    comm.send(data_0, dest = 2)

    print(rank, data)
    #data_0 = comm.recv(source = 1)
    print(rank, data_0)
    data[0] = data_0
    print(rank, data)

if rank == 1:
    data_0 = comm.recv(source = 0)
    print(rank, data_0)
    data_0 = 2*data_0
    comm.send(data_0, dest = 2)
    print(rank, data_0)
    data_2 = data[2]
    print(rank, data_2)

if rank ==2:
    da = comm.recv(source = 0)
    print("-------------------")
    print(rank, da)    
    print("-------------------")
    nda = comm.recv(source = 1)
    print(rank, nda)

print("Hello, World!")
