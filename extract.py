from owlready2 import *

aspect_names = ["Trustworthiness"]

# A class to destroy an instance and every instance reachable from it except for those we do not want to destroy. 
class EntityDestroyer:
    def __init__(self):
        self.not_destroying = []

    def __init__(self, not_destroying):
        self.not_destroying = not_destroying

    # destroy the 
    def destroy_entity_recur(self, instance):
        if (instance.name in self.not_destroying):
            return

        for prop in instance.get_properties():
            for value in prop[instance]:
                self.destroy_entity_recur(value)

        destroy_entity(instance)      

# get a list of instances reachable from the input instance.
def get_reachable_instances_recur(instance):
    result = [instance.name]
    for prop in instance.get_properties():
        for value in prop[instance]:
            result += get_reachable_instances_recur(value)
    return result

# count the number of nodes in the substree
def get_number_of_reachable_instances_recur(instance):
    result = 1
    for prop in instance.get_properties():
        for value in prop[instance]:
            result += get_number_of_reachable_instances_recur(value)
    return result

# load ontology
my_ontology = get_ontology('./cps.owl')
my_ontology.load()
#print(len(my_ontology['Concern'].instances()))

# get the right aspect and the related instances that we do not want to remove
not_to_be_destroyed = []
for aspect in my_ontology['Aspect'].instances():
    if aspect.name in aspect_names:
        not_to_be_destroyed += get_reachable_instances_recur(aspect)

# print      
for aspect_name in aspect_names:
    print(aspect_name, "after removing", get_number_of_reachable_instances_recur(my_ontology[aspect_name]))

# remove the unnecessary concerns
destroyer = EntityDestroyer(not_to_be_destroyed)
for aspect in my_ontology['Aspect'].instances():
    destroyer.destroy_entity_recur(aspect)

# print 
for aspect_name in aspect_names:
    print(aspect_name, "after removing", get_number_of_reachable_instances_recur(my_ontology[aspect_name]))
#print(len(my_ontology['Concern'].instances()))

# save the ontology
# file path for saving
onto_path.append("./")
my_ontology.save(file = "truncated.owl", format = "rdfxml")

        
