import logging
from typing import List, Optional
from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

from sql_model.state import Base, State as StateModel
from model.state import State, StateBase
from .base import BaseController

logger = logging.getLogger(__name__)


class StateController(BaseController):
    """Controller for managing application state data."""

    def __init__(self, database_url: str, expiration_seconds: int = 300):
        """Initialize the state controller with database connection."""
        super().__init__(database_url, Base.metadata)
        self.expiration_seconds = expiration_seconds

    def issue(self) -> Optional[State]:
        """Issue a new state entry."""
        state = StateBase()

        try:
            with self.get_session() as session:
                session = self._ensure_healthy_session(session)

                db_state = StateModel(
                    state=state.state,
                    created_at=datetime.now()
                )

                session.add(db_state)
                session.commit()
                session.refresh(db_state)

                return self._convert_to_model(db_state)

        except SQLAlchemyError as e:
            logger.error(f"Error creating state: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating state: {e}")
            return None

    def consume(self, state: str) -> Optional[State]:
        """Consume a state entry by ID (retrieve and delete)."""
        try:

            with self.get_session() as session:
                session = self._ensure_healthy_session(session)

                db_state = session.query(StateModel).filter(
                    StateModel.state == state).first()

                if db_state:
                    # Check if state has expired
                    time_elapsed = (datetime.now() -
                                    db_state.created_at).total_seconds()

                    session.delete(db_state)
                    session.commit()

                    if time_elapsed > self.expiration_seconds:
                        # State has expired, delete it but don't return it
                        logger.warning(
                            f"State has expired ({time_elapsed:.1f}s > {self.expiration_seconds}s) and was deleted")
                        return None

                    # Convert to model before deleting
                    state_model = self._convert_to_model(db_state)
                    logger.info(
                        f"Successfully consumed (retrieved and deleted) state ")
                    return state_model
                return None

        except SQLAlchemyError as e:
            logger.error(f"Error consuming state : {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error consuming state : {e}")
            return None

    def clear_old_states(self, keep_latest: int = 10) -> int:
        """Clear old state entries, keeping only the latest N entries."""
        try:
            with self.get_session() as session:
                session = self._ensure_healthy_session(session)

                # Get the IDs of the latest entries to keep
                latest_states = (session.query(StateModel)
                                 .order_by(desc(StateModel.created_at))
                                 .limit(keep_latest)
                                 .all())

                latest_ids = [state.id for state in latest_states]

                # Delete entries not in the latest list
                if latest_ids:
                    deleted_count = (session.query(StateModel)
                                     .filter(~StateModel.id.in_(latest_ids))
                                     .delete(synchronize_session=False))
                else:
                    deleted_count = session.query(
                        StateModel).delete(synchronize_session=False)

                session.commit()

                logger.info(
                    f"Cleared {deleted_count} old state entries, kept latest {keep_latest}")
                return deleted_count

        except SQLAlchemyError as e:
            logger.error(f"Error clearing old states: {e}")
            return 0
        except Exception as e:
            logger.error(f"Unexpected error clearing old states: {e}")
            return 0

    def _convert_to_model(self, db_state: StateModel) -> State:
        """Convert SQLAlchemy model to Pydantic model."""
        return State(
            id=getattr(db_state, 'id'),
            state=getattr(db_state, 'state'),
            created_at=getattr(db_state, 'created_at')
        )
