from pydantic import BaseModel, Field, validator, HttpUrl
from typing import Optional, List, Dict, Any, Union
from enum import Enum
from datetime import datetime, date
from decimal import Decimal


class PlatformType(str, Enum):
    """Platform type classifications"""
    HYPERSCALER = "Hyperscaler"  # AWS, GCP, Azure
    GPU_CLOUD = "GPU Cloud"      # CoreWeave, Lambda Labs, RunPod
    EDGE_CLOUD = "Edge Cloud"    # Smaller regional providers
    HYBRID_CLOUD = "Hybrid Cloud"
    PRIVATE_CLOUD = "Private Cloud"
    SPECIALIZED_AI = "Specialized AI"  # AI-focused platforms
    CONTAINER_PLATFORM = "Container Platform"  # Kubernetes-focused
    SERVERLESS = "Serverless"
    OTHER = "Other"


class DatacenterTier(str, Enum):
    """Datacenter tier classifications"""
    TIER_1 = "Tier 1"  # 99.671% uptime, basic infrastructure
    TIER_2 = "Tier 2"  # 99.741% uptime, redundant components
    TIER_3 = "Tier 3"  # 99.982% uptime, concurrently maintainable
    TIER_4 = "Tier 4"  # 99.995% uptime, fault tolerant
    TIER_5 = "Tier 5"  # 99.999% uptime, fully redundant
    COLOCATION = "Colocation"  # Third-party datacenter
    EDGE = "Edge"      # Edge computing facilities
    HYBRID = "Hybrid"  # Mix of tiers
    UNKNOWN = "Unknown"


class ComplianceStatus(str, Enum):
    """Compliance certification status"""
    CERTIFIED = "Certified"
    IN_PROGRESS = "In Progress"
    PLANNED = "Planned"
    NOT_APPLICABLE = "Not Applicable"
    UNKNOWN = "Unknown"


class PricingType(str, Enum):
    """Compute instance pricing models"""
    ON_DEMAND = "On-Demand"
    RESERVED = "Reserved"
    SPOT = "Spot"
    PREEMPTIBLE = "Preemptible"
    DEDICATED = "Dedicated"
    BURSTABLE = "Burstable"


class BillingIncrement(str, Enum):
    """Billing increment options"""
    PER_SECOND = "Per Second"
    PER_MINUTE = "Per Minute"
    PER_HOUR = "Per Hour"
    PER_DAY = "Per Day"
    PER_MONTH = "Per Month"
    PER_YEAR = "Per Year"
    ONE_TIME = "One Time"
    CUSTOM = "Custom"


class GeographicRegion(BaseModel):
    """Geographic region information"""
    region_name: str = Field(
        description="Name of the region"
    )
    region_code: Optional[str] = Field(
        None,
        description="Region code (e.g., us-east-1)"
    )
    country_code: str = Field(
        description="Country where region is located"
    )
    availability_zones: Optional[int] = Field(
        None,
        description="Number of availability zones"
    )
    datacenter_tier: DatacenterTier = Field(
        description="Datacenter tier classification"
    )
    edge_location: bool = Field(
        default=False,
        description="Whether this is an edge location"
    )


class ComplianceCertification(BaseModel):
    """Compliance certification details"""
    certification_name: str = Field(
        description="Name of certification"
    )
    status: ComplianceStatus = Field(
        description="Current status"
    )
    certification_date: Optional[date] = Field(
        None,
        description="Date of certification"
    )
    certifying_body: Optional[str] = Field(
        None,
        description="Certifying organization"
    )
    certificate_url: Optional[HttpUrl] = Field(
        None,
        description="URL to certificate"
    )


class PricingModel(BaseModel):
    """Pricing model details"""
    pricing_type: PricingType = Field(
        description="Type of pricing model"
    )
    price_per_hour: Optional[Decimal] = Field(
        None,
        description="Price per hour"
    )
    price_per_month: Optional[Decimal] = Field(
        None,
        description="Price per month"
    )
    minimum_commitment: Optional[str] = Field(
        None,
        description="Minimum commitment period"
    )
    billing_increment: Optional[BillingIncrement] = Field(
        None,
        description="Billing increment"
    )


class ComputeInstance(BaseModel):
    """Compute instance specification"""
    instance_name: str = Field(
        description="Instance type name"
    )
    instance_family: Optional[str] = Field(
        None,
        description="Instance family"
    )
    vcpus: int = Field(
        description="Number of vCPUs"
    )
    memory_gb: float = Field(
        description="Memory in GB"
    )
    storage_gb: Optional[float] = Field(
        None,
        description="Local storage in GB"
    )
    storage_type: Optional[str] = Field(
        None,
        description="Storage type (SSD, NVMe, etc.)"
    )
    gpu_count: Optional[int] = Field(
        None,
        description="Number of GPUs"
    )
    gpu_type: Optional[str] = Field(
        None,
        description="GPU type"
    )
    gpu_memory_gb: Optional[float] = Field(
        None,
        description="GPU memory in GB"
    )
    network_performance: Optional[str] = Field(
        None,
        description="Network performance tier"
    )
    pricing_models: List[PricingModel] = Field(
        description="Available pricing models for this instance"
    )
    architecture: Optional[str] = Field(
        None,
        description="CPU architecture (x86, ARM, etc.)"
    )
    specialized_hardware: Optional[str] = Field(
        None,
        description="Specialized hardware features"
    )


