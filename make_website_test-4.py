import unittest
import os
from make_website import *

class MakeWebsite_Test(unittest.TestCase):

    def test_surround_block(self):
        # test text with surrounding h1 tags
        self.assertEqual("<h1>Eagles</h1>", surround_block('h1', 'Eagles'))

        # test text with surrounding h2 tags
        self.assertEqual("<h2>Red Sox</h2>", surround_block('h2', 'Red Sox'))

        # test text with surrounding p tags
        self.assertEqual('<p>Lorem ipsum dolor sit amet, consectetur ' +
                         'adipiscing elit. Sed ac felis sit amet ante porta ' +
                         'hendrerit at at urna.</p>',
                         surround_block('p', 'Lorem ipsum dolor sit amet, consectetur ' +
                                        'adipiscing elit. Sed ac felis sit amet ante porta ' +
                                        'hendrerit at at urna.'))

    def test_create_email_link(self):

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>',
            create_email_link('lbrandon@wharton.upenn.edu')
        )

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:krakowsky@outlook.com">krakowsky[aT]outlook.com</a>',
            create_email_link('krakowsky@outlook.com')
        )

        # test email without @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon.at.seas.upenn.edu">lbrandon.at.seas.upenn.edu</a>',
            create_email_link('lbrandon.at.seas.upenn.edu')
        )


    def test_get_name(self):
        """Tests the functionality of the `get_name` function.
        
        This function extracts the name from the content, which is typically the first line.
        Here, we test to ensure that it correctly fetches the name.
        """
        content = ["Brandon\n", "Email: test@upenn.edu\n", "Projects\n", "Test project\n", "----\n"]
        self.assertEqual(get_name(content), "Brandon")

    def test_get_email(self):
        """Tests the functionality of the `get_email` function.
        
        This function extracts and validates the email address from the content.
        We test with a standard content format to ensure it fetches the email correctly.
        """
        content = ["Brandon\n", "test@upenn.edu\n", "Projects\n", "Test project\n", "----\n"]
        self.assertEqual(get_email(content), "test@upenn.edu")

    def test_get_courses(self):
        """Tests the functionality of the `get_courses` function.
        
        This function extracts the list of courses from the content. 
        Here, we test with a standard content format to ensure it fetches the courses correctly.
        """
        content = ["Brandon\n", "Email: test@upenn.edu\n", "Courses - CIT590, AB120\n", "Projects\n", "Test project\n", "----\n"]
        self.assertEqual(get_courses(content), ["CIT590", "AB120"])

    def test_get_projects(self):
        """Tests the functionality of the `get_projects` function.
        
        This function extracts the list of projects from the content until it encounters lines with multiple '-' characters.
        We test to ensure it correctly fetches the list of projects.
        """
        content = ["Brandon\n", "Email: test@upenn.edu\n", "Courses - CIT590, AB120\n", "Projects\n", "Test project\n", "Another project\n", "----\n"]
        self.assertEqual(get_projects(content), ["Test project", "Another project"])

    def setUp(self):
        """
        Set up test environment before for following test case.
        
        Creates a sample 'test_resume.txt' file with predefined content.
        This method is automatically called before each test case is run.
        """
        with open("test_resume.txt", "w") as file:
            file.write("John Doe\njohndoe@example.com\nProjects\nProject A\nProject B\n----\nCourses\nCourse A, Course B\n")
        self.txt_input_file = "test_resume.txt"
        self.html_output_file = "test_output.html"

    def test_load_txt_file(self):
        """
        Test the load_txt_file function.
        
        Checks if the function correctly loads content from a .txt file into a list.
        """
        content = load_txt_file(self.txt_input_file)
        self.assertIsInstance(content, list)
        self.assertEqual(content[0].strip(), "John Doe")
        self.assertEqual(content[1].strip(), "johndoe@example.com")

    def test_generate_html(self):
        """
        Test the generate_html function.
        
        Checks if the function creates an HTML file based on the content of the given .txt file.
        """
        generate_html(self.txt_input_file, self.html_output_file)
        # Check if the HTML file exist
        self.assertTrue(os.path.exists(self.html_output_file))

    def test_write_html_content(self):
        """
        Test the write_html_content function.
        
        Checks if the function correctly formats and writes the given data into an HTML file.
        """
        name = "John Doe"
        email = "johndoe@example.com"
        projects = ["Project A", "Project B"]
        courses = ["Course A", "Course B"]
        write_html_content(name, email, projects, courses, self.html_output_file)
        # Read and check the content of the HTML file
        with open(self.html_output_file, "r") as file:
            content = file.read()
            self.assertIn(name, content)
            self.assertIn(email, content)
            for project in projects:
                self.assertIn(project, content)
            for course in courses:
                self.assertIn(course, content)

    def tearDown(self):
        # Remove the test file
        os.remove(self.txt_input_file)
        if os.path.exists(self.html_output_file):
            os.remove(self.html_output_file)

if __name__ == '__main__':
    unittest.main()
