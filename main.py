# activate mpi
# mpiexec -n 4 python main.py
from mpi4py import MPI

#Initilazing MPI environment
comm = MPI.COMM_WORLD


size = comm.Get_size()
rank = comm.Get_rank()



class MachineNode:
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
                self.current_operation_id = 5


def read_input_file(file_path):
    global num_machines, num_cycles, wear_factors, maintenance_threshold, lines_list, nodes, node_dict, rootm, leaf_node_ids


    with open(file_path, 'r') as file:
        # Read the number of machines
        num_machines = int(file.readline().strip())

        # Read the number of production cycles
        num_cycles = int(file.readline().strip())

        # Read wear factors for each operation
        # in the order of enhance, reverse, chop, trim, split
        wear_factors = list(map(int, file.readline().split()))

        # Read the threshold value for maintenance
        maintenance_threshold = int(file.readline().strip())

        # Read the machines and fill out the adjacency dictionary

        for _ in range(num_machines - 1):
            child_id, parent_id, current_operation = file.readline().split()
            child_id = int(child_id)
            parent_id = int(parent_id)
            current_operation_id = operation_map[current_operation]
            
            lines_list.append((child_id, parent_id, current_operation_id))


        # Initialize a list of MachineNode objects based on the adjacency list
        # Each node is initialized with its machine ID, parent ID, and initial operation
        # Firstly, create the root node with no parent
        
        root_node = MachineNode(1, None, "add")
        nodes.append(root_node)
        # Then, create the rest of the nodes
        for child_id, parent_id, current_op in lines_list:
            node = MachineNode(child_id, parent_id, current_op)
            nodes.append(node)
        # Initialize a dictionary to map machine IDs to their corresponding nodes
        node_dict = {node.machine_id: node for node in nodes}

        # Connect nodes to form the tree structure
        
        for node in nodes:
            if node.parent == None:
                rootm = node
            else:
                parent_node = node_dict[node.parent]
                parent_node.add_child(node)
        
        #number of leaf nodes
        leaf_node_ids = [node.machine_id for node in nodes if node.children == []]

        # Read products received by leaf machines
        for leaf_id in leaf_node_ids:

            product = file.readline().strip()
            node_dict[leaf_id].first_input = product

    return 
#def add(machine, other_machine):
#    return machine + other_machine

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

# Example usage:
file_path = 'input.txt'
#rank ==0
if rank == 0:
    num_machines = 0
    num_cycles = 0
    wear_factors = []
    maintenance_threshold = 0
    node_dict = {} # maps machine IDs to their corresponding nodes
    rootm = None
    lines_list = [] 
    nodes = [] # list of MachineNode objects
    leaf_node_ids = [] # list of leaf node IDs
    operation_map = {"add": 0, "enhance": 1, "reverse": 2, "chop": 3, "trim": 4, "split": 5}
    
    #print("I am the master node")
    read_input_file(file_path)

    #send the number of machines to all the other nodes
else:
    num_machines = 0
    num_cycles = 0
#print("I am a slave, I have rank ", rank)
num_machines = comm.bcast(num_machines, root = 0)
#send the number of cycles to all the other nodes
num_cycles = comm.bcast(num_cycles, root = 0)


    #send the node to all the other nodes
if rank == 0:

    for i in range(1, size):
        comm.send(nodes[i], dest = i, tag = 1)

    for k in range(num_cycles):
    
        #receive the final result
        final_result = ""
        #first sort the children list
        rootm.children.sort(key = lambda x: x.machine_id)
        for ij in range(len(rootm.children)):
            final_result += comm.recv(source = rootm.children[ij].machine_id-1, tag = 2)

        print("for cycle", k, "final result: ", final_result)






#all the other nodes take the node from the master node
if rank != 0:   
    for j in range(num_machines-1,0,-1):
        if rank == j:
            node = comm.recv(source = 0, tag = 1)
            for m in range(num_cycles):
                result_data = ""

                if node.first_input != None:
                    if node.current_operation_id == 1:
                        result_data  = enhance(node.first_input)
                    elif node.current_operation_id == 2:
                        result_data = reverse(node.first_input)
                    elif node.current_operation_id == 3:
                        result_data = chop(node.first_input)
                    elif node.current_operation_id == 4:
                        result_data = trim(node.first_input)
                    elif node.current_operation_id == 5:
                        result_data = split(node.first_input)

                else:
                    coming_data = ""
                    #first sort the children list
                    node.children.sort(key = lambda x: x.machine_id)
                    for ii in range(len(node.children)):
                        coming_data += comm.recv(source = node.children[ii].machine_id-1, tag = 2)
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
                        result_data = split(coming_data)

                #if node.parent != None:
                #print(rank, result_data)
                #print("id:", node.current_operation_id)
                node.change_operation()
                #print("id after:", node.current_operation_id)

                comm.send(result_data, dest = node.parent-1, tag = 2)



                