class ProprietarySoftware(BaseModel):
    """Proprietary software developed by the platform"""
    software_name: str = Field(
        description="Name of the software"
    )
    software_type: str = Field(
        description="Type of software (orchestration, monitoring, etc.)"
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
        description="Whether software is open source"
    )
    license_type: Optional[str] = Field(
        None,
        description="License type"
    )
    documentation_url: Optional[HttpUrl] = Field(
        None,
        description="Documentation URL"
    )
    github_url: Optional[HttpUrl] = Field(
        None,
        description="GitHub repository URL"
    )
    use_cases: Optional[List[str]] = Field(
        None,
        description="Primary use cases"
    )


class ProprietaryHardware(BaseModel):
    """Proprietary hardware developed by the platform"""
    hardware_name: str = Field(
        description="Name of the hardware"
    )
    hardware_type: str = Field(
        description="Type of hardware (chip, server, networking, etc.)"
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
        description="Performance benchmarks"
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
        description="Manufacturing partner"
    )
    use_cases: Optional[List[str]] = Field(
        None,
        description="Primary use cases"
    )


class NetworkingCapabilities(BaseModel):
    """Networking capabilities and features"""
    bandwidth_gbps: Optional[float] = Field(
        None,
        description="Network bandwidth in Gbps"
    )
    network_type: Optional[str] = Field(
        None,
        description="Network type (Ethernet, InfiniBand, etc.)"
    )
    interconnect_technology: Optional[str] = Field(
        None,
        description="Interconnect technology"
    )
    vpc_support: bool = Field(
        default=False,
        description="Virtual Private Cloud support"
    )
    load_balancing: bool = Field(
        default=False,
        description="Load balancing capabilities"
    )
    cdn_integration: bool = Field(
        default=False,
        description="CDN integration"
    )
    private_networking: bool = Field(
        default=False,
        description="Private networking options"
    )


class SecurityFeatures(BaseModel):
    """Security features and capabilities"""
    encryption_at_rest: bool = Field(
        default=False,
        description="Encryption at rest"
    )
    encryption_in_transit: bool = Field(
        default=False,
        description="Encryption in transit"
    )
    key_management: bool = Field(
        default=False,
        description="Key management service"
    )
    identity_management: bool = Field(
        default=False,
        description="Identity and access management"
    )
    network_security: bool = Field(
        default=False,
        description="Network security features"
    )
    vulnerability_scanning: bool = Field(
        default=False,
        description="Vulnerability scanning"
    )
    security_monitoring: bool = Field(
        default=False,
        description="Security monitoring"
    )
    penetration_testing: bool = Field(
        default=False,
        description="Regular penetration testing"
    )


class SupportTier(BaseModel):
    """Support tier information"""
    tier_name: str = Field(
        description="Support tier name"
    )
    average_response_time: Optional[str] = Field(
        None,
        description="Average response time SLA"
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
        description="Premium support features"
    )


class PlatformInformation(BaseModel):
    """Comprehensive platform information model"""

    # Basic Platform Information
    platform_name: str = Field(
        description="Official platform name"
    )
    platform_type: PlatformType = Field(
        description="Platform type classification"
    )
    parent_company: Optional[str] = Field(
        None,
        description="Parent company name"
    )
    founded_date: Optional[date] = Field(
        None,
        description="Platform founding date"
    )
    headquarters: Optional[str] = Field(
        None,
        description="Company headquarters location"
    )
    website_url: HttpUrl = Field(
        description="Official website URL"
    )
    documentation_url: Optional[HttpUrl] = Field(
        None,
        description="Documentation URL"
    )

    # Geographic and Infrastructure
    regions: List[GeographicRegion] = Field(
        description="Available geographic regions"
    )
    primary_datacenter_tier: DatacenterTier = Field(
        description="Primary datacenter tier"
    )
    total_datacenters: Optional[int] = Field(
        None,
        description="Total number of datacenters"
    )
    edge_locations: Optional[int] = Field(
        None,
        description="Number of edge locations"
    )

    # Compliance and Certifications
    compliance_certifications: List[ComplianceCertification] = Field(
        default=[],
        description="Compliance certifications"
    )

    # Compute Resources
    compute_instances: List[ComputeInstance] = Field(
        description="Available compute instances"
    )
    custom_configuration_support: bool = Field(
        default=False,
        description="Custom configuration support"
    )
    bare_metal_available: bool = Field(
        default=False,
        description="Bare metal instances available"
    )

    # Proprietary Technology
    proprietary_software: List[ProprietarySoftware] = Field(
        default=[],
        description="Proprietary software developed by platform"
    )
    proprietary_hardware: List[ProprietaryHardware] = Field(
        default=[],
        description="Proprietary hardware developed by platform"
    )

    # Technical Capabilities
    networking: NetworkingCapabilities = Field(
        description="Networking capabilities"
    )
    security_features: SecurityFeatures = Field(
        description="Security features"
    )

    # Service and Support
    support_tiers: List[SupportTier] = Field(
        description="Available support tiers"
    )
    sla_uptime: Optional[float] = Field(
        None,
        description="SLA uptime percentage"
    )

    # Additional Information
    specializations: Optional[List[str]] = Field(
        None,
        description="Platform specializations"
    )
    target_markets: Optional[List[str]] = Field(
        None,
        description="Target market segments"
    )
    notable_customers: Optional[List[str]] = Field(
        None,
        description="Notable customers (if public)"
    )
    partnerships: Optional[List[str]] = Field(
        None,
        description="Strategic partnerships"
    )

    # Metadata
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )
    data_sources: Optional[List[str]] = Field(
        None,
        description="Sources of information"
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

    class Config:
        use_enum_values = True
        validate_assignment = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
