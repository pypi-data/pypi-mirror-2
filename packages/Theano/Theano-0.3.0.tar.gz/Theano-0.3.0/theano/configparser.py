#For flag of bool type, we consider the string 'False','false' and '0' as False 
# and the string 'True', 'true', '1' as true.
#We alsoaccept the bool type as its corresponding value!
#Normally numpy consider only the empty string as false, but this give 
# impression that it work when it do different people expected.


import os, StringIO, sys
import ConfigParser
import logging
_logger = logging.getLogger('theano.config')

for key in os.environ:
    if key.startswith("THEANO"):
        if key not in ("THEANO_FLAGS", "THEANORC"):
            print >> sys.stderr, "ERROR: Ignoring deprecated environment variable", key


THEANO_FLAGS=os.getenv("THEANO_FLAGS","")
# The THEANO_FLAGS environement variable should be a list of comma-separated
# [section.]option[=value] entries. If the section part is omited, their should be only one
# section with that contain the gived option.

# THEANORC can contain a colon-delimited list of config files, like
# THEANORC=~lisa/.theanorc:~/.theanorc
# In that case, definitions in files on the right (here, ~/.theanorc) have
# precedence over those in files on the left.
def config_files_from_theanorc():
    rval = [os.path.expanduser(s) for s in os.getenv('THEANORC', '~/.theanorc').split(os.pathsep)]
    if  os.getenv('THEANORC') is None and sys.platform=="win32":
        #To don't need to change the filename and make it open easily
        rval.append(os.path.expanduser('~/.theanorc.txt'))
    return rval
theano_cfg = ConfigParser.SafeConfigParser({'USER':os.getenv("USER", os.path.split(os.path.expanduser('~'))[-1])})
theano_cfg.read(config_files_from_theanorc())

def parse_env_flags(flags, name , default_value=None):
    #The value in the env variable THEANO_FLAGS override the previous value
    val = default_value
    for flag in flags.split(','):
        if not flag:
            continue
        sp=flag.split('=',1)
        if sp[0]==name:
            if len(sp)==1:
                val=True
            else:
                val=sp[1]
            val=str(val)
    return val

def fetch_val_for_key(key):
    """Return the overriding config value for a key.
    A successful search returs a string value.
    An unsuccessful search raises a KeyError

    The (decreasing) priority order is:
    - THEANO_FLAGS
    - ~./theanorc

    """

    # first try to find it in the FLAGS
    rval = None
    for name_val in THEANO_FLAGS.split(','):
        if not name_val:
            continue
        name_val_tuple=name_val.split('=',1)
        if len(name_val_tuple)==1:
            name, val = name_val_tuple, str(True)
        else:
            name, val = name_val_tuple

        if name == key:
            # rval might be overriden by a later definition in THEANO_FLAGS
            rval = val

    # If an rval is found, it should be a string
    if rval is not None:
        return rval

    # next try to find it in the config file

    # config file keys can be of form option, or section.option
    key_tokens = key.split('.')
    if len(key_tokens) > 2:
        raise KeyError(key)

    if len(key_tokens) == 2:
        section, option = key_tokens
    else:
        section, option = 'global', key
    try:
        return theano_cfg.get(section, option)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        raise KeyError(key)

_config_var_list = []

def _config_print(thing, buf):
    for cv in _config_var_list:
        print >> buf, cv
        print >> buf, "    Doc: ", cv.doc
        print >> buf, "    Value: ", cv.val
        print >> buf, ""

class TheanoConfigParser(object):
    #properties are installed by AddConfigVar
    _i_am_a_config_class = True
    def __str__(self):
        sio = StringIO.StringIO()
        _config_print(self.__class__, sio)
        return sio.getvalue()
# N.B. all instances of TheanoConfigParser give access to the same properties.
config = TheanoConfigParser()

#
# The data structure at work here is a tree of CLASSES with CLASS ATTRIBUTES/PROPERTIES that
# are either a) INSTANTIATED dynamically-generated CLASSES, or b) ConfigParam instances.
# The root of this tree is the TheanoConfigParser CLASS, and the internal nodes are the SubObj
# classes created inside of AddConfigVar().
# Why this design ?
# - The config object is a true singleton.  Every instance of TheanoConfigParser is an empty
#   instance that looks up attributes/properties in the [single] TheanoConfigParser.__dict__
# - The subtrees provide the same interface as the root
# - ConfigParser subclasses control get/set of config properties to guard against craziness.

