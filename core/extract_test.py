from owlready2 import *
from warnings import warn
from extractor_attemp1 import Extractor
from core.misc import *
from itertools import combinations

# all possible aspect names
all_aspect_names = ["Functional", "Business", "Human", "Trustworthiness", "Timing", "Data", "Boundaries", "Composition", "Lifecycle"]

# test cases

for aspect_names in combinations(all_aspect_names, 2):
    # load ontology
    my_ontology = get_ontology('./cps.owl')
    my_ontology.load()

    # print      
    before_nums = {}
    for aspect_name in all_aspect_names:
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
            exit(1)
        else:
            pass
            #print(f"Successfully got {aspect_name} from the ontology: {before_nums[aspect_name]} nodes")
    
    # save the ontology
    # file path for saving
    #onto_path.append("./")
    #my_ontology.save(file = "truncated.owl", format = "rdfxml")

print("worked for all cases of the current ontology")