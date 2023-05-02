from owlready2 import *
from warnings import warn
from extractor_attemp1 import Extractor
from misc import *
from itertools import permutations
import argparse
import shutil
import sys
import os
import subprocess

def extract(src, des, node_class_with_instances_names):
    # load ontology
    my_ontology = get_ontology(src)
    my_ontology.load()

    for myclass in node_class_with_instances_names:
        print("removed")
        # print      
        before_nums = {}
        instances_names = node_class_with_instances_names[myclass]
        for inst_name in instances_names:
            before_nums[inst_name] = get_number_of_reachable_instances_recur(my_ontology[inst_name])

        # permuation to test
        node_class = my_ontology[myclass]

        extractor = Extractor(node_class)
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
    my_ontology.save(file = des, format = "rdfxml")
    return 0

def query_sparql(srcs, des, sparql_paths):
    sparql_query = ""
    with open(sparql_path, "r") as f:
        sparql_query = f.readlines()

    if sparql_query == "":
        return 1

    sparql_query = f"--query={sparql_path}"
    data_path = f"--data={srcs}"
    command = ["sparql", f"{sparql_query}", f"{data_path}", "--results=RDF"]
    
#    print(sparql_query)
#    print(data_path)
#    print(command)

    result = subprocess.run(command, capture_output=True)
    if result.returncode == 0:
        result_content = result.stdout.decode("utf-8")
        with open(des, "w") as f:
            f.write(result_content);

    print(result.stdout.decode("utf-8"))
    print(sys.stderr, result.stderr.decode("utf-8"))
    
    return result.returncode

if __name__ == "__main__":
    if shutil.which("sparql") is None: 
        print("Error: SPARQL not found", file=sys.stderr)
        exit(1)

    parser = argparse.ArgumentParser(description='Extract a subtree of an ontology')
    parser.add_argument('--src', metavar='path_to_src_file', help='The file path original ontology file.')
    parser.add_argument('--des', metavar='path_to_des_file', help='The file path for the result ontology file.')
    parser.add_argument('--list', metavar='node_class', nargs="*", help='The list of class and the node names to keep, multiple list can be separated by a \'-\'.', action="extend")
    parser.add_argument('--sparql', metavar='path_to_sparql', help='The path to the file containg SPARQL query.')

    args = parser.parse_args()

    sparql_path = args.sparql
    if sparql_path is not None:
        exit(query_sparql(args.src, args.des, sparql_path))
    else: 
        # aspect names
        class_vs_instances = {}
        raw_input = args.list
        prev = 0
        temp = []
        i = 0
        for i in range(len(raw_input)):
            if raw_input[i] == '-':
                temp = raw_input[prev:i]

                if len(temp) < 2:
                    raise "List parameter not correct"
                class_vs_instances[temp[0]] = temp[1:]
                prev = i+1

        print(class_vs_instances)
        exit(extract(args.src, args.des, class_vs_instances))
  
