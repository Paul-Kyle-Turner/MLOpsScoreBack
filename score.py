from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class ScoreRange(BaseModel):
    """Score range validation model"""
    min_score: int = Field(default=1, ge=1, le=10)
    max_score: int = Field(default=10, ge=1, le=10)


class PlatformType(str, Enum):
    """Supported platform types"""
    AWS = "AWS"
    AZURE = "Azure"
    GCP = "Google Cloud Platform"
    COREWEAVE = "CoreWeave"
    LAMBDA_LABS = "Lambda Labs"
    DATABRICKS = "Databricks"
    OTHER = "Other"


class ComputeAndScaling(BaseModel):
    """Compute and scaling capabilities"""
    compute_variety_score: int = Field(
        ge=1,
        le=10,
        description="Variety of compute options (CPU, GPU, TPU, etc.)"
    )
    auto_scaling_score: int = Field(
        ge=1,
        le=10,
        description="Auto-scaling capabilities"
    )
    spot_instance_support: int = Field(
        ge=1,
        le=10,
        description="Spot/preemptible instance availability"
    )
    distributed_training_support: int = Field(
        ge=1,
        le=10,
        description="Multi-node distributed training"
    )

    @property
    def overall_score(self) -> float:
        return (self.compute_variety_score + self.auto_scaling_score +
                self.spot_instance_support + self.distributed_training_support) / 4


class DataManagement(BaseModel):
    """Data management and storage capabilities"""
    storage_options_score: int = Field(
        ge=1,
        le=10,
        description="Variety of storage solutions"
    )
    data_versioning_score: int = Field(
        ge=1,
        le=10,
        description="Data versioning capabilities"
    )
    data_pipeline_orchestration: int = Field(
        ge=1,
        le=10,
        description="Data pipeline tools"
    )
    data_integration_score: int = Field(
        ge=1,
        le=10,
        description="Integration with data sources"
    )

    @property
    def overall_score(self) -> float:
        return (self.storage_options_score + self.data_versioning_score +
                self.data_pipeline_orchestration + self.data_integration_score) / 4


class ModelDevelopment(BaseModel):
    """Model development and training capabilities"""
    framework_support_score: int = Field(
        ge=1,
        le=10,
        description="ML framework support"
    )
    experiment_tracking_score: int = Field(
        ge=1,
        le=10,
        description="Experiment tracking tools"
    )
    hyperparameter_tuning_score: int = Field(
        ge=1,
        le=10,
        description="Hyperparameter optimization"
    )
    notebook_environment_score: int = Field(
        ge=1,
        le=10,
        description="Managed notebook environments"
    )

    @property
    def overall_score(self) -> float:
        return (self.framework_support_score + self.experiment_tracking_score +
                self.hyperparameter_tuning_score + self.notebook_environment_score) / 4


class MLOpsPipeline(BaseModel):
    """MLOps pipeline and orchestration capabilities"""
    workflow_orchestration_score: int = Field(
        ge=1,
        le=10,
        description="Workflow orchestration tools"
    )
    cicd_integration_score: int = Field(
        ge=1,
        le=10,
        description="CI/CD integration"
    )
    model_validation_score: int = Field(
        ge=1,
        le=10,
        description="Automated model validation"
    )
    environment_management_score: int = Field(
        ge=1,
        le=10,
        description="Environment management"
    )

    @property
    def overall_score(self) -> float:
        return (self.workflow_orchestration_score + self.cicd_integration_score +
                self.model_validation_score + self.environment_management_score) / 4


class ModelDeployment(BaseModel):
    """Model deployment and serving capabilities"""
    deployment_options_score: int = Field(
        ge=1,
        le=10,
        description="Variety of deployment options"
    )
    real_time_inference_score: int = Field(
        ge=1,
        le=10,
        description="Real-time inference capabilities"
    )
    batch_inference_score: int = Field(
        ge=1,
        le=10,
        description="Batch inference capabilities"
    )
    ab_testing_score: int = Field(
        ge=1,
        le=10,
        description="A/B testing support"
    )
    canary_deployment_score: int = Field(
        ge=1,
        le=10,
        description="Canary deployment capabilities"
    )

    @property
    def overall_score(self) -> float:
        return (self.deployment_options_score + self.real_time_inference_score +
                self.batch_inference_score + self.ab_testing_score +
                self.canary_deployment_score) / 5


class MonitoringAndObservability(BaseModel):
    """Monitoring and observability capabilities"""
    model_performance_monitoring: int = Field(
        ge=1,
        le=10,
        description="Model performance monitoring"
    )
    data_drift_detection: int = Field(
        ge=1,
        le=10,
        description="Data drift detection"
    )
    infrastructure_monitoring: int = Field(
        ge=1,
        le=10,
        description="Infrastructure monitoring"
    )
    logging_and_alerting: int = Field(
        ge=1,
        le=10,
        description="Logging and alerting systems"
    )
    model_explainability: int = Field(
        ge=1,
        le=10,
        description="Model explainability tools"
    )

    @property
    def overall_score(self) -> float:
        return (self.model_performance_monitoring + self.data_drift_detection +
                self.infrastructure_monitoring + self.logging_and_alerting +
                self.model_explainability) / 5


class SecurityAndCompliance(BaseModel):
    """Security and compliance capabilities"""
    identity_access_management: int = Field(
        ge=1,
        le=10,
        description="IAM capabilities"
    )
    data_encryption_score: int = Field(
        ge=1,
        le=10,
        description="Data encryption at rest and in transit"
    )
    compliance_certifications: int = Field(
        ge=1,
        le=10,
        description="Compliance certifications"
    )
    network_security_score: int = Field(
        ge=1,
        le=10,
        description="Network security features"
    )
    audit_logging_score: int = Field(
        ge=1,
        le=10,
        description="Audit logging capabilities"
    )

    @property
    def overall_score(self) -> float:
        return (self.identity_access_management + self.data_encryption_score +
                self.compliance_certifications + self.network_security_score +
                self.audit_logging_score) / 5


