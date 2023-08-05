'''
.. module:: language
    :synopsis: Utility functions used for generating nice names.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import re


# A few misbehaving english words that might actually be used.
PLURAL_ABERRANT = {'self': 'selves', 'leaf': 'leaves', 'child': 'children',
                   'woman': 'women', 'man': 'men', 'person': 'people',
                   'nucleus': 'nuclei', 'syllabus': 'syllabi', 'focus': 'foci',
                   'phenomenon': 'phenomena', 'index': 'indices',
                   'appendix': 'appendices', 'criterion': 'criteria'}


def plural(word):
    '''
    Determines the *correct* plural form of a given word.  This is here because
    the way they do it in django annoys me to no end, and looks amateur.
    '''
    if word in PLURAL_ABERRANT:
        return PLURAL_ABERRANT[word]
    else:
        postfix = 's'
        if len(word) > 2:
            vowels = 'aeiou'
            if word[-2:] in ('ch', 'sh'):
                postfix = 'es'
            elif word[-1:] == 'y':
                if (word[-2:-1] in vowels):
                    postfix = 's'
                else:
                    postfix = 'ies'
                    word = word[:-1]
            elif word[-2:] == 'is':
                postfix = 'es'
                word = word[:-2]
            elif word[-1:] in ('s', 'z', 'x'):
                postfix = 'es'
        return word + postfix


def make_class_name(string):
    '''
    Generates an attractive class name from a string using standard naming
    conventions. 
    '''
    words = re.split("[^a-zA-Z0-9]", string)
    if len(words) > 1 or string.islower() or string.isupper():
        # Don't change anything unless we're sure the name is ugly.
        return "".join(word.capitalize() for word in words)
    else:
        return string