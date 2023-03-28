from owlready2 import *
from warnings import warn
from extractor_attemp1 import Extractor
from misc import *
from itertools import permutations
import argparse

def extract(src, des, node_class_with_instances_names):
    # load ontology
    my_ontology = get_ontology(src)
    my_ontology.load()

    for myclass in node_class_with_instances_names:
        # print      
        before_nums = {}
        instances_names = node_class_with_instances_names[myclass]
        for inst_name in instances_names:
            before_nums[inst_name] = get_number_of_reachable_instances_recur(my_ontology[inst_name])

        # permuation to test
        node_class = my_ontology[myclass]

        extractor = Extractor(node_class, my_ontology)
        extractor.extract(instances_names)

        # print 
        for inst_name in instances_names:
            diff = get_number_of_reachable_instances_recur(my_ontology[inst_name]) - before_nums[inst_name]
            if diff != 0:
                warn(f"Warning: At least an instance reachable from {inst_name} has been removed")
            else:
                print(f"Successfully got {inst_name} from the ontology with {before_nums[inst_name]} nodes")

    # save the ontology
    # file path for saving
    onto_path.append("./")
    my_ontology.save(file = des, format = "rdfxml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract a subtree of an ontology')
    parser.add_argument('--src', metavar='path_to_src_file', help='The file path original ontology file.')
    parser.add_argument('--des', metavar='path_to_des_file', help='The file path for the result ontology file.')
    parser.add_argument('--list', metavar='node_class', nargs="*", help='The list of class and the node names to keep, multiple list can be separated by a \'-\'.', action="extend")

    args = parser.parse_args()

    # aspect names
    class_vs_instances = {}
    raw_input = args.list
    prev = 0
    temp = []
    for i in range(len(raw_input)):
        if raw_input[i] == '-':
            temp = raw_input[prev:i]

            if len(temp) < 2:
                raise "List parameter not correct"
            class_vs_instances[temp[0]] = temp[1:]
            prev = i+1
    
    if i < len(raw_input):
        temp = raw_input[prev:len(raw_input)]
        if len(temp) < 2:
            raise "List parameter not correct"
        class_vs_instances[temp[0]] = temp[1:]

    extract(args.src, args.des, class_vs_instances)
  