class ConstLinkWithLessonsResponse:
    def __init__(self, const_link, lessons):
        self.__const_link = const_link
        self.__lessons = lessons
        print(lessons)

        self.__union_lessons()

    def __union_lessons(self):
        for i in self.__const_link:
            lesson_filter = filter(
                lambda x: "subject_id" in x and \
                          "teacher_id" in x and \
                          x["subject_id"] == i["subject_id"] and \
                          x["teacher_id"] == i["teacher_id"], 
                self.__lessons
            )
            lessons = list(lesson_filter)
            for j in lessons:
                del j["subject_id"]
                del j["teacher_id"]

            i["lessons"] = list(lessons)
      
    def to_list(self):
        return self.__const_link
