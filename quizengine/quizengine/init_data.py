from quizengine.models.quiz_models import Quiz 
from sqlalchemy import Engine
from quizengine.models.topic_models import Topic
from quizengine.models.question_models import QuestionBank 
from quizengine.models.quiz_models import Quiz,QuizQuestion
from quizengine.core.db_eng import engine
from quizengine.core.loggerconfig import loggerconfigu
from sqlmodel import SQLModel ,Session,select
from quizengine.models.answer_models import MCQOption
from sqlalchemy.exc import IntegrityError , SQLAlchemyError
from quizengine.models.quiz_settings import QuizSetting 
from fastapi import HTTPException,status
import datetime



from tenacity import stop_after_attempt , wait_fixed, before_log , after_log ,retry
 
logger=loggerconfigu(__name__)


start_time = datetime.datetime.utcnow()
time_limit_days = 3  # Assuming 3 days for the time limit
time_limit_interval = datetime.timedelta(days=time_limit_days)
end_time = start_time + datetime.timedelta(days=time_limit_days)





print(f"starttime  : {start_time}  ")
print(f"timeLimit  : {time_limit_days}  ")
print(f"timelimit interval  : {time_limit_interval}  ")
print(f"end_time  : {end_time}  ")

 
logger.info("Seeding database")


init_topic_name = "Learn TypeScript in Baby Steps"


init_sub_topic_name = "Typescript Errors"

# Topic & A SubTopic
topic = Topic(
    title=init_topic_name,
    description="""Learn TypeScript 5.0+ in Baby Steps. TypeScript (Which is a superset of JavaScript) is used for building user interfaces, 
    and it is a relatively new programming language that is gaining popularity due to its strong typing system and its ability to be used with 
    JavaScript, React, and Next.js.""",   
)

sub_topic = Topic(
    title= init_sub_topic_name,
    description="Errors in Typescript are common and can be difficult to debug. This topic will help you understand the common errors in TypeScript and how to fix them.",
    # parent_id=topic.id,
    parent_topic=topic,
)


topic2=Topic(
    title="Learn TypeScript in 1 Hour",
    description="Learn TypeScript in 1 Hour. TypeScript (Which is a superset of JavaScript) is used for building user interfaces, and it is a relatively new programming language that is gaining popularity due to its strong typing system and its ability to be used with JavaScript, React, and Next.js.",
)

sub_topic2=Topic(
    title="Typescript Errors",
    description="Errors in Typescript are common and can be difficult to debug. This topic will help you understand the common errors in TypeScript and how to fix them.",
    parent_topic=topic2,
)

sub_topic3=Topic(
    title="Typescript Errors",
    description="Errors in Typescript are common and can be difficult to debug. This topic will help you understand the common errors in TypeScript and how to fix them.",
    parent_topic=sub_topic2,
)

# QUESTION 1
mcq_option1 = MCQOption(
    option_text="NPM is a tool for dependency management and packaging in Python.",
    is_correct=False,
)
mcq_option2 = MCQOption(
    option_text="NPM is a tool for dependency management and packaging in Typescript.",
    is_correct=True,
)
mcq_option3 = MCQOption(
    option_text="NPM is a tool for dependency management and packaging in Java.",
    is_correct=False,
)
mcq_option4 = MCQOption(
    option_text="NPM is a tool for dependency management and packaging in C++.",
    is_correct=False,
)
question1=QuestionBank(
    question_text="What is a common cause of syntax errors in TypeScript?",
    difficulty="easy",
    is_verified=True,
    # question_type="single_select_mcq",
    points=1,
    topic=topic,
    options=[mcq_option1, mcq_option2, mcq_option3, mcq_option4],
)

mcq_option2_1 = MCQOption(
    option_text="Management and packaging in Javascript.", is_correct=True
)
mcq_option2_2 = MCQOption(
    option_text="Virtual Environments Management.", is_correct=False
)
mcq_option2_3 = MCQOption(option_text="Deployment", is_correct=False)
mcq_option2_4 = MCQOption(
    option_text="Dependency management and packaging in Typescript.", is_correct=True
)
question2=QuestionBank(
    question_text="smae What is the correct way to declare a variable in TypeScript?",
    difficulty="easy",
    is_verified=True,
    # question_type="single_select_mcq",
    points=1,
    topic=topic,
    options=[mcq_option2_1, mcq_option2_2, mcq_option2_3, mcq_option2_4],   
)

# QUESTION 3
mcq_option3_1 = MCQOption(option_text=".js file has been generated but it is not valid.", is_correct=True)
mcq_option3_2 = MCQOption(option_text=".js file is Not been generated.", is_correct=False)
mcq_option3_3 = MCQOption(
    option_text=".js is not valid extension at all", is_correct=False
)
mcq_option3_4 = MCQOption(option_text="All of Above", is_correct=False)

