# -*- coding: utf-8 -*-

"""
Utility class for taggers
"""

__author__ = 'Christian Körner'

class Tagger():
    """
    Class for taggers
    """

    def __init__(self, username = None):
        """
        Constructor
        """
        self.name = username
        self.tag_res_map = dict()
        self.res_tag_map = dict()
        
        
    def set_name(self, the_name):
        """sets the name of the tagger"""
        self.name = the_name
    
    def get_name(self):
        """returns the name"""
        return self.name
    
    def get_tas_number(self):
        """returns the number of tag assignments"""
        count = 0
        verify = 0
        
        for value in self.tag_res_map.values():
            count += len(value)
            
        for value in self.res_tag_map.values():
            verify += len(value)

        assert verify == count        
                
        return count
                
    
    def add_post(self, resource, tags):
        """adds a post to the user"""
        
        if not tags:
            print "no tags provided"
            return
        
        tag_set = self.res_tag_map.get(resource, set())
        tag_set.update(tags)
        self.res_tag_map[resource] = tag_set
            
        
        for tag in tags:
            resource_set = self.tag_res_map.get(tag, set())
            resource_set.add(resource)
            self.tag_res_map[tag] = resource_set
        

            
    def get_resources(self):
        """returns the resources of the user"""
        return self.res_tag_map.keys()
    
    def get_tags(self):
        """returns the tags of the user"""
        return self.tag_res_map.keys()
    
    def get_tags_and_occurence(self):
        """returns a dict of tags and their occurences"""
        tag_occurence_lookup = dict()
        
            
        for tag, resources in self.tag_res_map.iteritems():
            tag_occurence_lookup[tag] = len(resources)
            
        return tag_occurence_lookup

    def add_tas(self, tas_list):
        """adds a list of tas to the user information"""
        for document, tag in tas_list:
            tag_set = self.res_tag_map.get(document, set())
            tag_set.add(tag)
            self.res_tag_map[document] = tag_set
            resource_set = self.tag_res_map.get(tag, set())
            resource_set.add(document)
            self.tag_res_map[tag] = resource_set
            
    
    
if __name__ == '__main__':
    TAGGER = Tagger("hugo")


    tas_list = [("google.com", "search"), ("google.com", "player")]

    TAGGER.add_tas(tas_list)

    print "tags:", TAGGER.get_tags()
    print "resources:", TAGGER.get_resources()
    print TAGGER.get_tas_number()
    #print TAGGER.get_tags_and_occurence()
    