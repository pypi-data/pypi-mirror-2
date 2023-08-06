#-*- coding: utf-8 -*-



import datetime
import re






########################################################################
class SimpleEntity(object):
    """The base class of all the others
    
    This class has the basic information about an entity which are the name,
    the description, tags and the audit information like created_by,
    updated_by, date_created and date_updated about this entity. It also
    creates a ``nice_name`` attribute which filters the white space around and
    in the ``name`` attribute.
    
    :param name: a string or unicode attribute that holds the name of this
      entity. it could not be empty, the first letter should be an upper case
      alphabetic (not alphanumeric) and it should not contain any white space
      at the beggining and at the end of the string
    
    :param description: a string or unicode attribute that holds the
      description of this entity object, it could be an empty string, and it
      could not again have white spaces at the beggining and at the end of the
      string
    
    :param created_by: the created_by attribute should contain a User object
      who is created this object
    
    :param updated_by: the updated_by attribute should contain a User object
      who is updated the user lastly. the created_by and updated_by attributes
      should point the same object if this entity is just created
    
    :param date_created: the date that this object is created. it should be a
      time before now
    
    :param date_updated: this is the date that this object is updated lastly.
      for newly created entities this is equal to date_created and the
      date_updated cannot be before date_created
    
    """
    
    

    #----------------------------------------------------------------------
    def __init__(self,
                 name=None,
                 description="",
                 created_by=None,
                 updated_by=None,
                 date_created=datetime.datetime.now(),
                 date_updated=datetime.datetime.now(),
                 ):
        
        # name and nice_name
        self._nice_name = ""
        self._name = ""
        self.name = name
        
        self._description = self._check_description(description)
        self._created_by = self._check_created_by(created_by)
        self._updated_by = self._check_updated_by(updated_by)
        self._date_created = self._check_date_created(date_created)
        self._date_updated = self._check_date_updated(date_updated)
    
    
    
    #----------------------------------------------------------------------
    def _check_description(self, description_in):
        """checks the given description_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of string or unicode
        if not isinstance(description_in, (str, unicode)):
            raise ValueError("the description should be set to a string or \
            unicode")
        
        return description_in
    
    
    
    #----------------------------------------------------------------------
    def _check_name(self, name_in):
        """checks the given name_in value
        """
        
        # raise ValueError when:
        
        # it is None
        if name_in is None:
            raise ValueError("the name couldn't be set to None")
        
        # it is empty
        if name_in == "":
            raise ValueError("the name couldn't be an empty string")
        
        # it is not an instance of string or unicode
        if not isinstance(name_in, (str, unicode)):
            raise ValueError("the name attribute should be set to a string \
            or unicode")
        
        return self._condition_name(name_in)
    
    
    
    #----------------------------------------------------------------------
    def _condition_name(self, name_in):
        """conditions the name_in value
        """
        
        import re
        
        #print name_in
        # remove unnecesary characters from the beginning
        name_in = re.sub("(^[^A-Za-z]+)", r"", name_in)
        #print name_in
        
        # remove white spaces
        name_in = name_in.strip()
        #print name_in
        
        ## capitalize the first letter
        #name_in = name_in[0].upper() + name_in[1:]
        #print name_in
        
        return name_in
    
    
    
    #----------------------------------------------------------------------
    def _condition_nice_name(self, nice_name_in):
        """conditions the given nice name
        """
        
        # remove camel case letters
        nice_name_in = re.sub(r"(.+?[a-z]+)([A-Z])", r"\1_\2", nice_name_in)
        
        # replace white spaces with under score
        nice_name_in = re.sub("([\s])+", r"_", nice_name_in)
        
        # remove multiple underscores
        nice_name_in = re.sub(r"([_]+)", r"_", nice_name_in)
        
        # turn it to lower case
        nice_name_in = nice_name_in.lower()
        
        return nice_name_in
        
    
    
    
    #----------------------------------------------------------------------
    def description():
        
        def fget(self):
            return self._description
        
        def fset(self, description_in):
            self._description = self._check_description(description_in)
        
        doc = """the description of the entity"""
        
        return locals()
    
    description = property(**description())
    
    
    
    #----------------------------------------------------------------------
    def name():
        
        def fget(self):
            return self._name
        
        def fset(self, name_in):
            self._name = self._check_name(name_in)
            # also set the nice_name
            self._nice_name = self._condition_nice_name(self._name)
        
        doc = """the name of the entity"""
        
        return locals()
    
    name = property(**name())
    
    
    
    #----------------------------------------------------------------------
    def nice_name():
        
        def fget(self):
            return self._nice_name
        
        doc = "this is the nice name of the SimpleEntity, it is a string \
        which is a little bit more formatted than the name attribute"
        
        return locals()
    
    nice_name = property(**nice_name())
    
    
    
    
    
    #----------------------------------------------------------------------
    def _check_created_by(self, created_by_in):
        """checks the given created_by_in attribute
        """
        
        #-------------------------------------------------------------------
        # Python documentation says one of the nice ways to over come circular
        # imports is late imports and it is perfectly ok to use it like that
        # 
        # just try to import the module as late as possible
        # 
        # ref:
        # http://docs.python.org/faq/programming.html#what-are-the-best-
        #                               practices-for-using-import-in-a-module
        #-------------------------------------------------------------------
        from stalker.core.models import user
        
        ## raise ValueError when:
        ## it is None
        #if created_by_in is None:
            #raise ValueError("the created_by attribute can not be set to None")
        
        if created_by_in is not None:
            if not isinstance(created_by_in, user.User):
                raise ValueError("the created_by attribute should be an \
                instance of stalker.core.models.user.User")
        
        return created_by_in
    
    
    
    #----------------------------------------------------------------------
    def _check_updated_by(self, updated_by_in):
        """checks the given updated_by_in attribute
        """
        
        from stalker.core.models import user
        
        if updated_by_in is None:
            # set it to what created_by attribute has
            updated_by_in = self._created_by
        
        if updated_by_in is not None:
            if not isinstance(updated_by_in, user.User):
                raise ValueError("the updated_by attribute should be an \
                instance of stalker.core.models.user.User")
        
        return updated_by_in
    
    
    
    #----------------------------------------------------------------------
    def _check_date_created(self, date_created_in):
        """checks the given date_creaetd_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_created_in is None:
            raise ValueError("the date_created could not be None")
        
        if not isinstance(date_created_in, datetime.datetime):
            raise ValueError("the date_created should be an instance of \
            datetime.datetime")
        
        return date_created_in
    
    
    
    #----------------------------------------------------------------------
    def _check_date_updated(self, date_updated_in):
        """checks the given date_updated_in
        """
        
        # raise ValueError when:
        
        # it is None
        if date_updated_in is None:
            raise ValueError("the date_updated could not be None")
        
        # it is not an instance of datetime.datetime
        if not isinstance(date_updated_in, datetime.datetime):
            raise ValueError("the date_updated should be an instance of \
            datetime.datetime")
        
        # lower than date_created
        if date_updated_in < self.date_created:
            raise ValueError("the date_updated could not be set to a date \
            before date_created, try setting the date_created before")
        
        return date_updated_in
    
    
    
    #----------------------------------------------------------------------
    def created_by():
        
        def fget(self):
            return self._created_by
        
        def fset(self, created_by_in):
            self._created_by = self._check_created_by(created_by_in)
        
        doc = """gets and sets the User object who has created this
        AuditEntity"""
        
        return locals()
    
    created_by = property(**created_by())
    
    
    
    #----------------------------------------------------------------------
    def updated_by():
        
        def fget(self):
            return self._updated_by
        
        def fset(self, updated_by_in):
            self._updated_by = self._check_updated_by(updated_by_in)
        
        doc = """gets and sets the User object who has updated this
        AuditEntity"""
        
        return locals()
    
    updated_by = property(**updated_by())
    
    
    
    #----------------------------------------------------------------------
    def date_created():
        
        def fget(self):
            return self._date_created
        
        def fset(self, date_created_in):
            self._date_created = self._check_date_created(date_created_in)
        
        doc = """gets and sets the datetime.datetime object which shows when
        this object has been created"""
        
        return locals()
    
    date_created = property(**date_created())
    
    
    
    #----------------------------------------------------------------------
    def date_updated():
        
        def fget(self):
            return self._date_updated
        
        def fset(self, date_updated_in):
            self._date_updated = self._check_date_updated(date_updated_in)
        
        doc = """gets and sets the datetime.datetime object which shows when
        this object has been updated"""
        
        return locals()
    
    date_updated = property(**date_updated())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return isinstance(other, SimpleEntity) and \
           self.name == other.name and \
           self.description == other.description
    
    
    
    #----------------------------------------------------------------------
    def __ne__(self, other):
        """the inequality operator
        """
        
        return not self.__eq__(other)
        






