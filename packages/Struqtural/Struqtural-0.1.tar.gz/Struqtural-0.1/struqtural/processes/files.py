'''
.. module:: files
    :synopsis: Utility functions for dealing with files.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''


import re
import csv
import os.path
import lxml.etree as etree
import struqtural.processes.language as lang
import struqtural.utilities as util

from itertools import count, chain
from collections import defaultdict, namedtuple

tag_name_parts = re.compile(r"\W*([A-Z0-9]*?(?:[a-z0-9]|[A-Z0-9])+)")

#==============================================================================
#                                 Functions
#==============================================================================


def parse_csv(lines, dialect=None, delimiter=None):
    '''
    Parse the specified lines.
    
    :param lines: An iterable containing one or more strings.
    
    :param dialect: The csv dialect of the file .
    
    :param delimiter: The value delimiter.
    
    :returns: Lists of column names and row values.
    '''
    sniffer = csv.Sniffer()
    sample = "\n".join(lines[:10])
    has_header = True if sniffer.has_header(sample) else False
    if not dialect:
        dialect = sniffer.sniff(sample, delimiter)
    table_reader = csv.reader(lines, dialect)
    table = [row for row in table_reader]
    if not table:
        raise ValueError("table contains no instances")
    if has_header:
        header = table.pop(0)
    else:
        header = None
    return (header, table)


def parse_xml(input_, formatter, backref=True):
    '''
    Parse an XML *input_* file, using element transformation rules from
    *formatter*.
    '''
    defaultdict_list = lambda: defaultdict(list)
    seen_relationships = defaultdict(lambda: defaultdict(defaultdict_list))
    elements = defaultdict(lambda: defaultdict(dict))
    for event in etree.iterparse(input_, events=('end',)):
        element = event[1]
        formatter.process_element(element)
        seen_child_types = set()
        for child in element.getchildren():
            keys = formatter.element_primary_key(child)
            elements[child.tag][keys].update(child.attrib)
            if element.getparent() is None:
                # Don't create a relationship to the root node, it's just a
                # container.
                continue
            seen = seen_relationships[element.tag][child.tag]
            if child.tag in seen_child_types:
                # This parent has more than one child of this type.  We need
                # to check to see if any element has more than one parent of
                # this type.
                seen["many_children"] = True
            else:
                seen_child_types.add(child.tag)       
            if any(keys in seen[parent] for parent in seen
                   if type(seen[parent]) is not bool):
                # This child is present on more than one parent of this type.
                # We need to check to see if any element has more than one
                # child of this type to determine if the relationship is many
                # to one or many to many.
                seen["many_parents"] = True
            seen[formatter.element_primary_key(element)].append(keys)
    return define_relationships(seen_relationships, elements, formatter,
                                backref)

           
def define_relationships(seen_relationships, elements, formatter,
                         backref=True):
    '''
    Takes the information built up during the parsing process and builds
    dictionaries of relationship argument lists, which will be used to create
    the actual relationships at a later time when tables have been
    instantiated and classes have been mapped.
    
    :param seen_relationships: The relationships between tags observed during
        the parsing process.  This should be a mapping of the form::
        
            dict[parent_tag][child_tag][parent_primary] = list(child_primaries)
        
        in addition, at the [child_tag] dictionary should contain the metadata
        entries "many_parents" and/or "many_children" to indicate the
        cardinality of the relationship on each end.
        
    :param elements: The set of elements observed during the parsing process.
        This should be a mapping of the form::
        
            dict[element_tag][element_primary] = element_attributes
            
    :param formatter: The :class:`SchemaFormatter` used to generate names
        from input, and handle primary key assignment.
        
    :param backref: Should relationships have a back reference by default?
    
    :returns: A two item tuple. The second item is dictionary keyed by a
        tuple of the parent and child tags, with a relationship argument
        list as values.  The first item is a dictionary keyed by element tag
        with values being lists of observed element attribute dictionaries.
    '''
    # Now that we've parsed the entire thing (BAD! we need to be able to do
    # this in an iterative fashion) let's go ahead and build the
    # relationships.
    relationships = {}
    new_name = lambda n, k: "_".join((type(n).__name__.lower(), k))
    new_dict = lambda n: dict((new_name(n, k), v) for k, v in
                              n._asdict().items())
    for parent in seen_relationships:
        child_foreign = formatter.reference_keys(parent)
        parent_primary = formatter.primary_key_fields(parent)
        for child in seen_relationships[parent]:
            parent_foreign = formatter.reference_keys(child)
            child_primary = formatter.primary_key_fields(child)
            seen = seen_relationships[parent][child]
            parameters = {"backref":backref}
            many_children = seen.pop("many_children", False)
            many_parents = seen.pop("many_parents", False)
            if many_children and many_parents:
                # Many to many, so we are building a separate association
                # table for this relationship.
                current_associations = []
                int_to = ["_".join((parent.lower(), p)) for p in parent_primary]
                int_from = ["_".join((child.lower(), p)) for p in child_primary]
                for parent_ in seen:
                    for child_ in seen[parent_]:
                        relationship = new_dict(parent_)
                        relationship.update(new_dict(child_))
                        current_associations.append(relationship)
                # Parent is primary here since there will typically be a
                # reference to the child under each instance of the parent
                # node in an XML file.
                parameters.update({"primary":parent_primary,
                                   "foreign":child_primary,
                                   "intermediate_to":int_to,
                                   "intermediate_from":int_from,
                                   "intermediate_table":current_associations})
                relationships[(parent, child)] = parameters
            elif many_parents:
                # One to many, so we need to put the foreign key on the parent.
                for parent_ in seen:
                    for child_ in seen[parent_]:
                        child_reference = formatter.reference_attributes(child_)
                        element = elements[parent][parent_]
                        element.update(child_reference)
                parameters.update({"primary":child_primary,
                                   "foreign":parent_foreign})
                relationships[(child, parent)] = parameters
            else:
                # could be either many to one or one to one.
                for parent_ in seen:
                    for child_ in seen[parent_]:
                        parent_reference = formatter \
                            .reference_attributes(parent_)
                        element = elements[child][child_]
                        element.update(parent_reference)
                parameters.update({"primary":parent_primary,
                                   "foreign":child_foreign})
                relationships[(parent, child)] = parameters
    # We don't need to perform primary key lookups anymore, so strip it out.
    elements = dict((e, elements[e].values()) for e in elements)
    return (elements, relationships)
    
    
def tablename_from_filename(input_file):
    '''
    This generates a reasonable database table name given a file name.
    '''
    file_name = os.path.split(input_file)[1]
    return re.sub(r"\.", "_", file_name)


class SchemaFormatter(object):
    '''
    Formats the data from an XML schema to a desired standard.
    '''
    
    @util.mutable_mappings("primary_keys")
    def __init__(self, primary_keys=None):
        for key in primary_keys.keys():
            # All primary keys should be set-like at this point.
            primary_keys[key] = util.as_mutable_set(primary_keys[key])
        self._primary_keys = primary_keys
        self._primary_key_tuples = defaultdict(set)
        self._counter = defaultdict(lambda: count(1))
       
    def process_element(self, element):
        '''
        Process a lxml element, so that it conforms to a particular style and
        guarantees certain properties.
        '''
        element.text = element.text.strip()
        # Check to see if this is an "attribute" element.
        if not element.getchildren() and element.text and not element.keys():
            # This should be treated as a column in the parent table rather
            # than a row in its own table.
            tag = element.tag
            attribute = self.format_attribute(tag)
            parent_tag = element.getparent().tag
            if parent_tag in self._primary_keys:
                parent_primary_keys = self._primary_keys.get(parent_tag)
                if tag in parent_primary_keys:
                    parent_primary_keys.remove(tag)
                    parent_primary_keys.add(attribute)
            value = self.format_attribute_value(element.text)
            element.getparent().attrib[attribute] = value
            element.getparent().remove(element)
            return
        # First and foremost we need to get the primary key squared away.
        tag = element.tag
        if tag not in self._primary_keys:
            primary_key = self.match_primary_key(element)
            if not primary_key:
                primary_key = util.as_set(self.create_primary_key(element))
            self._primary_keys[tag] = set(primary_key)
        for key in self._primary_keys[tag]:
            if not element.attrib.get(key):
                element.attrib[key] = self.next_id(tag)
        # Now that we've dealt with the stuff that needed the old tag, update
        # the tag to the specified format.
        element.tag = self.format_tag(tag)
        # Now update all the attributes and values.
        primary_keys = set()
        for attribute in element.attrib.keys():
            value = element.attrib.pop(attribute)
            new_attribute = self.format_attribute(attribute)
            new_value = self.format_attribute_value(value)
            element.attrib[new_attribute] = new_value
            # Record the new primary key name referenced by the new element
            # tag so it can be used later.
            if attribute in self._primary_keys.get(tag):
                primary_keys.add(new_attribute)
        if element.tag not in self._primary_key_tuples:
            # Create a named tuple class for this element's primary keys to
            # make working with it easy.
            element_keys = namedtuple(element.tag, primary_keys)
            self._primary_key_tuples[element.tag] = element_keys
        self.process_text(element)

    def format_tag(self, tag):
        '''
        Formats the name of the tag.
        '''
        return lang.make_class_name(tag)
    
    def format_attribute(self, attribute):
        '''
        Formats an attribute name.
        '''
        return attribute.lower()
    
    def format_attribute_value(self, value):
        '''
        Formats an attribute value.
        '''
        return value # This is a stub to be overriden, if you were wondering
    
    def match_primary_key(self, element):
        '''
        Method to match primary keys from an element's attribute dictionary.
        '''
        return None
    
    def create_primary_key(self, element):
        '''
        Generate a primary key name.
        '''
        return "id"
    
    def process_text(self, element):
        '''
        Convert element text to an attribute.
        '''
        if element.text:
            element.set("content", element.text)
    
    def reference_attributes(self, primary_tuple):
        '''
        Generate reference key names and values for element.
        '''
        name = type(primary_tuple).__name__.lower()
        return dict(("_".join((name, k)), v) for (k, v) in
                    primary_tuple._asdict().items())
    
    def reference_keys(self, tag):
        '''
        Create reference attributes for tag suitable for inclusion in the
        attribute dictionary of a referencing tag. 
        '''
        reference_keys = self._primary_key_tuples[tag]._fields
        return ["_".join((tag.lower(), k)) for k in reference_keys]
    
    def primary_key(self, tag):
        '''
        Return the primary key values (as a named tuple) for this tag.
        '''
        return self._primary_key_tuples[tag]
    
    def primary_key_fields(self, tag):
        '''
        Returns the primary key names for this tag.
        '''
        return self._primary_key_tuples[tag]._fields
    
    def element_primary_key(self, element):
        '''
        Generates a primary key namedtuple for element.
        '''
        primary_tuple = self._primary_key_tuples[element.tag]
        return primary_tuple(*(element.get(k) for k in primary_tuple._fields))
    
    def next_id(self, tag):
        '''
        Return a unique primary key identifier for *tag*.
        '''
        return str(self._counter[tag].next())