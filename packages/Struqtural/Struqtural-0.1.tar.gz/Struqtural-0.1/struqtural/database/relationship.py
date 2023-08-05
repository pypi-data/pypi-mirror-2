'''
.. module:: relationship
    :synopsis: Facade functions for the SQL Alchemy relationship function
        providing ease of use and some additional intelligence.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import re
import difflib

import sqlalchemy as sa
import sqlalchemy.sql as sql
import sqlalchemy.orm as orm
import struqtural.utilities as util
import struqtural.processes.language as lang


column_name_parts = re.compile(r"\W*([A-Z0-9]*?(?:[a-z0-9]|[A-Z0-9])+)")


class JoinConditionError(Exception):
    '''
    Error thrown in the case that a join condition can not be identified.
    '''
    
    def __init__(self, error):
        value = "unable to determine join condition: {0}".format(error)
        super(JoinConditionError, self).__init__(value)
        

def get_fk(from_table, to_table):
    '''
    Gets all foreign keys on *to_table* referencing *from_table*
    '''
    foreign_keys = []
    for foreign_key in to_table.foreign_keys:
        if foreign_key.column.table == from_table:
            foreign_keys.append(foreign_key)
    return foreign_keys

    
def columns_from_join_table(table1, table2, join_table):
    '''
    Identifies referenced columns in *table1* and *table2* based on foreign
    keys in *join_table*.
    '''
    table1_columns = []
    table2_columns = []
    join1_columns = []
    join2_columns = []
    foreign_keys = get_fk(table1, join_table)
    foreign_keys.extend(get_fk(table2, join_table))
    for key in foreign_keys:
        if key.column.table == table1:
            table1_columns.append(key.column)
            join1_columns.append(key.parent)
        elif key.column.table == table2:
            table2_columns.append(key.column)
            join2_columns.append(key.parent)
        else:
            raise JoinConditionError("unexpected table found.")
    return (table1_columns, table2_columns, join1_columns, join2_columns)

  
def columns_from_tables(table1, table2):
    '''
    Identifies a join condition between *table1* and *table2* by searching for
    cross-referencing foreign keys.
    '''
    table1_columns = []
    table2_columns = []
    table1_foreign_keys = get_fk(table1, table2)
    table2_foreign_keys = get_fk(table2, table1)
    if table1_foreign_keys and table2_foreign_keys:
        raise JoinConditionError("foreign keys in both directions.")
    foreign_keys = table1_foreign_keys or table2_foreign_keys
    for key in foreign_keys:
        if key.parent.table == table1:
            table1_columns.append(key.parent)
            table2_columns.append(key.column)
        elif key.parent.table == table2:
            table2_columns.append(key.parent)
            table1_columns.append(key.column)
        else:
            raise JoinConditionError("unexpected table found.")
    return (table1_columns, table2_columns)


@util.sequences("columns")
def columns_from_foreign_keys(columns, table):
    '''
    Identifies columns in *table* related to *columns* by examining foreign
    keys on *table* and *columns*. 
    '''
    # Since references needs to be in order, we can't append.
    references = [None] * len(columns)
    for column in columns:
        for (index, key) in enumerate(column.foreign_keys):
            if key.column.table == table:
                references[index] = key.column
    for key in table.foreign_keys:
        if key.column in columns:
            references[columns.index(key.column)] = key.parent
    return references


@util.sequences("columns")
def referenced_by_name(columns, to_table):
    '''
    Attempts to identify columns on *to_table* that would be a suitable
    match based on name and type to those specified in *columns*.  Creates
    minor permutations of the names of *columns* to account for common
    referential naming practice.
    '''
    referenced = []
    to_table_names = [c.name.lower() for c in to_table.columns]
    to_name = to_table.name.lower()
    for column in columns:
        name = column.name
        # Since it is common practice to put the name of the table being
        # referenced (or an abbreviation), let's strip that out of the
        # column name first.
        name_parts = [n.lower() for n in column_name_parts.findall(name)]
        table_part = difflib.get_close_matches(to_name, name_parts, 1, 0.5)
        if table_part:
            name = re.sub(table_part[0], "", name, 1)
        # Now let's see what is similarly named
        matches = difflib.get_close_matches(name, to_table_names, 10, 0.5)
        for match in matches:
            # Check to see if the types are the same.  Since SQL Alchemy will
            # accept either a type or type instance for columns, we need to
            # check equality on both, since instances are not equal even if
            # all their parameters are equal.  Since the type of all SQL
            # Alchemy type classes is VisitableType, this allows us to check
            # if what we are being passed is a type or class. 
            to_type = type(to_table.columns[match].type)
            from_type = type(column.type)
            visitable_type = sql.visitors.VisitableType
            if (to_type == from_type and to_type != visitable_type) or \
               to_table.columns[match].type == column.type:
                referenced.append(to_table.columns[match])
                break
    if len(columns) != len(referenced):
        error = "could not identify a match between {0} and {1}."
        raise JoinConditionError(error.format(columns, to_table.columns))
    return referenced


@util.sequences("columns")    
def referencing_by_name(columns, from_table):
    '''
    Attempts to identify columns on *from_table* that would be a suitable
    match based on name and type to those specified in *columns*.  Creates
    minor permutations of the names of columns in *from_table* to account for
    common referential naming practice.
    '''
    referencing = []
    column_names = [c.name.lower() for c in from_table.columns]
    for column in columns:
        name = column.name
        altname = column.table.name + column.name
        scores = []
        matches = difflib.get_close_matches(name, column_names, 5, 0.5)
        # Look for columns that generally match the form to_table + to_column
        altmatches = difflib.get_close_matches(altname, column_names, 5, 0.5)
        for match in matches:
            match_score = difflib.SequenceMatcher(a=name, b=match)
            scores.append((match_score, match))
        for altmatch in altmatches:
            altmatch_score = difflib.SequenceMatcher(a=name, b=altmatch)
            scores.append((altmatch_score, altmatch))
        # Now put all the results in order.
        sorted_matches = [s[1] for s in sorted(scores, reverse=True)]
        for match in sorted_matches:
            # Check to see if the types are the same.  Since SQL Alchemy will
            # accept either a type or type instance for columns, we need to
            # check equality on both, since instances are not equal even if
            # all their parameters are equal.  Since the type of all SQL
            # Alchemy type classes is VisitableType, this allows us to check
            # if what we are being passed is a type or class. 
            from_type = type(from_table.columns[match].type)
            to_type = type(column.type)
            visitable_type = sql.visitors.VisitableType
            if (from_type == to_type and to_type != visitable_type) or \
               from_table.column[match].type == column.type:
                referencing.append(from_table.columns[match])
                break
    if len(columns) != len(referencing):
        error = "could not identify a match between {0} and {1}."
        raise JoinConditionError(error.format(columns, from_table.columns))
    return referencing


@util.iterables("from_columns", "to_columns")
def condition(from_columns, to_columns):
    '''
    Create a SQL Alchemy join condition.
    '''
    join_condition = None
    for (f, t) in zip(from_columns, to_columns):
        if join_condition is None:
            join_condition = f == t
        else:
            join_condition &= f == t
    return join_condition


def get_join_columns(to_table, from_table, to_columns=None, from_columns=None):
    '''
    Determine the join condition for a relationship.  If it is not completely
    specified, get_join_columns will look for foreign keys on both *to_table*
    and *from_table* that match the specification.  If no workable foreign
    keys are found, the names and types of columns in the tables will be
    examined to identify a good match. 
    '''
    if not (to_columns or from_columns):
        # We got a totally bare call, first check to see if foreign
        # keys have been configured already.
        (to_columns, from_columns) = columns_from_tables \
            (to_table, from_table)
    if not to_columns:
        try:
            # First try for foreign keys
            to_columns = columns_from_foreign_keys(from_columns, to_table)
            if any(c is None for c in to_columns) or not to_columns:
                # Uh oh.  Let's try fishing around using column names and
                # types.
                to_columns = referenced_by_name(from_columns, to_table)
        except JoinConditionError:
            # Let's fall back to the primary keys, that's a frequent target.
            to_columns = list(to_table.primary_key)
    if to_columns and not from_columns:
        from_columns = columns_from_foreign_keys(to_columns, from_table)
        if any(r is None for r in to_columns):
            # The primary key assumption is not as reasonable here
            from_columns = referencing_by_name(to_columns, from_table)
    return (to_columns, from_columns)


def get_many_to_many_join_columns(to_table, from_table, intermediate_table,
                                  to_columns=None, from_columns=None,
                                  intermediate_to=None, intermediate_from=None):
    '''
    Determine the join columns for a many to many relationship, and configure
    foreign keys for those columns if necessary.
    '''
    (to_columns, intermediate_to) = get_join_columns \
        (to_table, intermediate_table, to_columns, intermediate_to)
    (intermediate_from, from_columns) = get_join_columns \
        (intermediate_table, from_table, intermediate_from, from_columns)
    set_foreign_key(to_columns, intermediate_to)
    set_foreign_key(from_columns, intermediate_from)
    return (to_columns, from_columns, intermediate_to, intermediate_from)


def set_foreign_key(to_columns, from_columns):
    '''
    Determines if foreign keys are already present on the specified columns.
    If not, automatically adds them in the most sensible manner possible.
    '''
    # Set any foreign keys that were not already set.
    for (to_column, from_column) in zip(to_columns, from_columns):
        if not any(from_column == k.column for k in
                   to_column.foreign_keys) and \
           not any(to_column == k.column for k in
                   from_column.foreign_keys):
            if (from_column.name in from_column.table.primary_key and
                to_column.name not in to_column.table.primary_key):
                key = ".".join((from_column.table.name, from_column.name))
                to_column.append_foreign_key(sa.ForeignKey(key))
            else:
                key = ".".join((to_column.table.name, to_column.name))
                from_column.append_foreign_key(sa.ForeignKey(key))


def set_many_to_many_foreign_key(to_columns, from_columns, intermediate_to,
                                 intermediate_from):
    '''
    Configures the foreign keys for columns from an intermediate table in a
    many to many relationship.
    '''
    set_foreign_key(to_columns, intermediate_to)
    set_foreign_key(from_columns, intermediate_from)
        

def uniquely_specifies(columns, table):
    '''
    Determines if a set of columns is sufficient to uniquely specify a row
    in a table.
    '''
    if (all(c in columns for c in table.primary_key) or
        any(c.unique for c in table.columns)):
        return True
    else:
        return False


def generate_relation_name(thing, unique):
    '''
    Generate a relationship key for *thing*, taking into account *unique* to
    determine if the generated name should be plural or singular.
    '''
    if isinstance(thing, sa.schema.Table):
        # Don't pluralize if it's a table.
        return thing.name.lower()
    else:
        name = thing.__name__.lower()
        if not unique:
            name = lang.plural(name)
        return name


@util.mutable_sequences("primary", "foreign", "intermediate_to",
                        "intermediate_from")
@util.mutable_mappings("backref_args")
def relationship(to, from_, relationship_key=None, primary=None,
                 foreign=None, backref=None, intermediate_table=None,
                 intermediate_to=None, intermediate_from=None,
                 backref_args=None, **kwargs):
    '''
    Facade function for SQL Alchemy relationships, to simplify their creation
    as much as possible.  Implements a lot of intelligence for identification
    of join conditions, so in many cases you can call it with a minimum set of
    arguments, for instance:
    
    ::
    
        >>> relationship(a, b)
    
    where **a** and **b** are mapped classes or tables.  This is possible
    because relationship looks at a variety of factors when determining the
    join condition for a and b, including foreign keys, column names and
    column types.
    
    .. note::
        while the arguments indicate that in general this should be called
        with *to* being the referenced table and *from* being the referencing
        table with foreign key constraints, this function is very forgiving
        in that regard.
    
    :param to: Either a class or SQL Alchemy table being primary in the
        relationship.
    
    :param from\_: Either a class or SQL Alchemy table referencing in the
        relationship.
    
    :param relationship_key: The key on the referencing class that should
        be used to represent this relationship.  If not specified, it will
        be inferred from the name of the primary class. If the
        relationship is an x-to-many type on the primary end, the
        correct plural form of the class name is used.
    
    :param primary: A sequence of SQL Alchemy columns or column keys
        specifying the end point of the join condition.  If none are
        specified, first the columns of *foreign* and the table
        associated with *to* are searched for foreign keys.  If the
        required foreign keys are not found, the the table associated with
        *to* is searched for columns with similar names and identical data
        types to those in *referencing*.  If that is not successful, the
        table primary keys will be used.
    
    :param foreign: A sequence of SQL Alchemy columns or column keys
        specifying the referencing elements of the join condition.  If none
        are specified, first the columns of *primary* and the table
        associated with *from_* are searched for foreign keys.  If the
        required foreign keys are not found, the the table associated with
        *from_* is searched for columns with similar names and identical
        data types to those in *primary*.  If that is not successful,
        the table primary keys will be used.
    
    :param backref: The name of the back reference to place, or a tuple as
        created by :func:`sqlalchemy.orm.backref`.  If this argument
        evaluates to True in a boolean context but is not a string or tuple,
        a suitable back reference name will be automatically generated based
        on the name of the referencing class. If the relationship is an
        x-to-many type on the referencing end, the correct plural form of the
        class name is used.
        
    :param intermediate_table: The intermediate table, if this is a many to
        many relationship.
    
    :param intermediate_to: A sequence of SQL Alchemy columns or column names.
        If column names are provided, *intermediate_table* must also be
        specified.  Used to create a join condition from the table referenced
        by *to_* to *intermediate_table*.
    
    :param intermediate_from: A sequence of SQL Alchemy columns or column names.
        If column names are provided, *intermediate_table* must also be
        specified.  Used to create a join condition from the table referenced
        by *from_* to *intermediate_table*.
    
    :param backref_args: Additional keyword arguments that should be passed
        when creating the backref tuple.
    '''
    def as_column(item, table):
        if isinstance(item, basestring):
            return table.columns[item]
        else:
            return item
    def as_table(table):
        if isinstance(table, sa.schema.Table):
            return table
        else:
            return orm.class_mapper(table).local_table
    # Make sure we're dealing with tables and columns
    to_table = as_table(to)
    from_table = as_table(from_)
    to_columns = [as_column(c, to_table) for c in primary]
    from_columns = [as_column(c, from_table) for c in foreign]
    # See if this is a many to many, and if so, get everything set up.  If
    # intermediate_table has been specified, strings for intermediate_to
    # and intermediate_from are ok, otherwise they need to be columns.
    if (intermediate_to or intermediate_from) and intermediate_table is None:
        intermediate_table = (intermediate_to or intermediate_from)[0].table
    if intermediate_table is not None:
        # Verify that intermediate to/from are columns...
        intermediate_to = [as_column(c, intermediate_table) for c in
                           intermediate_to]
        intermediate_from = [as_column(c, intermediate_table) for c in
                             intermediate_from]
        (to_columns, from_columns, intermediate_to, intermediate_from) = \
            get_many_to_many_join_columns(to_table, from_table,
                                          intermediate_table, to_columns,
                                          from_columns, intermediate_to,
                                          intermediate_from)
        # Clearly, this is supposed to be a many to many relationship.
        to_unique = False
        from_unique = False
        # These are for compatibility purposes
        kwargs["primaryjoin"] = condition(from_columns, intermediate_from)
        kwargs["secondaryjoin"] = condition(to_columns, intermediate_to)
        kwargs["secondary"] = intermediate_table
    else:
        # Validate everything and set up the foreign keys if needed
        (to_columns, from_columns) = get_join_columns \
            (to_table, from_table, to_columns, from_columns)
        set_foreign_key(to_columns, from_columns)
        # Determine if this is a many to one, one to many or one to one.
        to_unique = uniquely_specifies(to_columns, to_table)
        from_unique = uniquely_specifies(from_columns, from_table)
        kwargs["primaryjoin"] = condition(from_columns, to_columns)
        kwargs["uselist"] = (not to_unique)
    if not relationship_key:
        # Come up with a reasonable key based on the name of the class
        # being primary.  If the relationship has many on the to end,
        # pluralize it.
        relationship_key = generate_relation_name(to, to_unique)
    if ((backref or intermediate_table is not None) and
        not isinstance(backref, tuple)):
        # We were passed a value that indicates that a back reference
        # is desired, but it was not completely specified.
        if not isinstance(backref, basestring):
            backref = generate_relation_name(from_, from_unique)
        backref = orm.backref(backref, uselist=(not from_unique),
                              **backref_args)       
    kwargs["lazy"] = kwargs.pop("lazy", False)
    kwargs["backref"] = backref
    relation = orm.relation(to, **kwargs)
    # If we got passed a class, we can do the service of updating its
    # mapping.
    if from_ != from_table:
        # But first we have to make sure it has been mapped.
        try:
            mapper = orm.class_mapper(from_)
            mapper.add_property(relationship_key, relation)
        except orm.exc.UnmappedClassError:
            pass
    return relation
