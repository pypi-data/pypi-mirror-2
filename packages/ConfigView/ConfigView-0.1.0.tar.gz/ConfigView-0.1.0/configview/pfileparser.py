import types
import codecs

class PythonConfigurationParser:

    def __init__(self):
        # locals dictionary will contain the import statements, filter them by type
        self.type_filters = [types.ModuleType, types.BuiltinFunctionType, types.BuiltinMethodType]

    def parse_python_file(self, filename, remove_execfile):
        """
        @param filename (str)
        @param remove_execfile (bool): Remove execfile statements from file
        """
        read_globals = {}
        # exec does not contain this variable
        read_locals = {'__file__': filename}

        # contruct the string to parse
        the_file = codecs.open(filename, 'r', 'utf-8')
        if remove_execfile:
            content_to_parse = ""
            for line in the_file:
                if line.find('execfile') == -1:
                    content_to_parse += line
        else:
            content_to_parse = the_file.read()
        exec(content_to_parse, read_globals, read_locals)

        # remove variables from locals which are not config items
        remove_counter = 0
        ret_dict = {}
        for key, value in read_locals.iteritems():
            if type(value) in self.type_filters or key.startswith('_'):
                remove_counter += 1
            else:
                ret_dict[key] = value
        #print remove_counter

        return ret_dict

if __name__ == "__main__":
    parser = PythonConfigurationParser()
    the_dict = parser.parse_python_file('testfile.py', True)

