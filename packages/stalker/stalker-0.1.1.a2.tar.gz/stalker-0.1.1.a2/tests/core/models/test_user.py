#-*- coding: utf-8 -*-



import datetime
import mocker
from stalker.core.models import (
    user,
    department,
    group,
    task,
    project,
    sequence
)






########################################################################
class UserTest(mocker.MockerTestCase):
    """Tests the user class
    """
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        # need to have some mock object for
        assert(isinstance(self.mocker, mocker.Mocker))
        
        # a department
        self.mock_department1 = self.mocker.mock(department.Department)
        self.mock_department2 = self.mocker.mock(department.Department)
        
        # a couple of permission groups
        self.mock_permission_group1 = self.mocker.mock(group.Group)
        self.mock_permission_group2 = self.mocker.mock(group.Group)
        self.mock_permission_group3 = self.mocker.mock(group.Group)
        
        # a couple of tasks
        self.mock_task1 = self.mocker.mock(task.Task)
        self.mock_task2 = self.mocker.mock(task.Task)
        self.mock_task3 = self.mocker.mock(task.Task)
        self.mock_task4 = self.mocker.mock(task.Task)
        
        # a couple of projects
        self.mock_project1 = self.mocker.mock(project.Project)
        self.mock_project2 = self.mocker.mock(project.Project)
        self.mock_project3 = self.mocker.mock(project.Project)
        
        # a couple of sequences
        self.mock_sequence1 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence2 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence3 = self.mocker.mock(sequence.Sequence)
        self.mock_sequence4 = self.mocker.mock(sequence.Sequence)
        
        # a mock user
        self.mock_admin = self.mocker.mock(user.User)
        
        self.mocker.replay()
        
        # create the default values for parameters
        
        self.kwargs = {
            "first_name": "Erkan Ozgur",
            "last_name": "Yilmaz",
            "description": "this is a test user",
            "login_name": "eoyilmaz",
            "password": "hidden",
            "email": "eoyilmaz@fake.com",
            "department": self.mock_department1,
            "permission_groups": [self.mock_permission_group1,
                                  self.mock_permission_group2],
            "tasks": [self.mock_task1,
                      self.mock_task2,
                      self.mock_task3,
                      self.mock_task4],
            "projects": [self.mock_project1,
                         self.mock_project2,
                         self.mock_project3],
            "projects_lead": [self.mock_project1,
                              self.mock_project2],
            "sequences_lead": [self.mock_sequence1,
                               self.mock_sequence2,
                               self.mock_sequence3,
                               self.mock_sequence4],
            "created_by": self.mock_admin,
            "updated_by": self.mock_admin,
            "last_login": None
        }
        
        # create a proper user object
        self.mock_user = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_skipped(self):
        """testing if a value will be set if code argument is skipped
        """
        
        #code = None
        #name = "something"
        # code value ?
        
        # be sure that we don't have code keyword
        if self.kwargs.has_key("code"):
            self.kwargs.pop("code")
        
        new_user = user.User(**self.kwargs)
        
        # check if it is not None and not an empty string and is an instance of
        # string or unicode
        self.assertTrue(new_user.code is not None)
        self.assertTrue(new_user.code != "")
        self.assertTrue(isinstance(new_user.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_None(self):
        """testing if a value will be set if code argument is set to None
        """
        
        self.kwargs["code"] = None
        
        new_user = user.User(**self.kwargs)
        
        self.assertTrue(new_user.code is not None)
        self.assertTrue(new_user.code != "")
        self.assertTrue(isinstance(new_user.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_argument_empty_string(self):
        """testing if a value will be set if code argument is set to an empty
        string
        """
        
        self.kwargs["code"] = ""
        
        new_user = user.User(**self.kwargs)
        
        self.assertTrue(new_user.code is not None)
        self.assertTrue(new_user.code != "")
        self.assertTrue(isinstance(new_user.code, (str, unicode)))
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_format_when_code_argument_skipped(self):
        """testing if code property is formatted correctly when skipped as an
        argument
        """
        
        #code = None or ""
        #name = "something"
        # code format ?
        
        test_values = [
            ("testCode", "TEST_CODE"),
            ("1testCode", "TEST_CODE"),
            ("_testCode", "TEST_CODE"),
            ("2423$+^^+^'%+%%&_testCode", "TEST_CODE"),
            ("2423$+^^+^'%+%%&_testCode_35", "TEST_CODE_35"),
            ("2423$ +^^+^ '%+%%&_ testCode_ 35", "TEST_CODE_35"),
            ("SH001","SH001"),
            ("My code is Ozgur", "MY_CODE_IS_OZGUR"),
            (" this is another code for an asset", 
             "THIS_IS_ANOTHER_CODE_FOR_AN_ASSET"),
        ]
        
        # set the name and check the code
        for test_value in test_values:
            self.kwargs["name"] = test_value[0]
            new_user = user.User(**self.kwargs)
            
            self.assertEquals(new_user.code, test_value[1])
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_is_set_when_both_code_and_name_is_given(self):
        """testing if both code argument and name argument is given then it is
        just set to the formatted version of code
        """
        
        test_values = [
            ("aName", "testCode","TEST_CODE"),
            ("aName", "1testCode", "TEST_CODE"),
            ("aName", "_testCode", "TEST_CODE"),
            ("aName", "2423$+^^+^'%+%%&_testCode", "TEST_CODE"),
            ("aName", "2423$+^^+^'%+%%&_testCode_35", "TEST_CODE_35"),
            ("aName", "2423$ +^^+^ '%+%%&_ testCode_ 35", "TEST_CODE_35"),
            ("aName", "SH001","SH001"),
            ("aName", "My CODE is Ozgur", "MY_CODE_IS_OZGUR"),
            ("aName", " this is another code for an asset", 
             "THIS_IS_ANOTHER_CODE_FOR_AN_ASSET"),
        ]
        
        # set the name and code and test the code
        for test_value in test_values:
            self.kwargs["name"] = test_value[0]
            self.kwargs["code"] = test_value[1]
            
            new_user = user.User(**self.kwargs)
            
            self.assertEquals(new_user.code, test_value[2])
    
    
    
    #----------------------------------------------------------------------
    def test_code_property_is_changed_after_setting_name(self):
        """testing if code was 
        """
        
        code = "something"
        name = "some name"
        new_name = "something new"
        expected_new_code = "SOMETHING_NEW"
        
        self.kwargs["code"] = code
        self.kwargs["name"] = name
        
        new_user = user.User(**self.kwargs)
        
        old_code = new_user.code
        
        # set the new name
        new_user.name = new_name
        
        # first check if it is different then the old_code
        self.assertNotEquals(new_user.code, old_code)
        
        # then check if it is set to the expected result
        self.assertEquals(new_user.code, expected_new_code)
    
    
    
    #----------------------------------------------------------------------
    def test_email_argument_accepting_only_string_or_unicode(self):
        """testing if email argument accepting only string or unicode
        values
        """
        
        # try to create a new user with wrong attribte
        test_values = [1, 1.3, ["an email"], {"an":"email"}]
        
        for test_value in test_values:
            self.kwargs["email"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_accepting_only_string_or_unicode(self):
        """testing if email property accepting only string or unicode
        values
        """
        
        # try to assign something else than a string or unicode
        test_value = 1
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "email",
            test_value
        )
        
        
        
        test_value = ["an email"]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "email",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_email_argument_format(self):
        """testing if given an email in wrong format will raise a ValueError
        """
        
        test_values = ["an email in no format",
                       "an_email_with_no_part2",
                       "@an_email_with_only_part2",
                       "@",
                       ]
        
        # any of this values should raise a ValueError
        for test_value in test_values:
            self.kwargs["email"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_format(self):
        """testing if given an email in wrong format will raise a ValueError 
        """
        
        test_values = ["an email in no format",
                       "an_email_with_no_part2",
                       "@an_email_with_only_part2",
                       "@",
                       "eoyilmaz@",
                       "eoyilmaz@somecompony@com",
                       ]
        
        # any of these email values should raise a ValueError
        for value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "email",
                value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_email_property_works_properly(self):
        """testing if email property works properly
        """
        
        test_email = "eoyilmaz@somemail.com"
        self.mock_user.email = test_email
        self.assertEquals( self.mock_user.email, test_email)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_accepts_only_strings(self):
        """testing if login_name argument accepts only strings or unicode
        """
        
        test_values = [23412, ["a_user_login_name"] , [], {}, 3234.12312]
        
        for test_value in test_values:
            self.kwargs["login_name"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_accepts_only_strings(self):
        """testing if login_name property accepts only strings or unicode
        """
        
        test_values = [12312, 132.123123, ["aloginname"], {}, []]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "login_name",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name argument
        """
        
        self.kwargs["login_name"] = ""
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_empty_string(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to login_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "login_name",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name argument
        """
        
        self.kwargs["login_name"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to login_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "login_name",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_formatted_correctly(self):
        """testing if login_name argument formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("e. ozgur", "eozgur"),
                        ("erkan", "erkan"),
                        ("Ozgur", "ozgur"),
                        ("Erkan ozgur", "erkanozgur"),
                        ("eRKAN", "erkan"),
                        ("eRkaN", "erkan"),
                        (" eRkAn", "erkan"),
                        (" eRkan ozGur", "erkanozgur"),
                        ("213 e.ozgur", "eozgur"),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            
            self.kwargs["login_name"] = valuePair[0]
            
            test_user = user.User(**self.kwargs)
            
            self.assertEquals(
                test_user.login_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_formatted_correctly(self):
        """testing if loing_name property formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("e. ozgur", "eozgur"),
                        ("erkan", "erkan"),
                        ("Ozgur", "ozgur"),
                        ("Erkan ozgur", "erkanozgur"),
                        ("eRKAN", "erkan"),
                        ("eRkaN", "erkan"),
                        (" eRkAn", "erkan"),
                        (" eRkan ozGur", "erkanozgur"),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            self.mock_user.login_name = valuePair[0]
            
            self.assertEquals(
                self.mock_user.login_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_skipped(self):
        """testing if skipping loing_name argument but supplying a name
        argument will set the login_name property correctly
        """
        
        self.kwargs["name"] = self.kwargs.pop("login_name")
        new_user = user.User(**self.kwargs)
        self.assertEquals(new_user.login_name, self.kwargs["name"])
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_argument_changing_name_property(self):
        """testing if the login_name argument is actually holding the same
        value with the name property
        """
        
        # just supply login_name and check if they are holding the same value
        new_user = user.User(**self.kwargs)
        self.assertEquals(new_user.login_name, new_user.name)
    
    
    
    #----------------------------------------------------------------------
    def test_login_name_property_changing_name_property(self):
        """testing if setting the login_name property sets the name property
        """
        
        # give a new value to login_name and
        self.mock_user.login_name = "newusername"
        self.assertEquals(self.mock_user.login_name, self.mock_user.name)
    
    
    
    #----------------------------------------------------------------------
    def test_name_argument_changing_login_name_property(self):
        """testing if setting the name argument sets the login_name property
        """
        # also checks for if the formatting of name is equal to formatting of
        # the login name
        self.kwargs["name"] = "EoYiLmaZ"
        self.kwargs.pop("login_name")
        
        new_user_with_name = user.User(**self.kwargs)
        self.assertEquals(new_user_with_name.login_name,
                          new_user_with_name.name)
    
    
    
    #----------------------------------------------------------------------
    def test_name_property_changing_login_name_property(self):
        """testing if setting the name property changes the login_name property 
        """
        
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_argument_None(self):
        """testing if a ValuError will be raised when trying to assing None to
        first_name argument
        """
        
        self.kwargs["first_name"] = None
        
        self.assertRaises(
            ValueError,
            user.User,
            **self.kwargs
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        first_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "first_name",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_argument_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name argument
        """
        
        # try to assign None to the first_name argument
        self.kwargs["first_name"] = ""
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_empty(self):
        """testing if a ValueError will be raised when trying to assign an
        empty string to first_name property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "first_name",
            ""
        )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_argument_formatted_correctly(self):
        """testing if first_name argument is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("e. ozgur", "E. Ozgur"),
                        ("erkan", "Erkan"),
                        ("ozgur", "Ozgur"),
                        ("Erkan ozgur", "Erkan Ozgur"),
                        ("eRKAN", "Erkan"),
                        ("eRkaN", "Erkan"),
                        (" eRkAn", "Erkan"),
                        (" eRkan ozGur", "Erkan Ozgur"),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            self.kwargs["first_name"] = valuePair[0]
            test_user = user.User(**self.kwargs)
            self.assertEquals(test_user._first_name, valuePair[1])
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_formatted_correctly(self):
        """testing if first_name property is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("e. ozgur", "E. Ozgur"),
                        ("erkan", "Erkan"),
                        ("ozgur", "Ozgur"),
                        ("Erkan ozgur", "Erkan Ozgur"),
                        ("eRKAN", "Erkan"),
                        ("eRkaN", "Erkan"),
                        (" eRkAn", "Erkan"),
                        (" eRkan ozGur", "Erkan Ozgur"),
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            
            self.mock_user.first_name = valuePair[0]
            
            self.assertEquals(
                self.mock_user.first_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_argument_accepts_only_strings(self):
        """testing if first_name argument accepts only strings or unicode
        """
        
        # try to assign something other than a string or unicode
        
        test_values = [1, 1.3, ["my first name"], {"a_frist":"name dict"}]
        
        for test_value in test_values:
            self.kwargs["first_name"]
            
            self.assertRaises(
                ValueError,
                user.User,
                self.kwargs
            )
    
    
    
    #----------------------------------------------------------------------
    def test_first_name_property_accepts_only_strings(self):
        """testing if first_name property accepts only strings or unicode
        """
        
        test_values = [12412, ["Erkan Ozgur"]]
        
        for value in test_values:
            
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "first_name",
                value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_login_argument_accepts_None(self):
        """testing if nothing happens when the last login argument is set to
        None
        """
        
        self.kwargs["last_login"] = None
        
        # nothing should happen
        a_new_user = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_last_login_property_None(self):
        """testing if nothing happens when the last login property is set to
        None
        """
        
        # nothing should happen
        self.mock_user.last_login = None
    
    
    
    #----------------------------------------------------------------------
    def test_last_login_argument_accepts_datetime_instance(self):
        """testing if a nothing happens when tried to set the last_login
        to a datetime.datetime instance
        """
        
        self.kwargs["last_login"] = datetime.datetime.now()
        
        # nothing should happen
        a_new_user = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_last_login_argument_accepts_only_datetime_instance_or_None(self):
        """testing if a ValueError will be raised for values other than a
        datetime.datetime instances or None tried to be set to last_login
        argument
        """
        
        test_values = [1, 2.3, "login time", ["last login time"],
                       {"a last": "login time"}]
        
        for test_value in test_values:
            self.kwargs["last_login"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_last_login_property_accepts_only_datetime_instance_or_None(self):
        """testing if a ValueError will be raised for values other than
        datetime.datetime instances tried to be assigned to last_login
        property
        """
        
        test_values = [1, 2.3, "login time", ["last login time"],
                       {"a last": "login time"}]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "last_login",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_argument_None(self):
        """testing if it will be converted to an empty string if None is
        assigned to last_name argument
        """
        
        self.kwargs["last_name"] = None
        aNewUser = user.User(**self.kwargs)
        self.assertEquals(aNewUser.last_name, "")
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_None(self):
        """testing if it will be converted to an empty string if None is
        assigned to last_name property
        """
        
        self.mock_user.last_name = None
        self.assertEquals(self.mock_user.last_name, "")
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_argument_formatted_correctly(self):
        """testing if last_name argument is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("yilmaz", "Yilmaz"),
                        ("Yilmaz", "Yilmaz"),
                        ("yILMAZ", "Yilmaz"),
                        ("yIlmaZ", "Yilmaz"),
                        (" yIlmAz", "Yilmaz"),
                        (" yILmAz  ", "Yilmaz"),
                        ("de niro", "De Niro")
                    ]
        
        for valuePair in test_values:
            # set the input and expect the expected output
            
            self.kwargs["last_name"] = valuePair[0]
            
            test_user = user.User(**self.kwargs)
            
            self.assertEquals(
                test_user._last_name,
                valuePair[1]
            )
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_formatted_correctly(self):
        """testing if last_name property is formatted correctly
        """
        
        #                 input       expected
        test_values = [ ("yilmaz", "Yilmaz"),
                        ("Yilmaz", "Yilmaz"),
                        ("yILMAZ", "Yilmaz"),
                        ("yIlmaZ", "Yilmaz"),
                        (" yIlmAz", "Yilmaz"),
                        (" yILmAz  ", "Yilmaz"),
                    ]
        
        for valuePair in test_values:
            self.mock_user.last_name = valuePair[0]
            self.assertEquals(self.mock_user.last_name, valuePair[1])
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_argument_accepts_only_strings(self):
        """testing if last_name argument accepts only strings or unicode
        """
        
        test_values = [123123, ["asdfas"], [], {}]
        
        for test_value in test_values:
            self.kwargs["last_name"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_last_name_property_accepts_only_strings(self):
        """testing if last_name property accepts only strings or unicode
        """
        
        test_values = [123123, ["a last name"], {},(), 234.23423]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "last_name",
                test_value
            )
    
    
    
    ##----------------------------------------------------------------------
    #def test_department_argument_None(self):
        #"""testing if a ValueError will be raised when trying to assign None
        #for the department argument
        #"""
        
        ##try to assign None to department
        #self.kwargs["department"] = None
        #self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    ##----------------------------------------------------------------------
    #def test_department_property_None(self):
        #"""testing if a ValueError will be raised when trying to assign None
        #for the department property
        #"""
        
        ## try to assign None to the department property
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.mock_user,
            #"department",
            #None
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_department_argument_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department argument
        """
        
        # try to assign something other than a department object
        test_values = ["A department", 1 , 1.0, ["a department"],
                       {"a": "deparment"}] 
        
        for test_value in test_values:
            self.kwargs["department"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_only_accepts_department_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a Department object to department property
        """
        
        # try to assign something other than a department
        test_value = "a department"
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "department",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_department_property_works_properly(self):
        """testing if department property works properly
        """
        
        # try to set and get the same value back
        self.mock_user.department = self.mock_department2
        self.assertEquals( self.mock_user.department, self.mock_department2)
        
    
    
    
    #----------------------------------------------------------------------
    def test_password_argument_being_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the password argument
        """
        
        self.kwargs["password"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_being_None(self):
        """testing if a ValueError will be raised when tyring to assign None
        to the password property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "password",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_works_properly(self):
        """testing if password property works properly
        """
        
        test_password = "a new test password"
        self.mock_user.password = test_password
        self.assertEquals(self.mock_user.password, test_password)
    
    
    
    #----------------------------------------------------------------------
    def test_password_argument_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        
        test_password = "a new test password"
        self.kwargs["password"] = test_password
        aNew_user = user.User(**self.kwargs)
        self.assertNotEquals(test_password, aNew_user._password)
    
    
    
    #----------------------------------------------------------------------
    def test_password_property_being_scrambled(self):
        """testing if password is scrambled when trying to store it
        """
        
        test_password = "a new test password"
        self.mock_user.password = test_password
        
        # test if they are not the same any more
        self.assertNotEquals(test_password, self.mock_user._password)
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_argument_retrieved_back_correctly(self):
        #"""testing if password argument decoded and retrieved correctly
        #"""
        
        #self.fail("test not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_password_property_retrieved_back_correctly(self):
        #"""testing if password property decoded and retrieved correctly
        #"""
        
        #self.fail("test not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_argument_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups argument
        """
        
        self.kwargs["permission_groups"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_for_None(self):
        """testing if a ValueError will be raised when trying to assign None to
        permission_groups property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "permission_groups",
            None
        )
    
    
    
    ##----------------------------------------------------------------------
    #def test_permission_groups_argument_for_empty_list(self):
        #"""testing if a ValueError will be raised when trying to assign an
        #empty list to the permission_groups argument
        #"""
        
        #test_value = []
        
        #self.assertRaises(
            #ValueError,
            #user.User,
            #name=self.name,
            #first_name=self.first_name,
            #last_name=self.last_name,
            #description=self.description,
            #email=self.email,
            #password=self.password,
            #login_name=self.login_name,
            #department=self.mock_department1,
            #permission_groups=test_value,
            #tasks=[self.mock_task1,
                   #self.mock_task2,
                   #self.mock_task3,
                   #self.mock_task4],
            #projects=[self.mock_project1,
                      #self.mock_project2,
                      #self.mock_project3],
            #projects_lead=[self.mock_project1,
                           #self.mock_project2],
            #sequences_lead=[self.mock_sequence1,
                            #self.mock_sequence2,
                            #self.mock_sequence3,
                            #self.mock_sequence4],
            #created_by=self.mock_admin,
            #updated_by=self.mock_admin
        #)
    
    
    
    ##----------------------------------------------------------------------
    #def test_permission_groups_property_for_empty_list(self):
        #"""testing if a ValueError will be raised when trying to assign an
        #empty list to the permission_groups property
        #"""
        
        #self.assertRaises(
            #ValueError,
            #setattr,
            #self.mock_user,
            #"permission_groups",
            #[]
        #)
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_argument_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group argument
        """
        
        test_values = [23123,
                       1231.43122,
                       "a_group",
                       ["group1", "group2", 234],
                       ]
        
        for test_value in test_values:
            self.kwargs["permission_groups"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_perimssion_groups_property_accepts_only_group_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other then a Group object to the permission_group property
        """
        
        test_values = [23123,
                       1231.43122,
                       "a_group",
                       ["group1", "group2", 234],
                       ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "permission_groups",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_permission_groups_property_works_properly(self):
        """testing if permission_groups property works properly
        """
        
        test_pg = [self.mock_permission_group3]
        self.mock_user.permission_groups = test_pg
        self.assertEquals(self.mock_user.permission_groups, test_pg)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks argument
        """
        
        self.kwargs["tasks"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the tasks argument
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "tasks",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks argument
        """
        
        test_values = [ 12312, 1233244.2341, ["aTask1", "aTask2"], "a_task"]
        
        for test_value in test_values:
            self.kwargs["tasks"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_only_list_of_task_objects(self):
        """testing if a ValueError will be raised when trying to assign
        anything other than a list of task objects to the tasks argument
        """
        
        test_values = [ 12312, 1233244.2341, ["aTask1", "aTask2"], "a_task"]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "tasks",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_argument_accepts_an_empty_list(self):
        """testing if nothing happens when trying to assing an empty list to
        tasks argument
        """
        
        self.kwargs["tasks"] = []
        
        # this should work without any error
        aUserObj = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_tasks_property_accepts_an_empty_list(self):
        """testing if nothing happends when trying to assign an empty list to
        tasks property
        """
        
        # this should work without any error
        self.mock_user.tasks = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_argument_accepts_an_empty_list(self):
        """testing if projects argument accepts an empty list
        """
        
        self.kwargs["projects"] = []
        
        # this should work properly
        user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_an_empty_list(self):
        """testing if projects property accepts an empty list
        """
        
        # this should work properly
        self.mock_user.projects = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_argument_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects argument
        """
        
        self.kwargs["projects"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_None(self):
        """testing if a ValueError will be raised when trying to assign None
        to the projects property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "projects",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_argument_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects project argument
        """
        
        test_values = [ 123123, 1231.2132, ["a_project1", "a_project2"] ]
        
        for test_value in test_values:
            self.kwargs["projects"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_property_accepts_only_a_list_of_project_objs(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects to projects property
        """
        
        test_values = [ 123123, 1231.2132, ["a_project1", "a_project2"] ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "projects",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_argument_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the projects_lead argument
        """
        
        self.kwargs["projects_lead"] = None
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the projects_lead property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "projects_lead",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_argument_accepts_empty_list(self):
        """testing if projects_lead argument accepts an empty list
        """
        
        self.kwargs["projects_lead"] = []
        
        # this should work without any problems
        self.mock_user = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_accepts_empty_list(self):
        """testing if projects_lead property accepts an empty list
        """
        
        # this should work without any problem
        self.mock_user.projects_lead = []
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_argument_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead argument
        """
        
        test_values = ["a project", 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.kwargs["projects_lead"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_argument_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead argument
        """
        
        test_value = ["a project", 123123, [], {}, 12.2132 ]
        self.kwargs["projects_lead"] = test_value
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_property_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        projects_lead property
        """
        
        test_values = ["a project", 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.assertRaises(
                ValueError,
                setattr,
                self.mock_user,
                "projects",
                test_value
            )
    
    
    
    #----------------------------------------------------------------------
    def test_projects_lead_prop_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        projects_lead property
        """
        
        test_value = ["a project", 123123, [], {}, 12.2132 ]
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "projects_lead",
            test_value
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_argument_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the sequences_lead argument
        """
        
        self.kwargs["sequences_lead"] = None
        
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_property_None(self):
        """testing if a ValueError will be raised when tyring to assign None to
        the sequences_lead property
        """
        
        self.assertRaises(
            ValueError,
            setattr,
            self.mock_user,
            "sequences_lead",
            None
        )
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_argument_accepts_empty_list(self):
        """testing if sequences_lead argument accepts an empty list
        """
        
        self.kwargs["sequences_lead"] = []
        
        #this should work
        a_user = user.User(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_property_accepts_empty_list(self):
        """testing if sequences_lead property accepts an empty list
        """
        
        # this should work without any error
        self.mock_user.leader_of_seuqences = []
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_argument_accepts_only_lits(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead argument
        """
        
        test_values = ["a sequence", 123123, {}, 12.2132 ]
        
        for test_value in test_values:
            self.kwargs["sequences_lead"] = test_value
            self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_argument_accepts_only_lits_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assign a list
        of other objects than a list of Project objects to the
        sequences_lead argument
        """
        
        test_value = ["a sequence", 123123, [], {}, 12.2132 ]
        self.kwargs["sequences_lead"] = test_value
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_sequences_lead_property_accepts_only_list_of_project_obj(self):
        """testing if a ValueError will be raised when trying to assing a list
        of other object than a list of Project objects to the
        sequences_lead property
        """
        
        test_value = ["a sequence", 123123, [], {}, 12.2132 ]
        self.kwargs["sequences_lead"] = test_value
        self.assertRaises(ValueError, user.User, **self.kwargs)
    
    
    