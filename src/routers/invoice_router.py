import io
from typing import Annotated, Union

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse, StreamingResponse
from loguru import logger

from cruds import invoice_crud
from dependencies import GetDBDep, GetCurrentAdminUserDep
from exceptions import DatabaseError, NotFoundError
from schemas.invoice_schema import InvoiceBaseSchema, InvoiceSchema

invoice_router = APIRouter(prefix="/invoices", tags=["Invoices"])


@invoice_router.get("/", response_model=list[InvoiceSchema])
async def read_invoices(
    db: GetDBDep,
    # current_user: GetCurrentAdminUserDep,
) -> list[InvoiceSchema]:
    """Reads and returns all invoices from the database."""
    try:
        invoices = invoice_crud.get_invoices(db)
        return invoices
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@invoice_router.get("/{invoice_id}", response_model=InvoiceSchema)
async def read_invoice(
    db: GetDBDep,
    # current_user: GetCurrentAdminUserDep,
    invoice_id: int,
) -> InvoiceSchema:
    """Reads and returns a specific invoice from the database."""
    try:
        invoice = invoice_crud.get_invoice_by_id(db, invoice_id)
        return invoice
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@invoice_router.get("/{invoice_id}/download")
async def download_invoice(
    db: GetDBDep,
    invoice_id: int
    # db: GetDBDep, current_user: GetCurrentAdminUserDep, invoice_id: int
):
    """Downloads a specific invoice from the database."""
    try:
        invoice_pdf, invoice_filename = invoice_crud.download_invoice_by_id(
            db, invoice_id
        )
        return StreamingResponse(
            invoice_pdf,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={invoice_filename}"},
        )
        # return FileResponse(
        #     invoice_pdf, filename=invoice_filename, media_type="application/pdf"
        # )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@invoice_router.put("/{invoice_id}/mark_as_paid", response_model=InvoiceSchema)
async def mark_invoice_as_paid(
    db: GetDBDep, current_user: GetCurrentAdminUserDep, invoice_id: int
) -> InvoiceSchema:
    """Sets the date paid for a specific invoice from the database."""
    try:
        invoice = invoice_crud.mark_invoice_paid_by_id(db, current_user, invoice_id)
        return invoice
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
