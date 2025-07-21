import logging
from typing import List, Optional, Dict, Any

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, DisconnectionError

from sql_model.scores import (
    Base,
    PlatformEvaluation,
    ComputeAndScaling,
    DataManagement,
    ModelDevelopment,
    MLOpsPipeline,
    ModelDeployment,
    MonitoringAndObservability,
    SecurityAndCompliance,
    CostManagement,
    DeveloperExperience,
    PerformanceAndReliability,
)

from model.score import (
    MLOpsPlatformEvaluation,
    ComputeAndScaling as ComputeAndScalingModel,
    DataManagement as DataManagementModel,
    ModelDevelopment as ModelDevelopmentModel,
    MLOpsPipeline as MLOpsPipelineModel,
    ModelDeployment as ModelDeploymentModel,
    MonitoringAndObservability as MonitoringAndObservabilityModel,
    SecurityAndCompliance as SecurityAndComplianceModel,
    CostManagement as CostManagementModel,
    DeveloperExperience as DeveloperExperienceModel,
    PerformanceAndReliability as PerformanceAndReliabilityModel,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLOpsScoreController:
    def __init__(self, database_url: str):
        """Initialize the scores controller with database connection."""
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

    # Platform Evaluation CRUD operations
    def create_platform_evaluation(self, evaluation_data: MLOpsPlatformEvaluation) -> MLOpsPlatformEvaluation:
        """Create a complete platform evaluation with all scores."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)

                # Create all score components first
                compute_scaling = self._create_compute_scaling(
                    session, evaluation_data.compute_and_scaling)
                data_mgmt = self._create_data_management(
                    session, evaluation_data.data_management)
                model_dev = self._create_model_development(
                    session, evaluation_data.model_development)
                mlops_pipeline = self._create_mlops_pipeline(
                    session, evaluation_data.mlops_pipeline)
                model_deploy = self._create_model_deployment(
                    session, evaluation_data.model_deployment)
                monitoring_obs = self._create_monitoring_observability(
                    session, evaluation_data.monitoring_and_observability)
                security_comp = self._create_security_compliance(
                    session, evaluation_data.security_and_compliance)
                cost_mgmt = self._create_cost_management(
                    session, evaluation_data.cost_management)
                dev_exp = self._create_developer_experience(
                    session, evaluation_data.developer_experience)
                perf_rel = self._create_performance_reliability(
                    session, evaluation_data.performance_and_reliability)

                # Create the main evaluation record
                evaluation = PlatformEvaluation(
                    platform_id=int(
                        evaluation_data.platform_id) if evaluation_data.platform_id else None,
                    platform_type=evaluation_data.platform_type,
                    evaluation_date=evaluation_data.evaluation_date,
                    evaluator_id=evaluation_data.evaluator_id,
                    compute_and_scaling_id=compute_scaling.id,
                    data_management_id=data_mgmt.id,
                    model_development_id=model_dev.id,
                    mlops_pipeline_id=mlops_pipeline.id,
                    model_deployment_id=model_deploy.id,
                    monitoring_and_observability_id=monitoring_obs.id,
                    security_and_compliance_id=security_comp.id,
                    cost_management_id=cost_mgmt.id,
                    developer_experience_id=dev_exp.id,
                    performance_and_reliability_id=perf_rel.id
                )
                session.add(evaluation)
                session.commit()
                session.refresh(evaluation)

                logger.info(
                    f"Created platform evaluation with ID: {evaluation.id}")
                return self._convert_to_model(evaluation)

            except Exception as e:
                session.rollback()
                logger.error(f"Error creating platform evaluation: {e}")
                raise

    def get_platform_evaluation(self, evaluation_id: int) -> Optional[MLOpsPlatformEvaluation]:
        """Get a platform evaluation by ID."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluation = session.query(PlatformEvaluation).filter(
                PlatformEvaluation.id == evaluation_id).first()
            if evaluation:
                return self._convert_to_model(evaluation)
            return None

    def get_evaluations_by_platform(self, platform_id: int) -> List[MLOpsPlatformEvaluation]:
        """Get all evaluations for a specific platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluations = session.query(PlatformEvaluation).filter(
                PlatformEvaluation.platform_id == platform_id).all()
            return [self._convert_to_model(eval) for eval in evaluations]

    def get_latest_evaluation_by_platform(self, platform_id: int) -> Optional[MLOpsPlatformEvaluation]:
        """Get the most recent evaluation for a platform."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluation = session.query(PlatformEvaluation).filter(
                PlatformEvaluation.platform_id == platform_id
            ).order_by(PlatformEvaluation.evaluation_date.desc()).first()
            if evaluation:
                return self._convert_to_model(evaluation)
            return None

    def get_all_evaluations(self, limit: int = 100, offset: int = 0) -> List[MLOpsPlatformEvaluation]:
        """Get all platform evaluations with pagination."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluations = session.query(PlatformEvaluation).offset(
                offset).limit(limit).all()
            return [self._convert_to_model(eval) for eval in evaluations]

    def update_platform_evaluation(self, evaluation_id: int, evaluation_data: MLOpsPlatformEvaluation) -> Optional[MLOpsPlatformEvaluation]:
        """Update an existing platform evaluation."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                evaluation = session.query(PlatformEvaluation).filter(
                    PlatformEvaluation.id == evaluation_id).first()
                if not evaluation:
                    return None

                # Update each score component
                if evaluation.compute_and_scaling:
                    self._update_compute_scaling(
                        session, evaluation.compute_and_scaling, evaluation_data.compute_and_scaling)
                if evaluation.data_management:
                    self._update_data_management(
                        session, evaluation.data_management, evaluation_data.data_management)
                if evaluation.model_development:
                    self._update_model_development(
                        session, evaluation.model_development, evaluation_data.model_development)
                if evaluation.mlops_pipeline:
                    self._update_mlops_pipeline(
                        session, evaluation.mlops_pipeline, evaluation_data.mlops_pipeline)
                if evaluation.model_deployment:
                    self._update_model_deployment(
                        session, evaluation.model_deployment, evaluation_data.model_deployment)
                if evaluation.monitoring_and_observability:
                    self._update_monitoring_observability(
                        session, evaluation.monitoring_and_observability, evaluation_data.monitoring_and_observability)
                if evaluation.security_and_compliance:
                    self._update_security_compliance(
                        session, evaluation.security_and_compliance, evaluation_data.security_and_compliance)
                if evaluation.cost_management:
                    self._update_cost_management(
                        session, evaluation.cost_management, evaluation_data.cost_management)
                if evaluation.developer_experience:
                    self._update_developer_experience(
                        session, evaluation.developer_experience, evaluation_data.developer_experience)
                if evaluation.performance_and_reliability:
                    self._update_performance_reliability(
                        session, evaluation.performance_and_reliability, evaluation_data.performance_and_reliability)

                # Update main evaluation fields
                evaluation.platform_type = evaluation_data.platform_type
                evaluation.evaluator_id = evaluation_data.evaluator_id

                session.commit()
                session.refresh(evaluation)
                logger.info(
                    f"Updated platform evaluation with ID: {evaluation_id}")
                return self._convert_to_model(evaluation)

            except Exception as e:
                session.rollback()
                logger.error(f"Error updating platform evaluation: {e}")
                raise

    def delete_platform_evaluation(self, evaluation_id: int) -> bool:
        """Delete a platform evaluation."""
        with self.get_session() as session:
            try:
                session = self._ensure_healthy_session(session)
                evaluation = session.query(PlatformEvaluation).filter(
                    PlatformEvaluation.id == evaluation_id).first()
                if evaluation:
                    session.delete(evaluation)
                    session.commit()
                    logger.info(
                        f"Deleted platform evaluation with ID: {evaluation_id}")
                    return True
                return False
            except Exception as e:
                session.rollback()
                logger.error(f"Error deleting platform evaluation: {e}")
                raise

    def get_evaluations_by_evaluator(self, evaluator_id: str) -> List[MLOpsPlatformEvaluation]:
        """Get all evaluations by a specific evaluator."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluations = session.query(PlatformEvaluation).filter(
                PlatformEvaluation.evaluator_id == evaluator_id).all()
            return [self._convert_to_model(eval) for eval in evaluations]

    def get_platform_score_history(self, platform_id: int) -> List[Dict[str, Any]]:
        """Get score history for a platform over time."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            evaluations = session.query(PlatformEvaluation).filter(
                PlatformEvaluation.platform_id == platform_id
            ).order_by(PlatformEvaluation.evaluation_date.asc()).all()

            history = []
            for eval in evaluations:
                eval_model = self._convert_to_model(eval)
                history.append({
                    'evaluation_date': eval.evaluation_date,
                    'overall_score': eval_model.overall_platform_score,
                    'proficiency_scores': eval_model.proficiency_summary
                })
            return history

    def get_top_platforms_by_score(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top platforms by overall score."""
        with self.get_session() as session:
            session = self._ensure_healthy_session(session)
            # Get latest evaluation for each platform
            latest_evaluations = {}
            platform_evaluations = session.query(PlatformEvaluation).order_by(
                PlatformEvaluation.platform_id, PlatformEvaluation.evaluation_date.desc()
            ).all()

            for platform_evaluation in platform_evaluations:
                if platform_evaluation.platform_id not in latest_evaluations:
                    latest_evaluations[platform_evaluation.platform_id] = platform_evaluation

            # Convert to models and sort by score
            scored_platforms = []
            for platform_evaluation in latest_evaluations.values():
                eval_model = self._convert_to_model(platform_evaluation)
                scored_platforms.append({
                    'platform_id': platform_evaluation.platform_id,
                    'evaluation_id': platform_evaluation.id,
                    'overall_score': eval_model.overall_platform_score,
                    'evaluation_date': platform_evaluation.evaluation_date,
                    'proficiency_scores': eval_model.proficiency_summary
                })

            return sorted(scored_platforms, key=lambda x: x['overall_score'], reverse=True)[:limit]

    def _convert_to_model(self, evaluation: PlatformEvaluation) -> MLOpsPlatformEvaluation:
        """Convert SQLAlchemy model to Pydantic model."""
        return MLOpsPlatformEvaluation(
            platform_id=str(evaluation.platform_id),
            platform_type=evaluation.platform_type,
            evaluation_date=evaluation.evaluation_date,
            evaluator_id=evaluation.evaluator_id,
            compute_and_scaling=ComputeAndScalingModel(
                compute_variety_score=evaluation.compute_and_scaling.compute_variety,
                auto_scaling_score=evaluation.compute_and_scaling.auto_scaling_score,
                spot_instance_support=evaluation.compute_and_scaling.spot_instance_support,
                distributed_training_support=evaluation.compute_and_scaling.distributed_training_support
            ),
            data_management=DataManagementModel(
                storage_options_score=evaluation.data_management.storage_options_score,
                data_versioning_score=evaluation.data_management.data_versioning_score,
                data_pipeline_orchestration=evaluation.data_management.data_pipeline_orchestration,
                data_integration_score=evaluation.data_management.data_integration_score
            ),
            model_development=ModelDevelopmentModel(
                framework_support_score=evaluation.model_development.framework_support_score,
                experiment_tracking_score=evaluation.model_development.experiment_tracking_score,
                hyperparameter_tuning_score=evaluation.model_development.hyperparameter_tuning_score,
                notebook_environment_score=evaluation.model_development.notebook_environment_score
            ),
            mlops_pipeline=MLOpsPipelineModel(
                workflow_orchestration_score=evaluation.mlops_pipeline.workflow_orchestration_score,
                cicd_integration_score=evaluation.mlops_pipeline.cicd_integration_score,
                model_validation_score=evaluation.mlops_pipeline.model_validation_score,
                environment_management_score=evaluation.mlops_pipeline.environment_management_score
            ),
            model_deployment=ModelDeploymentModel(
                deployment_options_score=evaluation.model_deployment.deployment_options_score,
                real_time_inference_score=evaluation.model_deployment.real_time_inference_score,
                batch_inference_score=evaluation.model_deployment.batch_inference_score,
                ab_testing_score=evaluation.model_deployment.ab_testing_score,
                canary_deployment_score=evaluation.model_deployment.canary_deployment_score
            ),
            monitoring_and_observability=MonitoringAndObservabilityModel(
                model_performance_monitoring=evaluation.monitoring_and_observability.model_performance_monitoring,
                data_drift_detection=evaluation.monitoring_and_observability.data_drift_detection,
                infrastructure_monitoring=evaluation.monitoring_and_observability.infrastructure_monitoring,
                logging_and_alerting=evaluation.monitoring_and_observability.logging_and_alerting,
                model_explainability=evaluation.monitoring_and_observability.model_explainability
            ),
            security_and_compliance=SecurityAndComplianceModel(
                identity_access_management=evaluation.security_and_compliance.identity_access_management,
                data_encryption=evaluation.security_and_compliance.data_encryption,
                compliance_certifications=evaluation.security_and_compliance.compliance_certifications,
                network_security=evaluation.security_and_compliance.network_security,
                audit_logging=evaluation.security_and_compliance.audit_logging
            ),
            cost_management=CostManagementModel(
                cost_transparency=evaluation.cost_management.cost_transparency,
                resource_optimization=evaluation.cost_management.resource_optimization,
                pricing_flexibility=evaluation.cost_management.pricing_flexibility,
                cost_prediction_score=evaluation.cost_management.cost_prediction_score
            ),
            developer_experience=DeveloperExperienceModel(
                api_sdk_quality=evaluation.developer_experience.api_sdk_quality,
                tool_integration=evaluation.developer_experience.tool_integration,
                documentation_quality=evaluation.developer_experience.documentation_quality,
                community_support=evaluation.developer_experience.community_support,
                migration_tools=evaluation.developer_experience.migration_tools
            ),
            performance_and_reliability=PerformanceAndReliabilityModel(
                sla_score=evaluation.performance_and_reliability.sla_score,
                global_availability=evaluation.performance_and_reliability.global_availability,
                disaster_recovery=evaluation.performance_and_reliability.disaster_recovery,
                performance_benchmarks=evaluation.performance_and_reliability.performance_benchmarks
            )
        )

    def _update_compute_scaling(self, session: Session, db_obj: ComputeAndScaling, model_obj: ComputeAndScalingModel):
        """Update compute and scaling scores."""
        db_obj.compute_variety = model_obj.compute_variety_score
        db_obj.auto_scaling_score = model_obj.auto_scaling_score
        db_obj.spot_instance_support = model_obj.spot_instance_support
        db_obj.distributed_training_support = model_obj.distributed_training_support

    def _update_data_management(self, session: Session, db_obj: DataManagement, model_obj: DataManagementModel):
        """Update data management scores."""
        db_obj.storage_options_score = model_obj.storage_options_score
        db_obj.data_versioning_score = model_obj.data_versioning_score
        db_obj.data_pipeline_orchestration = model_obj.data_pipeline_orchestration
        db_obj.data_integration_score = model_obj.data_integration_score

    def _update_model_development(self, session: Session, db_obj: ModelDevelopment, model_obj: ModelDevelopmentModel):
        """Update model development scores."""
        db_obj.framework_support_score = model_obj.framework_support_score
        db_obj.experiment_tracking_score = model_obj.experiment_tracking_score
        db_obj.hyperparameter_tuning_score = model_obj.hyperparameter_tuning_score
        db_obj.notebook_environment_score = model_obj.notebook_environment_score

    def _update_mlops_pipeline(self, session: Session, db_obj: MLOpsPipeline, model_obj: MLOpsPipelineModel):
        """Update MLOps pipeline scores."""
        db_obj.workflow_orchestration_score = model_obj.workflow_orchestration_score
        db_obj.cicd_integration_score = model_obj.cicd_integration_score
        db_obj.model_validation_score = model_obj.model_validation_score
        db_obj.environment_management_score = model_obj.environment_management_score

    def _update_model_deployment(self, session: Session, db_obj: ModelDeployment, model_obj: ModelDeploymentModel):
        """Update model deployment scores."""
        db_obj.deployment_options_score = model_obj.deployment_options_score
        db_obj.real_time_inference_score = model_obj.real_time_inference_score
        db_obj.batch_inference_score = model_obj.batch_inference_score
        db_obj.ab_testing_score = model_obj.ab_testing_score
        db_obj.canary_deployment_score = model_obj.canary_deployment_score

    def _update_monitoring_observability(self, session: Session, db_obj: MonitoringAndObservability, model_obj: MonitoringAndObservabilityModel):
        """Update monitoring and observability scores."""
        db_obj.model_performance_monitoring = model_obj.model_performance_monitoring
        db_obj.data_drift_detection = model_obj.data_drift_detection
        db_obj.infrastructure_monitoring = model_obj.infrastructure_monitoring
        db_obj.logging_and_alerting = model_obj.logging_and_alerting
        db_obj.model_explainability = model_obj.model_explainability

    def _update_security_compliance(self, session: Session, db_obj: SecurityAndCompliance, model_obj: SecurityAndComplianceModel):
        """Update security and compliance scores."""
        db_obj.identity_access_management = model_obj.identity_access_management
        db_obj.data_encryption = model_obj.data_encryption
        db_obj.compliance_certifications = model_obj.compliance_certifications
        db_obj.network_security = model_obj.network_security
        db_obj.audit_logging = model_obj.audit_logging

    def _update_cost_management(self, session: Session, db_obj: CostManagement, model_obj: CostManagementModel):
        """Update cost management scores."""
        db_obj.cost_transparency = model_obj.cost_transparency
        db_obj.resource_optimization = model_obj.resource_optimization
        db_obj.pricing_flexibility = model_obj.pricing_flexibility
        db_obj.cost_prediction_score = model_obj.cost_prediction_score

    def _update_developer_experience(self, session: Session, db_obj: DeveloperExperience, model_obj: DeveloperExperienceModel):
        """Update developer experience scores."""
        db_obj.api_sdk_quality = model_obj.api_sdk_quality
        db_obj.tool_integration = model_obj.tool_integration
        db_obj.documentation_quality = model_obj.documentation_quality
        db_obj.community_support = model_obj.community_support
        db_obj.migration_tools = model_obj.migration_tools

    def _update_performance_reliability(self, session: Session, db_obj: PerformanceAndReliability, model_obj: PerformanceAndReliabilityModel):
        """Update performance and reliability scores."""
        db_obj.sla_score = model_obj.sla_score
        db_obj.global_availability = model_obj.global_availability
        db_obj.disaster_recovery = model_obj.disaster_recovery
        db_obj.performance_benchmarks = model_obj.performance_benchmarks

    def close(self) -> None:
        """Close the database connection."""
        self.engine.dispose()

    def _create_compute_scaling(self, session: Session, data: ComputeAndScalingModel) -> ComputeAndScaling:
        """Create compute and scaling record."""
        compute_scaling = ComputeAndScaling(
            compute_variety=data.compute_variety_score,
            auto_scaling_score=data.auto_scaling_score,
            spot_instance_support=data.spot_instance_support,
            distributed_training_support=data.distributed_training_support
        )
        session.add(compute_scaling)
        session.flush()
        return compute_scaling

    def _create_data_management(self, session: Session, data: DataManagementModel) -> DataManagement:
        """Create data management record."""
        data_mgmt = DataManagement(
            storage_options_score=data.storage_options_score,
            data_versioning_score=data.data_versioning_score,
            data_pipeline_orchestration=data.data_pipeline_orchestration,
            data_integration_score=data.data_integration_score
        )
        session.add(data_mgmt)
        session.flush()
        return data_mgmt

    def _create_model_development(self, session: Session, data: ModelDevelopmentModel) -> ModelDevelopment:
        """Create model development record."""
        model_dev = ModelDevelopment(
            framework_support_score=data.framework_support_score,
            experiment_tracking_score=data.experiment_tracking_score,
            hyperparameter_tuning_score=data.hyperparameter_tuning_score,
            notebook_environment_score=data.notebook_environment_score
        )
        session.add(model_dev)
        session.flush()
        return model_dev

    def _create_mlops_pipeline(self, session: Session, data: MLOpsPipelineModel) -> MLOpsPipeline:
        """Create MLOps pipeline record."""
        mlops_pipeline = MLOpsPipeline(
            workflow_orchestration_score=data.workflow_orchestration_score,
            cicd_integration_score=data.cicd_integration_score,
            model_validation_score=data.model_validation_score,
            environment_management_score=data.environment_management_score
        )
        session.add(mlops_pipeline)
        session.flush()
        return mlops_pipeline

    def _create_model_deployment(self, session: Session, data: ModelDeploymentModel) -> ModelDeployment:
        """Create model deployment record."""
        model_deploy = ModelDeployment(
            deployment_options_score=data.deployment_options_score,
            real_time_inference_score=data.real_time_inference_score,
            batch_inference_score=data.batch_inference_score,
            ab_testing_score=data.ab_testing_score,
            canary_deployment_score=data.canary_deployment_score
        )
        session.add(model_deploy)
        session.flush()
        return model_deploy

    def _create_monitoring_observability(self, session: Session, data: MonitoringAndObservabilityModel) -> MonitoringAndObservability:
        """Create monitoring and observability record."""
        monitoring_obs = MonitoringAndObservability(
            model_performance_monitoring=data.model_performance_monitoring,
            data_drift_detection=data.data_drift_detection,
            infrastructure_monitoring=data.infrastructure_monitoring,
            logging_and_alerting=data.logging_and_alerting,
            model_explainability=data.model_explainability
        )
        session.add(monitoring_obs)
        session.flush()
        return monitoring_obs

    def _create_security_compliance(self, session: Session, data: SecurityAndComplianceModel) -> SecurityAndCompliance:
        """Create security and compliance record."""
        security_comp = SecurityAndCompliance(
            identity_access_management=data.identity_access_management,
            data_encryption=data.data_encryption,
            compliance_certifications=data.compliance_certifications,
            network_security=data.network_security,
            audit_logging=data.audit_logging
        )
        session.add(security_comp)
        session.flush()
        return security_comp

    def _create_cost_management(self, session: Session, data: CostManagementModel) -> CostManagement:
        """Create cost management record."""
        cost_mgmt = CostManagement(
            cost_transparency=data.cost_transparency,
            resource_optimization=data.resource_optimization,
            pricing_flexibility=data.pricing_flexibility,
            cost_prediction_score=data.cost_prediction_score
        )
        session.add(cost_mgmt)
        session.flush()
        return cost_mgmt

    def _create_developer_experience(self, session: Session, data: DeveloperExperienceModel) -> DeveloperExperience:
        """Create developer experience record."""
        dev_exp = DeveloperExperience(
            api_sdk_quality=data.api_sdk_quality,
            tool_integration=data.tool_integration,
            documentation_quality=data.documentation_quality,
            community_support=data.community_support,
            migration_tools=data.migration_tools
        )
        session.add(dev_exp)
        session.flush()
        return dev_exp

    def _create_performance_reliability(self, session: Session, data: PerformanceAndReliabilityModel) -> PerformanceAndReliability:
        """Create performance and reliability record."""
        perf_rel = PerformanceAndReliability(
            sla_score=data.sla_score,
            global_availability=data.global_availability,
            disaster_recovery=data.disaster_recovery,
            performance_benchmarks=data.performance_benchmarks
        )
        session.add(perf_rel)
        session.flush()
        return perf_rel
