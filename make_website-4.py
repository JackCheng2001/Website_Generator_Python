# TODO: Students, fill out statement of work header
# Student Name in Canvas: Cheng Erxi
# Penn ID: 62196105
# Did you do this homework on your own (yes / no): yes
# Resources used outside course materials: none


def surround_block(tag, text):
    """
    Surrounds the given text with the given html tag and returns the string.
    """

    # insert code
    return f"<{tag}>{text}</{tag}>"
    #pass

def create_email_link(email_address):
    """
    Creates an email link with the given email_address.
    To cut down on spammers harvesting the email address from the webpage,
    displays the email address with [aT] instead of @.

    Example: Given the email address: lbrandon@wharton.upenn.edu
    Generates the email link: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>

    Note: If, for some reason the email address does not contain @,
    use the email address as is and don't replace anything.
    """
    # insert code
    # If email_address contains "@", replace "@" with "[aT]" for display.
    # Otherwise, use email_address as it is.
    display_email = email_address.replace("@", "[aT]") if "@" in email_address else email_address   
    # Create and return the email link using the original email address for the "mailto:" part and 
    # the display_email for the link text
    return f'<a href="mailto:{email_address}">{display_email}</a>'
    

def generate_html(txt_input_file, html_output_file):
    """
    Loads given txt_input_file,
    gets the name, email address, list of projects, and list of courses,
    then writes the info to the given html_output_file.

    # Hint(s):
    # call function(s) to load given txt_input_file
    # call function(s) to get name
    # call function(s) to get email address
    # call function(s) to get list of projects
    # call function(s) to get list of courses
    # call function(s) to write the name, email address, list of projects, and list of courses to the given html_output_file
    """
    # insert code
    content = load_txt_file(txt_input_file) #1. Load the content of the txt_input_file.
    name = get_name(content)                #2. Extract the name from the loaded content.
    email = get_email(content)              #3. Extract the email address from the loaded content.
    projects = get_projects(content)        #4. Extract the list of projects from the loaded content.
    courses = get_courses(content)          #5. Extract the list of courses from the loaded content.
    write_html_content(name, email, projects, courses, html_output_file)    #6. Format the extracted information into HTML and write to the html_output_file.



def load_txt_file(filename):
    """Load content from a text file."""
    # Open the file in read-only mode
    with open(filename, 'r') as file:
        # Read the content of the file line-by-line into a list
        content = file.readlines()
    # Return the list of lines
    return content

def get_name(content):
    """Get name from the content."""
    # Extract the first line (assumed to be the name) and strip any leading/trailing whitespaces
    name = content[0].strip()
    # If the first character of the name is not an uppercase letter, return "Invalid Name"
    if not name[0].isupper():
        return "Invalid Name"
    # Return the extracted name
    return name

def get_email(content):
    """Get email from the content and validate it."""
    for line in content:
        if "@" in line:
            email = line.strip()
            
            # Check if email ends with '.com' or '.edu'
            if not (email.endswith('.com') or email.endswith('.edu')):
                return " "
            
            # Check if there is a lowercase English character after '@'
            at_index = email.index('@')
            if not any(char.islower() for char in email[at_index:]):
                return " "
            
            # Check if email contains digits
            if any(char.isdigit() for char in email):
                return " "

            return email
            
    return ""

def get_projects(content):
    """Get list of projects from the content."""
    # Identify the start of the projects section by locating the line with the word "Projects"
    projects_start = content.index("Projects\n") + 1
    # Identify the end of the projects section by locating the line containing multiple "-" characters
    projects_end = projects_start
    while "----" not in content[projects_end]:
        projects_end += 1
    # Extract the projects from the content between the start and end
    extracted_projects = content[projects_start:projects_end]
    # Clean up each extracted project
    cleaned_projects = []
    for project in extracted_projects:
        # Strip any leading/trailing whitespaces
        project = project.strip()
        # Find the start index of the project description 
        # (this is determined by the first alphabetical character in the project string)
        start_index = next((idx for idx, char in enumerate(project) if char.isalpha()), None)
        # If a start index is found (i.e., the project string contains an alphabetical character), 
        # append the cleaned project description to the list
        if start_index is not None:
            cleaned_projects.append(project[start_index:])
    # Return the cleaned projects list
    return cleaned_projects

