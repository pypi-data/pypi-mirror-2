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
        for i in self.params:
            if i.has_key(pref):
                del i[pref]
        self.add({pref: new_value})

    def uniq_key_value(self, pref, value):
        """
        If you need unique key value pairs.  For example if you have a
        parameter that my appear in more than one config file but you 
        only want one occurance reported.  Like ~./prefs has author mark
        and .cwd also has author mark you would only return one author
        mark but you could have another author that would also get returned.
        """
        if not self.has(pref, value):
           self.add({pref: value})
        else:
           found = False
           for i in self.params:
              if i.has_key(pref):
                 if i[pref] == value:
                     if found == False:
                         found = True
                     else:
                         del i[pref]

    def read_file(self, file):
        """
        Reads preferences from a file line by line.  Skipping all lines
        beginning with a # or newline. splitting on the first =, *  or :.  

        If split on an = other parameters with the same name are removed 
        then the preference is added irregardless of if there were 
        pre-exising preferences with the same name.  

        If split on an * the preference is simply added allowing for the
        same preference to appear several times even with the same value.

        If split on an : the key value pair is forced to be unique and if
        there are multipul key value pairs that match all but one set is
        removed.

        It will raise a Value error and provide the line number the error 
        appeard on if there is an line within your preferences file it
        doesn't know how to handle.
        """
        def which_delem(a, b):
            if a[1] != '' and b[1] != '':
               if len(a[0]) < len(b[0]):
                   return a
               else:
                   return b
            elif a[1] != '':
                return a
            elif b[1] != '':
                return b
            else:
                return a

        def insert_preference(key,value):
            if my_action == ':':
                self.uniq_key_value(key, value.lstrip().rstrip())
            elif my_action == '=':
                self.replace_key(key, value.lstrip().rstrip())
            elif my_action == '*':
                self.add({key: value.lstrip().rstrip()})
            else:
                raise ValueError('Invalid line format on %i.' % i)
  
        key, value, action, my_action = None, None, None, None
        infile = open(file, 'r')
        i = 0
        for line in iter(infile):
            i += 1
            if line[0] == '#' or line[0] == '\n': continue
            if line[0:4] == '    ' and value is not None:
                value += line[4:]
            else:
                split_line = which_delem(line.partition('*'),
                    which_delem(line.partition(':'), line.partition('=')))
                if split_line[1] != '':
                    if key == None and value == None:
                        (key, my_action, value) = split_line
                        continue
                    insert_preference(key,value)
                else:
                    raise ValueError('Invalid line format on %i.' % i)
                (key, my_action, value) = split_line
        insert_preference(key, value)
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