question3=QuestionBank(
    question_text="What is the correct way to declare a variable in TypeScript?",
    difficulty="easy",
    is_verified=True,
    # question_type="single_select_mcq",
    points=1,
    topic=topic2,
    options=[mcq_option3_1, mcq_option3_2, mcq_option3_3, mcq_option3_4],  
)


# question4=QuestionBank(
#     question_text="What is the correct way to declare a variable in TypeScript?",
#     difficulty="easy",
#     is_verified=True,
#     # question_type="single_select_mcq",
#     points=1,
#     topic=sub_topic2,
# )
# question5=QuestionBank(
#     question_text="What is the correct way to declare a variable in TypeScript?",
#     difficulty="easy",
#     is_verified=True,
#     # question_type="single_select_mcq",
#     points=1,
#     topic=sub_topic3,
# )








# Question Bank & MCQ Options


# question_bank1 = QuestionBank(
#     question_text="What is NPM?",
#     is_verified=True,
#     points=1,
#     difficulty="easy",
#     topic_id=sub_topic.id,
#     topic=sub_topic,
#     question_type="single_select_mcq",
#     options=[mcq_option1, mcq_option2, mcq_option3, mcq_option4],
# )

# QUESTION 2

# question_bank2 = QuestionBank(
#     question_text="Features of NPM Beneficial for Typescript Programming",
#     is_verified=True,
#     points=1,
#     difficulty="easy",
#     topic_id=sub_topic.id,
#     topic=sub_topic,
#     question_type="multiple_select_mcq",
#     options=[mcq_option2_1, mcq_option2_2, mcq_option2_3, mcq_option2_4],
# )


# question_bank3 = QuestionBank(
#     question_text="Syntax Error means that:",
#     is_verified=True,
#     points=1,
#     difficulty="easy",
#     topic_id=sub_topic.id,
#     topic=sub_topic,
#     question_type="single_select_mcq",
#     options=[mcq_option3_1, mcq_option3_2, mcq_option3_3, mcq_option3_4],
# )

# Quiz
# quiz_question Instances (This is a Separate COmposite Pattern Table as a Quiz Have Less Topic Questions than in Question Bank)
question_instance_1 = QuizQuestion(
    # question_id=question_bank1.id,
    question=question1,
    topic=topic,
)
question_instance_2 = QuizQuestion(
    # question_id=question_bank2.id,
    question=question2,
    # topic_id=sub_topic.id,
    topic=topic,
)
question_instance_3 = QuizQuestion(
    # question_id=question_bank3.id,
    question=question3,
    # topic_id=sub_topic.id,
    topic=topic2,
)
# Quiz Setting
quiz_setting = QuizSetting(
    # quiz_id=quiz.id,
    # quiz=quiz,
    instructions="Attempt Carefully",
    time_limit=time_limit_interval,
    start_time=start_time,
    end_time=end_time,
    quiz_key="TSQ",
)

quiz = Quiz(
    quiz_title="Typescript Errors Quiz",
    # difficulty_level="easy",
    random_flag=True,
    # total_points=sum(
    #     [question_bank1.points, question_bank2.points, question_bank3.points]
    # ),
    # course_id=init_course_id,
    topics=[topic,topic2],
    quiz_settings=[quiz_setting],
    quizquestion=[question_instance_1, question_instance_2, question_instance_3],
)








def initData_seed(*,session:Session):
    
    # logger.loggerconfigu(__name__)
    logger.info("Seeding database")     
    # session.add(sub_topic)   
    
    
    # session.add(sub_topic3)
    
    # session.add(question1)
    # session.add(question2)
    # session.add(question3)
    # session.add(question4)
    # session.add(question5)
    
    session.add(quiz_setting)
    session.commit()

    


@retry(
    stop=stop_after_attempt(3),
    wait=wait_fixed(1),
    before=before_log(logger, 200),
    after=after_log(logger, 300),
)   
def init_db(*,engine:Engine):
    try:
        logger.info("init db up ")
        with Session(engine) as session:
            logger.info("chking db seed alredy !")
            topicSeed=session.exec(select(Topic).where(Topic.title==init_topic_name))
            topic=topicSeed.one_or_none()
            logger.info("topic",topic)
            
            logger.info("chk topicseed is none")
            
            
            if topic is None:
                logger.info("seeding db")
                initData_seed(session=session)
            # logger.info("seeding db")                  
            # initData_seed(session=session)
            else:
                logger.info("seeded db")                
    except IntegrityError as e :
        raise  HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"{str(e)}"
        )  from e
                            
    except Exception as e :
        logger.error(e)
        raise e      
    
    
if __name__=="__main__":
    logger.info("In Initial Data Seeding Script")
    (init_db(engine=engine))
    logger.info("Database Seeding Completed!")
    logger.info("Database is Working!")
    logger.info("Backend Database Initial Data Seeding Completed!")

        
    
    