
from quizengine.models.quiz_models import QuizCreate,Quiz , QuizQuestion , QuizUpdate
from sqlalchemy.orm import selectinload
from fastapi import HTTPException,status
from typing import Set
from sqlmodel import SQLModel , Session,select,and_,delete
from quizengine.models.question_models import QuestionBank
from quizengine.models.topic_models import Topic
from quizengine.core.loggerconfig import loggerconfigu


logger=loggerconfigu(__name__)


class QuizEngine:
    
    def _fetchAllSubTopics(self,*,topicIds:list[int],db:Session):
        topicsAndSubtopics=db.exec(
            select(Topic)
            .options(selectinload(Topic.children_topics))
            .where(Topic.id.in_(topicIds))
        )
        topics_from_db = topicsAndSubtopics.all()
        print("\n---------topics_from_dbs--------\n", topics_from_db)
        if not topics_from_db:
            raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Incorrect Topic Ids Provided"
            )
        allTopicData=[]
        allTopicId=set()
        def fetch_subTopics(topicsIds):
            nonlocal allTopicData , allTopicId
            topicWithChild=db.exec(
                select(Topic)
                .options(selectinload(Topic.children_topics))
                .where(Topic.id.in_(topicsIds))
            )
            topics=topicWithChild.all()
            for topic in topics:
                if topic not in allTopicData:
                    allTopicData.append(topic)
                    allTopicId.add(topic.id)
                if topic.children_topics:
                    fetch_subTopics([child.id for child in topic.children_topics])
        fetch_subTopics(topicIds)
        return allTopicId , allTopicData 
        
        
    def readQuizById(self,*,quiz_id:int,db:Session):
       try:
            quiz:Quiz=db.exec(
                select(Quiz)
                .options(selectinload(Quiz.topics),
                        selectinload(Quiz.quiz_settings),
                        selectinload(Quiz.quizquestion)
                        .joinedload(QuizQuestion.question)
                        )   
                .where(Quiz.id==quiz_id)
            ).one() 
            if not quiz:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz Not Found"
                )
            # print("\n\n\n\n   ------     Quiz -------- \n\n\n",quiz)   
            # print("\n\n\n\n   ------     Quiz Question -------- \n\n\n",quiz.quizquestion)
            return quiz  
            ...        
       except ValueError as e :
           logger.error(F"read Quiz Error : {e}")
           raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz Not Found"
                )
           ...
       except Exception as e:
           logger.error(F"read Quiz Error : {e}")
           raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz Not Found"
                )
           ...
               
    def createQuiz(self,*,quiz:QuizCreate , db:Session):

        try:
            questionsIds_with_topicIds:list=[]  # store tuple of (questionid,Topicid)
            topicsFromDB:list=[]
            # Get all topics if topic_ids are provided and append to quiz.topics
            if quiz.add_topic_ids:
                all_topic_ids , all_topic_data=self._fetchAllSubTopics(
                    topicIds=quiz.add_topic_ids,db=db
                    )
                print(
                    "\n----Topic with  ids ----\n",
                    "\n\n\n",
                    all_topic_ids,   #   {8, 9, 10, 11, 12}
                )
                #fetch all Question linked with these Topics and subTopics !
                questionsResult=db.exec(
                    select(QuestionBank.id , QuestionBank.topic_id)
                    .where(and_(
                        QuestionBank.topic_id.in_(all_topic_ids),
                        QuestionBank.is_verified==True          
                    ))
                )
                all_QuestionIdsWithTopicId=questionsResult.all()
                print(
                    "\n----questions_result----\n",
                    "\n\n\n",
                    all_QuestionIdsWithTopicId, #  [(6, 8), (7, 8), (8, 9), (9, 11), (10, 12)]
                )
                questionsIds_with_topicIds.extend(all_QuestionIdsWithTopicId)
                topicsFromDB.extend(all_topic_data)
                print(
                    "\n----questions_result----\n",
                    "\n\n\n",
                    len(topicsFromDB) # right now lenght is 5!
                )
            quizToDb=Quiz.model_validate(quiz)
            quizToDb.topics=topicsFromDB
            db.add(quizToDb)
            db.commit()
            db.refresh(quizToDb)
            if  questionsIds_with_topicIds :
                quizQuestions=[
                    QuizQuestion(
                        quiz_id=quizToDb.id , question_id=question_id , topic_id=topic_id
                    )
                    for question_id , topic_id in questionsIds_with_topicIds
                ]   
                db.add_all(quizQuestions)
                db.commit()
            # print("\n----quiz_to_db----\n", quizToDb)
            # print("\n----quiz_to_db.id----\n", quizToDb.id)
            #   fecth the Quiz with Topics and Questions
            quizWithTopicsAndQuestions=self.readQuizById(quiz_id=quizToDb.id,db=db)
            return quizWithTopicsAndQuestions
        except HTTPException as httpExp:
            db.rollback()
            logger.error(f"Create Quiz Error : {httpExp}")
            raise httpExp                
        except Exception as e :
            db.rollback()
            logger.error(f"Create Quiz Error : {httpExp}")
            raise httpExp                
            
            
            
            
            #Just made function for practice 
    def  GetQuizByIds(self,*,quiz_id:int,db:Session)->None:
        
        #Get  Quiz by ID
        try:
            quiz:Quiz= db.exec(
                select(Quiz)
                .options(
                    selectinload(Quiz.topics),
                    selectinload(Quiz.quiz_settings),
                    selectinload(Quiz.quizquestion).joinedload(QuizQuestion.question)
                )
                .where(Quiz.id==quiz_id)    
            ).one()   
            if not quiz:
                raise ValueError("Quiz Not Found")
            print("\n\n\n\n   ------     Quiz -------- \n\n\n",quiz)   
            print("\n\n\n\n   ------     Quiz Question -------- \n\n\n",quiz.quizquestion)
            quiQu:list[QuizQuestion]=quiz.quizquestion
            for questn in quiQu:
                print("\n\n\n\n   ------     Question -------- \n\n\n",questn.question.mcq_options)
            return quiz
        
        
        
        
            # if you not made relationship with mcq_option in questionbank  then when you access the quizquestion[0].question.mcq_options  it will query to the databse 
           
           
           
            #  blow query   fecth the quizquestion and its questionbank and mcqs related to question in one query  (relationship made or not doesnot matter )
            # quizquestion=db.exec(select(QuizQuestion).options(selectinload(QuizQuestion.question).joinedload(QuestionBank.mcq_options)).where(QuizQuestion.question_id==17)).all()   
           
           
            
            #  blow query   fecth the quizquestion and its questionbank and it  will not fetch mcqs related to question in one query if mcq_option relation in questionbank  not made (when you access the quizquestion[0].question.mcq_options then it will query the database then fecth the records )
            # # quizquestion=db.exec(select(QuizQuestion).options(selectinload(QuizQuestion.question)).where(QuizQuestion.question_id==17)).all()
            # print("\n\n\n\n   ------     Quix Question -------- \n\n\n",quizquestion)
            # print("\n\n\n\n   ------     Question -------- \n\n\n",quizquestion[0].question)
            # print("\n\n\n\n   ------     Question -------- \n\n\n",quizquestion[0].question.mcq_options)
            
            
            
            
        except HTTPException as e:
            
            logger.error(f"Get Quiz Error ")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quiz Not found"
            )
        except Exception as e:
            logger.error(f"read_quiz Error: {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Error in fetching Quiz"
            )



    def _AddNewTopics(self,*,quizToUpdate:Quiz ,newTopicIds:Set,existingTopicIds:Set,db:Session ):
    
        newly_TopicsAdded=set()
        if newTopicIds:
            allNewTopicsData:list=[]
            allNewTopicsIds=set()

            def FetchtopicsWithSubTopics(topicIds:list[int]):
                nonlocal allNewTopicsData , allNewTopicsIds                
                TopicWithSubTopic=db.exec(
                    select(Topic)
                    .options(
                        selectinload(Topic.children_topics)
                        .where(Topic.id.in_(topicIds))
                    )
                ).all()
                
                for topic in TopicWithSubTopic:
                    if topic not in allNewTopicsData:
                        allNewTopicsData.append(topic)
                        allNewTopicsIds.add(topic.id)
                    if topic.children_topics:
                        FetchtopicsWithSubTopics([child.id for child in topic.children_topics])    
            FetchtopicsWithSubTopics(newTopicIds) 
            quizToUpdate.topics.extend(allNewTopicsData)
            db.commit()
            return allNewTopicsIds
        else :
            return False    


    def _AddNewQuestions(self,*,quidId:int,newAddedTopic:Set , db:Session):
    
        if newAddedTopic :
            questionBanks=db.exec(
                select(QuestionBank)
                .where(
                    and_(
                        QuestionBank.topic_id.in_(list(newAddedTopic)),
                        QuestionBank.is_verified==True
                    )
                )
            ).all()
            newQuizQuestion=[
                QuizQuestion(
                    quiz_id=quidId , question_id=question.id , topic_id=question.topic_id)
                for   question  in questionBanks
            ]
            db.add_all(newQuizQuestion)
            db.commit()
        else :
            ...  
            
        
    def _removeAddTopics(self,*,quizToUpdate:Quiz,TopicsToRemove:Set,db:Session ):
            # print("ooooo")
            if TopicsToRemove:
                # remove the QuizTopic Link
                quizToUpdate.topics=[topic for topic in quizToUpdate.topics if topic.id not in list(TopicsToRemove) ]   
                # print("ok")
                #remove the quizquestion instance with removeTopicid  and also remove the Question related to These Topics 
                db.execute(
                    delete(QuizQuestion)
                    .where(
                        and_(
                        QuizQuestion.question_id.in_(
                            select(QuestionBank.id).where(
                            QuestionBank.topic_id.in_(TopicsToRemove)       
                                )
                            ),
                        QuizQuestion.quiz_id == quizToUpdate.id
                            )
                        )
                )
                db.commit()
            else :
              ...    
    
    
    
        
    def UpdateQuiz(self,*,  quiz_id:int, updating_data:QuizUpdate, db:Session):
    
        try:
            #Get Quiz by Id
            quizToUpdate=self.readQuizById(quiz_id=quiz_id, db=db)
            existingTopicsWithids={topic.id for topic in quizToUpdate.topics }
            
            # if user enter the topics ids that are already in the database soo  below code filter out those ids that are not in datavase
            newTopicIds=(
                set(updating_data.add_topic_ids) - existingTopicsWithids
                if updating_data.add_topic_ids
                else set()
            )
            topicsToRemove=(
                set(updating_data.remove_topic_ids)
                if updating_data.remove_topic_ids
                else set()
            )
            
            # print("hello")
            if updating_data.add_topic_ids: 
                newlyTopicAdded=self._AddNewTopics(
                    quizToUpdate=quizToUpdate,
                    newTopicIds=newTopicIds,
                    existingTopicIds=existingTopicsWithids,
                    db=db
                    )
                # print("hello")

                newlyAddedQuestion=self._AddNewQuestions(
                    quidId=quizToUpdate.id,
                    newAddedTopic=newlyTopicAdded ,
                    db=db)
                        
            # print("Han g kithy oo")                
            # print(type(updating_data.remove_topic_ids))                
            if len(updating_data.remove_topic_ids)>0:
                # print("okokokokokkkkkokkkkook")
                self._removeAddTopics(
                        quizToUpdate=quizToUpdate,TopicsToRemove=topicsToRemove,db=db
                    )
            # print("Han g kithy oo")                
            for key , value in updating_data.model_dump(exclude_unset=True).items():
                if hasattr(quizToUpdate , key):
                    setattr(quizToUpdate , key , value)
            db.commit()
            db.expire_all()
            UpdatedQuiz=self.GetQuizByIds(quiz_id=quiz_id,db=db)
            return UpdatedQuiz
            # Update Quiz
            # for key , value in updating_data.dict().items():
            #     if key !="topics" and value is not None:
            #         setattr(quiz, key, value)

            # Update Quiz Topics
            # if updating_data.topics:
            #     existingTopicIds=set([topic.id for topic in quiz.topics])
            #     newTopicIds=set(updating_data.topics)

            #     #Remove Topics
            #     for topic in quiz.topics:
            #         if topic.id not in newTopicIds:
            #             quiz.topics.remove(topic)

            #     #Add New Topics
            #     quiz.topics.extend(
            #         self._fetchAllSubTopics(
            #             topicIds=list(newTopicIds-existingTopicIds), db=db
            #         )[1]
            #     )

            # db.commit()
            ...
        except HTTPException :
            db.rollback()
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"update_quiz Error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
    def deleteQuiz(self,*,quiz_id:int,db:Session):
        try:
            
            quizToDelete:Quiz=db.get(Quiz,quiz_id)
            if quizToDelete is None:
                raise ValueError("Quiz not Found")            
            logger.info(f"DELETE_QUIZ_TEST: {quiz_to_delete}")
            db.delete(quizToDelete)
            db.commit()
            return {"message":"Message Deleted SuccessFully"}
        except ValueError as e:
            logger.error(f"Delete Quiz Error  : {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , detail="Quiz not found"
            )
        except Exception as e:
            logger.error(f"Delete Quiz Error  : {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND , detail="Quiz not found"
            )
                                 
                                 
                                 
                                 
quizEngine=QuizEngine()  