from src.infrastructure.database import Module, Subject

from typing import List



class ModuleWithSubjectResponse:
    def __init__(self, modules: List[Module], subjects: List[Subject]):
        self.modules = modules
        self.subjects = subjects

    def __get_dict_of_module(self, module: Module):
        return module.model_dump(exclude={"is_disabled", "institute_id"})
    
    def __get_dict_of_subject(self, subject: Subject):
        return subject.model_dump(exclude={"is_disabled", "module_id"})
    
    def __get_module_subjects(self, module: Module):
        subjects_with_module_id = filter(
            lambda x: x.module_id == module.id, 
            self.subjects
        )
        subjects_list = list(
            map(self.__get_dict_of_subject, subjects_with_module_id)
        )

        return subjects_list


    def __extend_module_with_subjects(self, module: Module):
        subjects_list = self.__get_module_subjects(module)
        
        module_dict = self.__get_dict_of_module(module)
        module_dict["subjects"] = subjects_list

        return module_dict
    
    def __get_extended_modules(self):
        return [
            self.__extend_module_with_subjects(m) for m in self.modules
        ]
    
    def to_dict(self):
        return list(i for i in self.__get_extended_modules() if i is not None)
        