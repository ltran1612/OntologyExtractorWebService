from owlready2 import *
from warnings import warn
from extractor_attemp1 import Extractor
from misc import *
from itertools import permutations
import argparse

# aspect names
aspect_names = ["Trustworthiness"]

def extract(src, des):
    # load ontology
    my_ontology = get_ontology(src)
    my_ontology.load()

    # print      
    before_nums = {}
    for aspect_name in aspect_names:
        before_nums[aspect_name] = get_number_of_reachable_instances_recur(my_ontology[aspect_name])

    # permuation to test
    node_class = my_ontology['Aspect']

    extractor = Extractor(node_class)
    extractor.extract(aspect_names)

    # print 
    for aspect_name in aspect_names:
        diff = get_number_of_reachable_instances_recur(my_ontology[aspect_name]) - before_nums[aspect_name]
        if diff != 0:
            warn(f"Warning: At least an instance reachable from {aspect_name} has been removed")
        else:
            print(f"Successfully got {aspect_name} from the ontology with {before_nums[aspect_name]} nodes")

    # save the ontology
    # file path for saving
    onto_path.append("./")
    my_ontology.save(file = des, format = "rdfxml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract a subtree of an ontology')
    parser.add_argument('--src', metavar='path_to_src_file', help='The file path original ontology file')
    parser.add_argument('--des', metavar='path_to_des_file', help='The file path for the result ontology file')
    
    args = parser.parse_args()

    extract(args.src, args.des)
  