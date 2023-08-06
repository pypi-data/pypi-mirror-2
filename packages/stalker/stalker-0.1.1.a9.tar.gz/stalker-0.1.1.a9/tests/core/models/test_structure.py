#-*- coding: utf-8 -*-



import mocker
from stalker.core.models import Structure, FilenameTemplate, Type
from stalker.ext.validatedList import ValidatedList






########################################################################
class StructureTester(mocker.MockerTestCase):
    """tests the stalker.core.models.Structure class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """seting up the tests
        """
        
        # create mocks
        
        # mock type templates
        self.asset_template = self.mocker.mock(FilenameTemplate)
        self.shot_template = self.mocker.mock(FilenameTemplate)
        self.reference_template = self.mocker.mock(FilenameTemplate)
        
        self.mock_templates = [self.asset_template,
                               self.shot_template,
                               self.reference_template]
        
        self.mock_templates2 = [self.asset_template]
        
        self.custom_template = "a custom template"
        
        self.mock_type = self.mocker.mock(Type)
        
        self.mocker.replay()
        
        # keyword arguments
        self.kwargs = {
            "name": "Test Structure",
            "description": "This is a test structure",
            "templates": self.mock_templates,
            "custom_template": self.custom_template,
            "type": self.mock_type,
        }
        
        self.mock_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_custom_template_argument_can_be_skipped(self):
        """testing if the custom_template argument can be skipped
        """
        
        self.kwargs.pop("custom_template")
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_custom_template_argument_is_None(self):
        """testing if no error will be raised when the custom_template argument
        is None.
        """
        
        self.kwargs["custom_template"] = None
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_custom_template_argument_is_empty_string(self):
        """testing if no error will be raised when the custom_template argument
        is an empty string
        """
        
        self.kwargs["custom_template"] = ""
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_argument_can_be_skipped(self):
        """testing if no error will be raised when the templates argument is
        skipped
        """
        
        self.kwargs.pop("templates")
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_argument_can_be_None(self):
        """testing if no error will be raised when the templates argument is
        None
        """
        
        self.kwargs["templates"] = None
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_attribute_can_be_set_to_None(self):
        """testing if no error will be raised when the templates attribute is
        set to None
        """
        
        self.mock_structure.templates = None
    
    
    
    #----------------------------------------------------------------------
    def test_templates_argument_only_accepts_list(self):
        """testing if a TypeError will be raised when the given templates
        argument is not a list
        """
        
        self.kwargs["templates"] = 1
        self.assertRaises(TypeError, Structure, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_attribute_only_accepts_list(self):
        """teting if a TypeError will be raised when the templates attribute
        is tried to be set to an object which is not a list instance.
        """
        
        self.assertRaises(TypeError, setattr, self.mock_structure, "templates",
                          1.121)
        
        # test the correct value
        self.mock_structure.templates = self.mock_templates
    
    
    
    #----------------------------------------------------------------------
    def test_templates_argument_accepts_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates argument is
        a list but the elements are not all instances of FilenameTemplate
        class.
        """
        
        test_value = [1, 1.2, "a string"]
        self.kwargs["templates"] = test_value
        self.assertRaises(TypeError, Structure, **self.kwargs)
        
        # test the correct value
        self.kwargs["templates"] = self.mock_templates
        new_structure = Structure(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_attribute_accpets_only_list_of_FilenameTemplate_instances(self):
        """testing if a TypeError will be raised when the templates attribute
        is a list but the elements are not all instances of FilenameTemplate
        class.
        """
        
        test_value = [1, 1.2, "a string"]
        self.assertRaises(TypeError, setattr, self.mock_structure, "templates",
                          test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_templates_attribute_is_instance_of_ValidatedList(self):
        """testing if the templates attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_structure.templates, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test___strictly_typed___is_True(self):
        """testing if the __strictly_typed__ is True
        """
        
        self.assertTrue(Structure.__strictly_typed__, True)
    
    
    
    #----------------------------------------------------------------------
    def test_equality_operator(self):
        """testing equality of two Structure objects
        """
        
        new_structure2 = Structure(**self.kwargs)
        
        self.kwargs["custom_template"] = "a mock custom template"
        new_structure3 = Structure(**self.kwargs)
        
        self.kwargs["custom_template"] = self.mock_structure.custom_template
        self.kwargs["templates"] = self.mock_templates2
        new_structure4 = Structure(**self.kwargs)
        
        self.assertTrue(self.mock_structure==new_structure2)
        self.assertFalse(self.mock_structure==new_structure3)
        self.assertFalse(self.mock_structure==new_structure4)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality_operator(self):
        """testing inequality of two Structure objects
        """
        
        new_structure2 = Structure(**self.kwargs)
        
        self.kwargs["custom_template"] = "a mock custom template"
        new_structure3 = Structure(**self.kwargs)
        
        self.kwargs["custom_template"] = self.mock_structure.custom_template
        self.kwargs["templates"] = self.mock_templates2
        new_structure4 = Structure(**self.kwargs)
        
        self.assertFalse(self.mock_structure!=new_structure2)
        self.assertTrue(self.mock_structure!=new_structure3)
        self.assertTrue(self.mock_structure!=new_structure4)
    
    
    
    #----------------------------------------------------------------------
    def test_plural_name(self):
        """testing the plural name of Structure class
        """
        
        self.assertTrue(Structure.plural_name, "Structures")
    
    
    