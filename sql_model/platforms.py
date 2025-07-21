from sqlalchemy import Column, Integer, BigInteger, String, Boolean, Numeric, DateTime, ARRAY, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy import ForeignKey
from datetime import datetime

Base = declarative_base()

#  Define enums
platform_types_enum = ENUM(
    'hyperscaler', 'gpu_cloud', 'edge_cloud', 'hybrid_cloud',
    'private_cloud', 'specialized_ai', 'container_platform',
    'serverless', 'other',
    name='platform_types',
    schema='platforms'
)

datacenter_tier_enum = ENUM(
    'tier_1', 'tier_2', 'tier_3', 'tier_4', 'tier_5',
    'colocation', 'edge', 'hybrid', 'unknown',
    name='datacenter_tier',
    schema='platforms'
)

pricing_type_enum = ENUM(
    'on_demand', 'reserved', 'spot', 'preemptible',
    'dedicated', 'burstable',
    name='pricing_type',
    schema='platforms'
)

compliance_status_enum = ENUM(
    'certified', 'in_progress', 'planned', 'not_applicable', 'unknown',
    name='compliance_status',
    schema='platforms'
)

billing_increment_enum = ENUM(
    'per_second', 'per_minute', 'per_hour', 'per_day',
    'per_month', 'per_year', 'one_time', 'custom',
    name='billing_increment',
    schema='platforms'
)

# Define SQLAlchemy models


class NetworkCapabilities(Base):
    __tablename__ = 'network_capabilities'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    bandwidth_gbps = Column(Numeric(4))
    network_type = Column(String(1024))
    interconnect_technology = Column(String(1024))
    vpc_support = Column(Boolean)
    load_balancing = Column(Boolean)
    cdn_integration = Column(Boolean)
    private_networking = Column(Boolean)


class SecurityFeatures(Base):
    __tablename__ = 'security_features'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    encryption_at_rest = Column(Boolean)
    encryption_in_transit = Column(Boolean)
    key_management = Column(Boolean)
    identity_management = Column(Boolean)
    network_security = Column(Boolean)
    vulnerability_scanning = Column(Boolean)
    security_monitoring = Column(Boolean)
    penetration_testing = Column(Boolean)


class PlatformInformation(Base):
    __tablename__ = 'platform_information'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_name = Column(String(512))
    platform_type = Column(platform_types_enum)
    parent_company = Column(String(512))
    founded_date = Column(DateTime(timezone=True))
    headquarters = Column(String(512))
    website_url = Column(String(1024))
    documentation_url = Column(String(1024))
    primary_datacenter_tier = Column(datacenter_tier_enum)
    total_datacenters = Column(Integer)
    edge_locations = Column(Integer)
    custom_configuration_support = Column(Boolean)
    bare_metal_available = Column(Boolean)
    networking_id = Column(
        BigInteger,
        ForeignKey(
            'platforms.network_capabilities.id',
            ondelete='CASCADE'
        )
    )
    security_id = Column(
        BigInteger,
        ForeignKey(
            'platforms.security_features.id',
            ondelete='CASCADE'
        )
    )
    sla_uptime = Column(Numeric(20))
    specializations = Column(ARRAY(String(1024)))
    target_markets = Column(ARRAY(String(1024)))
    notable_customers = Column(ARRAY(String(1024)))
    partnerships = Column(ARRAY(String(512)))
    last_updated = Column(DateTime(timezone=True), default=datetime.utcnow)
    data_sources = Column(ARRAY(String(1024)))

    # Relationships
    network_capabilities = relationship(
        "NetworkCapabilities", backref="platforms")
    security_features = relationship("SecurityFeatures", backref="platforms")


class GeographicRegions(Base):
    __tablename__ = 'geographic_regions'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    region_name = Column(String(256), nullable=False)
    region_code = Column(String(256), nullable=False)
    country = Column(String(2), nullable=False)
    availability_zones = Column(Integer)
    datacenter_tier = Column(datacenter_tier_enum)
    edge_location = Column(Boolean)

    platform = relationship("PlatformInformation",
                            backref="geographic_regions")


class ComplianceCertification(Base):
    __tablename__ = 'compliance_certification'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    certification_name = Column(String(100), nullable=False)
    certification_date = Column(DateTime(timezone=True))
    certifying_body = Column(String(256))
    certificate_url = Column(String(512))

    platform = relationship("PlatformInformation",
                            backref="compliance_certifications")


class ComputeInstance(Base):
    __tablename__ = 'compute_instance'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    instance_name = Column(String(512))
    instance_family = Column(String(512))
    vcpus = Column(Integer, nullable=False)
    memory_gb = Column(Numeric(2))
    storage_gb = Column(Numeric(2))
    storage_type = Column(String(128))
    gpu_count = Column(Integer)
    gpu_type = Column(String(512))
    gpu_memory_gb = Column(Numeric(2))
    network_performance = Column(String(512))
    architecture = Column(String(128))
    specialized_hardware = Column(String(1024))

    platform = relationship("PlatformInformation", backref="compute_instances")


class PricingModel(Base):
    __tablename__ = 'pricing_model'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    compute_instance_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    pricing_type = Column(pricing_type_enum)
    price_per_hour = Column(Numeric(6))
    price_per_month = Column(Numeric(6))
    minimum_commitment = Column(String(1024))
    billing_increment = Column(billing_increment_enum)

    platform = relationship("PlatformInformation", backref="pricing_models")


class SupportTier(Base):
    __tablename__ = 'support_tier'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    tier_name = Column(String(256))
    average_response_time = Column(String(512))
    channels = Column(ARRAY(String(256)))
    hours = Column(String(512))
    price = Column(String(512))
    premium_features = Column(ARRAY(String(1024)))

    platform = relationship("PlatformInformation", backref="support_tiers")


class ProprietarySoftware(Base):
    __tablename__ = 'proprietary_software'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    software_name = Column(String(512))
    software_type = Column(String(256))
    description = Column(String(1024))
    version = Column(String(128))
    open_source = Column(Boolean)
    license_type = Column(String(128))
    documentation_url = Column(String(1024))
    github_url = Column(String(1024))
    use_cases = Column(ARRAY(String(1024)))

    platform = relationship("PlatformInformation",
                            backref="proprietary_software")


class ProprietaryHardware(Base):
    __tablename__ = 'proprietary_hardware'
    __table_args__ = {'schema': 'platforms'}

    id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger, ForeignKey(
        'platforms.platform_information.id'), nullable=False)
    hardware_name = Column(String(512))
    hardware_type = Column(String(256))
    description = Column(String(1024))
    specifications = Column(JSON)
    performance_metrics = Column(JSON)
    availability = Column(String(512))
    generation = Column(String(128))
    manufacturing_partner = Column(ARRAY(String(512)))
    use_cases = Column(ARRAY(String(1024)))

    platform = relationship("PlatformInformation",
                            backref="proprietary_hardware")