def get_courses(content):
    """Get list of courses from the content."""
    for line in content:
        if "Courses" in line:
            # Split the line using "Courses" as the delimiter to isolate the course names
            courses_parts = line.split("Courses")[-1].strip().split(',')
            # Clean up each extracted course name            
            cleaned_courses = []
            for course in courses_parts:
                # Strip any leading/trailing whitespaces
                course = course.strip()
                # Find the start index of the course name 
                # (this is determined by the first alphabetical character in the course string)
                start_index = next((idx for idx, char in enumerate(course) if char.isalpha()), None)
                # If a start index is found (i.e., the course string contains an alphabetical character), 
                # append the cleaned course name to the list
                if start_index is not None:
                    cleaned_courses.append(course[start_index:])
            return cleaned_courses
    # If no courses are found in content, return an empty list            
    return []

def write_html_content(name, email, projects, courses, html_output_file):
    """Write the HTML formatted content to the output file."""
    # Open the specified output file in write mode
    with open(html_output_file, 'w') as file:
        # Start with the main content wrapper
        file.write('<div id="page-wrap">\n')
        # Write the name enclosed in <h1> tags and wrapped in a <div>
        file.write(surround_block('div', surround_block('h1', name)))
        # If there's a valid email, write it as a link
        if email:
            email_link = create_email_link(email)
            file.write(surround_block('div', f"Email: {email_link}"))
        # Convert each project into a list item and wrap the entire list in <ul> tags. 
        # Also, precede the list with the heading "Projects" enclosed in <h2> tags. 
        # Wrap everything in a <div>
        projects_list = ''.join([surround_block('li', project) for project in projects])
        file.write(surround_block('div', surround_block('h2', 'Projects') + surround_block('ul', projects_list)))
        # Join all courses into a single string separated by commas, 
        # wrap it in a <span> tag and precede it with the heading "Courses" enclosed in <h3> tags.
        # Wrap everything in a <div>
        courses_text = ', '.join(courses)
        file.write(surround_block('div', surround_block('h3', 'Courses') + surround_block('span', courses_text)))
        # End the main content wrapper and close the body and html tags
        file.write('</div>\n</body>\n</html>')



def main():

    # DO NOT REMOVE OR UPDATE THIS CODE
    # generate resume.html file from provided sample resume.txt
    generate_html('resume.txt', 'resume.html')

    # DO NOT REMOVE OR UPDATE THIS CODE.
    # Uncomment each call to the generate_html function when you’re ready
    # to test how your program handles each additional test resume.txt file
    generate_html('TestResumes/resume_bad_name_lowercase/resume.txt', 'TestResumes/resume_bad_name_lowercase/resume.html')
    generate_html('TestResumes/resume_courses_w_whitespace/resume.txt', 'TestResumes/resume_courses_w_whitespace/resume.html')
    generate_html('TestResumes/resume_courses_weird_punc/resume.txt', 'TestResumes/resume_courses_weird_punc/resume.html')
    generate_html('TestResumes/resume_projects_w_whitespace/resume.txt', 'TestResumes/resume_projects_w_whitespace/resume.html')
    generate_html('TestResumes/resume_projects_with_blanks/resume.txt', 'TestResumes/resume_projects_with_blanks/resume.html')
    generate_html('TestResumes/resume_template_email_w_whitespace/resume.txt', 'TestResumes/resume_template_email_w_whitespace/resume.html')
    generate_html('TestResumes/resume_wrong_email/resume.txt', 'TestResumes/resume_wrong_email/resume.html')

    # If you want to test additional resume files, call the generate_html function with the given .txt file
    # and desired name of output .html file

if __name__ == '__main__':
    main()