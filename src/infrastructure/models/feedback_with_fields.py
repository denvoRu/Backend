class FeedbackWithExtraFieldsResponse:
    def __init__(self, feedbacks, extra_fields):
        self.feedbacks = feedbacks
        self.extra_fields = extra_fields


    def __union_answers(self):
        return list(i + self.__get_extra_fields(i["id"]) for i in self.feedbacks)


    def __get_extra_fields(self, feedback_id):
        return {"extra_fields": self.__get_extra_fields_by_id(feedback_id)}


    def __get_extra_fields_by_id(self, feedback_id):
        return list(i for i in self.extra_fields if i["feedback_id"] == feedback_id)


    def to_dict(self):
        return self.__union_answers()