import pprint

import configdict
from html import HTML

import pfileparser


def to_txt(mydict):
    pprint.pprint(mydict)


def get_all_values(id, configs):
    """@param config (dict) key: filename, value: config_dict
    @return (dict):
      - key: config item name
      - value: dict  * (key: filename, value: config item value)
                     * (key: 'final-<set_id>', value: filename that has the
                                                      final value)
    """
    allv = {}
    # for every file
    for name, values in configs:
        # for every config item
        for k,v in values.iteritems():
            if k not in allv:
                allv[k] = {}
            allv[k][name] = v
            allv[k]['final-%s' % id] = name
    return allv


def to_html(*configs_list):
    """
    @param config_list list of pairs (filename, config_dict)
    """
    h = HTML()
    style = """
* {font-size:small;}
.final {background-color: #87CEEB;}
.set0 {background-color: #FF7373;}
.set1 {background-color: #67E667;}
.set2 {background-color: #FFB273;}
.set3 {background-color: #E667AF;}
.set4 {background-color: #C9F76F;}
td {max-width: 20em;}
table {border-spacing: 0px;
       border-collapse: collapse;}
"""
    html = h.html()

    head = html.head()
    head.style(style, type="text/css")

    body = html.body()
    tbl = body.table(border='1')

    # table headers
    head_row = tbl.tr()
    head_row.th('')
    columns = [[i[0] for i in configs] for configs in configs_list]
    for id, set_columns in enumerate(columns):
        if set_columns:
            head_row.th('|')
        for name in set_columns:
            head_row.th(name, klass="set%s" % id)

    # combine value dictionary from all config sets
    allv = {}
    all_dict = [get_all_values(n, configs) for n,configs in enumerate(configs_list)]
    for set_dict in all_dict:
        for k,v in set_dict.iteritems():
            allv.setdefault(k,{}).update(v)

    #return pprint.pprint(allv)

    # config values
    num_sets = len(configs_list)
    for key, values in sorted(allv.iteritems()):
        # a new row for every config item
        row = tbl.tr()
        row.td(key) # config item name
        finals = {} # key: set-id, value (config-value, html element)

        # for every config set
        for id,columns_set in enumerate(columns):
            separator = row.td('') # column separator
            separator.attrs['class'] = "set%s" % id
            for name in columns_set:
                if name in values:
                    this_value = row.td(repr(values[name]))
                else:
                    this_value = row.td('&nbsp;', escape=False)
                # if value is final from a set, save in 'finals' dict
                if values.get('final-%s'%id) == name:
                    if values.get(name) is not None:
                        finals[id]= (repr(values.get(name)),this_value)

            # set CSS class for final elements
            if (len(finals)!=num_sets or # element is not defined in all sets
                len(set([v[0] for v in finals.values()])) > 1): # not the same
                # use set CSS
                for i, final in finals.iteritems():
                    final[1].attrs['class'] = "set%s" % i
            else:
                # use common CSS
                for value, ele in finals.values():
                    ele.attrs['class'] = "final"

    return str(html)


def split_list(input_list, separator):
    counter = 0
    ll = [[]]
    for ele in input_list:
        if ele == separator:
            counter += 1
            ll.append([])
        else:
            ll[counter].append(ele)
    return ll


def html_diff(filenames):
    """read config from files and generate HTML output"""
    sets = split_list(filenames, '+')

    configs_list = []
    for config_set in sets:
        set_dicts = []
        for config_file in config_set:
            if config_file.find('.py') > -1:
                parser = pfileparser.PythonConfigurationParser()
                config_dict = parser.parse_python_file(config_file, True)
            else:
                config_dict = configdict.ConfigDict(config_file)['__GLOBAL__']
            set_dicts.append([config_file, config_dict])
        configs_list.append(set_dicts)

    print to_html(*configs_list)



if __name__ == '__main__':
    import sys
    filenames = sys.argv[1:]
    html_diff(filenames)
