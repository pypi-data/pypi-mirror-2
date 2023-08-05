def key_sort(l, *keys):
    """
    Sort an iterable given an arbitary number of keys relative to it
    and return the result as a list. When a key starts with '-' the
    sorting is reversed.

    Example: key_sort(people, 'lastname', '-age')
    """
    l = list(l)
    for key in keys:
        #Find out if we want a reversed ordering
        if key.startswith('-'):
            reverse = True
            key = key[1:]
        else:
            reverse = False

        attrs = key.split('.')
        def fun(x):
            # Calculate x.attr1.attr2...
            for attr in attrs:
                x = getattr(x, attr)
            # If the key attribute is a string we lowercase it
            if isinstance(x, basestring):
                x = x.lower()
            return x
        l.sort(key=fun, reverse=reverse)
    return l

def size_human(size):
    """
    Make the size in bytes to a more human readable format.
    
    This function compares the size value with some thresholds and returns
    a new value with the appropriate suffix (K, M, T, P). The correct input
    is an integer value not a string!!!
    
    >>> size_human(755745434)
    '721.0M'
    """

    if size:
        _abbrevs = [
        (1<<50L, 'P'),
        (1<<40L, 'T'), 
        (1<<30L, 'G'), 
        (1<<20L, 'M'), 
        (1<<10L, 'k'),
        (1, 'bytes')]

        for factor, suffix in _abbrevs:
            if size > factor:
                break
        if factor == 1:
            return "%d %s" % (size, suffix)
        else:
            return "%.3f%s" % (float(size)/float(factor), suffix)


def restructured_table(column_names, column_ids, object_list, truncate_len=13):
    """Restructured table creation method
    
    This method takes some objects in a list and present them in a table format.
    The format is similar with the one used in restructured text, so it can easily
    be used in formatted text.
    The arguments are the following:
    column_names : a list or tupple with the title of each column
    column_id : a list or tupple of all the keys which will be presented from 
    each object
    object_list : the list of the objects which contain the data to be presented
    truncate_len : the length of the strings in each cell
    
    Example output :
    +---------------+---------------+---------------+
    |Alfa           |Beta           |Gama           |
    +---------------+---------------+---------------+
    |2314           |34545          |5666           |
    |12165          |34512345       |53254          |
    +---------------+---------------+---------------+

    """
    single_cell_border = "+" + (truncate_len+2) * "-"
    border = len(column_names) * single_cell_border + "+"
    table = "\n" + border + "\n"
    # Column Headers first
    for column in column_names:
        table += "| %-13s " % column[:truncate_len]
    table += "|\n" + border + "\n"
    # Data next
    for obj in object_list:
        for i in column_ids:
            levels = i.split(".")
            attr = obj
            for l in levels:
                attr = getattr(attr, l)
            table += "| %-13s " % str(attr)[:truncate_len]
        table += "|\n"
    table += border + "\n"
    return table
