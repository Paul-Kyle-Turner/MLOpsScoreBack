
from sql_model.platforms import (
    PlatformInformation,
)

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
        raise e
