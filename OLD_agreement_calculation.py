'''
Created on Dec 14, 2009

@author: chris
'''
from utilities import FrequencyCounter
import csv
import os
from xml.dom.minidom import parse

def main():
    topUrlFile = open("top1000urlsWithoutFrequency.txt")
    topUrlList = []
    
    cat_url_tag_freq_dict = dict()
    desc_url_tag_freq_dict = dict()
    
    cat_url_freq = FrequencyCounter()
    desc_url_freq = FrequencyCounter()
    
    for line in topUrlFile:
        # print line.replace("\n","")
        #print line
        
        topUrlList.append(line.replace("\n",""))
    
    csv_reader = csv.reader(open('statistics/delicious_statistics_name_and_combined.csv'), delimiter='\t')
    
    categorizer_set = set()
    describer_set = set()
    
    threshhold = 0.5514  # Magic!
    
    for line in csv_reader:
        
        if float(line[1]) > threshhold:
            #print line[0], "< is describer"
            describer_set.add(line[0].replace(" ",""))
        else:
            #print line[0], "< is categorizer"
            categorizer_set.add(line[0].replace(" ",""))
            
    path = "/Users/chris/Documents/Kassel/data_sets/delicious/"
    
    dir_list = os.listdir(path)
       
    print "cat:", len(categorizer_set), " " , " desc: ", len(describer_set)
    
    for file_name in dir_list:
        if os.path.isdir(path + file_name):
            # print file_name,"is directory"
            continue
        
        fqpn = path + file_name
        print fqpn
        
        user_name = file_name.replace("personomy_", "").replace(".xml","")
        
        is_categorizer = False
        
        if user_name in categorizer_set:
            is_categorizer = True
        
        xml_doc = parse(fqpn)
        
        for tag_app in xml_doc.getElementsByTagName("tag_application"):
            url = tag_app.getElementsByTagName("uri")[0].firstChild.toxml()
            
            if url not in topUrlList:
                continue
            
            url_tag_freq_dict = 0
            url_freq = 0
            
            if is_categorizer:
                url_tag_freq_dict = cat_url_tag_freq_dict
                url_freq = cat_url_freq
            else:
                url_tag_freq_dict = desc_url_tag_freq_dict
                url_freq = desc_url_freq
                
            url_freq.register_item(url)
            
            if not url_tag_freq_dict.has_key(url):
                tag_fq = FrequencyCounter()
                url_tag_freq_dict[url] = tag_fq
            
            tag_fq = url_tag_freq_dict[url]
            
            tags_of_url = set()
            
            for tag in tag_app.getElementsByTagName("tag"):
                new_tag = tag.firstChild.toxml()
                
                tags_of_url.add(new_tag)
            
            for tag in tags_of_url:
                tag_fq.register_item(tag)
                
            url_tag_freq_dict[url] = tag_fq
        
        xml_doc.unlink()
        
    
    #writing the whole stuff out
    
    output_file = open("frequencies.csv", "w")
    
    for line in topUrlList:
        cat_output_line = ""
        desc_output_line = ""
        
        url = line.replace("\n","")
        
        cat_output_line += url + ";"
        desc_output_line += url + ";"
        
        cat_output_line += "categorizer" + ";"
        desc_output_line += "describer" + ";"
        
        cat_output_line += str(cat_url_freq.get_frequency(line)) + ";"
        desc_output_line += str(desc_url_freq.get_frequency(line)) + ";"
        
        for tag, frequency in cat_url_tag_freq_dict[line].get_sorted_list(True):
            cat_output_line += str(frequency) + ";"
            
        for tag, frequency in desc_url_tag_freq_dict[line].get_sorted_list(True):
            desc_output_line += str(frequency) + ";"
        
        cat_output_line += "\n"
        desc_output_line += "\n" 
        
        output_file.write(desc_output_line)
        output_file.write(cat_output_line)
            
        
    output_file.close()
    

if __name__ == '__main__':
    main()