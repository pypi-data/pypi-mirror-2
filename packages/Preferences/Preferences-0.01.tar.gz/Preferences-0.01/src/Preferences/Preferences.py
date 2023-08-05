import os

class Preferences:
    """
    Preference CLASS

    It a simple class that creates a list of dictionarries to store
    preferences as key value pairs for managing parameter sets.  You
    can use the class directly or load the parameters from files.
    The main reason I wrote it was so that I could have an easy way 
    of storing more than one preference with the same name and load 
    them form files in a manner that allows for easy appending or 
    replacing of parmeters that could have been loaded from a 
    default prameter file.

    Config Files:
    
    The load_files will try to read files from three locations
    by default: /etc/file, ~/.file, cwd/.file and load them in
    that order but you can always pass in a list of files to 
    load. load_files uses read_file so you can use it to load
    files one at a time if you would prefer.
    Here are a few examples.

       /etc/my_prefs
          Organization: NosrednaKram.com

       [User Home]/.my_prefs
          Author: Mark Anderson
          Maintainer: Mark Anderson
          Email: Nosrednakram < at > GMail < dot > Com

      [CWD]/.my_prefs
          Project= Nosrednakram Preferences
          Description= You can do multi-line
              Just start lines with four spaces
              and they will be appended regardless
              of formating
          Author: Someone Else
          Author: Yet again Somone Else

    The file content should begin in postion 1 of the file unless
    it's a continuation then it should start with four spaces then
    the content.

    The : seperator allows for more than one paramter with that
    name.  

    The = Seperator will remove all previous loaded parameters
    with the same name and then add.  It will just add if no
    previous parameters were set.  Basiclly use for a preference
    when you only want one returned.

    Code Examples: (Assuming at least one file exists)

    # Import
    from Preferences import Preferences

    # Create Preferences instance
    project = Preferences()
   
    # Load Preferences for dfault locations if they exist 
    project.load_files('my_prefs')

    # List the Authors with a loop
    for author in project.get('Author'):
        print('Author: %s' % author

    # Print Authors as a CSV
    print project.get_csv('Author')

    # Add and additional Author
    project.add({'Author': 'Yet Another Person'})

    # Add more preferences from another file
    project.read_file('additional_file.prf')

    # Dump the project preferences to standard out
    project.dump()

    # see test.py for more usage examples.
    """

    params = []

    def __init__(self,param=None):
        if param != None:
            self.params.append(param)

    def add(self,pref=None):
        """
        Append a parameter to the params list.
        """
        self.params.append(pref)

    def has_pref(self,pref):
        """
        Returns True if a parameter with that name exists and fails 
        otherwise.
        """
        for i in self.params:
            if i.has_key(pref):
                return True
        return False 

    def get(self,pref):
        """
        get(self, pref)

        Looks up all preferences of the provieded type.

        Returns '' if no parameters were found.
        Returns value if only one parameter was found
        Returns list of values if more than one parameter was found.
        """
        list = []
        for i in self.params:
            if i.has_key(pref):
                list.append(i[pref])
        if len(list) > 1:
            return list
        elif len(list) == 0:
            return ''
        elif len(list) == 1:
            return list[0]

    def get_csv(self,pref):
        """
        This return a csv list of the specified preference values or 
        '' if there are not matching preferences.
        """
        return_result = ''
        get_result = self.get(pref)
        if isinstance(get_result, list):
            for i in self.get(pref):
                if return_result == '':
                    return_result += i
                else:
                    return_result += ', %s' % i
            return return_result
        else:
            return get_result


    def has(self,pref,value):
        """
        When passed a parameter and value it returns true if a matching
        key value pair exists and False otherwise.
        """
        for i in self.params:
            if i.has_key(pref):
                if i[pref] == value:
                    return True
        return False

    def replace_key(self, pref, new_value):
        """
        First all occurances of the preference are removed.  Then the
        parameter is added regardless of weather or not an existing 
        parameter was found.  See add for more details
        """
        replaced = False
        for i in self.params:
            if i.has_key(pref):
                del i[pref]
        self.add({pref: new_value})

    def read_file(self, file):
        """
        Reads preferences from a file line by line.  Skipping all lines
        beginning with a #. splitting on the first = or :.  If split
        on an = other parameters with the same name are removed then the
        preference is added irregardless of if there were pre-exising 
        preferences with the same name.  If split on an : the preference
        is simply added allowing for the same preference to appear 
        several times.

        It will raise a Value error and provide the line number the error 
        appeard on if there is an line withing your preferences file it
        doesn't know how to handle.
        """
        key, value, action, my_action = None, None, None, None
        infile = open(file, 'r')
        i = 0
        for line in iter(infile):
            i += 1
            if line[0] == '#': continue
            if line[0:4] == '    ' and value is not None:
                value += line[4:]
            else:
                line_add = line.partition(':')
                line_repl = line.partition('=')
                if line_add[1] == ':':
                    if line_repl[1] == '=':
                        if len(line_add[0]) < len(line_repl[0]):
                            action = 'Add'
                            line_part = line_add
                        else:
                            action = 'Replace'
                            line_part = line_repl
                    else:
                        action = 'Add'
                        line_part = line_add
                elif line_repl[1] == '=':
                    action = 'Replace'
                    line_part = line_repl
                else:
                    raise ValueError('Invalid line format on %i.' % i)
                if key != None and value != None:
                    if my_action == 'Add':
                        self.add({key: value.rstrip()})
                    elif my_action == 'Replace':
                        self.replace_key(key, value.rstrip())
                my_action = action
                key = line_part[0]
                value = line_part[2].lstrip()
        self.add({key: value})
        infile.close()

    def load_files(self, file_name, path=[]):
        """
        When called with a path that is a list of paths to configuration
        files they are read in the order they appear in the list.  If not
        it will first look for files in /etc, the users home directory, and
        then the current working director for the passed in file name.  The
        exception is a . is prepended to the file name in the users 
        directory. These files are all loaded so you can define global,
        local and user preferences.  See read_file for more on thy syntax.
        """
        if path == []:
            home = os.path.expanduser('~')
            if os.path.isfile(os.path.join('/etc',file_name)): 
                path.append(os.path.join('/etc',file_name))
            if os.path.isfile(os.path.join(home,'.%s' % file_name)):
                path.append(os.path.join(home, '.%s' % file_name))
            if os.path.isfile(os.path.join(os.getcwd(), file_name)):
                path.append(os.path.join(os.getcwd(), file_name))
        for file in path:
            self.read_file(file)

    def dump(self):
        """
        I use this for debugging some times.
        """
        for i in self.params:
            print i
