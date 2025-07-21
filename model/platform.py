from pydantic import AliasChoices, BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime, date
from decimal import Decimal


class PlatformType(str, Enum):
    """Platform type classifications"""
    HYPERSCALER = "hyperscaler"  # AWS, GCP, Azure
    GPU_CLOUD = "gpu_cloud"      # CoreWeave, Lambda Labs, RunPod
    EDGE_CLOUD = "edge_cloud"    # Smaller regional providers
    HYBRID_CLOUD = "hybrid_cloud"
    PRIVATE_CLOUD = "private_cloud"
    SPECIALIZED_AI = "specialized_ai"  # AI-focused platforms
    CONTAINER_PLATFORM = "container_platform"  # Kubernetes-focused
    SERVERLESS = "serverless"
    OTHER = "other"


class DatacenterTier(str, Enum):
    """Datacenter tier classifications"""
    TIER_1 = "tier_1"  # 99.671% uptime, basic infrastructure
    TIER_2 = "tier_2"  # 99.741% uptime, redundant components
    TIER_3 = "tier_3"  # 99.982% uptime, concurrently maintainable
    TIER_4 = "tier_4"  # 99.995% uptime, fault tolerant
    TIER_5 = "tier_5"  # 99.999% uptime, fully redundant
    COLOCATION = "colocation"  # Third-party datacenter
    EDGE = "edge"      # Edge computing facilities
    HYBRID = "hybrid"  # Mix of tiers
    UNKNOWN = "unknown"


class ComplianceStatus(str, Enum):
    """Compliance certification status"""
    CERTIFIED = "certified"
    IN_PROGRESS = "in_progress"
    PLANNED = "planned"
    NOT_APPLICABLE = "not_applicable"
    UNKNOWN = "unknown"


class PricingType(str, Enum):
    """Compute instance pricing models"""
    ON_DEMAND = "on_demand"
    RESERVED = "reserved"
    SPOT = "spot"
    PREEMPTIBLE = "preemptible"
    DEDICATED = "dedicated"
    BURSTABLE = "burstable"


class BillingIncrement(str, Enum):
    """Billing increment options"""
    PER_SECOND = "per_second"
    PER_MINUTE = "per_minute"
    PER_HOUR = "per_hour"
    PER_DAY = "per_day"
    PER_MONTH = "per_month"
    PER_YEAR = "per_year"
    ONE_TIME = "one_time"
    CUSTOM = "custom"


class GeographicRegion(BaseModel):
    """Geographic region information"""
    id: Optional[int] = Field(None, description="Unique identifier")
    region_name: str = Field(
        description="Name of the region",
        validation_alias=AliasChoices("region", "region_name", "regionName")
    )
    region_code: Optional[str] = Field(
        None,
        description="Region code (e.g., us-east-1)",
        validation_alias=AliasChoices("region_code", "regionCode")
    )
    country_code: str = Field(
        description="Country where region is located",
        validation_alias=AliasChoices("country_code", "countryCode")
    )
    availability_zones: Optional[int] = Field(
        None,
        description="Number of availability zones",
        validation_alias=AliasChoices(
            "availability_zones", "availabilityZones")
    )
    datacenter_tier: DatacenterTier = Field(
        description="Datacenter tier classification",
        validation_alias=AliasChoices("datacenter_tier", "datacenterTier")
    )
    edge_location: bool = Field(
        default=False,
        description="Whether this is an edge location",
        validation_alias=AliasChoices("edge_location", "edgeLocation")
    )

    @field_validator('datacenter_tier', mode='before')
    @classmethod
    def validate_datacenter_tier(cls, v):
        """Normalize datacenter tier input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for tier in DatacenterTier:
                if tier.value == normalized:
                    return tier
            # If no exact match, return original for standard enum validation
            return v
        return v


class ComplianceCertification(BaseModel):
    """Compliance certification details"""
    id: Optional[int] = Field(None, description="Unique identifier")
    certification_name: str = Field(
        description="Name of certification",
        validation_alias=AliasChoices(
            "certification_name", "certificationName")
    )
    status: ComplianceStatus = Field(
        description="Current status"
    )
    certification_date: Optional[date] = Field(
        None,
        description="Date of certification",
        validation_alias=AliasChoices(
            "certification_date", "certificationDate")
    )
    certifying_body: Optional[str] = Field(
        None,
        description="Certifying organization",
        validation_alias=AliasChoices("certifying_body", "certifyingBody")
    )
    certificate_url: Optional[str] = Field(
        None,
        description="URL to certificate",
        validation_alias=AliasChoices("certificate_url", "certificateUrl")
    )

    @field_validator('status', mode='before')
    @classmethod
    def validate_status(cls, v):
        """Normalize compliance status input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for status in ComplianceStatus:
                if status.value == normalized:
                    return status
            # If no exact match, return original for standard enum validation
            return v
        return v


