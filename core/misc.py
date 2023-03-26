# count the number of nodes in the substree
def get_number_of_reachable_instances_recur(instance):
    result = 1
    for prop in instance.get_properties():
        #print(prop.name)
        for value in prop[instance]:
            result += get_number_of_reachable_instances_recur(value)
    return result