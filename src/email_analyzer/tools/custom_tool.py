import os
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class InvoicePDFInput(BaseModel):
    company_name: str = Field(..., alias="Company Name")
    invoice_date: str = Field(..., alias="Invoice Date")
    invoice_amount: str = Field(..., alias="Invoice Amount")
    invoice_no: str = Field(..., alias="Invoice Number")


class GenerateInvoicePDFTool(BaseTool):
    name: str = "Generate Invoice PDF"
    description: str = (
        "Generates a professional PDF invoice using structured data like "
        "Company Name, Invoice Date, Invoice Amount, and Invoice Number."
    )
    args_schema: Type[BaseModel] = InvoicePDFInput

    def _run(
        self,
        company_name: str,
        invoice_date: str,
        invoice_amount: str,
        invoice_no: str
    ) -> dict:

        output_dir = r"C:\Invoice"
        os.makedirs(output_dir, exist_ok=True)

        safe_invoice_no = invoice_no.replace(" ", "_").replace("/", "_")
        file_path = os.path.join(output_dir, f"{safe_invoice_no}.pdf")
        file_path = os.path.normpath(file_path)

        doc = SimpleDocTemplate(file_path)
        styles = getSampleStyleSheet()

        content = []
        content.append(Paragraph("<b>Invoice Details</b>", styles["Title"]))
        content.append(Spacer(1, 20))

        content.append(Paragraph(f"<b>Company Name:</b> {company_name}", styles["Normal"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"<b>Invoice Date:</b> {invoice_date}", styles["Normal"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"<b>Invoice Amount:</b> {invoice_amount}", styles["Normal"]))
        content.append(Spacer(1, 12))

        content.append(Paragraph(f"<b>Invoice Number:</b> {invoice_no}", styles["Normal"]))

        doc.build(content)

        return {
            "status": "success",
            "file_path": file_path
        }