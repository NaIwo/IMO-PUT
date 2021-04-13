
def replace_nodes_between_cycles(instance_object, first_cycle_node, second_cycle_node, first_cycle, second_cycle, currenct_cost):
    first_index = first_cycle.index(first_cycle_node)
    second_index = second_cycle.index(second_cycle_node)

    c1 = first_cycle[:-1]
    c2 = second_cycle[:-1]
    length1 = len(c1)
    length2 = len(c2)
    new_cost = currenct_cost - (instance_object.instance.matrix[c1[first_index-1], c1[first_index]] +\
                                instance_object.instance.matrix[c1[first_index], c1[(first_index+1) % length1]] +\
                                instance_object.instance.matrix[c2[second_index-1], c2[second_index]] +\
                                instance_object.instance.matrix[c2[second_index], c2[(second_index+1) % length2]]) +\
                                (instance_object.instance.matrix[c1[first_index-1], c2[second_index]] +\
                                instance_object.instance.matrix[c2[second_index], c1[(first_index+1) % length1]] +\
                                instance_object.instance.matrix[c2[second_index-1], c1[first_index]] +\
                                instance_object.instance.matrix[c1[first_index], c2[(second_index+1) % length2]])
    
    first_cycle[first_index] = second_cycle_node
    second_cycle[second_index] = first_cycle_node

    first_cycle[-1] = first_cycle[0]
    second_cycle[-1] = second_cycle[0]

    return first_cycle, second_cycle, new_cost

def replace_nodes_inside_cycle(instance_object, first_node, second_node, cycle, currenct_cost):
    first_index = cycle.index(first_node)
    second_index = cycle.index(second_node)
    c = cycle[:-1]
    length = len(c)
    if first_index == 0 and second_index == length-1:
        new_cost = currenct_cost - (instance_object.instance.matrix[c[second_index-1], c[second_index]] + \
                                    instance_object.instance.matrix[c[first_index], c[(first_index+1) % length]]) + \
                                    (instance_object.instance.matrix[c[second_index-1], c[first_index]] + \
                                    instance_object.instance.matrix[c[second_index], c[(first_index+1) % length]])
    elif second_index - first_index == 1:
        new_cost = currenct_cost - (instance_object.instance.matrix[c[first_index-1], c[first_index]] + \
                                    instance_object.instance.matrix[c[second_index], c[(second_index+1) % length]]) + \
                                    (instance_object.instance.matrix[c[first_index-1], c[second_index]] + \
                                    instance_object.instance.matrix[c[first_index], c[(second_index+1) % length]])
    else:
        new_cost = currenct_cost - (instance_object.instance.matrix[c[first_index-1], c[first_index]] + \
                                instance_object.instance.matrix[c[first_index], c[(first_index+1) % length]] + \
                                instance_object.instance.matrix[c[second_index-1], c[second_index]] + \
                                instance_object.instance.matrix[c[second_index], c[(second_index+1) % length]]) + \
                                (instance_object.instance.matrix[c[first_index-1], c[second_index]] + \
                                instance_object.instance.matrix[c[second_index], c[(first_index+1) % length]] + \
                                instance_object.instance.matrix[c[second_index-1], c[first_index]] + \
                                instance_object.instance.matrix[c[first_index], c[(second_index+1) % length]])

    cycle[first_index], cycle[second_index] = second_node, first_node
    cycle[-1] = cycle[0]

    return cycle, new_cost

def replace_edges_inside_cycle(instance_object, first_node, second_node, cycle, currenct_cost):
    first_index = cycle.index(first_node) 
    second_index = cycle.index(second_node) 
    part_of_cycle = cycle[first_index:second_index]
    part_of_cycle = part_of_cycle[::-1]

    c = cycle[:-1]
    new_cost = currenct_cost - (instance_object.instance.matrix[c[first_index-1], c[first_index]] +\
                                instance_object.instance.matrix[c[second_index-1], c[second_index]] ) +\
                                (instance_object.instance.matrix[c[first_index-1], c[second_index-1]] +\
                                instance_object.instance.matrix[c[first_index], c[second_index]] )

    cycle = cycle[:first_index] + part_of_cycle + cycle[second_index:]
    cycle[-1] = cycle[0]
    return cycle, new_cost