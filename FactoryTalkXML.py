class FactoryTalkXML:
    def __init__(self, name, attributes, children, nest_level,
                 line_number, isPair, soft_tabs=True):
        self.name = name # String containing name, which can correspond to Object Explorer name
        self.attributes = attributes # List contatining attributes
        self.children = children # List contatining xml_objects that are children
        self.nest_level = nest_level
        self.line_number = line_number # Int line the object was encountered in original XML document
        self.isPair = isPair # Bool True if of the form <foo></foo> False if <foo bar/>
        self.soft_tabs = soft_tabs

    def render(self, text='', soft_tabs=True): # Always use soft tabs for Factory Talk XML
        """Renders a logical XML object and its children as a string of XML text while preserving
        the original ordering."""
        if soft_tabs:
            delimiter = '    '
        else:
            delimiter = '\t'
        text = text + self.nest_level*delimiter + '<' # Open bracket at proper nest level
        for attribute in self.attributes:
            text = text + attribute + ' '
        text = text.rstrip(' ')
        if self.isPair:
            text = text + '>' + '\n'
            for child in self.children:
                render(self=child, text=text)
            text = text + '</' + self.attribute[0] + '>' + '\n'
        else:
            text = text + '/>' + '\n'
        return text



def populate(xml_filename): # Requires 4-space delimited XML files with no more than one tag per line
    xml_file = open(xml_filename, "r")   
xml_object_dict = {}
    line_number = 0
    autogen_names = 0

    
    new_attributes = [] # temp holding place until assigned to an object
    new_children = []
    new_name = ''
    new_nest_level = None
    
    
    nest_in_prev_object = False
    new_xml = None # Go back and see if this statement is necessary
    prev_nest_level = 0
    prev_name = ""
    
    for line in xml_file:        
        line_number += 1

        
        new_nest_level = line.find('<')/4 
        isChild = (prev_nest_level < new_nest_level)
        line = line.lstrip(' ') #trim the indentations
        isClosingTag = '</' in line # Determines if this line is a tag is of form </foo>        
        if isClosingTag:
            continue # There is nothing to do if this is the closing tag. Escape from this interation
        isPair = (not '/>' in line) and (not '</' in line)  # Determines if tag is a single <foo bar/> or a <foo></foo> pair        
        line = line.lstrip('<') # trim the open angle bracket        
        while (line.find(' ') != -1): # strip attributes one by one
            attribute_end_char = line.find(' ')
            new_attributes.append(line[0:attribute_end_char])
            line = line[attribute_end_char+1:]
        attribute_end_char = line.find('>')
        if not isPair:
            attribute_end_char = attribute_end_char - 1
        new_attributes.append(line[1:attribute_end_char]) # Get the final attribute that's touching the '>'
        name = get_name(new_attributes)        
        if name == 'xml_object':
            autogen_names = autogen_names + 1   
            name = name + str(autogen_names)          
        new_xml = xml_object(new_attributes, name, isPair) #First create the new object
        xml_object_dict[name] = new_xml # Now add it to the complete dictionary by name
        xml_object_dict[line_number] = new_xml # Also pair a key for line number it was encountered
        if (nest_in_prev_object and (prev_name!="") ):
            xml_object_dict[prev_name].attributes.append(new_xml) # Now add it as a child to the parent
        prev_name = name
        new_attributes = [] #Clear the temporary list for reuse
    xml_file.close()
    return xml_object_dict