########################################################################
class Entity(SimpleEntity):
    """This is the entity class which is derived from the SimpleEntity and adds
    only tags to the list of parameters.
    
    :param tags: a list of tag objects related to this entity. tags could be an
      empty list, or when omitted it will be set to an empty list
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self, tags=[], **kwargs):
        
        super(Entity, self).__init__(**kwargs)
        
        self._tags = self._check_tags(tags)
    
    
    
    #----------------------------------------------------------------------
    def _check_tags(self, tags_in):
        """checks the given tags_in value
        """
        
        # raise ValueError when:
        
        # it is not an instance of list
        if not isinstance(tags_in, list):
            raise ValueError("the tags attribute should be set to a list")
        
        return tags_in
    
    
    
    #----------------------------------------------------------------------
    def tags():
        
        def fget(self):
            return self._tags
        
        def fset(self, tags_in):
            self._tags = self._check_tags(tags_in)
        
        doc = """a list of Tag objects which shows the related tags to the
        entity"""
        
        return locals()
    
    tags = property(**tags())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(Entity, self).__eq__(other) and \
               isinstance(other, Entity) and \
               self.tags==other.tags






########################################################################
class StatusedEntity(Entity):
    """This is a normal entity class that derives from Entity and adds status
    variables and notes to the parameters list. Any object that needs a status
    and a corresponding status list should be derived from this class.
    
    :param status_list: this attribute holds a status list object, which shows
      the possible statuses that this entity could be in. This attribute can
      not be empty.
    
    :param status: an integer value which is the index of the status in the
      status_list attribute. So the value of this attribute couldn't be lower
      than 0 and higher than the length of the status_list object and nothing
      other than an integer
    """
    
    
    
    #----------------------------------------------------------------------
    def __init__(self,
                 status_list=[],
                 status=0,
                 #notes=[],
                 **kwargs
                 ):
        super(StatusedEntity, self).__init__(**kwargs)
        
        # the attributes
        #self._references = self._check_references(references)
        self._status_list = self._check_status_list(status_list)
        self._status = self._check_status(status)
        #self._notes = self._check_notes(notes)
        #self._thumbnail = thumbnail
    
    
    
    ##----------------------------------------------------------------------
    #def _check_references(self, references_in):
        #"""checks the given references_in list
        #"""
        
        ## raise ValueError when:
        
        ## it is not an instance of list
        #if not isinstance(references_in, list):
            #raise ValueError("the lists attribute should be set to a list")
        
        #return references_in
    
    
    
    ##----------------------------------------------------------------------
    #def _check_notes(self, notes_in):
        #"""checks the given notes_in value
        #"""
        
        ## raise ValueError when:
        
        ## it is not an instance of list
        #if not isinstance(notes_in, list):
            #raise ValueError("the notes attribute should be an instance of \
            #list")
        
        #return notes_in
    
    
    
    #----------------------------------------------------------------------
    def _check_status_list(self, status_list_in):
        """checks the given status_list_in value
        """
        
        # raise ValueError when:
        
        # import the status module
        from stalker.core.models import status
        
        # it is not an instance of status_list
        if not isinstance(status_list_in, status.StatusList):
            raise ValueError("the status list should be an instance of \
            stalker.core.models.status.StatusList")
        
        return status_list_in
    
    
    
    #----------------------------------------------------------------------
    def _check_status(self, status_in):
        """checks the given status_in value
        """
        
        # raise ValueError when:
        # it is set to None
        if status_in is None:
            raise ValueError("the status couldn't be None, set it to a \
            non-negative integer")
        
        # it is not an instance of int
        if not isinstance(status_in, int):
            raise ValueError("the status must be an instance of integer")
        
        # if it is not in the correct range:
        if status_in < 0:
            raise ValueError("the status must be a non-negative integer")
        
        if status_in >= len(self._status_list.statuses):
            raise ValueError("the status can not be bigger than the length of \
            the status_list")
    
    
    
    ##----------------------------------------------------------------------
    #def refereneces():
        
        #def fget(self):
            #return self._references
        
        #def fset(self, references_in):
            #self._references = self._check_references(references_in)
        
        #doc = """this is the property that sets and returns the references \
        #attribute"""
        
        #return locals()
    
    #references = property(**references())
    
    
    
    #----------------------------------------------------------------------
    def status():
        
        def fget(self):
            return self._status
        
        def fset(self, status_in):
            self._status = self._check_status(status_in)
        
        doc = """this is the property that sets and returns the status \
        attribute"""
        
        return locals()
    
    status = property(**status())
        
    
    
    
    #----------------------------------------------------------------------
    def status_list():
        
        def fget(self):
            return self._status_list
        
        def fset(self, status_list_in):
            self._status_list = self._check_status_list(status_list_in)
        
        doc = """this is the property that sets and returns the status_list \
        attribute"""
        
        return locals()
    
    status_list = property(**status_list())
    
    
    
    ##----------------------------------------------------------------------
    #def notes():
        
        #def fget(self):
            #return self._notes
        
        #def fset(self, notes_in):
            #self._notes = self._check_notes(notes_in)
        
        #doc = """notes is a list of Notes objects, it is a place to store notes
        #about this entity"""
        
        #return locals()
    
    #notes = property(**notes())
    
    
    
    #----------------------------------------------------------------------
    def __eq__(self, other):
        """the equality operator
        """
        
        return super(StatusedEntity, self).__eq__(other) and \
               self.status_list==other.status_list






########################################################################
class TypeEntity(Entity):
    """TypeEntity is the entry point for types.
    
    It is created to group the `Type` objects, so any other classes accepting a
    ``TypeEntity`` object can have one of the derived classes, this is done in
    that way mainly to ease the of creation of only one
    :class:`~stalker.core.models.types.TypeTemplate` class and let the
    others to use this one TypeTemplate class.
    
    It doesn't add any new parameters to it's super.
    """
    
    #----------------------------------------------------------------------
    def __init__(self, **kwargs):
        super(TypeEntity, self).__init__(**kwargs)