from datetime import datetime
import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError


from sql_model.platforms import (
    Base,
    PlatformInformation,
    ComputeInstance,
    GeographicRegions,
    NetworkCapabilities,
    SecurityFeatures,
)

from model.platform import (
    PlatformInformation as PlatformInformationModel,
    ComputeInstance as ComputeInstanceModel,
    GeographicRegion as GeographicRegionModel,
    NetworkingCapabilities as NetworkingCapabilitiesModel,
    SecurityFeatures as SecurityFeaturesModel,
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLOpsPlatformController:
    def __init__(self, database_url: str):
        """Initialize the controller with database connection."""
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        self.session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

    def get_session(self) -> Session:
        """Get a database session."""
        return self.session_local()

    def _check_session_health(self, session: Session) -> bool:
        """Check if the database session is healthy."""
        try:
            # Simple query to test connection
            session.execute(text("SELECT 1"))
            return True
        except (SQLAlchemyError, DisconnectionError) as e:
            logger.error(f"Session health check failed: {e}")
            return False

    def _ensure_healthy_session(self, session: Session) -> Session:
        """Ensure we have a healthy session, create new one if needed."""
        if not self._check_session_health(session):
            logger.warning("Session is unhealthy, creating new session")
            session.close()
            return self.get_session()
        return session

    # Platform Information CRUD operations
    def create_platform(self, platform_data: PlatformInformationModel) -> PlatformInformationModel:
        """Create a new platform."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                platform = PlatformInformation(**platform_data.model_dump())
                session.add(platform)
                session.commit()
                session.refresh(platform)
                logger.info(f"Created platform with ID: {platform.id}")
                return PlatformInformationModel.model_validate(platform)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating platform: {e}")
                raise

    def get_platform(self, platform_id: int) -> Optional[PlatformInformationModel]:
        """Get a platform by ID."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            platform = session.query(PlatformInformation).filter(
                PlatformInformation.id == platform_id).first()
            if platform:
                return PlatformInformationModel.model_validate(platform)
            return None

    def get_platform_by_name(self, platform_name: str) -> Optional[PlatformInformationModel]:
        """Get a platform by name."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            platform = session.query(PlatformInformation).filter(
                PlatformInformation.platform_name == platform_name).first()
            if platform:
                return PlatformInformationModel.model_validate(platform)
            return None

    def get_all_platforms(self, limit: int = 100, offset: int = 0) -> List[PlatformInformationModel]:
        """Get all platforms with pagination."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [
                PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).offset(offset).limit(limit).all()
            ]

    def update_platform(self, platform_id: int, update_data: Dict[str, Any]) -> Optional[PlatformInformationModel]:
        """Update a platform."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                platform: Optional[PlatformInformation] = session.query(
                    PlatformInformation).filter(PlatformInformation.id == platform_id).first()
                if platform:
                    for key, value in update_data.items():
                        setattr(platform, key, value)
                    platform.last_updated = datetime.now()  # type: ignore
                    session.commit()
                    session.refresh(platform)
                    logger.info(f"Updated platform with ID: {platform_id}")
                    return PlatformInformationModel.model_validate(platform)
                return None
            except Exception as e:
                session.rollback()
                logger.error(f"Error updating platform: {e}")
                raise

    def delete_platform(self, platform_id: int) -> bool:
        """Delete a platform."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                platform = session.query(PlatformInformation).filter(
                    PlatformInformation.id == platform_id).first()
                if platform:
                    session.delete(platform)
                    session.commit()
                    logger.info(f"Deleted platform with ID: {platform_id}")
                    return True
                return False
            except Exception as e:
                session.rollback()
                logger.error(f"Error deleting platform: {e}")
                raise

    # Compute Instance operations
    def create_compute_instance(self, instance_data: ComputeInstanceModel) -> ComputeInstanceModel:
        """Create a new compute instance."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                instance = ComputeInstance(**instance_data.model_dump())
                session.add(instance)
                session.commit()
                session.refresh(instance)
                logger.info(f"Created compute instance with ID: {instance.id}")
                return ComputeInstanceModel.model_validate(instance)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating compute instance: {e}")
                raise

    def get_compute_instances_by_platform(self, platform_id: int) -> List[ComputeInstanceModel]:
        """Get all compute instances for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [ComputeInstanceModel.model_validate(instance) for instance in session.query(ComputeInstance).filter(ComputeInstance.platform_id == platform_id).all()]

    # Geographic Regions operations
    def create_geographic_region(self, region_data: GeographicRegionModel) -> GeographicRegionModel:
        """Create a new geographic region."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                region = GeographicRegions(**region_data.model_dump())
                session.add(region)
                session.commit()
                session.refresh(region)
                logger.info(f"Created geographic region with ID: {region.id}")
                return GeographicRegionModel.model_validate(region)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating geographic region: {e}")
                raise

    def get_regions_by_platform(self, platform_id: int) -> List[GeographicRegionModel]:
        """Get all regions for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [GeographicRegionModel.model_validate(region) for region in session.query(GeographicRegions).filter(GeographicRegions.platform_id == platform_id).all()]

    # Network Capabilities operations
    def create_network_capabilities(self, network_data: NetworkingCapabilitiesModel) -> NetworkingCapabilitiesModel:
        """Create network capabilities."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                network = NetworkCapabilities(**network_data.model_dump())
                session.add(network)
                session.commit()
                session.refresh(network)
                logger.info(
                    f"Created network capabilities with ID: {network.id}")
                return NetworkingCapabilitiesModel.model_validate(network)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating network capabilities: {e}")
                raise

    # Security Features operations
    def create_security_features(self, security_data: SecurityFeaturesModel) -> SecurityFeaturesModel:
        """Create security features."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                security = SecurityFeatures(**security_data.model_dump())
                session.add(security)
                session.commit()
                session.refresh(security)
                logger.info(
                    f"Created security features with ID: {security.id}")
                return SecurityFeaturesModel.model_validate(security)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating security features: {e}")
                raise

    def search_platforms_by_name(self, name: str) -> List[PlatformInformationModel]:
        """Search platforms by name."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.platform_name.ilike(f"%{name}%")
            ).all()]

    # Search and filter operations
    def search_platforms_by_type(self, platform_type: str) -> List[PlatformInformationModel]:
        """Search platforms by type."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.platform_type == platform_type
            ).all()]

    def search_platforms_by_company(self, company_name: str) -> List[PlatformInformationModel]:
        """Search platforms by parent company."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.parent_company.ilike(f"%{company_name}%")
            ).all()]

    def get_platforms_with_gpu_instances(self) -> List[PlatformInformationModel]:
        """Get platforms that have GPU compute instances."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).join(ComputeInstance).filter(
                ComputeInstance.gpu_count > 0
            ).distinct().all()]

    def paginate_platforms(self, page: int = 1, page_size: int = 10) -> List[PlatformInformationModel]:
        """Paginate platforms."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            offset = (page - 1) * page_size
            return [
                PlatformInformationModel.model_validate(platform) for platform in session.query(PlatformInformation).offset(offset).limit(page_size).all()
            ]

    def close(self) -> None:
        """Close the database connection."""
        self.engine.dispose()