class CostManagement(BaseModel):
    """Cost management and optimization capabilities"""
    cost_transparency_score: int = Field(
        ge=1,
        le=10,
        description="Cost transparency and reporting"
    )
    resource_optimization_score: int = Field(
        ge=1,
        le=10,
        description="Resource utilization optimization"
    )
    pricing_flexibility_score: int = Field(
        ge=1,
        le=10,
        description="Flexible pricing models"
    )
    cost_prediction_score: int = Field(
        ge=1,
        le=10,
        description="Cost prediction and budgeting"
    )

    @property
    def overall_score(self) -> float:
        return (self.cost_transparency_score + self.resource_optimization_score +
                self.pricing_flexibility_score + self.cost_prediction_score) / 4


class DeveloperExperience(BaseModel):
    """Developer experience and integration capabilities"""
    api_sdk_quality_score: int = Field(
        ge=1,
        le=10,
        description="API and SDK quality"
    )
    tool_integration_score: int = Field(
        ge=1,
        le=10,
        description="Integration with ML tools"
    )
    documentation_quality: int = Field(
        ge=1,
        le=10,
        description="Documentation quality"
    )
    community_support_score: int = Field(
        ge=1,
        le=10,
        description="Community and support"
    )
    migration_tools_score: int = Field(
        ge=1,
        le=10,
        description="Migration tools and support"
    )

    @property
    def overall_score(self) -> float:
        return (self.api_sdk_quality_score + self.tool_integration_score +
                self.documentation_quality + self.community_support_score +
                self.migration_tools_score) / 5


class PerformanceAndReliability(BaseModel):
    """Performance and reliability capabilities"""
    sla_score: int = Field(
        ge=1,
        le=10,
        description="Service level agreements"
    )
    global_availability_score: int = Field(
        ge=1,
        le=10,
        description="Global availability and regions"
    )
    disaster_recovery_score: int = Field(
        ge=1,
        le=10,
        description="Disaster recovery capabilities"
    )
    performance_benchmarks: int = Field(
        ge=1,
        le=10,
        description="Performance benchmarks for ML workloads"
    )

    @property
    def overall_score(self) -> float:
        return (self.sla_score + self.global_availability_score +
                self.disaster_recovery_score + self.performance_benchmarks) / 4


class MLOpsPlatformEvaluation(BaseModel):
    """Complete MLOps platform evaluation model"""
    platform_name: str = Field(
        description="Name of the platform being evaluated"
    )
    platform_type: PlatformType = Field(
        description="Type of platform"
    )
    evaluation_date: datetime = Field(
        default_factory=datetime.now,
        description="Date of evaluation"
    )
    evaluator_name: Optional[str] = Field(
        None,
        description="Name of the evaluator"
    )

    # Core proficiency scores
    compute_and_scaling: ComputeAndScaling
    data_management: DataManagement
    model_development: ModelDevelopment
    mlops_pipeline: MLOpsPipeline
    model_deployment: ModelDeployment
    monitoring_and_observability: MonitoringAndObservability
    security_and_compliance: SecurityAndCompliance
    cost_management: CostManagement
    developer_experience: DeveloperExperience
    performance_and_reliability: PerformanceAndReliability

    # Optional fields
    notes: Optional[str] = Field(
        None, description="Additional notes about the evaluation")

    @property
    def overall_platform_score(self) -> float:
        """Calculate overall platform score as average of all proficiency scores"""
        scores = [
            self.compute_and_scaling.overall_score,
            self.data_management.overall_score,
            self.model_development.overall_score,
            self.mlops_pipeline.overall_score,
            self.model_deployment.overall_score,
            self.monitoring_and_observability.overall_score,
            self.security_and_compliance.overall_score,
            self.cost_management.overall_score,
            self.developer_experience.overall_score,
            self.performance_and_reliability.overall_score
        ]
        return sum(scores) / len(scores)

    @property
    def proficiency_summary(self) -> Dict[str, float]:
        """Return a summary of all proficiency scores"""
        return {
            "compute_and_scaling": self.compute_and_scaling.overall_score,
            "data_management": self.data_management.overall_score,
            "model_development": self.model_development.overall_score,
            "mlops_pipeline": self.mlops_pipeline.overall_score,
            "model_deployment": self.model_deployment.overall_score,
            "monitoring_and_observability": self.monitoring_and_observability.overall_score,
            "security_and_compliance": self.security_and_compliance.overall_score,
            "cost_management": self.cost_management.overall_score,
            "developer_experience": self.developer_experience.overall_score,
            "performance_and_reliability": self.performance_and_reliability.overall_score,
            "overall_score": self.overall_platform_score
        }

    def get_top_strengths(self, top_n: int = 3) -> List[tuple]:
        """Get the top N strengths of the platform"""
        summary = self.proficiency_summary
        # Remove overall_score from comparison
        summary.pop('overall_score', None)
        sorted_scores = sorted(
            summary.items(), key=lambda x: x[1], reverse=True)
        return sorted_scores[:top_n]

    def get_top_weaknesses(self, top_n: int = 3) -> List[tuple]:
        """Get the top N weaknesses of the platform"""
        summary = self.proficiency_summary
        # Remove overall_score from comparison
        summary.pop('overall_score', None)
        sorted_scores = sorted(summary.items(), key=lambda x: x[1])
        return sorted_scores[:top_n]

    class Config:
        use_enum_values = True
        validate_assignment = True
