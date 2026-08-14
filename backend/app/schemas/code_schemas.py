"""
PHANTOM AI CODE ENGINE SCHEMAS
==============================

Request/response models used by the Code Engine.
"""

from typing import Optional

from pydantic import BaseModel, Field


# ============================================================
# CODE GENERATION
# ============================================================

class CodeGenerateRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Describe the code you want PhantomAI to generate.",
    )

    language: str = Field(
        default="python",
        description="Programming language.",
    )

    model_name: Optional[str] = None


# ============================================================
# DIRECT CODE INPUT
# ============================================================

class CodeInputRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
    )

    language: str = Field(
        default="python",
    )

    model_name: Optional[str] = None


# ============================================================
# CODE FIX
# ============================================================

class CodeFixRequest(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
    )

    language: str = Field(
        default="python",
    )

    problem: str = Field(
        default="Find and fix problems in this code.",
    )

    model_name: Optional[str] = None


# ============================================================
# PROJECT CREATION
# ============================================================

class ProjectCreateRequest(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
    )

    description: str = Field(
        default="",
    )


# ============================================================
# PROJECT FILE
# ============================================================

class ProjectFileRequest(BaseModel):
    path: str = Field(
        ...,
        min_length=1,
    )

    content: str = Field(
        default="",
    )


# ============================================================
# PROJECT RENAME
# ============================================================

class ProjectRenameRequest(BaseModel):
    old_path: str = Field(
        ...,
        min_length=1,
    )

    new_path: str = Field(
        ...,
        min_length=1,
    )


# ============================================================
# PROJECT BUILD
# ============================================================

class ProjectBuildRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        description="Describe the application PhantomAI should build.",
    )

    model_name: Optional[str] = None


# ============================================================
# PROJECT APPLY CHANGES
# ============================================================

class ProjectChange(BaseModel):
    action: str
    path: str
    content: Optional[str] = None
    new_path: Optional[str] = None


class ProjectApplyRequest(BaseModel):
    changes: list[ProjectChange]