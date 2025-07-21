from pydantic import AliasChoices, BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime

from model.platform import PlatformType


class ScoreRange(BaseModel):
    """Score range validation model"""
    min_score: int = Field(
        default=1,
        ge=1,
        le=10,
        validation_alias=AliasChoices("min_score", "minScore"),
        serialization_alias="minScore"
    )
    max_score: int = Field(
        default=10,
        ge=1,
        le=10,
        validation_alias=AliasChoices("max_score", "maxScore"),
        serialization_alias="maxScore"
    )


class ComputeAndScaling(BaseModel):
    """Compute and scaling capabilities"""
    compute_variety_score: int = Field(
        ge=1,
        le=10,
        description="Variety of compute options (CPU, GPU, TPU, etc.)",
        validation_alias=AliasChoices(
            "compute_variety_score", "computeVarietyScore"),
        serialization_alias="computeVarietyScore"
    )
    auto_scaling_score: int = Field(
        ge=1,
        le=10,
        description="Auto-scaling capabilities",
        validation_alias=AliasChoices(
            "auto_scaling_score", "autoScalingScore"),
        serialization_alias="autoScalingScore"
    )
    spot_instance_support: int = Field(
        ge=1,
        le=10,
        description="Spot/preemptible instance availability",
        validation_alias=AliasChoices(
            "spot_instance_support", "spotInstanceSupport"),
        serialization_alias="spotInstanceSupport"
    )
    distributed_training_support: int = Field(
        ge=1,
        le=10,
        description="Multi-node distributed training",
        validation_alias=AliasChoices(
            "distributed_training_support", "distributedTrainingSupport"),
        serialization_alias="distributedTrainingSupport"
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
        description="Variety of storage solutions",
        validation_alias=AliasChoices(
            "storage_options_score", "storageOptionsScore"),
        serialization_alias="storageOptionsScore"
    )
    data_versioning_score: int = Field(
        ge=1,
        le=10,
        description="Data versioning capabilities",
        validation_alias=AliasChoices(
            "data_versioning_score", "dataVersioningScore"),
        serialization_alias="dataVersioningScore"
    )
    data_pipeline_orchestration: int = Field(
        ge=1,
        le=10,
        description="Data pipeline tools",
        validation_alias=AliasChoices(
            "data_pipeline_orchestration", "dataPipelineOrchestration"),
        serialization_alias="dataPipelineOrchestration"
    )
    data_integration_score: int = Field(
        ge=1,
        le=10,
        description="Integration with data sources",
        validation_alias=AliasChoices(
            "data_integration_score", "dataIntegrationScore"),
        serialization_alias="dataIntegrationScore"
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
        description="ML framework support",
        validation_alias=AliasChoices(
            "framework_support_score", "frameworkSupportScore"),
        serialization_alias="frameworkSupportScore"
    )
    experiment_tracking_score: int = Field(
        ge=1,
        le=10,
        description="Experiment tracking tools",
        validation_alias=AliasChoices(
            "experiment_tracking_score", "experimentTrackingScore"),
        serialization_alias="experimentTrackingScore"
    )
    hyperparameter_tuning_score: int = Field(
        ge=1,
        le=10,
        description="Hyperparameter optimization",
        validation_alias=AliasChoices(
            "hyperparameter_tuning_score", "hyperparameterTuningScore"),
        serialization_alias="hyperparameterTuningScore"
    )
    notebook_environment_score: int = Field(
        ge=1,
        le=10,
        description="Managed notebook environments",
        validation_alias=AliasChoices(
            "notebook_environment_score", "notebookEnvironmentScore"),
        serialization_alias="notebookEnvironmentScore"
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
        description="Workflow orchestration tools",
        validation_alias=AliasChoices(
            "workflow_orchestration_score", "workflowOrchestrationScore"),
        serialization_alias="workflowOrchestrationScore"
    )
    cicd_integration_score: int = Field(
        ge=1,
        le=10,
        description="CI/CD integration",
        validation_alias=AliasChoices(
            "cicd_integration_score", "cicdIntegrationScore"),
        serialization_alias="cicdIntegrationScore"
    )
    model_validation_score: int = Field(
        ge=1,
        le=10,
        description="Automated model validation",
        validation_alias=AliasChoices(
            "model_validation_score", "modelValidationScore"),
        serialization_alias="modelValidationScore"
    )
    environment_management_score: int = Field(
        ge=1,
        le=10,
        description="Environment management",
        validation_alias=AliasChoices(
            "environment_management_score", "environmentManagementScore"),
        serialization_alias="environmentManagementScore"
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
        description="Variety of deployment options",
        validation_alias=AliasChoices(
            "deployment_options_score", "deploymentOptionsScore"),
        serialization_alias="deploymentOptionsScore"
    )
    real_time_inference_score: int = Field(
        ge=1,
        le=10,
        description="Real-time inference capabilities",
        validation_alias=AliasChoices(
            "real_time_inference_score", "realTimeInferenceScore"),
        serialization_alias="realTimeInferenceScore"
    )
    batch_inference_score: int = Field(
        ge=1,
        le=10,
        description="Batch inference capabilities",
        validation_alias=AliasChoices(
            "batch_inference_score", "batchInferenceScore"),
        serialization_alias="batchInferenceScore"
    )
    ab_testing_score: int = Field(
        ge=1,
        le=10,
        description="A/B testing support",
        validation_alias=AliasChoices("ab_testing_score", "abTestingScore"),
        serialization_alias="abTestingScore"
    )
    canary_deployment_score: int = Field(
        ge=1,
        le=10,
        description="Canary deployment capabilities",
        validation_alias=AliasChoices(
            "canary_deployment_score", "canaryDeploymentScore"),
        serialization_alias="canaryDeploymentScore"
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
        description="Model performance monitoring",
        validation_alias=AliasChoices(
            "model_performance_monitoring", "modelPerformanceMonitoring"),
        serialization_alias="modelPerformanceMonitoring"
    )
    data_drift_detection: int = Field(
        ge=1,
        le=10,
        description="Data drift detection",
        validation_alias=AliasChoices(
            "data_drift_detection", "dataDriftDetection"),
        serialization_alias="dataDriftDetection"
    )
    infrastructure_monitoring: int = Field(
        ge=1,
        le=10,
        description="Infrastructure monitoring",
        validation_alias=AliasChoices(
            "infrastructure_monitoring", "infrastructureMonitoring"),
        serialization_alias="infrastructureMonitoring"
    )
    logging_and_alerting: int = Field(
        ge=1,
        le=10,
        description="Logging and alerting systems",
        validation_alias=AliasChoices(
            "logging_and_alerting", "loggingAndAlerting"),
        serialization_alias="loggingAndAlerting"
    )
    model_explainability: int = Field(
        ge=1,
        le=10,
        description="Model explainability tools",
        validation_alias=AliasChoices(
            "model_explainability", "modelExplainability"),
        serialization_alias="modelExplainability"
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
        description="IAM capabilities",
        validation_alias=AliasChoices(
            "identity_access_management", "identityAccessManagement"),
        serialization_alias="identityAccessManagement"
    )
    data_encryption: int = Field(
        ge=1,
        le=10,
        description="Data encryption at rest and in transit",
        validation_alias=AliasChoices("data_encryption", "dataEncryption"),
        serialization_alias="dataEncryption"
    )
    compliance_certifications: int = Field(
        ge=1,
        le=10,
        description="Compliance certifications",
        validation_alias=AliasChoices(
            "compliance_certifications", "complianceCertifications"),
        serialization_alias="complianceCertifications"
    )
    network_security: int = Field(
        ge=1,
        le=10,
        description="Network security features",
        validation_alias=AliasChoices("network_security", "networkSecurity"),
        serialization_alias="networkSecurity"
    )
    audit_logging: int = Field(
        ge=1,
        le=10,
        description="Audit logging capabilities",
        validation_alias=AliasChoices("audit_logging", "auditLogging"),
        serialization_alias="auditLogging"
    )

    @property
    def overall_score(self) -> float:
        return (self.identity_access_management + self.data_encryption +
                self.compliance_certifications + self.network_security +
                self.audit_logging) / 5