def AddConfigVar(name, doc, configparam, root=config):
    """Add a new variable to theano.config

    :type name: string for form "[section0.[section1.[etc]]].option"
    :param name: the full name for this configuration variable.
    :type doc: string
    :param doc: What does this variable specify?
    :type configparam: ConfigParam instance
    :param configparam: an object for getting and setting this configuration  parameter
    :type root: object
    :param root: used for recusive calls -- don't provide an argument for this parameter.

    :returns: None
    """

    # this method also performs some of the work of initializing ConfigParam instances

    if root is config:
        #only set the name in the first call, not the recursive ones
        configparam.fullname = name
    sections = name.split('.')
    if len(sections) > 1:
        # set up a subobject
        if not hasattr(root, sections[0]):
            # every internal node in the config tree is an instance of its own unique class
            class SubObj(object):
                _i_am_a_config_class = True
            setattr(root.__class__, sections[0], SubObj())
        newroot = getattr(root, sections[0])
        if not getattr(newroot, '_i_am_a_config_class', False) or isinstance(newroot, type):
            raise TypeError('Internal config nodes must be config class instances', newroot)
        return AddConfigVar('.'.join(sections[1:]), doc, configparam, root=newroot)
    else:
        if hasattr(root, name):
            raise AttributeError('This name is already taken', configparam.fullname)
        configparam.doc = doc
        configparam.__get__() # trigger a read of the value from config files and env vars
        setattr(root.__class__, sections[0], configparam)
        _config_var_list.append(configparam)

class ConfigParam(object):
    def __init__(self, default, filter=None,  allow_override=True):
        """
        If allow_override is False, we can't change the value after the import of Theano.
        So the value should be the same during all the execution
        """
        self.default = default
        self.filter=filter
        self.allow_override = allow_override
        # N.B. --
        # self.fullname  # set by AddConfigVar
        # self.doc       # set by AddConfigVar

    def __get__(self, *args):
        #print "GETTING PARAM", self.fullname, self, args
        if not hasattr(self, 'val'):
            try:
                val_str = fetch_val_for_key(self.fullname)
            except KeyError:
                val_str = self.default
            self.__set__(None, val_str)
        #print "RVAL", self.val
        return self.val

    def __set__(self, cls, val):
        if not self.allow_override and hasattr(self,'val'):
            raise Exception("Can't change the value of this config parameter after initialization!")
        #print "SETTING PARAM", self.fullname,(cls), val
        if self.filter:
            self.val = self.filter(val)
        else:
            self.val = val

    deleter=None

class EnumStr(ConfigParam):
    def __init__(self, default, *options, **kwargs):
        self.default = default
        self.all = (default,) + options
        def filter(val):
            if val in self.all:
                return val
            else:
                raise ValueError('Invalid value (%s) for configuration variable "%s". Legal options are %s'
                        % (val, self.fullname, self.all), val)
        over = kwargs.get("allow_override", True)
        super(EnumStr, self).__init__(default, filter, over)

    def __str__(self):
        return '%s (%s) ' % (self.fullname, self.all)

class TypedParam(ConfigParam):
    def __init__(self, default, mytype, is_valid=None, allow_override=True):
        self.mytype = mytype
        def filter(val):
            casted_val = mytype(val)
            if callable(is_valid):
                if is_valid(casted_val):
                    return casted_val
                else:
                    raise ValueError('Invalid value (%s) for configuration variable "%s".'
                            % (val, self.fullname), val)
            return casted_val
        super(TypedParam, self).__init__(default, filter,  allow_override=allow_override)
    def __str__(self):
        return '%s (%s) ' % (self.fullname, self.mytype)

def StrParam(default, is_valid=None, allow_override=True):
    return TypedParam(default, str, is_valid, allow_override=allow_override)
def IntParam(default, is_valid=None, allow_override=True):
    return TypedParam(default, int, is_valid, allow_override=allow_override)
def FloatParam(default, is_valid=None, allow_override=True):
    return TypedParam(default, float, is_valid, allow_override=allow_override)
def BoolParam(default, is_valid=None, allow_override=True):
#see comment at the beggining of this file.
    def booltype(s):
        if s in ['False','false','0', False]:
            return False
        elif s in ['True','true','1', True]:
            return True

    def is_valid_bool(s):
        if s in ['False', 'false', '0', 'True', 'true', '1', False, True]:
            return True
        else: 
            return False
    if is_valid is None:
        is_valid = is_valid_bool
    return TypedParam(default, booltype, is_valid, allow_override=allow_override)
