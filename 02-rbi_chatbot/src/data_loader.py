# src/data_loader.py
import requests
import PyPDF2
import io
import re
import json
from src.config import Config

class DataLoader:
    def __init__(self):
        self.config = Config()
    
    def download_pdf(self):
        """Download and extract text from PDF with better error handling"""
        try:
            print("📥 Downloading RBI PDF from live URL...")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'application/pdf, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://rbi.org.in/'
            }
            
            # Increase timeout and add streaming
            response = requests.get(self.config.PDF_URL, headers=headers, timeout=120, stream=True)
            response.raise_for_status()
            
            # Save PDF to file first for debugging
            pdf_content = response.content
            with open("data/raw/downloaded_rbi.pdf", "wb") as f:
                f.write(pdf_content)
            print("✅ PDF downloaded and saved to data/raw/downloaded_rbi.pdf")
            
            # Try to read the PDF
            pdf_file = io.BytesIO(pdf_content)
            
            try:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                total_pages = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                    print(f"📄 Processed page {page_num + 1}/{total_pages}")
                
                # Clean text
                text = self.clean_text(text)
                print(f"✅ PDF text extracted successfully. Total length: {len(text)} characters")
                return text
                
            except Exception as pdf_error:
                print(f"⚠️ PDF parsing error: {pdf_error}")
                print("🔄 Using enhanced sample data...")
                return self._get_enhanced_sample_text()
            
        except Exception as e:
            print(f"❌ Error downloading PDF: {e}")
            print("🔄 Using comprehensive sample data...")
            return self._get_enhanced_sample_text()
    
    def _get_enhanced_sample_text(self):
        """Return comprehensive, realistic sample text"""
        sample_text = """
        RESERVE BANK OF INDIA
        MASTER DIRECTION - NON-BANKING FINANCIAL COMPANY - SCALE BASED REGULATION (RESERVE BANK) DIRECTIONS, 2023
        
        Notification Date: October 19, 2023
        Effective Date: October 19, 2023
        
        CHAPTER 1: PRELIMINARY
        1.1 Short title and commencement: 
        (a) These directions shall be called the Non-Banking Financial Company - Scale Based Regulation (Reserve Bank) Directions, 2023.
        (b) They shall come into force with effect from the date of their publication in the Official Gazette.
        
        1.2 Applicability: 
        These directions shall apply to every Non-Banking Financial Company (NBFC) including government companies, except those specifically exempted by the Reserve Bank.
        
        CHAPTER 2: DEFINITIONS
        2.1 "Non-Banking Financial Company" (NBFC) means a company registered under the Companies Act, 2013 which carries on as its business the acquisition of shares, stocks, bonds, debentures, securities or the business of banking as defined in clause (b) of section 5 of the Banking Regulation Act, 1949.
        
        2.2 "Scale Based Regulation" means a regulatory framework where the regulation of NBFCs is calibrated based on their size, activity, and perceived riskiness.
        
        2.3 "Capital to Risk-weighted Assets Ratio" (CRAR) means the ratio, expressed as a percentage, of capital funds to risk-weighted assets.
        
        2.4 "Base Layer" means the layer comprising NBFCs with asset size of less than ₹1000 crore.
        
        2.5 "Middle Layer" means the layer comprising NBFCs with asset size of ₹1000 crore and above.
        
        2.6 "Upper Layer" means the layer comprising NBFCs which are identified as systemically significant.
        
        CHAPTER 3: REGULATORY STRUCTURE - SCALE BASED REGULATION (SBR)
        3.1 The Scale Based Regulation framework comprises four layers:
        a) Base Layer: NBFCs with asset size below ₹1000 crore
        b) Middle Layer: NBFCs with asset size of ₹1000 crore and above, and other specified NBFCs
        c) Upper Layer: NBFCs identified as systemically significant based on scoring method
        d) Top Layer: NBFCs in the Upper Layer that may be asked to maintain higher capital buffers
        
        3.2 Capital Adequacy Requirements:
        - Base Layer NBFCs: Minimum CRAR of 15%
        - Middle Layer NBFCs: Minimum CRAR of 15% with Tier I capital of at least 10%
        - Upper Layer NBFCs: Enhanced capital requirements as specified by RBI from time to time
        
        3.3 Leverage Ratio:
        - All Middle and Upper Layer NBFCs shall maintain a leverage ratio of not less than 7%
        - The leverage ratio shall be calculated as Tier I capital as a percentage of exposure
        
        3.4 Liquidity Requirements:
        - All NBFCs shall maintain a liquidity coverage ratio (LCR) as specified
        - Middle and Upper Layer NBFCs shall maintain high-quality liquid assets
        
        CHAPTER 4: GOVERNANCE REQUIREMENTS
        4.1 Board of Directors:
        - Every NBFC shall have a Board of Directors with adequate expertise
        - The Board shall meet at least once every quarter
        - The Board shall constitute various committees including Audit Committee, Risk Management Committee, etc.
        
        4.2 Fit and Proper Criteria:
        - All directors shall meet fit and proper criteria prescribed by RBI
        - Background checks and due diligence shall be conducted
        
        4.3 Risk Management:
        - Middle and Upper Layer NBFCs shall constitute a Risk Management Committee
        - Comprehensive risk management framework shall be established
        - Regular risk assessments shall be conducted
        
        CHAPTER 5: PRUDENTIAL REGULATIONS
        5.1 Asset Classification:
        NBFCs shall classify their assets into the following categories:
        - Standard Assets
        - Sub-standard Assets
        - Doubtful Assets
        - Loss Assets
        
        5.2 Provisioning Requirements:
        - Sub-standard Assets: 10% provision
        - Doubtful Assets: 20% to 100% provision based on period
        - Loss Assets: 100% provision
        
        5.3 Income Recognition:
        - Income on non-performing assets shall not be recognized
        - Interest on NPAs shall be recognized only on actual receipt
        
        5.4 Concentration Norms:
        - Single borrower exposure: 25% of capital funds
        - Group borrower exposure: 40% of capital funds
        - Substantial exposure restrictions for sensitive sectors
        
        CHAPTER 6: REPORTING AND DISCLOSURES
        6.1 Periodic Returns:
        NBFCs shall submit the following returns to RBI:
        - Monthly return on important financial parameters (FORM NBS-1)
        - Quarterly return on asset-liability management (FORM NBS-2)
        - Annual audited financial statements
        - Certificate from statutory auditors
        
        6.2 Disclosure Requirements:
        - NBFCs shall disclose CRAR, NPAs, and other financial parameters
        - Upper Layer NBFCs shall make additional disclosures
        - All disclosures shall be made in the annual report
        
        6.3 Compliance Certificate:
        - NBFCs shall submit a certificate from statutory auditors regarding compliance with these directions
        - The certificate shall be submitted within 3 months from the end of financial year
        
        CHAPTER 7: TRANSITIONAL PROVISIONS
        7.1 Existing NBFCs shall comply with these directions within the specified timelines
        7.2 New NBFCs shall comply with these directions from the date of registration
        7.3 The Reserve Bank may grant specific exemptions on case-to-case basis
        """
        print("✅ Using enhanced sample RBI data for demonstration")
        return sample_text
    
    def create_sample_faqs(self):
        """Create realistic sample FAQs based on actual RBI content"""
        sample_faqs = [
            {
                "question": "What are the different layers in the Scale Based Regulation framework?",
                "answer": "The Scale Based Regulation framework comprises four layers: Base Layer (NBFCs with asset size below ₹1000 crore), Middle Layer (NBFCs with asset size of ₹1000 crore and above), Upper Layer (NBFCs identified as systemically significant), and Top Layer (NBFCs in the Upper Layer that may be asked to maintain higher capital buffers)."
            },
            {
                "question": "What is the minimum capital requirement for Base Layer NBFCs?",
                "answer": "NBFCs in the Base Layer must maintain a minimum Capital to Risk-weighted Assets Ratio (CRAR) of 15%."
            },
            {
                "question": "What are the reporting requirements for NBFCs under SBR?",
                "answer": "NBFCs are required to submit various returns to RBI including monthly return on important financial parameters (FORM NBS-1), quarterly return on asset-liability management (FORM NBS-2), annual audited financial statements, and a compliance certificate from statutory auditors."
            },
            {
                "question": "What is the leverage ratio requirement for Middle Layer NBFCs?",
                "answer": "All Middle and Upper Layer NBFCs shall maintain a leverage ratio of not less than 7%, calculated as Tier I capital as a percentage of exposure."
            },
            {
                "question": "How should NBFCs classify their assets?",
                "answer": "NBFCs shall classify their assets into four categories: Standard Assets, Sub-standard Assets, Doubtful Assets, and Loss Assets, with provisioning requirements of 10% for sub-standard assets, 20-100% for doubtful assets based on period, and 100% for loss assets."
            },
            {
                "question": "What are the governance requirements for NBFC Boards?",
                "answer": "Every NBFC shall have a Board of Directors with adequate expertise that meets at least once every quarter and constitutes various committees including Audit Committee and Risk Management Committee. All directors must meet fit and proper criteria prescribed by RBI."
            }
        ]
        
        print(f"✅ Created {len(sample_faqs)} realistic sample FAQs for evaluation")
        return sample_faqs
    
    def clean_text(self, text: str):
        """Clean extracted text"""
        # Remove extra whitespace but preserve structure
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def create_evaluation_dataset(self, faqs):
        """Create evaluation dataset from FAQs"""
        return [{"question": faq["question"], "reference_answer": faq["answer"]} for faq in faqs]
    
    def save_evaluation_results(self, results, filename="evaluation_results.json"):
        """Save evaluation results to JSON file"""
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Results saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")