class MachineNode:
    def _init_(self, machine_id, parent=None, current_operation=None):
        self.machine_id = machine_id
        self.parent = parent
        self.children = []
        self.current_operation = current_operation
        self.first_input = None

    def add_child(self, child):
        self.children.append(child)


num_machines = 0
num_cycles = 0
wear_factors = []
maintenance_threshold = 0
node_dict = {} 
root = None
lines_list = []
nodes = []
leaf_node_ids = []


def read_input_file(file_path):
    global num_machines, num_cycles, wear_factors, maintenance_threshold, lines_list, nodes, node_dict, root, leaf_node_ids


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
            
            lines_list.append((child_id, parent_id, current_operation))


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
                root = node
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

# Example usage:
file_path = 'input.txt'
read_input_file(file_path)

print(num_machines)
print("input file" + file_path)
print(num_cycles)
print(wear_factors)
print(maintenance_threshold)
print(lines_list)
print(nodes)
print(node_dict)
print(root)
print(leaf_node_ids)

for everynode in nodes:
    print(everynode.machine_id, everynode.parent, everynode.current_operation, everynode.first_input)