#-*- coding: utf-8 -*-



import datetime
import mocker
from stalker.conf import defaults
from stalker.core.errors import CircularDependencyError
from stalker.core.models import (SimpleEntity, Entity, Task, User, Status,
                                 StatusList, Project, Type)
from stalker.ext.validatedList import ValidatedList





########################################################################
class TaskTester(mocker.MockerTestCase):
    """Tests the stalker.core.models.Task class
    """
    
    
    
    #----------------------------------------------------------------------
    def setUp(self):
        """setup the test
        """
        
        status_wip = Status(name="Work In Progress", code="WIP")
        status_complete = Status(name="Complete", code="CMPLT")
        status_pending_review = Status(name="Pending Review", code="PNDR")
        
        task_status_list = StatusList(
            name="Task Statuses",
            statuses=[status_wip, status_pending_review, status_complete],
            target_entity_type="Task",
        )
        
        self.mock_user1 = self.mocker.mock(User)
        self.mock_user2 = self.mocker.mock(User)
        
        self.expect(self.mock_user1.tasks).result([]).count(0, None)
        self.expect(self.mock_user2.tasks).result([]).count(0, None)
        self.expect(self.mock_user1._tasks).result([]).count(0, None)
        self.expect(self.mock_user2._tasks).result([]).count(0, None)
        
        self.mock_dependent_task1 = self.mocker.mock(Task)
        self.mock_dependent_task2 = self.mocker.mock(Task)
        
        self.expect(self.mock_dependent_task1.depends).\
            result([]).count(0, None)
        
        self.expect(self.mock_dependent_task2.depends).\
            result([]).count(0, None)
        
        # for part_of attribute tests
        self.mock_simpleEntity = self.mocker.mock(SimpleEntity)
        self.mock_entity = self.mocker.mock(Entity)
        
        self.expect(self.mock_simpleEntity.tasks).result([]).count(0, None)
        self.expect(self.mock_entity.tasks).result([]).count(0, None)
        
        ## task dependency relation 1
        #self.mock_taskDependencyRelation1 =\
            #self.mocker.mock(TaskDependencyRelation)
        
        #self.expect(self.mock_taskDependencyRelation1.depends).\
            #result(self.mock_dependent_task1).count(0, None)
        
        #self.expect(self.mock_taskDependencyRelation1.lag).\
            #result(0).count(0, None)
        
        ## task dependency relation 2
        #self.mock_taskDependencyRelation2 =\
            #self.mocker.mock(TaskDependencyRelation)
        
        #self.expect(self.mock_taskDependencyRelation2.depends).\
            #result(self.mock_dependent_task2).count(0, None)
        
        #self.expect(self.mock_taskDependencyRelation2.lag).\
            #result(0).count(0, None)
        
        self.mock_project = self.mocker.mock(Project)
        
        self.mocker.replay()
        
        self.kwargs = {
            "name": "Modeling",
            "description": "A Modeling Task",
            "priority": 500,
            "resources": [self.mock_user1, self.mock_user2],
            "effort": datetime.timedelta(4),
            "duration": datetime.timedelta(2),
            "depends": [self.mock_dependent_task1,
                        self.mock_dependent_task2],
            "complete": False,
            "bookings": [],
            "versions": [],
            "milestone": False,
            "status": 0,
            "status_list": task_status_list,
            "project": self.mock_project,
            "part_of": self.mock_simpleEntity,
        }
        
        # create a mock Task
        self.mock_task = Task(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_skipped_defaults_to_DEFAULT_TASK_PRIORITY(self):
        """testing if skipping the priority argument will default the priority
        attribute to DEFAULT_TASK_PRIORITY.
        """
        
        self.kwargs.pop("priority")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, defaults.DEFAULT_TASK_PRIORITY)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_given_as_None_will_default_to_DEFAULT_TASK_PRIORITY(self):
        """testing if the priority argument is given as None will default the
        priority attribute to DEFAULT_TASK_PRIORITY.
        """
        
        self.kwargs["priority"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, defaults.DEFAULT_TASK_PRIORITY)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_given_as_None_will_default_to_DEFAULT_TASK_PRIORITY(self):
        """testing if the priority attribute is given as None will default the
        priority attribute to DEFAULT_TASK_PRIORITY.
        """
        
        self.mock_task.priority = None
        self.assertEqual(self.mock_task.priority,
                         defaults.DEFAULT_TASK_PRIORITY)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_any_given_other_value_then_integer_will_default_to_DEFAULT_TASK_PRIORITY(self):
        """testing if any other value then an positif integer for priority
        argument will default the priority attribute to DEFAULT_TASK_PRIORITY.
        """
        
        test_values = ["a324", None, []]
        
        for test_value in test_values:
            self.kwargs["priority"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.priority, defaults.DEFAULT_TASK_PRIORITY)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_any_given_other_value_then_integer_will_default_to_DEFAULT_TASK_PRIORITY(self):
        """testing if any other value then an positif integer for priority
        attribute will default it to DEFAULT_TASK_PRIORITY.
        """
        
        test_values = ["a324", None, []]
        
        for test_value in test_values:
            self.mock_task.priority = test_value
            self.assertEqual(self.mock_task.priority,
                             defaults.DEFAULT_TASK_PRIORITY)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_negative(self):
        """testing if the priority argument is given as a negative value will
        set the priority attribute to zero.
        """
        
        self.kwargs["priority"] = -1
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, 0)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_negative(self):
        """testing if the priority attribute is given as a negative value will
        set the priority attribute to zero.
        """
        
        self.mock_task.priority = -1
        self.assertEqual(self.mock_task.priority, 0)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_too_big(self):
        """testing if the priority argument is given bigger then 1000 will
        clamp the priority attribute value to 1000
        """
        
        self.kwargs["priority"] = 1001
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.priority, 1000)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_too_big(self):
        """testing if the priority attribute is set to a value bigger than 1000
        will clamp the value to 1000
        """
        
        self.mock_task.priority = 1001
        self.assertEqual(self.mock_task.priority, 1000)
    
    
    
    #----------------------------------------------------------------------
    def test_priority_argument_is_float(self):
        """testing if float numbers for prority argument will be converted to
        integer
        """
        
        test_values = [500.1, 334.23]
        
        for test_value in test_values:
            self.kwargs["priority"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.priority, int(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_float(self):
        """testing if float numbers for priority attribute will be converted to
        integer
        """
        
        test_values = [500.1, 334.23]
        
        for test_value in test_values:
            self.mock_task.priority = test_value
            self.assertEqual(self.mock_task.priority, int(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_priority_attribute_is_working_properly(self):
        """testing if the priority attribute is working properly
        """
        
        test_value = 234
        self.mock_task.priority = test_value
        self.assertEqual(self.mock_task.priority, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_skipped(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is skipped
        """
        
        self.kwargs.pop("resources")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_None(self):
        """testing if the resources attribute will be an empty list when the
        resources argument is None
        """
        
        self.kwargs["resources"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_None(self):
        """testing if the resources attribute will be an empty list when it is
        set to None
        """
        
        self.mock_task.resources = None
        self.assertEqual(self.mock_task.resources, [])
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_not_list(self):
        """testing if a TypeError will be raised when the resources argument is
        not a list
        """
        
        self.kwargs["resources"] = "a resource"
        self.assertRaises(TypeError, Task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_not_list(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to any other value then a list
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "resources",
                          "a resource")
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources argument is
        set to a list of other values then a User
        """
        
        self.kwargs["resources"] = ["a", "list", "of", "resources",
                                    self.mock_user1]
        self.assertRaises(TypeError, Task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_set_to_a_list_of_other_values_then_User(self):
        """testing if a TypeError will be raised when the resources attribute
        is set to a list of other values then a User
        """
        
        self.kwargs["resources"] = ["a", "list", "of", "resources",
                                    self.mock_user1]
        self.assertRaises(TypeError, self.mock_task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_instance_of_ValidatedList(self):
        """testing if the resources attribute is an instance of ValidatedList
        """
        
        self.assertIsInstance(self.mock_task.resources, ValidatedList)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_is_working_properly(self):
        """testing if the resources attribute is working properly
        """
        
        test_value = [self.mock_user1]
        self.mock_task.resources = test_value
        self.assertEqual(self.mock_task.resources, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_argument_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        
        # create a new user
        new_user = User(first_name="Test",
                        last_name="User",
                        login_name="testuser",
                        email="testuser@test.com",
                        password="testpass")
        
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_backreferences_to_User(self):
        """testing if the User instances passed with the resources argument
        will have the current task in their User.tasks attribute
        """
        
        # create a new user
        new_user = User(first_name="Test",
                        last_name="User",
                        login_name="testuser",
                        email="testuser@test.com",
                        password="testpass")
        
        # assign it to a newly created task
        #self.kwargs["resources"] = [new_user]
        new_task = Task(**self.kwargs)
        new_task.resources = [new_user]
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user.tasks)
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_clear_itself_from_the_previous_Users(self):
        """testing if the resources attribute is updated will clear itself from
        the current resources tasks attribute.
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources = [new_user3, new_user4]
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
        
        # and if it is not in the previous users tasks
        self.assertNotIn(new_task, new_user1.tasks)
        self.assertNotIn(new_task, new_user2.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle_append(self):
        """testing if the resources attribute will handle appending users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources.append(new_user3)
        new_task.resources.append(new_user4)
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle_extend(self):
        """testing if the resources attribute will handle extendeding users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources.extend([new_user3, new_user4])
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle___setitem__(self):
        """testing if the resources attribute will handle __setitem__ing users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources[0] = new_user3
        new_task.resources[1] = new_user4
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
        
        # and check if the first and second tasks doesn't have task anymore
        self.assertNotIn(new_task, new_user1.tasks)
        self.assertNotIn(new_task, new_user2.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle___setslice__(self):
        """testing if the resources attribute will handle __setslice__ing users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources[1:2] = [new_user3, new_user4]
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
        
        # and check if the first and second tasks doesn't have task anymore
        self.assertNotIn(new_task, new_user2.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle_insert(self):
        """testing if the resources attribute will handle inserting users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources.insert(0, new_user3)
        new_task.resources.insert(0, new_user4)
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle___add__(self):
        """testing if the resources attribute will handle __add__ing users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources = new_task.resources + [new_user3, new_user4]
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle___iadd__(self):
        """testing if the resources attribute will handle __iadd__ing users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        new_user3 = User(first_name="Test3",
                         last_name="User3",
                         login_name="testuser3",
                         email="testuser3@test.com",
                         password="testpass")
        
        new_user4 = User(first_name="Test4",
                         last_name="User4",
                         login_name="testuser4",
                         email="testuser4@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now update the resources list
        new_task.resources += [new_user3, new_user4]
        
        # now check if the new resources has the task in their tasks attribute
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        self.assertIn(new_task, new_user3.tasks)
        self.assertIn(new_task, new_user4.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle_pop(self):
        """testing if the resources attribute will handle popping users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now pop the resources
        new_task.resources.pop(0)
        self.assertNotIn(new_task, new_user1.tasks)
        
        new_task.resources.pop()
        self.assertNotIn(new_task, new_user2.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_resources_attribute_will_handle_remove(self):
        """testing if the resources attribute will handle removing users
        """
        
        # create a couple of new users
        new_user1 = User(first_name="Test1",
                         last_name="User1",
                         login_name="testuser1",
                         email="testuser1@test.com",
                         password="testpass")
        
        new_user2 = User(first_name="Test2",
                         last_name="User2",
                         login_name="testuser2",
                         email="testuser2@test.com",
                         password="testpass")
        
        # now add the 1 and 2 to the resources with the resources argument
        # assign it to a newly created task
        self.kwargs["resources"] = [new_user1, new_user2]
        new_task = Task(**self.kwargs)
        
        # now check if the user has the task in its tasks list
        self.assertIn(new_task, new_user1.tasks)
        self.assertIn(new_task, new_user2.tasks)
        
        # now pop the resources
        new_task.resources.remove(new_user1)
        self.assertNotIn(new_task, new_user1.tasks)
        
        new_task.resources.remove(new_user2)
        self.assertNotIn(new_task, new_user2.tasks)
    
    
    
    #----------------------------------------------------------------------
    def test_effort_and_duration_argument_is_skipped(self):
        """testing if the effort attribute is set to the default value of
        duration divided by the number of resources
        """
        
        self.kwargs.pop("effort")
        self.kwargs.pop("duration")
        
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.duration, defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_task.effort, defaults.DEFAULT_TASK_DURATION *
                         len(new_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_skipped_but_duration_is_present(self):
        """testing if the effort argument is skipped but the duration is
        present the effort attribute is calculated from the
        duration * len(resources) formula
        """
        
        self.kwargs.pop("effort")
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.duration, self.kwargs["duration"])
        self.assertEqual(new_task.effort, new_task.duration *
                         len(new_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_present_but_duration_is_skipped(self):
        """testing if the effort argument is present but the duration is
        skipped the duration attribute is calculated from the
        effort / len(resources) formula
        """
        
        self.kwargs.pop("duration")
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.effort, self.kwargs["effort"])
        self.assertEqual(new_task.duration, new_task.effort /
                         len(new_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_and_duration_argument_is_None(self):
        """testing if the effort and duration is None then effort will be
        calculated from the value of duration and count of resources
        """
        
        self.kwargs["effort"] = None
        self.kwargs["duration"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.duration, defaults.DEFAULT_TASK_DURATION)
        self.assertEqual(new_task.effort, new_task.duration *
                         len(new_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_set_to_None(self):
        """testing if the effort attribute is set to None then the effort is
        calculated from duration and count of resources
        """
        
        self.mock_task.effort = None
        self.assertEqual(self.mock_task.effort, self.mock_task.duration *
                         len(self.mock_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_is_not_an_instance_of_timedelta(self):
        """testing if effort attribute is calculated from the duration
        attribute when the effort argument is not an instance of timedelta
        """
        
        self.kwargs["effort"] = "not a timedelta"
        new_task = Task(**self.kwargs)
        self.assertIsInstance(new_task.effort, datetime.timedelta)
        self.assertEqual(new_task.effort, new_task.duration *
                         len(new_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_not_an_instance_of_timedelta(self):
        """testing if effort attribute is calculated from the duration
        attribute when it is set to something else then a timedelta instance.
        """
        
        self.mock_task.effort = "not a timedelta"
        self.assertIsInstance(self.mock_task.effort, datetime.timedelta)
        self.assertEqual(self.mock_task.effort, self.mock_task.duration *
                         len(self.mock_task.resources))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_is_working_properly(self):
        """testing if the effort attribute is working properly
        """
        
        test_value = datetime.timedelta(18)
        self.mock_task.effort = test_value
        self.assertEqual(self.mock_task.effort, test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_effort_argument_preceeds_duration_argument(self):
        """testing if the effort argument is preceeds duration argument 
        """
        
        self.kwargs["effort"] = datetime.timedelta(40)
        self.kwargs["duration"] = datetime.timedelta(2)
        
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.effort, self.kwargs["effort"])
        self.assertEqual(new_task.duration, self.kwargs["effort"] /
                         len(self.kwargs["resources"]))
    
    
    
    #----------------------------------------------------------------------
    def test_effort_attribute_changes_duration(self):
        """testing if the effort attribute changes the duration
        """
        
        test_effort = datetime.timedelta(100)
        test_duration = test_effort / len(self.mock_task.resources)
        
        # be sure it is not already in the current value
        self.assertNotEqual(self.mock_task.duration, test_duration)
        
        self.mock_task.effort = test_effort
        
        self.assertEqual(self.mock_task.duration, test_duration)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_changes_effort(self):
        """testing if the duration attribute changes the effort attribute value
        by the effort = duration / len(resources) formula
        """
        
        test_duration = datetime.timedelta(100)
        test_effort = test_duration * len(self.mock_task.resources)
        
        # be sure it is not already in the current value
        self.assertNotEqual(self.mock_task.effort, test_effort)
        
        self.mock_task.duration = test_duration
        
        self.assertEqual(self.mock_task.effort, test_effort)
    
    
    
    #----------------------------------------------------------------------
    def test_duration_attribute_will_be_equal_to_effort_if_there_is_no_resources_argument(self):
        """testing if the duration will be equal to the effort if there is no
        resource assigned
        """
        
        self.kwargs.pop("resources")
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.effort, self.kwargs["effort"])
        self.assertEqual(new_task.effort, new_task.duration)
    
    
    
    #----------------------------------------------------------------------
    def test_depends_argument_is_skipped_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is skipped
        """
        
        self.kwargs.pop("depends")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.depends, [])
    
    
    
    #----------------------------------------------------------------------
    def test_depends_argument_is_none_depends_attribute_is_empty_list(self):
        """testing if the depends attribute is an empty list when the depends
        argument is None
        """
        
        self.kwargs["depends"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.depends, [])
    
    
    
    #----------------------------------------------------------------------
    def test_depends_argument_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends argument is
        not a list
        """
        
        self.kwargs["depends"] = self.mock_dependent_task1
        self.assertRaises(TypeError, Task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the depends attribute is
        set to something else then a list
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "depends",
                          self.mock_dependent_task1)
    
    
    
    #----------------------------------------------------------------------
    def test_depends_argument_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a TypeError will be raised when the depends argument is
        a list of other typed objects than Task
        """
        
        test_value = ["a", "dependent", "task", 1, 1.2]
        self.kwargs["depends"] = test_value
        self.assertRaises(TypeError, Task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_is_a_list_of_other_objects_than_a_Task(self):
        """testing if a TypeError will be raised when the depends attribute is
        set to a list of other typed objects than Task
        """
        
        test_value = ["a", "dependent", "task", 1, 1.2]
        self.assertRaises(TypeError, setattr, self.mock_task, "depends",
                          test_value)
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_is_a_ValidatedList_instance(self):
        """testing if the depends attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_task.depends, ValidatedList)
    
    
    
    ##----------------------------------------------------------------------
    #def test_depends_argument_shifts_the_start_date_by_traversing_dependency_list(self):
        #"""testing if the depends argument shifts the start_date attribute by
        #traversing the dependent tasks list and placing the current task after
        #the latest dependent task
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_depends_attribute_shifts_the_start_date_by_traversing_dependency_list(self):
        #"""testing if the depends attribute shifts the start_date attribute by
        #traversing the dependent tasks list
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_doesnt_allow_simple_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a simple circurlar dependency in dependencies
        """
        
        # create two new tasks A, B
        # make B dependent to A
        # and make A dependent to B
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None
        
        taskA = Task(**self.kwargs)
        taskB = Task(**self.kwargs)
        
        taskB.depends = [taskA]
        
        self.assertRaises(CircularDependencyError, setattr, taskA, "depends",
                          [taskB])
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_doesnt_allow_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a circurlar dependency in dependencies
        """
        
        # create three new tasks A, B, C
        # make B dependent to A
        # make C dependent to B
        # and make A dependent to C
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None
        
        taskA = Task(**self.kwargs)
        taskB = Task(**self.kwargs)
        taskC = Task(**self.kwargs)
        
        taskB.depends = [taskA]
        taskC.depends = [taskB]
        
        self.assertRaises(CircularDependencyError, setattr, taskA, "depends",
                          [taskC])
    
    
    
    #----------------------------------------------------------------------
    def test_depends_attribute_doesnt_allow_more_deeper_cyclic_dependencies(self):
        """testing if a CircularDependencyError will be raised when the depends
        attribute has a deeper circular dependency in dependencies
        """
        
        # create new tasks A, B, C, D
        # make B dependent to A
        # make C dependent to B
        # make D dependent to C
        # and make A dependent to D
        # and expect a CircularDependencyError
        self.kwargs["depends"] = None
        
        taskA = Task(**self.kwargs)
        taskB = Task(**self.kwargs)
        taskC = Task(**self.kwargs)
        taskD = Task(**self.kwargs)
        
        taskB.depends = [taskA]
        taskC.depends = [taskB]
        taskD.depends = [taskC]
        
        self.assertRaises(CircularDependencyError, setattr, taskA, "depends",
                          [taskD])
    
    
    
    
    
    
    
    ##----------------------------------------------------------------------
    #def test_complete_argument_is_skipped(self):
        #"""testing if the default value of the complete attribute is going to
        #be False when the complete argument is skipped
        #"""
        
        #self.kwargs.pop("complete")
        #new_task = Task(**self.kwargs)
        #self.assertEqual(new_task.complete, False)
    
    
    
    ##----------------------------------------------------------------------
    #def test_complete_argument_is_None(self):
        #"""testing if the complete attribute will be set to False when the
        #complete argument is given as None
        #"""
        
        #self.kwargs["complete"] = None
        #new_task = Task(**self.kwargs)
        #self.assertEqual(new_task.complete, False)
    
    
    
    #----------------------------------------------------------------------
    def test_complete_attribute_is_None(self):
        """testing if the complete attribute will be False when set to None
        """
        
        self.mock_task.complete = None
        self.assertEqual(self.mock_task.complete, False)
    
    
    
    ##----------------------------------------------------------------------
    #def test_complete_argument_evaluates_the_given_value_to_a_bool(self):
        #"""testing if the complete attribute is evaluated correctly to a bool
        #value when the complete argument is anything other than a bool value.
        #"""
        
        #test_values = [1, 0, 1.2, "A string", "", [], [1]]
        
        #for test_value in test_values:
            #self.kwargs["complete"] = test_value
            #new_task = Task(**self.kwargs)
            #self.assertEqual(new_task.complete, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_complete_attribute_evaluates_the_given_value_to_a_bool(self):
        """testing if the complete attribute is evaluated correctly to a bool
        valnue when set to anything other than a bool value.
        """
        
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        
        for test_value in test_values:
            self.mock_task.complete = test_value
            self.assertEqual(self.mock_task.complete, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_argument_is_skipped(self):
        """testing if the default value of the milestone attribute is going to
        be False when the milestone argument is skipped
        """
        
        self.kwargs.pop("milestone")
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.milestone, False)
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_argument_is_None(self):
        """testing if the milestone attribute will be set to False when the
        milestone argument is given as None
        """
        
        self.kwargs["milestone"] = None
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.milestone, False)
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_attribute_is_None(self):
        """testing if the milestone attribute will be False when set to None
        """
        
        self.mock_task.milestone = None
        self.assertEqual(self.mock_task.milestone, False)
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_argument_evaluates_the_given_value_to_a_bool(self):
        """testing if the milestone attribute is evaluated correctly to a bool
        value when the milestone argument is anything other than a bool value.
        """
        
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        
        for test_value in test_values:
            self.kwargs["milestone"] = test_value
            new_task = Task(**self.kwargs)
            self.assertEqual(new_task.milestone, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_attribute_evaluates_the_given_value_to_a_bool(self):
        """testing if the milestone attribute is evaluated correctly to a bool
        valnue when set to anything other than a bool value.
        """
        
        test_values = [1, 0, 1.2, "A string", "", [], [1]]
        
        for test_value in test_values:
            self.mock_task.milestone = test_value
            self.assertEqual(self.mock_task.milestone, bool(test_value))
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_argument_makes_the_resources_list_an_empty_list(self):
        """testing if the resources will be an empty list when the milestone
        argument is given as True
        """
        
        self.kwargs["milestone"] = True
        self.kwargs["resources"] = [self.mock_user1, self.mock_user2]
        
        new_task = Task(**self.kwargs)
        self.assertEqual(new_task.resources, [])
    
    
    
    #----------------------------------------------------------------------
    def test_milestone_attribute_makes_the_resource_list_an_empty_list(self):
        """testing if the resources will be an empty list when the milestone
        attribute is given as True
        """
        
        self.mock_task.resources = [self.mock_user1, self.mock_user2]
        self.mock_task.milestone = True
        self.assertEqual(self.mock_task.resources, [])
    
    
    
    ##----------------------------------------------------------------------
    #def test_bookings_argument_is_skipped(self):
        #"""testing if the bookings attribute will be an empty list when the
        #bookings argument is skipped
        #"""
        
        #self.kwargs.pop("bookings")
        #new_task = Task(**self.kwargs)
        #self.assertEqual(new_task.bookings, [])
    
    
    
    ##----------------------------------------------------------------------
    #def test_bookings_argument_is_None(self):
        #"""testing if the booking attribute will be an empty list when the
        #bookings argument is None
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_bookings_attribute_is_None(self):
        """testing if the bookings attribute will be an empty list when it is
        set to None
        """
        
        self.mock_task.bookings = None
        self.assertEqual(self.mock_task.bookings, [])
    
    
    
    ##----------------------------------------------------------------------
    #def test_bookings_argument_is_not_a_list(self):
        #"""testing if a TypeError will be raised when the bookings argument is
        #not a list
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_bookings_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the bookings attribute is
        not set to a list
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "bookings", 123)
    
    
    
    ##----------------------------------------------------------------------
    #def test_bookings_argument_is_not_a_list_of_Booking_instances(self):
        #"""testing if a TypeError will be raised when the bookings argument is
        #not a list of Booking instances
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_bookings_attribute_is_not_a_list_of_Booking_instances(self):
        """testing if a TypeError will be raised when the bookings attribute is
        not a list of Booking instances
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "bookings",
                          [1, "1", 1.2, "a booking", []])
    
    
    
    #----------------------------------------------------------------------
    def test_bookings_attribute_is_a_ValidatedList_instance(self):
        """testing if the bookings attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_task.bookings, ValidatedList)
    
    
    
    ##----------------------------------------------------------------------
    #def test_versions_argument_is_skipped(self):
        #"""testing if the versions attribute will be an empty list when the
        #versions argument is skipped
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_versions_argument_is_None(self):
        #"""testing if the versions attribute will be an empty list when the
        #versions argument is None
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_versions_attribute_is_None(self):
        """testing if the versions attribute will be an empty list when it is
        set to None
        """
        
        self.mock_task.versions = None
        self.assertEqual(self.mock_task.versions, [])
    
    
    
    ##----------------------------------------------------------------------
    #def test_versions_argument_is_not_a_list(self):
        #"""testing if a TypeError will be raised when the versions argument is
        #not a list
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_versions_attribute_is_not_a_list(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a value other than a list
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "versions", 1)
    
    
    
    ##----------------------------------------------------------------------
    #def test_versions_argument_is_not_a_list_of_Version_instances(self):
        #"""testing if a TypeError will be raised when the versions argument is
        #a list of other objects than Version instances
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_versions_attribute_is_not_a_list_of_Version_instances(self):
        """testing if a TypeError will be raised when the versions attribute is
        set to a list of other objects than Version instances
        """
        
        self.assertRaises(TypeError, setattr, self.mock_task, "versions",
                          [1, 1.2, "a version"])
    
    
    
    #----------------------------------------------------------------------
    def test_versions_attribute_is_a_ValidatedList_instance(self):
        """testing if the versions attribute is a ValidatedList instance
        """
        
        self.assertIsInstance(self.mock_task.versions, ValidatedList)
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_argument_is_skiped(self):
        #"""testing if the parent_task attribute will be None when the
        #parent_task argument is skipped.
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_argument_is_None(self):
        #"""testing if the parent_task attribute will be None when the
        #parent_task argument is None
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_attribute_is_set_to_None(self):
        #"""testing if the parent_task attribute will be None when it is set to
        #None.
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_argument_is_not_a_Task_instance(self):
        #"""testing if a TypeError will be raised when the parent_task argument
        #is not a Task instance
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_attribute_is_not_a_Task_instance(self):
        #"""testing if a TypeError will be raised when the parent_task argument
        #is not a Task instance
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_argument_is_a_Task_instance(self):
        #"""testing if the Task given with the parent_task argument will have
        #the new task in its sub_tasks attribute
        #"""
        
        #self.fail("test is not implemented yet")
    
    
    
    ##----------------------------------------------------------------------
    #def test_parent_task_attribute_is_a_Task_instance(self):
        #"""testing if the Task given with the parent_task attribute will have
        #the current task in its sub_tasks attribute
        #"""
        
        #self.fail("test is not implented yet")
    
    
    
    #----------------------------------------------------------------------
    def test_equality(self):
        """testing the equality operator
        """
        
        entity1 = Entity(**self.kwargs)
        task1 = Task(**self.kwargs)
        
        self.assertFalse(self.mock_task==entity1)
        self.assertTrue(self.mock_task==task1)
    
    
    
    #----------------------------------------------------------------------
    def test_inequality(self):
        """testing the inequality operator
        """
        
        entity1 = Entity(**self.kwargs)
        task1 = Task(**self.kwargs)
        
        self.assertTrue(self.mock_task!=entity1)
        self.assertFalse(self.mock_task!=task1)
    
    
    
    #----------------------------------------------------------------------
    def test_ProjectMixin_initialization(self):
        """testing if the ProjectMixin part is initialized correctly
        """
        
        status1 = Status(name="On Hold", code="OH")
        
        project_status_list = StatusList(
            name="Project Statuses", statuses=[status1],
            target_entity_type=Project.entity_type
        )
        
        project_type = Type(name="Commercial", target_entity_type=Project)
        
        new_project = Project(name="Test Project", status=0,
                              status_list=project_status_list,
                              type=project_type)
        
        self.kwargs["project"] = new_project
        
        new_task = Task(**self.kwargs)
        
        self.assertEqual(new_task.project, new_project)
    
    
    
    #----------------------------------------------------------------------
    def test_part_of_argument_accepts_anything_deriving_from_the_SimpleEntity(self):
        """testing if the part_of attribute accepts anything deriving from
        SimpleEntity
        """
        
        self.kwargs["part_of"] = self.mock_entity
        new_task = Task(**self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_part_of_attribute_accepts_anything_deriving_from_the_SimpleEntity(self):
        """testing if  the part_of attribute accepts anything deriving from
        SimpleEntity
        """
        
        self.mock_task.part_of = self.mock_entity
    
    
    
    #----------------------------------------------------------------------
    def test_part_of_argument_accepts_only_SimpleEntity_derivatives(self):
        """testing if a TypeError will be raised when the part_of argument has
        something which is not derived from the SimpleEntity
        """
        self.kwargs["part_of"] = 1
        self.assertRaises(TypeError, Task, **self.kwargs)
    
    
    
    #----------------------------------------------------------------------
    def test_part_of_attribute_accepts_only_SimpleEntity_derivatives(self):
        """testing if a TypeError will be raised when the part_of attribute has
        something which is not derived from the SimpleEntity
        """
        self.assertRaises(TypeError, setattr, self.mock_task, "part_of", 1)
    
    
    
    #----------------------------------------------------------------------
    def test_part_of_attribute_updates_the_back_reference_attribute_tasks(self):
        """testing if the part_of updates the back reference attribute which
        is called tasks
        """
        
        # create a project and test if the Task.part_of will also update the
        # project.tasks attribute
        
        status_complete = Status(name="complete", code="CMPLT")
        status_wip = Status(name="work in progress", code="WIP")
        
        project_status_list = StatusList(
            name="Project Status List",
            target_entity_type=Project,
            statuses=[status_complete, status_wip],
        )
        
        project_type_commercial = Type(
            name="Commercial",
            target_entity_type=Project,
        )
        
        new_project1 = Project(
            name="Test Project 1",
            status_list=project_status_list,
            type=project_type_commercial,
        )
        
        new_project2 = Project(
            name="Test Project 2",
            status_list=project_status_list,
            type=project_type_commercial,
        )
        
        # create a Task
        task_status_list = StatusList(
            name="Task Status List",
            target_entity_type=Task,
            statuses=[status_complete, status_wip],
        )
        
        new_task = Task(
            name="Modeling",
            project=new_project1,
            status_list=task_status_list,
            part_of=new_project1,
        )
        
        # now assign a new project to the part of attribute
        new_task.part_of = new_project2
        self.assertNotIn(new_task, new_project1.tasks)
        self.assertIn(new_task, new_project2.tasks)
        
        
    
    
    