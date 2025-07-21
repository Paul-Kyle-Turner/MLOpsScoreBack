from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime

from controller.scores import MLOpsScoreController
from model.score import MLOpsPlatformEvaluation
from settings import SETTINGS

router = APIRouter(prefix="/scores", tags=["scoring", "scores", "score"])

# Initialize the controller
controller = MLOpsScoreController(SETTINGS.pg_connection_string)


@router.get("/", summary="Get all platform evaluations")
async def get_all_evaluations(
    limit: int = Query(100, ge=1, le=1000,
                       description="Number of evaluations to return"),
    offset: int = Query(0, ge=0, description="Number of evaluations to skip")
) -> List[MLOpsPlatformEvaluation]:
    """Get all platform evaluations with pagination."""
    try:
        evaluations = controller.get_all_evaluations(
            limit=limit, offset=offset)
        return evaluations
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving evaluations: {str(e)}")


@router.get("/platform/{platform_id}", summary="Get evaluations for a specific platform")
async def get_platform_evaluations(platform_id: int) -> List[MLOpsPlatformEvaluation]:
    """Get all evaluations for a specific platform."""
    try:
        evaluations = controller.get_evaluations_by_platform(platform_id)
        if not evaluations:
            raise HTTPException(
                status_code=404, detail="No evaluations found for this platform")
        return evaluations
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving platform evaluations: {str(e)}")


@router.get("/platform/{platform_id}/latest", summary="Get latest evaluation for a platform")
async def get_latest_platform_evaluation(platform_id: int) -> MLOpsPlatformEvaluation:
    """Get the most recent evaluation for a specific platform."""
    try:
        evaluation = controller.get_latest_evaluation_by_platform(platform_id)
        if not evaluation:
            raise HTTPException(
                status_code=404, detail="No evaluation found for this platform")
        return evaluation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving latest evaluation: {str(e)}")


@router.get("/platform/{platform_id}/history", summary="Get score history for a platform")
async def get_platform_score_history(platform_id: int) -> List[Dict[str, Any]]:
    """Get score history for a platform over time."""
    try:
        history = controller.get_platform_score_history(platform_id)
        if not history:
            raise HTTPException(
                status_code=404, detail="No score history found for this platform")
        return history
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving score history: {str(e)}")


@router.get("/evaluator/{evaluator_id}", summary="Get evaluations by evaluator")
async def get_evaluations_by_evaluator(evaluator_id: str) -> List[MLOpsPlatformEvaluation]:
    """Get all evaluations created by a specific evaluator."""
    try:
        evaluations = controller.get_evaluations_by_evaluator(evaluator_id)
        if not evaluations:
            raise HTTPException(
                status_code=404, detail="No evaluations found for this evaluator")
        return evaluations
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving evaluator evaluations: {str(e)}")


@router.get("/top-platforms", summary="Get top platforms by score")
async def get_top_platforms(
    limit: int = Query(
        10, ge=1, le=50, description="Number of top platforms to return")
) -> List[Dict[str, Any]]:
    """Get top platforms ranked by their overall scores."""
    try:
        top_platforms = controller.get_top_platforms_by_score(limit=limit)
        return top_platforms
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving top platforms: {str(e)}")


@router.get("/{evaluation_id}", summary="Get evaluation by ID")
async def get_evaluation(evaluation_id: int) -> MLOpsPlatformEvaluation:
    """Get a specific platform evaluation by its ID."""
    try:
        evaluation = controller.get_platform_evaluation(evaluation_id)
        if not evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return evaluation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving evaluation: {str(e)}")


@router.post("/{platform_id}", summary="Create a new platform evaluation")
async def create_evaluation(platform_id: int, evaluation: MLOpsPlatformEvaluation) -> MLOpsPlatformEvaluation:
    """Create a new platform evaluation with all scores."""
    try:
        # Set evaluation date if not provided
        if not evaluation.evaluation_date:
            evaluation.evaluation_date = datetime.now()

        created_evaluation = controller.create_platform_evaluation(platform_id,evaluation)
        return created_evaluation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating evaluation: {str(e)}")


@router.post("/update/{evaluation_id}", summary="Update an existing evaluation")
async def update_evaluation(
    evaluation_id: int,
    evaluation: MLOpsPlatformEvaluation
) -> MLOpsPlatformEvaluation:
    """Update an existing platform evaluation."""
    try:
        updated_evaluation = controller.update_platform_evaluation(
            evaluation_id, evaluation)
        if not updated_evaluation:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return updated_evaluation
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating evaluation: {str(e)}")


@router.delete("/{evaluation_id}", summary="Delete an evaluation")
async def delete_evaluation(evaluation_id: int) -> Dict[str, str]:
    """Delete a platform evaluation."""
    try:
        success = controller.delete_platform_evaluation(evaluation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Evaluation not found")
        return {"message": "Evaluation deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting evaluation: {str(e)}")
