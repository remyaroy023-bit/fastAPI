import pytest

class Student():
    def __init__(self,first_name: str,last_name: str,major: str,years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def student_instance():
    return Student('remi','ry','cs',4)

def test_student_intialization(student_instance):

    assert student_instance.first_name == 'remi', 'assert first name is remi'