class CostManagement(BaseModel):
    """Cost management and optimization capabilities"""
    cost_transparency: int = Field(
        ge=1,
        le=10,
        description="Cost transparency and reporting",
        validation_alias=AliasChoices("cost_transparency", "costTransparency"),
        serialization_alias="costTransparency"
    )
    resource_optimization: int = Field(
        ge=1,
        le=10,
        description="Resource utilization optimization",
        validation_alias=AliasChoices(
            "resource_optimization", "resourceOptimization"),
        serialization_alias="resourceOptimization"
    )
    pricing_flexibility: int = Field(
        ge=1,
        le=10,
        description="Flexible pricing models",
        validation_alias=AliasChoices(
            "pricing_flexibility", "pricingFlexibility"),
        serialization_alias="pricingFlexibility"
    )
    cost_prediction_score: int = Field(
        ge=1,
        le=10,
        description="Cost prediction and budgeting",
        validation_alias=AliasChoices(
            "cost_prediction_score", "costPredictionScore"),
        serialization_alias="costPredictionScore"
    )

    @property
    def overall_score(self) -> float:
        return (self.cost_transparency + self.resource_optimization +
                self.pricing_flexibility + self.cost_prediction_score) / 4


class DeveloperExperience(BaseModel):
    """Developer experience and integration capabilities"""
    api_sdk_quality: int = Field(
        ge=1,
        le=10,
        description="API and SDK quality",
        validation_alias=AliasChoices("api_sdk_quality", "apiSdkQuality"),
        serialization_alias="apiSdkQuality"
    )
    tool_integration: int = Field(
        ge=1,
        le=10,
        description="Integration with ML tools",
        validation_alias=AliasChoices("tool_integration", "toolIntegration"),
        serialization_alias="toolIntegration"
    )
    documentation_quality: int = Field(
        ge=1,
        le=10,
        description="Documentation quality",
        validation_alias=AliasChoices(
            "documentation_quality", "documentationQuality"),
        serialization_alias="documentationQuality"
    )
    community_support: int = Field(
        ge=1,
        le=10,
        description="Community and support",
        validation_alias=AliasChoices("community_support", "communitySupport"),
        serialization_alias="communitySupport"
    )
    migration_tools: int = Field(
        ge=1,
        le=10,
        description="Migration tools and support",
        validation_alias=AliasChoices("migration_tools", "migrationTools"),
        serialization_alias="migrationTools"
    )

    @property
    def overall_score(self) -> float:
        return (self.api_sdk_quality + self.tool_integration +
                self.documentation_quality + self.community_support +
                self.migration_tools) / 5


