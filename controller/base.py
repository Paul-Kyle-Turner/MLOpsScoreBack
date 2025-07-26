import logging
from abc import ABC
from typing import Optional

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseController(ABC):
    """
    Base controller class that provides common database functionality
    for all MLOps platform controllers.
    """

    def __init__(self, database_url: str, base_metadata=None):
        """
        Initialize the base controller with database connection.
        
        Args:
            database_url: Database connection string
            base_metadata: SQLAlchemy Base metadata for table creation
        """
        self.database_url = database_url
        self.engine = create_engine(database_url)
        
        # Create tables if Base metadata is provided
        if base_metadata is not None:
            base_metadata.create_all(self.engine)
        
        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        logger.info(f"Initialized {self.__class__.__name__} with database connection")

    def get_session(self) -> Session:
        """
        Get a database session.
        
        Returns:
            SQLAlchemy Session object
        """
        return self.session_local()

    def _check_session_health(self, session: Session) -> bool:
        """
        Check if the database session is healthy.
        
        Args:
            session: SQLAlchemy session to check
            
        Returns:
            bool: True if session is healthy, False otherwise
        """
        try:
            session.execute(text("SELECT 1"))
            return True
        except (SQLAlchemyError, DisconnectionError) as e:
            logger.warning(f"Database session health check failed: {e}")
            return False

    def _ensure_healthy_session(self, session: Session) -> Session:
        """
        Ensure we have a healthy session, create new one if needed.
        
        Args:
            session: Session to check and potentially replace
            
        Returns:
            Session: Healthy session (either the original or a new one)
        """
        if not self._check_session_health(session):
            logger.warning("Session is unhealthy, creating new session")
            session.close()
            session = self.get_session()
        return session

    def _handle_database_error(self, operation: str, error: Exception) -> None:
        """
        Standard error handling for database operations.
        
        Args:
            operation: Description of the operation that failed
            error: The exception that was raised
        """
        if isinstance(error, SQLAlchemyError):
            logger.error(f"Database error during {operation}: {error}")
        else:
            logger.error(f"Unexpected error during {operation}: {error}")

    def _log_operation(self, operation: str, details: Optional[str] = None) -> None:
        """
        Log database operations for debugging and monitoring.
        
        Args:
            operation: Description of the operation
            details: Additional details about the operation
        """
        if details:
            logger.info(f"{self.__class__.__name__}: {operation} - {details}")
        else:
            logger.info(f"{self.__class__.__name__}: {operation}")

    def close(self) -> None:
        """
        Close the database connection and clean up resources.
        """
        try:
            self.engine.dispose()
            logger.info(f"{self.__class__.__name__} database connection closed")
        except Exception as e:
            logger.error(f"Error closing database connection: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures connection is closed."""
        self.close()

    def get_engine_info(self) -> dict:
        """
        Get information about the database engine.
        
        Returns:
            dict: Engine information including URL and driver
        """
        return {
            "url": str(self.engine.url),
            "driver": self.engine.url.drivername,
            "pool_size": getattr(self.engine.pool, 'size', None),
            "max_overflow": getattr(self.engine.pool, 'max_overflow', None)
        }

    def test_connection(self) -> bool:
        """
        Test the database connection.
        
        Returns:
            bool: True if connection is successful, False otherwise
        """
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
