# Copyright (c) Microsoft. All rights reserved.

import os
import sys
import json
import asyncio
from datetime import datetime
from dotenv import load_dotenv

# Add the SourceDesigned directory to the path to import the MCP client
sys.path.insert(0, r"C:\TelefonicaProcessAgent\Data\SourceDesigned")

# Load environment variables
load_dotenv(r"C:\TelefonicaProcessAgent\Data\SourceDesigned\.env")

# Import the MCP client methods
from telefonica_mcp_client import (
    call_deuda_fija,
    call_listado_de_boletas_fija,
    call_retrieve_invoice_link
)

"""
Process Orchestrator Main

This orchestrator runs the MCP client methods in sequence:
1. call_listado_de_boletas_fija - Get customer invoices
2. call_retrieve_invoice_link - Get download link for first unpaid invoice
3. call_deuda_fija - Get payment details (if needed)

Each step uses outputs from previous steps as inputs.
"""


class TelefonicaProcessOrchestrator:
    """Orchestrates execution of Telefonica API calls in a business workflow."""
    
    def __init__(self):
        self.execution_log = []
        self.results = {}
        self.customer_data = None
        
    def log_step(self, step_name: str, status: str, data: dict = None):
        """Log execution step."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'step': step_name,
            'status': status,
            'data': data
        }
        self.execution_log.append(log_entry)
        
        status_icon = "✓" if status == "success" else "✗" if status == "error" else "⏳"
        print(f"\n[{status_icon}] {step_name} - {status}")
        if data and status == "error":
            print(f"    Error: {data.get('error', 'Unknown error')}")
        
    async def step_1_get_customer_invoices(self, customer_id: int, msisidn: str):
        """
        Step 1: Get list of customer invoices.
        
        Args:
            customer_id: Customer account ID
            msisidn: Customer phone number
            
        Returns:
            dict: Invoice list response
        """
        self.log_step("Step 1: Get Customer Invoices", "running")
        
        try:
            response = await call_listado_de_boletas_fija(
                customerId=customer_id,
                msisidn=msisidn
            )
            
            # Parse the response
            if 'raw_response' in response:
                # Extract JSON from the raw response
                raw = response['raw_response']
                if '```json' in raw:
                    json_str = raw.split('```json')[1].split('```')[0].strip()
                    invoice_data = json.loads(json_str)
                else:
                    invoice_data = response
            else:
                invoice_data = response
            
            self.results['invoices'] = invoice_data
            self.customer_data = {
                'customer_id': customer_id,
                'msisidn': msisidn,
                'customer_name': invoice_data.get('implInvoiceLists', [{}])[0].get('name', 'Unknown'),
                'customer_rut': invoice_data.get('implInvoiceLists', [{}])[0].get('customerRut', 'Unknown')
            }
            
            # Count invoice statuses
            invoices = invoice_data.get('implInvoiceLists', [])
            open_count = sum(1 for inv in invoices if inv.get('invoiceStatusInd') == 'O')
            paid_count = sum(1 for inv in invoices if inv.get('invoiceStatusInd') == 'P')
            
            self.log_step(
                "Step 1: Get Customer Invoices",
                "success",
                {
                    'total_invoices': len(invoices),
                    'open_invoices': open_count,
                    'paid_invoices': paid_count,
                    'customer_name': self.customer_data['customer_name']
                }
            )
            
            return invoice_data
            
        except Exception as e:
            self.log_step("Step 1: Get Customer Invoices", "error", {'error': str(e)})
            raise
    
    async def step_2_get_first_unpaid_invoice_link(self):
        """
        Step 2: Get download link for the first unpaid invoice from Step 1.
        
        Returns:
            dict: Invoice link response or None if no unpaid invoices
        """
        self.log_step("Step 2: Get Unpaid Invoice Link", "running")
        
        try:
            invoices = self.results['invoices'].get('implInvoiceLists', [])
            
            # Find first unpaid invoice (status 'O' = Open)
            unpaid_invoice = None
            for invoice in invoices:
                if invoice.get('invoiceStatusInd') == 'O':
                    unpaid_invoice = invoice
                    break
            
            if not unpaid_invoice:
                self.log_step(
                    "Step 2: Get Unpaid Invoice Link",
                    "success",
                    {'message': 'No unpaid invoices found'}
                )
                return None
            
            # Get download link for this invoice
            billing_invoice_number = unpaid_invoice['billingInvoiceNumber']
            is_cyclic = unpaid_invoice.get('documentType') == 'CY'
            
            response = await call_retrieve_invoice_link(
                billingInvoiceNumber=billing_invoice_number,
                isCyclicInvoice=is_cyclic
            )
            
            self.results['invoice_link'] = response
            
            self.log_step(
                "Step 2: Get Unpaid Invoice Link",
                "success",
                {
                    'invoice_number': billing_invoice_number,
                    'amount': unpaid_invoice.get('totalAmount'),
                    'due_date': unpaid_invoice.get('dueDate'),
                    'has_link': 'downloadLink' in unpaid_invoice
                }
            )
            
            return response
            
        except Exception as e:
            self.log_step("Step 2: Get Unpaid Invoice Link", "error", {'error': str(e)})
            # Don't raise - continue to next step
            return None
    
    async def step_3_get_payment_details(self, document_id: str):
        """
        Step 3: Get payment details using deuda_fija API.
        
        Args:
            document_id: Document ID for payment lookup
            
        Returns:
            dict: Payment details response
        """
        self.log_step("Step 3: Get Payment Details", "running")
        
        try:
            response = await call_deuda_fija(
                customerIdentification=self.customer_data['customer_rut'],
                type="RUT",
                document=document_id
            )
            
            self.results['payment_details'] = response
            
            self.log_step(
                "Step 3: Get Payment Details",
                "success",
                {'document_id': document_id}
            )
            
            return response
            
        except Exception as e:
            self.log_step("Step 3: Get Payment Details", "error", {'error': str(e)})
            # Don't raise - this API might be blocked by WAF
            return None
    
    def print_summary(self):
        """Print execution summary."""
        print("\n" + "=" * 80)
        print("PROCESS ORCHESTRATION SUMMARY")
        print("=" * 80)
        
        if self.customer_data:
            print(f"\nCustomer Information:")
            print(f"  Name: {self.customer_data['customer_name']}")
            print(f"  RUT: {self.customer_data['customer_rut']}")
            print(f"  Account ID: {self.customer_data['customer_id']}")
            print(f"  Phone: {self.customer_data['msisidn']}")
        
        if 'invoices' in self.results:
            invoices = self.results['invoices'].get('implInvoiceLists', [])
            print(f"\nInvoice Summary:")
            print(f"  Total invoices: {len(invoices)}")
            
            for invoice in invoices:
                status = "OPEN" if invoice.get('invoiceStatusInd') == 'O' else "PAID"
                print(f"    - {invoice['billingInvoiceNumber']}: ${invoice['totalAmount']} CLP ({status})")
        
        print("\nExecution Log:")
        for entry in self.execution_log:
            if entry['status'] in ['success', 'error']:
                status_icon = "✓" if entry['status'] == 'success' else "✗"
                print(f"  [{status_icon}] {entry['step']}")
        
        # Save results to file
        output_file = r"C:\TelefonicaProcessAgent\Data\SourceDesigned\orchestrator_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'customer_data': self.customer_data,
                'results': self.results,
                'execution_log': self.execution_log
            }, f, indent=2)
        
        print(f"\n✓ Results saved to: {output_file}")
        print("=" * 80)


async def main():
    """Main orchestration flow."""
    
    print("=" * 80)
    print("TELEFONICA PROCESS ORCHESTRATOR")
    print("=" * 80)
    print("\nThis orchestrator will execute a complete business process:")
    print("1. Retrieve customer invoices")
    print("2. Get download link for unpaid invoice")
    print("3. Get payment details (if available)")
    
    # Initialize orchestrator
    orchestrator = TelefonicaProcessOrchestrator()
    
    # Define customer to process
    # Using the test data that worked successfully
    CUSTOMER_ID = 45829374
    MSISIDN = "56987654321"
    
    print(f"\nProcessing customer: {CUSTOMER_ID} (Phone: {MSISIDN})")
    print("=" * 80)
    
    try:
        # Step 1: Get customer invoices
        await orchestrator.step_1_get_customer_invoices(CUSTOMER_ID, MSISIDN)
        
        # Step 2: Get invoice link for first unpaid invoice
        await orchestrator.step_2_get_first_unpaid_invoice_link()
        
        # Step 3: Get payment details (optional - may be blocked by WAF)
        # Using the customer RUT from step 1
        if orchestrator.customer_data:
            await orchestrator.step_3_get_payment_details(
                document_id=str(CUSTOMER_ID)
            )
        
    except Exception as e:
        print(f"\n✗ Fatal error in orchestration: {e}")
    
    finally:
        # Print summary
        orchestrator.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
