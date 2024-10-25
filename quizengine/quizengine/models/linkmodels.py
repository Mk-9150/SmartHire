from sqlmodel import SQLModel , Field

class QuizesTopics(SQLModel ,table=True):
    quiz_id:int|None=Field(foreign_key="quiz.id",default=None, primary_key=True)
    topic_id:int|None=Field(foreign_key="topic.id",default=None,primary_key=True)
    
    