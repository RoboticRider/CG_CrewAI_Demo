import os
import base64
from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


# =========================
# INPUT SCHEMA
# =========================
class InvoicePDFInput(BaseModel):
    company_name: str = Field(..., alias="Company Name")
    invoice_date: str = Field(..., alias="Invoice Date")
    invoice_amount: str = Field(..., alias="Invoice Amount")
    invoice_no: str = Field(..., alias="Invoice Number")


# =========================
# TOOL CLASS
# =========================
class GenerateInvoicePDFTool(BaseTool):
    name: str = "Generate Invoice PDF"
    description: str = (
        "Generates a PDF invoice and returns it as Base64 along with file name."
    )
    args_schema: Type[BaseModel] = InvoicePDFInput

    def _run(
        self,
        company_name: str,
        invoice_date: str,
        invoice_amount: str,
        invoice_no: str
    ) -> dict:

        # =========================
        # STEP 1: CREATE PDF (Cloud Safe)
        # =========================
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        safe_invoice_no = invoice_no.replace(" ", "_").replace("/", "_")
        file_name = f"{safe_invoice_no}.pdf"
        file_path = os.path.join(output_dir, file_name)

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

        # =========================
        # STEP 2: CONVERT TO BASE64
        # =========================
        with open(file_path, "rb") as f:
            encoded_pdf = base64.b64encode(f.read()).decode("utf-8")

        # =========================
        # STEP 3: RETURN STRUCTURED OUTPUT
        # =========================
        return {
            "status": "success",
            "file_name": file_name,
            "file_content": encoded_pdf,
            "message": "PDF generated and encoded successfully"
        }