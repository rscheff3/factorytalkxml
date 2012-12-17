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

def populate(xml_filename): # Requires 4-space delimited XML files, one tag per line
    xml_file = open(xml_filename, "r")   
    xml_object_dict = {}
    line_number = 0
    autogen_names = 0
    children = [] 
    this_isChild = False
    prev_nest_level = -1
    
    for line in xml_file:        
        line_number += 1
        nest_level = get_nest_level(line)
        attributes = get_attributes(line)
        isChild = (prev_nest_level < nest_level)
        type = get_type(line)
        if this_type == 'close':
            continue
        elif type == 'open':
            isPair = True
        elif type == 'single':
            isPair = False
        else:
            print "Bad line encountered on line " + str(line_number)
            assert False
        name = get_name(attributes)
        if name = 'xml_object':
            autogen_names += 1
            name = name + str(autogen_names)                
        xml = FactoryTalkXML(name, attributes, children, nest_level, line_number, isPair)
        xml_dict[name] = xml # Now add it to the complete dictionary by name
        xml_dict[line_number] = xml # Also pair a key for line number it was encountered
        if isChild:
            nest_key = get_nest_key(xml)
            xml_dict[nest_key].children.append(xml) 
    xml_file.close()
    return xml_dict

def get_nest_level(line):
    return line.find('<')/4

def get_attributes(line):
    attributes = []
    this_attribte = ''
    line = line.lstrip(' ')
    line = line.lstrip('<')
    for char in line:
        if is not ' ' and is not '>':
            this_attribute = this_attribute + char
        else:
            attributes.append(this_attribute)
            this_attribute = ''
    return attributes
        
def get_type(line):
    if '/>' in line:
        return 'single'
    elif '</' in line:
        return 'close'
    elif '<' in line:
        return 'open'
    else:
        return 'bad'
        
def get_name(attributes):
    for attribute in attributes:
        if 'name' in attribute:
            isFactoryTalkName = attribute[len(attribute-2)].isnumberic() # FT names in the object explorer end in a number
            if isFactoryTalkName:
                start_char = attribute.find('"') + 1
                end_char = attribute.rfind('"')
                return attribute[start_char:end_char]
    return 'xml_object'

def get_nest_key(xml, xml_dict):
    current_nest_level = xml.nest_level
    current_line_number = xml.line_number
    while xml.nest_level == current_nest_level:
        current_line_number -= 1
        current_nest_level = xml_dict[current_line_number].nest_level
    return current_line_number
        
  