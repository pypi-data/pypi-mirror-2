'''
.. module:: extension
    :synopsis: SQL Alchemy extension implementations.
    
.. moduleauthor:: Nathan Rice <nathan.alexander.rice@gmail.com>
'''

import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.sql as sql
import struqtural.utilities as util

PRE = "pre"
POST = "post"


#==============================================================================
#                                 Functions
#==============================================================================


@util.mutable_mappings("table_args")
def tree_table(name, metadata, join_columns, table_args=None):
    '''
    Generates the nesting table required for single-join parent and child
    queries in trees.
    
    :param name: The nesting table name.
    
    :param metadata: The metadata that the nesting table should be associated
        with.
        
    :param join_columns: The columns that will be used in the join between
        the node table and the nesting table.
        
    :param table_args:  Allows you to specify additional keyword arguments
        which should be passed when instantiating the 
        :class:`sqlalchemy.schema.Table`.
    '''
    for column in join_columns:
        column.element_primary_key = True
        column.nullable = False
    pre = sa.Column(PRE, sa.Integer(), nullable=False)
    post = sa.Column(POST, sa.Integer(), nullable=False)
    columns = [pre, post] + join_columns
    return sa.Table(name, metadata, *columns, **table_args)


def dag_table(name_prefix, *args, **kwargs):
    '''
    Generates the nesting table required for single-join parent and child
    queries in directed acyclic graphs.  Additional arguments to this
    function are the same as those for :func:`tree_table`.
    '''
    table = tree_table(*args, **kwargs)
    # Generate a primary key column here since more than one partially
    # ordered instance will have the same instance id.
    sequence = sa.Sequence(name_prefix + "_sequence")
    key = "_".join((name_prefix, "id")) 
    id_column = sa.Column(key, sa.Integer(), sequence, primary_key=True)
    table.append_column(id_column)
    return table


#==============================================================================
#                                  Classes
#==============================================================================


class TreeExtension(orm.MapperExtension):
    '''
    Automates generation of integer pre/post values for join-free nesting.
    This was adapted from the sqlalchemy nested set example.
    
    .. attribute:: id_columns
    
        ..
        
        |    The primary key columns for the instance being mapped.  Used to
        |    identify sibling nodes for a given node, so it can be inserted at
        |    the correct position.
    '''

    def __init__(self, id_columns):
        '''
        :param id_columns: The primary key columns for the table being mapped.
        '''
        super(TreeExtension, self).__init__()
        self.id_columns = id_columns

    def before_insert(self, mapper, connection, instance_):
        '''
        Triggered by session.add()
        ''' 
        table = mapper.mapped_table
        if not instance_.parent:
            instance_.pre = 1
            instance_.post = 2
        else:
            self._update(table, connection, instance_)

    def _update(self, table, connection, instance_):
        post = table.columns[POST]
        pre = table.columns[PRE]
        select = sa.select([post])
        for column in self.id_columns:
            c = table.columns[column]
            select = select.where(c == getattr(instance_.parent, column))
        last_sibling = connection.scalar(select)
        cases = {pre: [(pre > last_sibling, pre + 2)],
                 post: [(post >= last_sibling, post + 2)]}
        val = lambda x: sa.case(cases[x], else_=x)
        update = table.update(post >= last_sibling)
        update = update.values(pre=val(pre), post=val(post))
        connection.execute(update)
        instance_.pre = last_sibling
        instance_.post = last_sibling + 1


class DirectedAcyclicGraphExtension(TreeExtension):
    '''
    Automates generation of integer pre/post values for join-free partial
    ordering.  This was adapted from the sqlalchemy nested set example and
    extended to handle nodes with more than one parent.
    '''

    def before_insert(self, mapper, connection, instance_):
        '''
        Triggered by session.add()
        '''
        table = mapper.mapped_table
        if not instance_.parent:
            max_post = sql.select([sql.func.max(table.columns[POST])]).scalar()
            if not max_post:
                instance_.pre = 1
                instance_.post = 2
            else:
                instance_.pre = max_post + 1
                instance_.post = max_post + 2
        else:
            self._update(table, connection, instance_)