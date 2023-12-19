# activate mpi
# mpiexec -n 4 python main.py
import subprocess
from mpi4py import MPI
import numpy as np

#Initilazing MPI environment
worker_comm = MPI.Comm.Get_parent()


size = worker_comm.Get_size()
spawned_rank = worker_comm.Get_rank()



""" class MachineNode:
    def __init__(self, machine_id, parent=None, current_operation_id=None):
        self.machine_id = machine_id
        self.parent = parent
        self.children = []
        self.current_operation_id = current_operation_id
        self.first_input = None

    def add_child(self, child):
        self.children.append(child)

    #for odd machine id's it is reverse -> trim -> reverse ...
    #for even machine id's it is split -> chop -> enhance ...
    def change_operation(self):
        if (self.machine_id+1) % 2 == 0:
            if self.current_operation_id == 4:
                self.current_operation_id = 2
            elif self.current_operation_id == 2:
                self.current_operation_id = 4
        
        else:
            if self.current_operation_id == 5:
                self.current_operation_id = 3
            elif self.current_operation_id == 3:
                self.current_operation_id = 1
            elif self.current_operation_id == 1:
                self.current_operation_id = 5 """



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

# get the number of cycles from the main room
num_cycles = worker_comm.recv(source = 0, tag = 7)

for y in range(num_cycles):

    if spawned_rank != 0:

        #all the other nodes take the node from the master node
        #for j in range(num_machines-1,0,-1):
        #if spawned_rank == j:
        #print("worker rank: ", spawned_rank)
        input_data = worker_comm.recv(source = 0, tag = 1)
        id = worker_comm.recv(source = 0, tag = 5)

        #print("worker rank: ", spawned_rank, "input data: ", input_data, "id: ", id)
        #for m in range(num_cycles):
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

        #print("worker rank: ", spawned_rank, "calculated result data: ", result_data)
        worker_comm.send(result_data, dest = 0, tag = 2)

"""  else:
    coming_data = ""
    #first sort the children list
    node.children.sort(key = lambda x: x.machine_id)
    for ii in range(len(node.children)):
        coming_data += worker_comm.recv(source = node.children[ii].machine_id-1, tag = 2)
    #print("coming data and rank: ", rank, coming_data)
    
    if node.current_operation_id == 1:
        result_data  = enhance(coming_data)
    elif node.current_operation_id == 2:
        result_data = reverse(coming_data)
    elif node.current_operation_id == 3:
        result_data = chop(coming_data)
    elif node.current_operation_id == 4:
        result_data = trim(coming_data)
    elif node.current_operation_id == 5:
        result_data = split(coming_data) """

#if node.parent != None:
#print(rank, result_data)
#print("id:", node.current_operation_id)

#print("id after:", node.current_operation_id)

        



            
