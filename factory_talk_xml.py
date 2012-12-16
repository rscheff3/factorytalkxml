class xml_object: 
    def __init__(self, attributes, name, isPair=True):
            self.attributes = attributes
            self.isPair = isPair
            self.name = name
        
##    def __str__(self):
##        s = self.render()
##        return s

def Render(xml, rendered_tag='', nest_level=1, soft_tabs=True): #always use soft tabs
        """Render an XML object as a string of XML text.
        Pass xml_object, and return a string.
        rendered_tag is internally modified dring recusrion
        nest_level defaults to 1 which is only modified in recursion
        """
        parent_closed = False # Track parent tags so they are closed with ">" only once
        if soft_tabs:
            delimiter = '    '
        else:
            delimiter = '\t'
        rendered_tag = rendered_tag + nest_level*delimiter + '<' # Each recursion adds an open angle bracket
        tag_name = xml.attributes[0] # Save the initial element. It is needed for closing tag pairs
        for i in range(0, len(xml.attributes)):
                element = xml.attributes[i]
                if (type(element) == str):
                        rendered_tag = rendered_tag + element + ' '
                elif isinstance(element, xml_object): 
                        if xml.isPair:
                            if (rendered_tag[len(rendered_tag)-1] == ' '): # If the last char is " " remove it.
                                rendered_tag=rendered_tag[0:len(rendered_tag)-1]
                            if not parent_closed:
                                rendered_tag = rendered_tag + '>' 
                                parent_closed = True
                            rendered_tag = rendered_tag + '\n' 
                        else:
                                rendered_tag = rendered_tag + '/>' + '\n'
                        nest_level = nest_level + 1
                        rendered_tag = render(element, rendered_tag=rendered_tag, nest_level=nest_level)
                        nest_level = nest_level - 1 
                else:
                        print 'All XML objects should have attributes consisting of strings or other xml_objects.'
                        assert False  # There is a better way to throw a real exception
        if (rendered_tag[len(rendered_tag)-1] == ' '): # If the last char is " " remove it.
                rendered_tag=rendered_tag[0:len(rendered_tag)-1]
        if xml.isPair and not parent_closed:
                rendered_tag = rendered_tag + '\n' + nest_level*delimiter + '</' + tag_name + '>' # Close the pair
        elif not xml.isPair:
            rendered_tag = rendered_tag + '/>'    # Close the tag
        return rendered_tag


    

def populate(xml_filename): # Requires 4-space delimited XML files with no more than one tag per line
    xml_file = open(xml_filename, "r")   
    line_number = 0 # This increments each line read, and the first line is 1
    autogen_names = 0
    temp_attribute_list = [] # temp holding place until assigned to an object
    xml_object_dict = {} # Contains all dynamically generated xml objects
    nest_in_prev_object = False
    new_xml_object = None # Go back and see if this statement is necessary
    prev_nest_level = 0
    prev_name = ""
    for line in xml_file:        
        line_number = line_number + 1
        nest_level = line.find('<')/4 # Each nest level=4 spaces. First nonspace on every line is always '<'
        nest_in_prev_object = (prev_nest_level < nest_level)
        line = line.lstrip(' ') #trim the indentations
        isClosingTag = '</' in line # Determines if this line is a tag is of form </foo>        
        if isClosingTag:
            continue # There is nothing to do if this is the closing tag. Escape from this interation
        isPair = (not '/>' in line) and (not '</' in line)  # Determines if tag is a single <foo bar/> or a <foo></foo> pair        
        line = line.lstrip('<') # trim the open angle bracket        
        while (line.find(' ') != -1): # strip attributes one by one
            attribute_end_char = line.find(' ')
            temp_attribute_list.append(line[0:attribute_end_char])
            line = line[attribute_end_char+1:]
        attribute_end_char = line.find('>')
        if not isPair:
            attribute_end_char = attribute_end_char - 1
        temp_attribute_list.append(line[1:attribute_end_char]) # Get the final attribute that's touching the '>'
        name = get_name(temp_attribute_list)        
        if name == 'xml_object':
            autogen_names = autogen_names + 1   
            name = name + str(autogen_names)          
        new_xml_object = xml_object(temp_attribute_list, name, isPair) #First create the new object
        xml_object_dict[name] = new_xml_object # Now add it to the complete dictionary by name
        xml_object_dict[line_number] = new_xml_object # Also pair a key for line number it was encountered
        if (nest_in_prev_object and (prev_name!="") ):
            xml_object_dict[prev_name].attributes.append(new_xml_object) # Now add it as a child to the parent
        prev_name = name
        temp_attribute_list = [] #Clear the temporary list for reuse
    xml_file.close()
    return xml_object_dict


def get_name(attribute_list, autogen_base_name='xml_object'): # If it exists, extract object name from attribute list. Else, autogen.
    name_position = 0
    has_name = False
    meaningful_name = False
    for attribute in attribute_list:
        has_name = 'name' in attribute # If there is a name attribute, check to see if it is meaningful
        if has_name:
            break
        name_position = name_position + 1
    if has_name:        
        meaningful_name = attribute[len(attribute)-2].isdigit() # meaningful names always have a digit like name="MultistateIndicator1"
    if meaningful_name:
        start_char = attribute_list[name_position].find('"')+1 # Finds this char: name="_ultistateIndicator1"
        end_char = attribute_list[name_position].rfind('"')-1 # Finds this char: name="MultistateIndicator_"
        return_name = attribute_list[name_position][start_char:end_char+1]
        return return_name
    return autogen_base_name # It is up to the caller of the function to concatonate a suffix on autogens

# Runtime/Test Related from here down
# For info on Dicts, see http://docs.python.org/2/library/stdtypes.html#dict


dict1 = populate('1.xml')
root = dict1[1]
string1 = Render(root)
file1 = open('6.xml', 'w')
file1.write(string1)
file1.close()

##xml_object1 = dict1['xml_object1']
##new_xml = open('3.xml', 'w')
##new_xml.write(Render(xml_object1))
##new_xml.write(str(xml_object1.attributes))
##new_xml.close()


##attributes1 = ['caption', 'fontFamily="Arial"', 'fontSize="10"', 'bold="false"', \
##    'italic="false"', 'underline="false"', 'sstrikethrough="false"', \
##    'caption="Error"', 'color="white"', 'backColor="navy"', 'backStyle="transparent"', \
##    'alignment="middleCenter"', 'wordWrap="true"', 'blink="false"']
##caption1 = xml_object(attributes1, 'object1', isPair=False)
##attributes2 = ['imageSettings', 'backColor="navy"', 'backStyle="transparent"', 'blink="false"', \
##               'alignment="middleCenter"', 'color="white"', 'scaled="false"', 'imageName=""']
##imagesettings1 = xml_object(attributes2, 'object2', isPair=False)
##attributes3 = ['state', 'backColor="navy"', 'blink="false"', 'patternStyle="none"', 'patternColor="white"', \
##               'borderColor="navy"', 'stateId="Error"', caption1, imagesettings1]
##state1 = xml_object(attributes3, 'object3', isPair=True)
##attributes4 = ['state', 'backColor="navy"', 'blink="false"', 'patternStyle="none"', 'patternColor="white"', \
##               'borderColor="navy"', 'stateId="Error"', caption1, imagesettings1, state1]
##print Render(state1)


#Test Cases
#<pair> </pair> 
#<pair attributes="true" displaythem="true"> </pair>
#<singletag attributes="true", displaythem="true"/>

