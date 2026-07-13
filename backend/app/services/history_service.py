import logging

from sqlalchemy import (
    delete,
    select,
)

from sqlalchemy.orm import Session


from ..models.query_history import (
    QueryHistory,
)


from ..schemas.history import (
    HistoryCreate,
)





logger = logging.getLogger(__name__)







class HistoryService:
    """
    Handles query history persistence.

    Responsibilities:
    - Create query history
    - Retrieve user history
    - Delete user history

    Security:
    - All operations are user scoped
    - Ownership validation handled before creation
    """







    def create_history(
        self,
        db: Session,
        user_id: int,
        data: HistoryCreate,
    ) -> QueryHistory:
        """
        Store query execution history.
        """



        try:


            history = QueryHistory(

                user_id=user_id,

                connection_id=data.connection_id,

                prompt=data.prompt,

                generated_sql=data.generated_sql,

                explanation=data.explanation,

                confidence=data.confidence,

                execution_time_ms=
                data.execution_time_ms,

                rows_returned=
                data.rows_returned,

                status=data.status,

                error_message=
                data.error_message,

            )



            db.add(
                history
            )


            db.commit()


            db.refresh(
                history
            )



            logger.info(

                "Query history created. user_id=%s history_id=%s",

                user_id,

                history.id,

            )



            return history





        except Exception as error:


            db.rollback()



            logger.error(

                "History creation failed. user_id=%s error=%s",

                user_id,

                error,

            )


            raise







    def get_history(
        self,
        db: Session,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
        status: str | None = None,
        connection_id: int | None = None,
    ):
        """
        Retrieve only current user's history.
        """



        query = (
            select(QueryHistory)
            .where(
                QueryHistory.user_id == user_id
            )
        )



        if status:


            query = query.where(

                QueryHistory.status
                ==
                status

            )




        if connection_id is not None:


            query = query.where(

                QueryHistory.connection_id
                ==
                connection_id

            )





        query = (

            query

            .order_by(

                QueryHistory.created_at.desc()

            )

            .offset(

                (page - 1) * page_size

            )

            .limit(

                page_size

            )

        )





        result = db.execute(
            query
        )



        return result.scalars().all()







    def get_history_by_id(
        self,
        db: Session,
        user_id: int,
        history_id: int,
    ):
        """
        Retrieve single history record
        owned by current user.
        """



        query = (

            select(QueryHistory)

            .where(

                QueryHistory.id
                ==
                history_id,


                QueryHistory.user_id
                ==
                user_id,

            )

        )



        result = db.execute(
            query
        )



        return result.scalar_one_or_none()







    def delete_history(
        self,
        db: Session,
        user_id: int,
        history_id: int,
    ) -> bool:
        """
        Delete only user's own history.
        """



        record = self.get_history_by_id(

            db,

            user_id,

            history_id,

        )



        if record is None:


            return False






        db.delete(
            record
        )


        db.commit()



        logger.info(

            "History deleted. user_id=%s history_id=%s",

            user_id,

            history_id,

        )



        return True







    def clear_history(
        self,
        db: Session,
        user_id: int,
    ) -> int:
        """
        Delete all history belonging to user.
        """



        query = (

            delete(QueryHistory)

            .where(

                QueryHistory.user_id
                ==
                user_id

            )

        )



        result = db.execute(
            query
        )


        db.commit()



        logger.info(

            "All history cleared. user_id=%s deleted=%s",

            user_id,

            result.rowcount,

        )



        return result.rowcount







history_service = HistoryService()