class PricingModel(BaseModel):
    """Pricing model details"""
    id: Optional[int] = Field(None, description="Unique identifier")
    pricing_type: PricingType = Field(
        description="Type of pricing model",
        validation_alias=AliasChoices("pricing_type", "pricingType")
    )
    price_per_hour: Optional[Decimal] = Field(
        None,
        description="Price per hour",
        validation_alias=AliasChoices("price_per_hour", "pricePerHour")
    )
    price_per_month: Optional[Decimal] = Field(
        None,
        description="Price per month",
        validation_alias=AliasChoices("price_per_month", "pricePerMonth")
    )
    minimum_commitment: Optional[str] = Field(
        None,
        description="Minimum commitment period",
        validation_alias=AliasChoices(
            "minimum_commitment", "minimumCommitment")
    )
    billing_increment: Optional[BillingIncrement] = Field(
        None,
        description="Billing increment",
        validation_alias=AliasChoices("billing_increment", "billingIncrement")
    )

    @field_validator('pricing_type', mode='before')
    @classmethod
    def validate_pricing_type(cls, v):
        """Normalize pricing type input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for pricing_type in PricingType:
                if pricing_type.value == normalized:
                    return pricing_type
            # If no exact match, return original for standard enum validation
            return v
        return v

    @field_validator('billing_increment', mode='before')
    @classmethod
    def validate_billing_increment(cls, v):
        """Normalize billing increment input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for increment in BillingIncrement:
                if increment.value == normalized:
                    return increment
            # If no exact match, return original for standard enum validation
            return v
        return v


class ComputeInstance(BaseModel):
    """Compute instance specification"""
    id: Optional[int] = Field(None, description="Unique identifier")
    instance_name: str = Field(
        description="Instance type name",
        validation_alias=AliasChoices("instance_name", "instanceName")
    )
    instance_family: Optional[str] = Field(
        None,
        description="Instance family",
        validation_alias=AliasChoices("instance_family", "instanceFamily")
    )
    vcpus: int = Field(
        description="Number of vCPUs"
    )
    memory_gb: float = Field(
        description="Memory in GB",
        validation_alias=AliasChoices("memory_gb", "memoryGb")
    )
    storage_gb: Optional[float] = Field(
        None,
        description="Local storage in GB",
        validation_alias=AliasChoices("storage_gb", "storageGb")
    )
    storage_type: Optional[str] = Field(
        None,
        description="Storage type (SSD, NVMe, etc.)",
        validation_alias=AliasChoices("storage_type", "storageType")
    )
    gpu_count: Optional[int] = Field(
        None,
        description="Number of GPUs",
        validation_alias=AliasChoices("gpu_count", "gpuCount")
    )
    gpu_type: Optional[str] = Field(
        None,
        description="GPU type",
        validation_alias=AliasChoices("gpu_type", "gpuType")
    )
    gpu_memory_gb: Optional[float] = Field(
        None,
        description="GPU memory in GB",
        validation_alias=AliasChoices("gpu_memory_gb", "gpuMemoryGb")
    )
    network_performance: Optional[str] = Field(
        None,
        description="Network performance tier",
        validation_alias=AliasChoices(
            "network_performance", "networkPerformance")
    )
    pricing_models: List[PricingModel] = Field(
        description="Available pricing models for this instance",
        validation_alias=AliasChoices("pricing_models", "pricingModels")
    )
    architecture: Optional[str] = Field(
        None,
        description="CPU architecture (x86, ARM, etc.)"
    )
    specialized_hardware: Optional[str] = Field(
        None,
        description="Specialized hardware features",
        validation_alias=AliasChoices(
            "specialized_hardware", "specializedHardware")
    )