class PerformanceAndReliability(BaseModel):
    """Performance and reliability capabilities"""
    sla_score: int = Field(
        ge=1,
        le=10,
        description="Service level agreements",
        validation_alias=AliasChoices("sla_score", "slaScore"),
        serialization_alias="slaScore"
    )
    global_availability: int = Field(
        ge=1,
        le=10,
        description="Global availability and regions",
        validation_alias=AliasChoices(
            "global_availability", "globalAvailability"),
        serialization_alias="globalAvailability"
    )
    disaster_recovery: int = Field(
        ge=1,
        le=10,
        description="Disaster recovery capabilities",
        validation_alias=AliasChoices("disaster_recovery", "disasterRecovery"),
        serialization_alias="disasterRecovery"
    )
    performance_benchmarks: int = Field(
        ge=1,
        le=10,
        description="Performance benchmarks for ML workloads",
        validation_alias=AliasChoices(
            "performance_benchmarks", "performanceBenchmarks"),
        serialization_alias="performanceBenchmarks"
    )

    @property
    def overall_score(self) -> float:
        return (self.sla_score + self.global_availability +
                self.disaster_recovery + self.performance_benchmarks) / 4


class MLOpsPlatformEvaluation(BaseModel):
    """Complete MLOps platform evaluation model"""
    platform_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("platform_id", "id", "platformId"),
        serialization_alias="platformId",
        description="Unique identifier for the platform"
    )
    platform_type: PlatformType = Field(
        description="Type of platform",
        validation_alias=AliasChoices("platform_type", "platformType"),
        serialization_alias="platformType"
    )
    evaluation_date: datetime = Field(
        default_factory=datetime.now,
        description="Date of evaluation",
        validation_alias=AliasChoices("evaluation_date", "evaluationDate"),
        serialization_alias="evaluationDate"
    )
    evaluator_id: Optional[str] = Field(
        None,
        description="ID of the evaluator, probably slack id",
        validation_alias=AliasChoices("evaluator_id", "evaluatorId"),
        serialization_alias="evaluatorId"
    )

    # Core proficiency scores
    compute_and_scaling: ComputeAndScaling = Field(
        validation_alias=AliasChoices(
            "compute_and_scaling", "computeAndScaling"),
        serialization_alias="computeAndScaling"
    )
    data_management: DataManagement = Field(
        validation_alias=AliasChoices("data_management", "dataManagement"),
        serialization_alias="dataManagement"
    )
    model_development: ModelDevelopment = Field(
        validation_alias=AliasChoices("model_development", "modelDevelopment"),
        serialization_alias="modelDevelopment"
    )
    mlops_pipeline: MLOpsPipeline = Field(
        validation_alias=AliasChoices("mlops_pipeline", "mlopsPipeline", "mlOpsPipeline"),
        serialization_alias="mlOpsPipeline"
    )
    model_deployment: ModelDeployment = Field(
        validation_alias=AliasChoices("model_deployment", "modelDeployment"),
        serialization_alias="modelDeployment"
    )
    monitoring_and_observability: MonitoringAndObservability = Field(
        validation_alias=AliasChoices(
            "monitoring_and_observability", "monitoringAndObservability"),
        serialization_alias="monitoringAndObservability"
    )
    security_and_compliance: SecurityAndCompliance = Field(
        validation_alias=AliasChoices(
            "security_and_compliance", "securityAndCompliance"),
        serialization_alias="securityAndCompliance"
    )
    cost_management: CostManagement = Field(
        validation_alias=AliasChoices("cost_management", "costManagement"),
        serialization_alias="costManagement"
    )
    developer_experience: DeveloperExperience = Field(
        validation_alias=AliasChoices(
            "developer_experience", "developerExperience"),
        serialization_alias="developerExperience"
    )
    performance_and_reliability: PerformanceAndReliability = Field(
        validation_alias=AliasChoices(
            "performance_and_reliability", "performanceAndReliability"),
        serialization_alias="performanceAndReliability"
    )

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
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
