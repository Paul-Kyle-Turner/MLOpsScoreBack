from sqlalchemy import Column, BigInteger, Integer, String, DateTime, ForeignKey, Enum, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from sql_model.platforms import platform_types_enum

Base = declarative_base()


class ComputeAndScaling(Base):
    __tablename__ = 'compute_and_scaling'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    compute_variety = Column(Integer)
    auto_scaling_score = Column(Integer)
    spot_instance_support = Column(Integer)
    distributed_training_support = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="compute_and_scaling")


class DataManagement(Base):
    __tablename__ = 'data_management'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    storage_options_score = Column(Integer)
    data_versioning_score = Column(Integer)
    data_pipeline_orchestration = Column(Integer)
    data_integration_score = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="data_management")


class ModelDevelopment(Base):
    __tablename__ = 'model_development'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    framework_support_score = Column(Integer)
    experiment_tracking_score = Column(Integer)
    hyperparameter_tuning_score = Column(Integer)
    notebook_environment_score = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="model_development")


class MLOpsPipeline(Base):
    __tablename__ = 'mlops_pipeline'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    workflow_orchestration_score = Column(Integer)
    cicd_integration_score = Column(Integer)
    model_validation_score = Column(Integer)
    environment_management_score = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="mlops_pipeline")


class ModelDeployment(Base):
    __tablename__ = 'model_deployment'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    deployment_options_score = Column(Integer)
    real_time_inference_score = Column(Integer)
    batch_inference_score = Column(Integer)
    ab_testing_score = Column(Integer)
    canary_deployment_score = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="model_deployment")


class MonitoringAndObservability(Base):
    __tablename__ = 'monitoring_and_observability'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    model_performance_monitoring = Column(Integer)
    data_drift_detection = Column(Integer)
    infrastructure_monitoring = Column(Integer)
    logging_and_alerting = Column(Integer)
    model_explainability = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="monitoring_and_observability")


class SecurityAndCompliance(Base):
    __tablename__ = 'security_and_compliance'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    identity_access_management = Column(Integer)
    data_encryption = Column(Integer)
    compliance_certifications = Column(Integer)
    network_security = Column(Integer)
    audit_logging = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="security_and_compliance")


class CostManagement(Base):
    __tablename__ = 'cost_management'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cost_transparency = Column(Integer)
    resource_optimization = Column(Integer)
    pricing_flexibility = Column(Integer)
    cost_prediction_score = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="cost_management")


class DeveloperExperience(Base):
    __tablename__ = 'developer_experience'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    api_sdk_quality = Column(Integer)
    tool_integration = Column(Integer)
    documentation_quality = Column(Integer)
    community_support = Column(Integer)
    migration_tools = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="developer_experience")


class PerformanceAndReliability(Base):
    __tablename__ = 'performance_and_reliability'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sla_score = Column(Integer)
    global_availability = Column(Integer)
    disaster_recovery = Column(Integer)
    performance_benchmarks = Column(Integer)

    # Relationship
    platform_evaluations = relationship(
        "PlatformEvaluation", back_populates="performance_and_reliability")