class ProprietarySoftware(BaseModel):
    """Proprietary software developed by the platform"""
    id: Optional[int] = Field(None, description="Unique identifier")
    software_name: str = Field(
        description="Name of the software",
        validation_alias=AliasChoices("software_name", "softwareName")
    )
    software_type: str = Field(
        description="Type of software (orchestration, monitoring, etc.)",
        validation_alias=AliasChoices("software_type", "softwareType")
    )
    description: str = Field(
        description="Description of the software"
    )
    version: Optional[str] = Field(
        None,
        description="Current version"
    )
    open_source: bool = Field(
        default=False,
        description="Whether software is open source",
        validation_alias=AliasChoices("open_source", "openSource")
    )
    license_type: Optional[str] = Field(
        None,
        description="License type",
        validation_alias=AliasChoices("license_type", "licenseType")
    )
    documentation_url: Optional[str] = Field(
        None,
        description="Documentation URL",
        validation_alias=AliasChoices("documentation_url", "documentationUrl")
    )
    github_url: Optional[str] = Field(
        None,
        description="GitHub repository URL",
        validation_alias=AliasChoices("github_url", "githubUrl")
    )
    use_cases: Optional[List[str]] = Field(
        None,
        description="Primary use cases",
        validation_alias=AliasChoices("use_cases", "useCases")
    )


class ProprietaryHardware(BaseModel):
    """Proprietary hardware developed by the platform"""
    id: Optional[int] = Field(None, description="Unique identifier")
    hardware_name: str = Field(
        description="Name of the hardware",
        validation_alias=AliasChoices("hardware_name", "hardwareName")
    )
    hardware_type: str = Field(
        description="Type of hardware (chip, server, networking, etc.)",
        validation_alias=AliasChoices("hardware_type", "hardwareType")
    )
    description: str = Field(
        description="Description of the hardware"
    )
    specifications: Optional[Dict[str, Any]] = Field(
        None,
        description="Hardware specifications"
    )
    performance_metrics: Optional[Dict[str, Any]] = Field(
        None,
        description="Performance benchmarks",
        validation_alias=AliasChoices(
            "performance_metrics", "performanceMetrics")
    )
    availability: Optional[str] = Field(
        None,
        description="Availability status"
    )
    generation: Optional[str] = Field(
        None,
        description="Hardware generation"
    )
    manufacturing_partner: Optional[str] = Field(
        None,
        description="Manufacturing partner",
        validation_alias=AliasChoices(
            "manufacturing_partner", "manufacturingPartner")
    )
    use_cases: Optional[List[str]] = Field(
        None,
        description="Primary use cases",
        validation_alias=AliasChoices("use_cases", "useCases")
    )


class NetworkingCapabilities(BaseModel):
    """Networking capabilities and features"""
    id: Optional[int] = Field(None, description="Unique identifier")
    bandwidth_gbps: Optional[float] = Field(
        None,
        description="Network bandwidth in Gbps",
        validation_alias=AliasChoices("bandwidth_gbps", "bandwidthGbps")
    )
    network_type: Optional[str] = Field(
        None,
        description="Network type (Ethernet, InfiniBand, etc.)",
        validation_alias=AliasChoices("network_type", "networkType")
    )
    interconnect_technology: Optional[str] = Field(
        None,
        description="Interconnect technology",
        validation_alias=AliasChoices(
            "interconnect_technology", "interconnectTechnology")
    )
    vpc_support: bool = Field(
        default=False,
        description="Virtual Private Cloud support",
        validation_alias=AliasChoices("vpc_support", "vpcSupport")
    )
    load_balancing: bool = Field(
        default=False,
        description="Load balancing capabilities",
        validation_alias=AliasChoices("load_balancing", "loadBalancing")
    )
    cdn_integration: bool = Field(
        default=False,
        description="CDN integration",
        validation_alias=AliasChoices("cdn_integration", "cdnIntegration")
    )
    private_networking: bool = Field(
        default=False,
        description="Private networking options",
        validation_alias=AliasChoices(
            "private_networking", "privateNetworking")
    )


