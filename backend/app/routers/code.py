"""
PHANTOM AI CODE ROUTER
======================

Complete API for PhantomAI's Code Engine.

Supports:

- Code analysis
- AI analysis
- Code generation
- Code explanation
- Code review
- Code fixing
- Security analysis
- Optimization
- Project creation
- Project inspection
- Project file management
- Project analysis
- AI project generation
- Multi-file changes
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from backend.app.dependencies.auth import (
    get_current_user,
)

from backend.app.models.user import User

from backend.app.services.code.code_engine import (
    run_code_analysis,
)

from backend.app.services.code.universal_analyzer import (
    analyze_code,
)

from backend.app.services.code.code_generation_service import (
    generate_code,
    explain_code,
    review_code,
    fix_code,
)

from backend.app.services.code.project_service import (
    create_project,
    list_projects,
    get_project_tree,
    read_project_file,
    write_project_file,
    delete_project_file,
    rename_project_file,
    apply_project_changes,
)

from backend.app.services.code.project_builder_service import (
    generate_project_plan,
)

from backend.app.schemas.code_schemas import (
    CodeGenerateRequest,
    CodeInputRequest,
    CodeFixRequest,
    ProjectCreateRequest,
    ProjectFileRequest,
    ProjectRenameRequest,
    ProjectBuildRequest,
    ProjectApplyRequest,
)


router = APIRouter(
    prefix="/code",
    tags=["Code"],
)


# ============================================================
# BASIC STRUCTURAL ANALYSIS
# ============================================================

@router.post("/analyze")
def analyze_code_file(
    file_path: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = analyze_code(
        file_path
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Code analysis failed.",
            ),
        )

    return result


# ============================================================
# AI CODE ANALYSIS
# ============================================================

@router.post("/ai-analyze")
def ai_analyze_code(
    file_path: str,
    task: str = "explain",
    model_name: str | None = None,
    current_user: User = Depends(
        get_current_user
    ),
):

    allowed_tasks = {
        "explain",
        "find bugs",
        "debug",
        "improve",
        "review",
        "security",
        "optimize",
        "architecture",
        "document",
    }

    if task not in allowed_tasks:

        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported analysis task. "
                f"Allowed tasks: "
                f"{sorted(allowed_tasks)}"
            ),
        )

    result = run_code_analysis(
        file_path=file_path,
        task=task,
        model_name=model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "AI code analysis failed.",
            ),
        )

    return result


# ============================================================
# GENERATE CODE
# ============================================================

@router.post("/generate")
def generate_code_endpoint(
    request: CodeGenerateRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = generate_code(
        prompt=request.prompt,
        language=request.language,
        model_name=request.model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Code generation failed.",
            ),
        )

    return result


# ============================================================
# EXPLAIN CODE
# ============================================================

@router.post("/explain")
def explain_code_endpoint(
    request: CodeInputRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = explain_code(
        code=request.code,
        language=request.language,
        model_name=request.model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Code explanation failed.",
            ),
        )

    return result


# ============================================================
# REVIEW CODE
# ============================================================

@router.post("/review")
def review_code_endpoint(
    request: CodeInputRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = review_code(
        code=request.code,
        language=request.language,
        model_name=request.model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Code review failed.",
            ),
        )

    return result


# ============================================================
# FIX CODE
# ============================================================

@router.post("/fix")
def fix_code_endpoint(
    request: CodeFixRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = fix_code(
        code=request.code,
        language=request.language,
        problem=request.problem,
        model_name=request.model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Code fixing failed.",
            ),
        )

    return result


# ============================================================
# SECURITY ANALYSIS
# ============================================================

@router.post("/security")
def security_analysis_endpoint(
    request: CodeInputRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = run_code_analysis_from_text(
        code=request.code,
        language=request.language,
        task="security",
        model_name=request.model_name,
    )

    return result


# ============================================================
# OPTIMIZATION
# ============================================================

@router.post("/optimize")
def optimization_endpoint(
    request: CodeInputRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = run_code_analysis_from_text(
        code=request.code,
        language=request.language,
        task="optimize",
        model_name=request.model_name,
    )

    return result


# ============================================================
# PROJECT CREATE
# ============================================================

@router.post("/projects")
def create_project_endpoint(
    request: ProjectCreateRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = create_project(
        name=request.name,
        description=request.description,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Project creation failed.",
            ),
        )

    return result


# ============================================================
# PROJECT LIST
# ============================================================

@router.get("/projects")
def list_projects_endpoint(
    current_user: User = Depends(
        get_current_user
    ),
):

    return list_projects()


# ============================================================
# PROJECT TREE
# ============================================================

@router.get("/projects/{project_name}/tree")
def project_tree_endpoint(
    project_name: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = get_project_tree(
        project_name
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=404,
            detail=result.get(
                "error",
                "Project not found.",
            ),
        )

    return result


# ============================================================
# READ PROJECT FILE
# ============================================================

@router.get("/projects/{project_name}/file")
def read_project_file_endpoint(
    project_name: str,
    path: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = read_project_file(
        project_name,
        path,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=404,
            detail=result.get(
                "error",
                "File could not be read.",
            ),
        )

    return result


# ============================================================
# WRITE PROJECT FILE
# ============================================================

@router.put("/projects/{project_name}/file")
def write_project_file_endpoint(
    project_name: str,
    request: ProjectFileRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = write_project_file(
        project_name,
        request.path,
        request.content,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "File could not be written.",
            ),
        )

    return result


# ============================================================
# DELETE PROJECT FILE
# ============================================================

@router.delete("/projects/{project_name}/file")
def delete_project_file_endpoint(
    project_name: str,
    path: str,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = delete_project_file(
        project_name,
        path,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "File could not be deleted.",
            ),
        )

    return result


# ============================================================
# RENAME PROJECT FILE
# ============================================================

@router.post("/projects/{project_name}/rename")
def rename_project_file_endpoint(
    project_name: str,
    request: ProjectRenameRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = rename_project_file(
        project_name,
        request.old_path,
        request.new_path,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Rename failed.",
            ),
        )

    return result


# ============================================================
# PROJECT BUILD PLAN
# ============================================================

@router.post("/projects/build-plan")
def build_project_plan_endpoint(
    request: ProjectBuildRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    result = generate_project_plan(
        prompt=request.prompt,
        model_name=request.model_name,
    )

    if not result.get("success"):

        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Project planning failed.",
            ),
        )

    return result


# ============================================================
# BUILD PROJECT
# ============================================================

@router.post("/projects/{project_name}/build")
def build_project_endpoint(
    project_name: str,
    request: ProjectBuildRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    plan = generate_project_plan(
        prompt=request.prompt,
        model_name=request.model_name,
    )

    if not plan.get("success"):

        raise HTTPException(
            status_code=400,
            detail=plan.get(
                "error",
                "Project generation failed.",
            ),
        )

    result = apply_project_changes(
        project_name=project_name,
        changes=plan.get(
            "files",
            [],
        ),
    )

    return {
        "success": result.get(
            "success"
        ),
        "project": project_name,
        "plan": plan,
        "changes": result,
    }


# ============================================================
# APPLY MULTI-FILE CHANGES
# ============================================================

@router.post("/projects/{project_name}/apply")
def apply_project_changes_endpoint(
    project_name: str,
    request: ProjectApplyRequest,
    current_user: User = Depends(
        get_current_user
    ),
):

    changes = [
        change.model_dump()
        for change in request.changes
    ]

    result = apply_project_changes(
        project_name,
        changes,
    )

    return result


# ============================================================
# INTERNAL TEXT ANALYSIS HELPER
# ============================================================

def run_code_analysis_from_text(
    code: str,
    language: str,
    task: str,
    model_name: str | None = None,
):

    from backend.app.services.code.ai_code_analyzer import (
        analyze_code_with_ai,
    )

    response = analyze_code_with_ai(
        code=code,
        language=language,
        task=task,
        model_name=model_name,
    )

    return {
        "success": True,
        "language": language,
        "task": task,
        "ai": {
            "requested": True,
            "success": True,
            "response": response,
            "model": model_name,
        },
    }