class PlatformEvaluation(Base):
    __tablename__ = 'platform_evaluation'
    __table_args__ = {'schema': 'scores'}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    # References platforms.platform_information(id)
    platform_id = Column(BigInteger, nullable=False)
    platform_type = Column(platform_types_enum, nullable=False)
    evaluation_date = Column(DateTime(timezone=True),
                             default=func.current_timestamp())
    evaluator_id = Column(String(64), nullable=True)

    # Foreign Keys
    compute_and_scaling_id = Column(BigInteger, ForeignKey(
        'scores.compute_and_scaling.id', ondelete='CASCADE'))
    data_management_id = Column(BigInteger, ForeignKey(
        'scores.data_management.id', ondelete='CASCADE'))
    model_development_id = Column(BigInteger, ForeignKey(
        'scores.model_development.id', ondelete='CASCADE'))
    mlops_pipeline_id = Column(BigInteger, ForeignKey(
        'scores.mlops_pipeline.id', ondelete='CASCADE'))
    model_deployment_id = Column(BigInteger, ForeignKey(
        'scores.model_deployment.id', ondelete='CASCADE'))
    monitoring_and_observability_id = Column(BigInteger, ForeignKey(
        'scores.monitoring_and_observability.id', ondelete='CASCADE'))
    security_and_compliance_id = Column(BigInteger, ForeignKey(
        'scores.security_and_compliance.id', ondelete='CASCADE'))
    cost_management_id = Column(BigInteger, ForeignKey(
        'scores.cost_management.id', ondelete='CASCADE'))
    developer_experience_id = Column(BigInteger, ForeignKey(
        'scores.developer_experience.id', ondelete='CASCADE'))
    performance_and_reliability_id = Column(BigInteger, ForeignKey(
        'scores.performance_and_reliability.id', ondelete='CASCADE'))

    # Relationships
    compute_and_scaling = relationship(
        "ComputeAndScaling", back_populates="platform_evaluations")
    data_management = relationship(
        "DataManagement", back_populates="platform_evaluations")
    model_development = relationship(
        "ModelDevelopment", back_populates="platform_evaluations")
    mlops_pipeline = relationship(
        "MLOpsPipeline", back_populates="platform_evaluations")
    model_deployment = relationship(
        "ModelDeployment", back_populates="platform_evaluations")
    monitoring_and_observability = relationship(
        "MonitoringAndObservability", back_populates="platform_evaluations")
    security_and_compliance = relationship(
        "SecurityAndCompliance", back_populates="platform_evaluations")
    cost_management = relationship(
        "CostManagement", back_populates="platform_evaluations")
    developer_experience = relationship(
        "DeveloperExperience", back_populates="platform_evaluations")
    performance_and_reliability = relationship(
        "PerformanceAndReliability", back_populates="platform_evaluations")


class PlatformScoresComprehensive(Base):
    __tablename__ = 'platform_scores_comprehensive'
    __table_args__ = {'schema': 'scores'}

    # This is a view, so we need to define it as non-insertable
    __mapper_args__ = {
        'primary_key': ['evaluation_id']
    }

    evaluation_id = Column(BigInteger, primary_key=True)
    platform_id = Column(BigInteger)
    platform_type = Column(platform_types_enum)
    evaluation_date = Column(DateTime(timezone=True))
    evaluator_id = Column(String(64))

    # Compute and Scaling scores
    compute_variety = Column(Integer)
    auto_scaling_score = Column(Integer)
    spot_instance_support = Column(Integer)
    distributed_training_support = Column(Integer)

    # Data Management scores
    storage_options_score = Column(Integer)
    data_versioning_score = Column(Integer)
    data_pipeline_orchestration = Column(Integer)
    data_integration_score = Column(Integer)

    # Model Development scores
    framework_support_score = Column(Integer)
    experiment_tracking_score = Column(Integer)
    hyperparameter_tuning_score = Column(Integer)
    notebook_environment_score = Column(Integer)

    # MLOps Pipeline scores
    workflow_orchestration_score = Column(Integer)
    cicd_integration_score = Column(Integer)
    model_validation_score = Column(Integer)
    environment_management_score = Column(Integer)

    # Model Deployment scores
    deployment_options_score = Column(Integer)
    real_time_inference_score = Column(Integer)
    batch_inference_score = Column(Integer)
    ab_testing_score = Column(Integer)
    canary_deployment_score = Column(Integer)

    # Monitoring and Observability scores
    model_performance_monitoring = Column(Integer)
    data_drift_detection = Column(Integer)
    infrastructure_monitoring = Column(Integer)
    logging_and_alerting = Column(Integer)
    model_explainability = Column(Integer)

    # Security and Compliance scores
    identity_access_management = Column(Integer)
    data_encryption = Column(Integer)
    compliance_certifications = Column(Integer)
    network_security = Column(Integer)
    audit_logging = Column(Integer)

    # Cost Management scores
    cost_transparency = Column(Integer)
    resource_optimization = Column(Integer)
    pricing_flexibility = Column(Integer)
    cost_prediction_score = Column(Integer)

    # Developer Experience scores
    api_sdk_quality = Column(Integer)
    tool_integration = Column(Integer)
    documentation_quality = Column(Integer)
    community_support = Column(Integer)
    migration_tools = Column(Integer)

    # Performance and Reliability scores
    sla_score = Column(Integer)
    global_availability = Column(Integer)
    disaster_recovery = Column(Integer)
    performance_benchmarks = Column(Integer)