class SecurityFeatures(BaseModel):
    """Security features and capabilities"""
    id: Optional[int] = Field(None, description="Unique identifier")
    encryption_at_rest: bool = Field(
        default=False,
        description="Encryption at rest",
        validation_alias=AliasChoices("encryption_at_rest", "encryptionAtRest")
    )
    encryption_in_transit: bool = Field(
        default=False,
        description="Encryption in transit",
        validation_alias=AliasChoices(
            "encryption_in_transit", "encryptionInTransit")
    )
    key_management: bool = Field(
        default=False,
        description="Key management service",
        validation_alias=AliasChoices("key_management", "keyManagement")
    )
    identity_management: bool = Field(
        default=False,
        description="Identity and access management",
        validation_alias=AliasChoices(
            "identity_management", "identityManagement")
    )
    network_security: bool = Field(
        default=False,
        description="Network security features",
        validation_alias=AliasChoices("network_security", "networkSecurity")
    )
    vulnerability_scanning: bool = Field(
        default=False,
        description="Vulnerability scanning",
        validation_alias=AliasChoices(
            "vulnerability_scanning", "vulnerabilityScanning")
    )
    security_monitoring: bool = Field(
        default=False,
        description="Security monitoring",
        validation_alias=AliasChoices(
            "security_monitoring", "securityMonitoring")
    )
    penetration_testing: bool = Field(
        default=False,
        description="Regular penetration testing",
        validation_alias=AliasChoices(
            "penetration_testing", "penetrationTesting")
    )


class SupportTier(BaseModel):
    """Support tier information"""
    id: Optional[int] = Field(None, description="Unique identifier")
    tier_name: str = Field(
        description="Support tier name",
        validation_alias=AliasChoices("tier_name", "tierName")
    )
    average_response_time: Optional[str] = Field(
        None,
        description="Average response time SLA",
        validation_alias=AliasChoices(
            "average_response_time", "averageResponseTime")
    )
    channels: List[str] = Field(
        description="Support channels available"
    )
    hours: str = Field(
        description="Support hours"
    )
    price: Optional[str] = Field(
        None,
        description="Pricing structure"
    )
    premium_features: Optional[List[str]] = Field(
        None,
        description="Premium support features",
        validation_alias=AliasChoices("premium_features", "premiumFeatures")
    )


