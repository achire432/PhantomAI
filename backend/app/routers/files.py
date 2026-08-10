import os

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi.responses import Response
from pydantic import BaseModel

from backend.app.dependencies.auth import (
    get_current_user,
)
from backend.app.models.user import User

from backend.app.services.file_management_service import (
    list_directory,
    get_file_info,
    search_files,
    get_folder_size,
)

from backend.app.services.file_reader import (
    extract_text,
)

from backend.app.services.file_ai_service import (
    ask_about_file,
    summarize_file,
)

from backend.app.services.pdf_service import (
    generate_file_pdf,
)


router = APIRouter(
    prefix="/files",
    tags=["Files"],
)


class FileQuestionRequest(BaseModel):
    path: str
    question: str


class FileSummaryRequest(BaseModel):
    path: str


@router.get("/list")
def list_files(
    path: str = None,
    current_user: User = Depends(get_current_user),
):
    """
    List files and folders in a directory.
    """

    if not path:
        path = os.path.expanduser("~")

    result = list_directory(path)

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Unable to list directory.",
            ),
        )

    return result


@router.get("/info")
def file_info(
    path: str,
    current_user: User = Depends(get_current_user),
):
    """
    Get detailed information about a file.
    """

    result = get_file_info(path)

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Unable to get file information.",
            ),
        )

    return result


@router.get("/search")
def search(
    query: str,
    path: str = None,
    current_user: User = Depends(get_current_user),
):
    """
    Search for files by name.
    """

    if not path:
        path = os.path.expanduser("~")

    result = search_files(
        path,
        query,
    )

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Unable to search files.",
            ),
        )

    return result


@router.get("/size")
def folder_size(
    path: str,
    current_user: User = Depends(get_current_user),
):
    """
    Get the total size of a folder.
    """

    result = get_folder_size(path)

    if not result.get("success"):
        raise HTTPException(
            status_code=400,
            detail=result.get(
                "error",
                "Unable to calculate folder size.",
            ),
        )

    return result


@router.get("/read")
def read_file(
    path: str,
    current_user: User = Depends(get_current_user),
):
    """
    Read and extract text from a supported file.
    """

    if not os.path.isfile(path):
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    try:
        text = extract_text(path)

        if text.startswith("Unsupported file type"):
            raise HTTPException(
                status_code=400,
                detail=text,
            )

        return {
            "success": True,
            "file_name": os.path.basename(path),
            "path": path,
            "text": text,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to read file: {error}",
        )


@router.post("/ask")
def ask_file(
    request: FileQuestionRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Ask PhantomAI a question about a file.
    """

    if not os.path.isfile(request.path):
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    try:
        file_text = extract_text(request.path)

        if file_text.startswith(
            "Unsupported file type"
        ):
            raise HTTPException(
                status_code=400,
                detail=file_text,
            )

        answer = ask_about_file(
            file_name=os.path.basename(
                request.path
            ),
            file_text=file_text,
            question=request.question,
        )

        return {
            "success": True,
            "file_name": os.path.basename(
                request.path
            ),
            "question": request.question,
            "answer": answer,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to analyze file: {error}",
        )


@router.post("/summarize")
def summarize_file_endpoint(
    request: FileSummaryRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Summarize a file using PhantomAI.
    """

    if not os.path.isfile(request.path):
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    try:
        file_text = extract_text(request.path)

        if file_text.startswith(
            "Unsupported file type"
        ):
            raise HTTPException(
                status_code=400,
                detail=file_text,
            )

        summary = summarize_file(
            file_name=os.path.basename(
                request.path
            ),
            file_text=file_text,
        )

        return {
            "success": True,
            "file_name": os.path.basename(
                request.path
            ),
            "summary": summary,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to summarize file: {error}",
        )


@router.get("/export-pdf")
def export_file_pdf(
    path: str,
    current_user: User = Depends(get_current_user),
):
    """
    Read a file and export its extracted content
    as a PDF.
    """

    if not os.path.isfile(path):
        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    try:
        text = extract_text(path)

        if text.startswith(
            "Unsupported file type"
        ):
            raise HTTPException(
                status_code=400,
                detail=text,
            )

        pdf_buffer = generate_file_pdf(
            file_name=os.path.basename(path),
            file_path=path,
            content=text,
        )

        return Response(
            content=pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={
                "Content-Disposition": (
                    f'attachment; '
                    f'filename="{os.path.basename(path)}.pdf"'
                )
            },
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to export PDF: {error}",
        )