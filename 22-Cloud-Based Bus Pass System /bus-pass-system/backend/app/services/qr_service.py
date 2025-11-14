import qrcode
import json
import base64
from io import BytesIO

class QRService:
    def generate_qr_code(self, data: dict) -> str:
        """
        Generate QR code containing ticket information
        Returns base64 encoded image string
        """
        # Convert data to JSON string
        json_data = json.dumps(data, indent=2)
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json_data)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str

    def verify_ticket(self, qr_data: str) -> dict:
        """
        Verify ticket from QR code data
        """
        try:
            # In a real implementation, you would decode and verify against database
            decoded_data = base64.b64decode(qr_data)
            # Implementation for ticket verification
            return {"valid": True, "message": "Ticket verified successfully"}
        except Exception as e:
            return {"valid": False, "message": f"Ticket verification failed: {str(e)}"}