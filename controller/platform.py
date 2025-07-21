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
    ComplianceCertification,
    ProprietarySoftware,
    ProprietaryHardware,
    SupportTier,
    PricingModel,
)

from pinecone import PineconeAsyncio as Pinecone

from model.platform import (
    PlatformInformation as PlatformInformationModel,
    ComputeInstance as ComputeInstanceModel,
    GeographicRegion as GeographicRegionModel,
    NetworkingCapabilities as NetworkingCapabilitiesModel,
    SecurityFeatures as SecurityFeaturesModel,
    ComplianceCertification as ComplianceCertificationModel,
    ProprietarySoftware as ProprietarySoftwareModel,
    ProprietaryHardware as ProprietaryHardwareModel,
    SupportTier as SupportTierModel,
    PricingModel as PricingModelModel,
    ComplianceStatus,
)

from settings import SETTINGS

# Initialize Pinecone client
pc = Pinecone(api_key=SETTINGS.pinecone_api_key)
index = pc.IndexAsyncio(host=SETTINGS.pinecone_index_hostname)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_sql_to_platform_model(platform: PlatformInformation) -> PlatformInformationModel:
    """Convert SQL model to Pydantic platform model."""
    try:
        # Convert basic platform data
        platform_data = {
            'platform_name': platform.platform_name,
            'platform_type': platform.platform_type,
            'parent_company': platform.parent_company,
            'founded_date': platform.founded_date,
            'headquarters': platform.headquarters,
            'website_url': platform.website_url,
            'documentation_url': platform.documentation_url,
            'primary_datacenter_tier': platform.primary_datacenter_tier,
            'total_datacenters': platform.total_datacenters,
            'edge_locations': platform.edge_locations,
            'custom_configuration_support': platform.custom_configuration_support,
            'bare_metal_available': platform.bare_metal_available,
            'sla_uptime': platform.sla_uptime,
            'specializations': platform.specializations or [],
            'target_markets': platform.target_markets or [],
            'notable_customers': platform.notable_customers or [],
            'partnerships': platform.partnerships or [],
            'last_updated': platform.last_updated,
            'data_sources': platform.data_sources or [],
        }

        # Convert networking capabilities
        networking = NetworkingCapabilitiesModel(
            id=platform.network_capabilities.id if platform.network_capabilities else None,
            bandwidth_gbps=platform.network_capabilities.bandwidth_gbps if platform.network_capabilities else None,
            network_type=platform.network_capabilities.network_type if platform.network_capabilities else None,
            interconnect_technology=platform.network_capabilities.interconnect_technology if platform.network_capabilities else None,
            vpc_support=platform.network_capabilities.vpc_support if platform.network_capabilities else False,
            load_balancing=platform.network_capabilities.load_balancing if platform.network_capabilities else False,
            cdn_integration=platform.network_capabilities.cdn_integration if platform.network_capabilities else False,
            private_networking=platform.network_capabilities.private_networking if platform.network_capabilities else False,
        )
        platform_data['networking'] = networking

        # Convert security features
        security_features = SecurityFeaturesModel(
            id=platform.security_features.id if platform.security_features else None,
            encryption_at_rest=platform.security_features.encryption_at_rest if platform.security_features else False,
            encryption_in_transit=platform.security_features.encryption_in_transit if platform.security_features else False,
            key_management=platform.security_features.key_management if platform.security_features else False,
            identity_management=platform.security_features.identity_management if platform.security_features else False,
            network_security=platform.security_features.network_security if platform.security_features else False,
            vulnerability_scanning=platform.security_features.vulnerability_scanning if platform.security_features else False,
            security_monitoring=platform.security_features.security_monitoring if platform.security_features else False,
            penetration_testing=platform.security_features.penetration_testing if platform.security_features else False,
        )
        platform_data['security_features'] = security_features

        # Convert geographic regions
        regions = []
        for region in platform.geographic_regions:
            region_data = GeographicRegionModel(
                id=region.id if region else None,
                region_name=region.region_name,
                region_code=region.region_code,
                country_code=region.country,  # Note: mapping 'country' to 'country_code'
                availability_zones=region.availability_zones,
                datacenter_tier=region.datacenter_tier,
                edge_location=region.edge_location or False,
            )
            regions.append(region_data)
        platform_data['regions'] = regions

        # Convert compute instances
        compute_instances = []
        for instance in platform.compute_instances:
            # Get pricing models for this instance (they're linked to platform in current schema)
            pricing_models = []
            for pricing in platform.pricing_models:
                if pricing.compute_instance_id == platform.id:  # This links to platform due to schema design
                    pricing_model = PricingModelModel(
                        id=pricing.id if pricing else None,
                        pricing_type=pricing.pricing_type,
                        price_per_hour=pricing.price_per_hour,
                        price_per_month=pricing.price_per_month,
                        minimum_commitment=pricing.minimum_commitment,
                        billing_increment=pricing.billing_increment,
                    )
                    pricing_models.append(pricing_model)

            instance_data = ComputeInstanceModel(
                id=instance.id if instance else None,
                instance_name=instance.instance_name,
                instance_family=instance.instance_family,
                vcpus=instance.vcpus,
                memory_gb=float(
                    instance.memory_gb) if instance.memory_gb else 0.0,
                storage_gb=float(
                    instance.storage_gb) if instance.storage_gb else None,
                storage_type=instance.storage_type,
                gpu_count=instance.gpu_count,
                gpu_type=instance.gpu_type,
                gpu_memory_gb=float(
                    instance.gpu_memory_gb) if instance.gpu_memory_gb else None,
                network_performance=instance.network_performance,
                pricing_models=pricing_models,
                architecture=instance.architecture,
                specialized_hardware=instance.specialized_hardware,
            )
            compute_instances.append(instance_data)
        platform_data['compute_instances'] = compute_instances

        # Convert compliance certifications
        compliance_certifications = []
        for cert in platform.compliance_certifications:
            cert_data = ComplianceCertificationModel(
                id=cert.id if cert else None,
                certification_name=cert.certification_name,
                status=ComplianceStatus.CERTIFIED,  # Default status since not in SQL model
                certification_date=cert.certification_date,
                certifying_body=cert.certifying_body,
                certificate_url=cert.certificate_url,
            )
            compliance_certifications.append(cert_data)
        platform_data['compliance_certifications'] = compliance_certifications

        # Convert proprietary software
        proprietary_software = []
        for software in platform.proprietary_software:
            software_data = ProprietarySoftwareModel(
                id=software.id if software else None,
                software_name=software.software_name,
                software_type=software.software_type,
                description=software.description,
                version=software.version,
                open_source=software.open_source or False,
                license_type=software.license_type,
                documentation_url=software.documentation_url,
                github_url=software.github_url,
                use_cases=software.use_cases or [],
            )
            proprietary_software.append(software_data)
        platform_data['proprietary_software'] = proprietary_software

        # Convert proprietary hardware
        proprietary_hardware = []
        for hardware in platform.proprietary_hardware:
            hardware_data = ProprietaryHardwareModel(
                id=hardware.id if hardware else None,
                hardware_name=hardware.hardware_name,
                hardware_type=hardware.hardware_type,
                description=hardware.description,
                specifications=hardware.specifications,
                performance_metrics=hardware.performance_metrics,
                availability=hardware.availability,
                generation=hardware.generation,
                # Convert array to single value
                manufacturing_partner=hardware.manufacturing_partner[
                    0] if hardware.manufacturing_partner else None,
                use_cases=hardware.use_cases or [],
            )
            proprietary_hardware.append(hardware_data)
        platform_data['proprietary_hardware'] = proprietary_hardware

        # Convert support tiers
        support_tiers = []
        for tier in platform.support_tiers:
            tier_data = SupportTierModel(
                id=tier.id if tier else None,
                tier_name=tier.tier_name,
                average_response_time=tier.average_response_time,
                channels=tier.channels or [],
                hours=tier.hours,
                price=tier.price,
                premium_features=tier.premium_features or [],
            )
            support_tiers.append(tier_data)
        platform_data['support_tiers'] = support_tiers

        return PlatformInformationModel(**platform_data)

    except Exception as e:
        logger.error(f"Error converting SQL model to platform model: {e}")
        import traceback
        traceback.print_exc()
        raise


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
    async def create_platform(self, platform_data: PlatformInformationModel) -> PlatformInformationModel:
        """Create a new platform."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)

                # Create networking capabilities first
                network_capabilities = None
                if hasattr(platform_data, 'networking') and platform_data.networking:
                    network_capabilities = NetworkCapabilities(
                        **platform_data.networking.model_dump())
                    session.add(network_capabilities)
                    session.flush()  # Get the ID without committing

                # Create security features
                security_features = None
                if hasattr(platform_data, 'security_features') and platform_data.security_features:
                    security_features = SecurityFeatures(
                        **platform_data.security_features.model_dump())
                    session.add(security_features)
                    session.flush()  # Get the ID without committing

                # Prepare platform data, excluding nested objects
                platform_dict = platform_data.model_dump(exclude={
                    'networking', 'security_features', 'regions', 'compute_instances',
                    'compliance_certifications', 'proprietary_software', 'proprietary_hardware',
                    'support_tiers'
                })

                # Add foreign key references
                if network_capabilities:
                    platform_dict['networking_id'] = network_capabilities.id
                if security_features:
                    platform_dict['security_id'] = security_features.id

                # Create the platform record
                platform = PlatformInformation(**platform_dict)
                session.add(platform)
                session.flush()  # Get the platform ID

                # Create related records
                # Geographic regions
                if hasattr(platform_data, 'regions') and platform_data.regions:
                    for region_data in platform_data.regions:
                        region_dict = region_data.model_dump()
                        region_dict['platform_id'] = platform.id
                        # Map the field name from country_code to country to match the database schema
                        if 'country_code' in region_dict:
                            region_dict['country'] = region_dict.pop(
                                'country_code')
                        region = GeographicRegions(**region_dict)
                        session.add(region)

                # Compute instances
                if hasattr(platform_data, 'compute_instances') and platform_data.compute_instances:
                    for instance_data in platform_data.compute_instances:
                        instance_dict = instance_data.model_dump(
                            exclude={'pricing_models'})
                        instance_dict['platform_id'] = platform.id
                        instance = ComputeInstance(**instance_dict)
                        session.add(instance)

                        # Handle pricing models - note: in current schema they're linked to platform, not instance
                        if hasattr(instance_data, 'pricing_models') and instance_data.pricing_models:
                            for pricing_data in instance_data.pricing_models:
                                pricing_dict = pricing_data.model_dump()
                                # Using platform.id due to schema design
                                pricing_dict['compute_instance_id'] = platform.id
                                pricing_model = PricingModel(**pricing_dict)
                                session.add(pricing_model)

                # Compliance certifications
                if hasattr(platform_data, 'compliance_certifications') and platform_data.compliance_certifications:
                    for cert_data in platform_data.compliance_certifications:
                        cert_dict = cert_data.model_dump()
                        cert_dict['platform_id'] = platform.id
                        cert = ComplianceCertification(**cert_dict)
                        session.add(cert)

                # Proprietary software
                if hasattr(platform_data, 'proprietary_software') and platform_data.proprietary_software:
                    for software_data in platform_data.proprietary_software:
                        software_dict = software_data.model_dump()
                        software_dict['platform_id'] = platform.id
                        software = ProprietarySoftware(**software_dict)
                        session.add(software)

                # Proprietary hardware
                if hasattr(platform_data, 'proprietary_hardware') and platform_data.proprietary_hardware:
                    for hardware_data in platform_data.proprietary_hardware:
                        hardware_dict = hardware_data.model_dump()
                        hardware_dict['platform_id'] = platform.id
                        hardware = ProprietaryHardware(**hardware_dict)
                        session.add(hardware)

                # Support tiers
                if hasattr(platform_data, 'support_tiers') and platform_data.support_tiers:
                    for support_data in platform_data.support_tiers:
                        support_dict = support_data.model_dump()
                        support_dict['platform_id'] = platform.id
                        support_tier = SupportTier(**support_dict)
                        session.add(support_tier)

                session.commit()
                session.refresh(platform)
                logger.info(f"Created platform with ID: {platform.id}")

                platform_model = convert_sql_to_platform_model(platform)

                # Add platform to Pinecone
                try:
                    await self.add_platform_to_pinecone(platform_model)
                except Exception as e:
                    logger.warning(f"Failed to add platform to Pinecone: {e}")
                    # Don't fail the entire operation if Pinecone fails

                return platform_model
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating platform: {e}")
                import traceback
                print(traceback.print_exc())
                raise

    def get_platform(self, platform_id: int) -> Optional[PlatformInformationModel]:
        """Get a platform by ID."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            platform = session.query(PlatformInformation).filter(
                PlatformInformation.id == platform_id).first()
            if platform:
                return convert_sql_to_platform_model(platform)
            return None

    def get_platform_by_name(self, platform_name: str) -> Optional[PlatformInformationModel]:
        """Get a platform by name."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            platform = session.query(PlatformInformation).filter(
                PlatformInformation.platform_name == platform_name).first()
            if platform:
                return convert_sql_to_platform_model(platform)
            return None

    def get_all_platforms(self, limit: int = 100, offset: int = 0) -> List[PlatformInformationModel]:
        """Get all platforms with pagination."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [
                convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).offset(offset).limit(limit).all()
            ]

    async def update_platform(self, platform_id: int, update_data: Dict[str, Any]) -> Optional[PlatformInformationModel]:
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

                    platform_model = convert_sql_to_platform_model(platform)

                    # Update platform in Pinecone
                    try:
                        await self.update_platform_in_pinecone(platform_model)
                    except Exception as e:
                        logger.warning(
                            f"Failed to update platform in Pinecone: {e}")
                        # Don't fail the entire operation if Pinecone fails

                    return platform_model
                return None
            except Exception as e:
                session.rollback()
                logger.error(f"Error updating platform: {e}")
                raise

    async def delete_platform(self, platform_id: int) -> bool:
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

                    # Delete platform from Pinecone
                    try:
                        await self.delete_platform_from_pinecone(platform_id)
                    except Exception as e:
                        logger.warning(
                            f"Failed to delete platform from Pinecone: {e}")
                        # Don't fail the entire operation if Pinecone fails

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
            return [convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.platform_name.ilike(f"%{name}%")
            ).all()]

    # Search and filter operations
    def search_platforms_by_type(self, platform_type: str) -> List[PlatformInformationModel]:
        """Search platforms by type."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.platform_type == platform_type
            ).all()]

    def search_platforms_by_company(self, company_name: str) -> List[PlatformInformationModel]:
        """Search platforms by parent company."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).filter(
                PlatformInformation.parent_company.ilike(f"%{company_name}%")
            ).all()]

    def get_platforms_with_gpu_instances(self) -> List[PlatformInformationModel]:
        """Get platforms that have GPU compute instances."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).join(ComputeInstance).filter(
                ComputeInstance.gpu_count > 0
            ).distinct().all()]

    def paginate_platforms(self, page: int = 1, page_size: int = 10) -> List[PlatformInformationModel]:
        """Paginate platforms."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            offset = (page - 1) * page_size
            return [
                convert_sql_to_platform_model(platform) for platform in session.query(PlatformInformation).offset(offset).limit(page_size).all()
            ]

    # Compliance Certification operations
    def create_compliance_certification(self, cert_data: ComplianceCertificationModel) -> ComplianceCertificationModel:
        """Create a new compliance certification."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                cert = ComplianceCertification(**cert_data.model_dump())
                session.add(cert)
                session.commit()
                session.refresh(cert)
                logger.info(
                    f"Created compliance certification with ID: {cert.id}")
                return ComplianceCertificationModel.model_validate(cert)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating compliance certification: {e}")
                raise

    def get_compliance_certifications_by_platform(self, platform_id: int) -> List[ComplianceCertificationModel]:
        """Get all compliance certifications for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [ComplianceCertificationModel.model_validate(cert) for cert in session.query(ComplianceCertification).filter(ComplianceCertification.platform_id == platform_id).all()]

    # Proprietary Software operations
    def create_proprietary_software(self, software_data: ProprietarySoftwareModel) -> ProprietarySoftwareModel:
        """Create a new proprietary software entry."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                software = ProprietarySoftware(**software_data.model_dump())
                session.add(software)
                session.commit()
                session.refresh(software)
                logger.info(
                    f"Created proprietary software with ID: {software.id}")
                return ProprietarySoftwareModel.model_validate(software)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating proprietary software: {e}")
                raise

    def get_proprietary_software_by_platform(self, platform_id: int) -> List[ProprietarySoftwareModel]:
        """Get all proprietary software for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [ProprietarySoftwareModel.model_validate(software) for software in session.query(ProprietarySoftware).filter(ProprietarySoftware.platform_id == platform_id).all()]

    # Proprietary Hardware operations
    def create_proprietary_hardware(self, hardware_data: ProprietaryHardwareModel) -> ProprietaryHardwareModel:
        """Create a new proprietary hardware entry."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                hardware = ProprietaryHardware(**hardware_data.model_dump())
                session.add(hardware)
                session.commit()
                session.refresh(hardware)
                logger.info(
                    f"Created proprietary hardware with ID: {hardware.id}")
                return ProprietaryHardwareModel.model_validate(hardware)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating proprietary hardware: {e}")
                raise

    def get_proprietary_hardware_by_platform(self, platform_id: int) -> List[ProprietaryHardwareModel]:
        """Get all proprietary hardware for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [ProprietaryHardwareModel.model_validate(hardware) for hardware in session.query(ProprietaryHardware).filter(ProprietaryHardware.platform_id == platform_id).all()]

    # Support Tier operations
    def create_support_tier(self, support_data: SupportTierModel) -> SupportTierModel:
        """Create a new support tier."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                support_tier = SupportTier(**support_data.model_dump())
                session.add(support_tier)
                session.commit()
                session.refresh(support_tier)
                logger.info(f"Created support tier with ID: {support_tier.id}")
                return SupportTierModel.model_validate(support_tier)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating support tier: {e}")
                raise

    def get_support_tiers_by_platform(self, platform_id: int) -> List[SupportTierModel]:
        """Get all support tiers for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [SupportTierModel.model_validate(tier) for tier in session.query(SupportTier).filter(SupportTier.platform_id == platform_id).all()]

    # Pricing Model operations
    def create_pricing_model(self, pricing_data: PricingModelModel) -> PricingModelModel:
        """Create a new pricing model."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                pricing_model = PricingModel(**pricing_data.model_dump())
                session.add(pricing_model)
                session.commit()
                session.refresh(pricing_model)
                logger.info(
                    f"Created pricing model with ID: {pricing_model.id}")
                return PricingModelModel.model_validate(pricing_model)
            except Exception as e:
                session.rollback()
                logger.error(f"Error creating pricing model: {e}")
                raise

    def get_pricing_models_by_platform(self, platform_id: int) -> List[PricingModelModel]:
        """Get all pricing models for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            return [PricingModelModel.model_validate(pricing) for pricing in session.query(PricingModel).filter(PricingModel.compute_instance_id == platform_id).all()]

    def close(self) -> None:
        """Close the database connection."""
        self.engine.dispose()

    async def add_platform_to_pinecone(self, platform: PlatformInformationModel) -> None:
        """Add a platform record to Pinecone."""
        try:
            # Convert the platform model to JSON string
            platform_json = platform.model_dump_json()
            platform_data = platform.model_dump()

            # Create the record in the required format
            record = {
                "_id": str(platform.id),
                "data": platform_json,
                **platform_data
            }

            # Upsert the record into Pinecone using the platforms namespace
            await index.upsert_records(
                records=[record],
                namespace=SETTINGS.pinecone_platform_namespace
            )
            logger.info(
                f"Platform {platform.platform_name} added to Pinecone index.")
        except Exception as e:
            logger.error(f"Error adding platform to Pinecone: {e}")
            raise

    async def update_platform_in_pinecone(self, platform: PlatformInformationModel) -> None:
        """Update a platform record in Pinecone."""
        try:
            # Convert the platform model to JSON string
            platform_json = platform.model_dump_json()
            platform_data = platform.model_dump()

            # Create the record in the required format
            record = {
                "_id": str(platform.id),
                "data": platform_json,
                **platform_data
            }

            # Upsert the record into Pinecone using the platforms namespace
            await index.upsert_records(
                records=[record],
                namespace=SETTINGS.pinecone_platform_namespace
            )
            logger.info(
                f"Platform {platform.platform_name} updated in Pinecone index.")
        except Exception as e:
            logger.error(f"Error updating platform in Pinecone: {e}")
            raise

    async def delete_platform_from_pinecone(self, platform_id: int) -> None:
        """Delete a platform record from Pinecone."""
        try:
            # Delete the record from Pinecone using the platforms namespace
            await index.delete(
                ids=[str(platform_id)],
                namespace=SETTINGS.pinecone_platform_namespace
            )
            logger.info(
                f"Platform with ID {platform_id} deleted from Pinecone index.")
        except Exception as e:
            logger.error(f"Error deleting platform from Pinecone: {e}")
            raise

    async def sync_all_platforms_to_pinecone(self, limit: int = 100, offset: int = 0) -> None:
        """Sync all platforms from database to Pinecone."""
        try:
            platforms = self.get_all_platforms(limit=limit, offset=offset)
            records = []

            for platform in platforms:
                # Convert the platform model to JSON string
                platform_json = platform.model_dump_json()
                platform_data = platform.model_dump()

                # Create the record in the required format
                record = {
                    "_id": str(platform.id),
                    "data": platform_json,
                    **platform_data
                }
                records.append(record)

            if records:
                # Batch upsert records to Pinecone
                await index.upsert_records(
                    records=records,
                    namespace=SETTINGS.pinecone_platform_namespace
                )
                logger.info(
                    f"Synced {len(records)} platforms to Pinecone index.")
            else:
                logger.info("No platforms found to sync to Pinecone.")

        except Exception as e:
            logger.error(f"Error syncing platforms to Pinecone: {e}")
            raise