class PlatformInformation(BaseModel):
    """Comprehensive platform information model"""

    # Unique identifier
    id: Optional[int] = Field(None, description="Unique identifier")

    # Basic Platform Information
    platform_name: str = Field(
        description="Official platform name",
        validation_alias=AliasChoices("platform_name", "platformName")
    )
    platform_type: PlatformType = Field(
        description="Platform type classification",
        validation_alias=AliasChoices("platform_type", "platformType")
    )
    parent_company: Optional[str] = Field(
        None,
        description="Parent company name",
        validation_alias=AliasChoices("parent_company", "parentCompany")
    )
    founded_date: Optional[date] = Field(
        None,
        description="Platform founding date",
        validation_alias=AliasChoices("founded_date", "foundedDate")
    )
    headquarters: Optional[str] = Field(
        None,
        description="Company headquarters location"
    )
    website_url: str = Field(
        description="Official website URL",
        validation_alias=AliasChoices("website_url", "websiteUrl")
    )
    documentation_url: Optional[str] = Field(
        None,
        description="Documentation URL",
        validation_alias=AliasChoices("documentation_url", "documentationUrl")
    )

    # Geographic and Infrastructure
    regions: List[GeographicRegion] = Field(
        description="Available geographic regions"
    )
    primary_datacenter_tier: DatacenterTier = Field(
        description="Primary datacenter tier",
        validation_alias=AliasChoices(
            "primary_datacenter_tier", "primaryDatacenterTier")
    )
    total_datacenters: Optional[int] = Field(
        None,
        description="Total number of datacenters",
        validation_alias=AliasChoices("total_datacenters", "totalDatacenters")
    )
    edge_locations: Optional[int] = Field(
        None,
        description="Number of edge locations",
        validation_alias=AliasChoices("edge_locations", "edgeLocations")
    )

    # Compliance and Certifications
    compliance_certifications: List[ComplianceCertification] = Field(
        default=[],
        description="Compliance certifications",
        validation_alias=AliasChoices(
            "compliance_certifications", "complianceCertifications")
    )

    # Compute Resources
    compute_instances: List[ComputeInstance] = Field(
        description="Available compute instances",
        validation_alias=AliasChoices("compute_instances", "computeInstances")
    )
    custom_configuration_support: bool = Field(
        default=False,
        description="Custom configuration support",
        validation_alias=AliasChoices(
            "custom_configuration_support", "customConfigurationSupport")
    )
    bare_metal_available: bool = Field(
        default=False,
        description="Bare metal instances available",
        validation_alias=AliasChoices(
            "bare_metal_available", "bareMetalAvailable")
    )

    # Proprietary Technology
    proprietary_software: List[ProprietarySoftware] = Field(
        default=[],
        description="Proprietary software developed by platform",
        validation_alias=AliasChoices(
            "proprietary_software", "proprietarySoftware")
    )
    proprietary_hardware: List[ProprietaryHardware] = Field(
        default=[],
        description="Proprietary hardware developed by platform",
        validation_alias=AliasChoices(
            "proprietary_hardware", "proprietaryHardware")
    )

    # Technical Capabilities
    networking: NetworkingCapabilities = Field(
        description="Networking capabilities"
    )
    security_features: SecurityFeatures = Field(
        description="Security features",
        validation_alias=AliasChoices("security_features", "securityFeatures")
    )

    # Service and Support
    support_tiers: List[SupportTier] = Field(
        description="Available support tiers",
        validation_alias=AliasChoices("support_tiers", "supportTiers")
    )
    sla_uptime: Optional[float] = Field(
        None,
        description="SLA uptime percentage",
        validation_alias=AliasChoices("sla_uptime", "slaUptime")
    )

    # Additional Information
    specializations: Optional[List[str]] = Field(
        None,
        description="Platform specializations"
    )
    target_markets: Optional[List[str]] = Field(
        None,
        description="Target market segments",
        validation_alias=AliasChoices("target_markets", "targetMarkets")
    )
    notable_customers: Optional[List[str]] = Field(
        None,
        description="Notable customers (if public)",
        validation_alias=AliasChoices("notable_customers", "notableCustomers")
    )
    partnerships: Optional[List[str]] = Field(
        None,
        description="Strategic partnerships"
    )

    # Metadata
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp",
        validation_alias=AliasChoices("last_updated", "lastUpdated")
    )
    data_sources: Optional[List[str]] = Field(
        None,
        description="Sources of information",
        validation_alias=AliasChoices("data_sources", "dataSources")
    )

    # Computed Properties
    @property
    def has_soc2_compliance(self) -> bool:
        """Check if platform has SOC2 compliance"""
        return any(cert.certification_name.upper() == "SOC2" or "SOC 2" in cert.certification_name.upper()
                   for cert in self.compliance_certifications)

    @property
    def available_pricing_types(self) -> List[PricingType]:
        """Get list of available pricing types across all instances"""
        pricing_types = set()
        for instance in self.compute_instances:
            for pricing_model in instance.pricing_models:
                pricing_types.add(pricing_model.pricing_type)
        return list(pricing_types)

    @property
    def gpu_instances_available(self) -> bool:
        """Check if GPU instances are available"""
        return any(instance.gpu_count and instance.gpu_count > 0 for instance in self.compute_instances)

    @property
    def compliance_summary(self) -> Dict[str, int]:
        """Get compliance certification summary"""
        summary = {}
        for cert in self.compliance_certifications:
            summary[cert.status] = summary.get(cert.status, 0) + 1
        return summary

    def get_instances_by_pricing_type(self, pricing_type: PricingType) -> List[ComputeInstance]:
        """Get instances that support a specific pricing type"""
        return [instance for instance in self.compute_instances
                if any(pm.pricing_type == pricing_type for pm in instance.pricing_models)]

    def get_regions_by_tier(self, tier: DatacenterTier) -> List[GeographicRegion]:
        """Get regions by datacenter tier"""
        return [region for region in self.regions if region.datacenter_tier == tier]

    def get_compliance_by_status(self, status: ComplianceStatus) -> List[ComplianceCertification]:
        """Get compliance certifications by status"""
        return [cert for cert in self.compliance_certifications if cert.status == status]

    def get_pricing_models_by_type(self, pricing_type: PricingType) -> List[PricingModel]:
        """Get all pricing models of a specific type"""
        models = []
        # From compute instances
        for instance in self.compute_instances:
            models.extend(
                [pm for pm in instance.pricing_models if pm.pricing_type == pricing_type])
        return models

    @field_validator('platform_type', mode='before')
    @classmethod
    def validate_platform_type(cls, v):
        """Normalize platform type input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for platform_type in PlatformType:
                if platform_type.value == normalized:
                    return platform_type
            # If no exact match, return original for standard enum validation
            return v
        return v

    @field_validator('primary_datacenter_tier', mode='before')
    @classmethod
    def validate_primary_datacenter_tier(cls, v):
        """Normalize primary datacenter tier input"""
        if isinstance(v, str):
            normalized = v.lower().replace(' ', '_')
            # Try to find matching enum value
            for tier in DatacenterTier:
                if tier.value == normalized:
                    return tier
            # If no exact match, return original for standard enum validation
            return v
        return v

    class Config:
        use_enum_values = True
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
