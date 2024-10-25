class LikeandComment(SQLModel):
    """
        *  also for university like or comments
    """
    id:Annotated[Optional[int],Field(default=None)]
    like:Union[str,None]=None
    comment:Optional[str]=None
    likeorCommentFrom:Annotated[int,Field(foreign_key="teacher.id")]  
    likeorCommentTo:Teacher=Relationship(back_populates="haveLikeComment")
    # likeorCommetTo:Annotated[int,Field(foreign_key="teacher.id")]