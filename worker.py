# Fatih Demir 2020400093
# Eymen Esad Çeliktürk 2020400165
# Group id : 18
# activate mpi
from mpi4py import MPI
import numpy as np

#Initilazing MPI environment
worker_comm = MPI.Comm.Get_parent()

size = worker_comm.Get_size()
spawned_rank = worker_comm.Get_rank()

# string operations
def enhance(product):
    
    return product[0] + product + product[-1]

def reverse(product):
    return product[::-1]

def chop(product):
    if len(product) > 1:
        return product[:-1]
    else:
        return product

def trim(product):
    if len(product) > 2:
        return product[1:-1]
    else:
        return product

def split(product):
    length = len(product)
    if length > 1:
        if length % 2 == 0:
            middle = length // 2
        else:
            middle = length // 2 + 1
        return product[:middle]
    else:
        return product

# get the number of cycles, maintenance threshold and wear factors from the main control room
num_cycles = worker_comm.recv(source = 0, tag = 7)
maintenance_threshold = worker_comm.recv(source = 0, tag = 6)
wear_factors = worker_comm.recv(source = 0, tag = 9)

wear = 0

for y in range(num_cycles):

    if spawned_rank != 0:

        #all the other nodes take the node from the master node
        
        
        input_data = worker_comm.recv(source = 0, tag = 1)
        id = worker_comm.recv(source = 0, tag = 5)

        result_data = ""


        if id == 1:
            result_data  = enhance(input_data)
        elif id == 2:
            result_data = reverse(input_data)
        elif id == 3:
            result_data = chop(input_data)
        elif id == 4:
            result_data = trim(input_data)
        elif id == 5:
            result_data = split(input_data)

        # Calculate wear based on the operation
        wear += wear_factors[id-1]  # Adjust index for wear_factors list

        # Check for maintenance need
        if wear >= maintenance_threshold:
            #print(f"Worker {spawned_rank+1} is sending {wear} message to the main control room")
            maintenance_cost = (wear - maintenance_threshold + 1) * wear_factors[id-1]
            maintenance_message = f"{spawned_rank+1}-{maintenance_cost}-{y+1}"
            # Send maintenance message to the main control room (non-blocking)
            requ = worker_comm.isend(maintenance_message, dest=0, tag=8)
            # print debugging to see isend has worked   
           
            requ.wait()  # Ensure the message is sent
            wear = 0  # Reset wear after maintenance
        
        #print("worker rank: ", spawned_rank, "calculated result data: ", result_data)
        worker_comm.send(result_data, dest = 0, tag = 2)

        