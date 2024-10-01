from models.backend_models import Account, Assignment, Course, Student
from abc import ABC


class Storage_I(ABC):
    # Download to disk

    def create_course(self, course: Course) -> Course: 
        raise NotImplementedError
    
    def update_course(self, course: Course) -> bool:
        raise NotImplementedError
    
    def delete_course(self, course: Course) -> bool:
        raise NotImplementedError

    def store_assignment(self, assignment: Assignment): 
        raise NotImplementedError

    def create_account(self, account: Account) -> Account:
        raise NotImplementedError