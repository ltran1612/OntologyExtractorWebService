from owlready2 import *
# A class to destroy an instance and every instance reachable from it except for those we do not want to destroy. 
class EntityDestroyer:
    def __init__(self):
        self.not_destroying = []

    def __init__(self, not_destroying):
        self.not_destroying = not_destroying

    # destroy the entity
    def destroy_entity_recur(self, instance):
        if (instance.name in self.not_destroying):
            return

        for prop in instance.get_properties():
            for value in prop[instance]:
                self.destroy_entity_recur(value)

        destroy_entity(instance)      

class ExtractorSPARQL:
    def __init__(self, ontology):
        self.onto = ontology

    def extract(self, node_names):
        classes = {}
        # get the classes
        for node in node_names:
            name = node[node.index("#")+1:] 
            #
            myclass = self.onto[name].is_a
            for c in myclass:
                classes[c] = c 
        
        for myclass in classes:
            for node in myclass.instances():
                if node.iri in node_names:  
                        continue

                destroy_entity(node)
                    

class Extractor:

    def __init__(self):
        self.node_class = None
    
    def __init__(self, node_class):
        self.node_class = node_class

    # get a list of instances reachable from the input instance.
    def get_reachable_instances_recur(self, instance):
        result = [instance.name]
        for prop in instance.get_properties():
            for value in prop[instance]:
                result += self.get_reachable_instances_recur(value)
        return result
    
    def extract(self, node_names):
        # get the right node and the nodes reachable from these nodes that we do not want to remove
        not_to_be_destroyed = []
        for node in self.node_class.instances():
            if node.name in node_names:
                not_to_be_destroyed += self.get_reachable_instances_recur(node)

        # remove the unnecessary nodes reachable from the nodes. 
        destroyer = EntityDestroyer(not_to_be_destroyed)
        for node in self.node_class.instances():
            destroyer.destroy_entity_recur(node)
    
