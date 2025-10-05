"""
Enhanced Multimodal Document Processor for NASA RAG System
Handles images, tables, formulas, and charts from research papers
"""
import os
from pathlib import Path
from typing import List, Dict
import fitz  # PyMuPDF
from PIL import Image
import config


class MultimodalProcessor:
    """Process PDFs with images, tables, and formulas"""
    
    def __init__(self):
        """Initialize the multimodal processor"""
        self.image_dir = Path(config.IMAGE_EXTRACTION_DIR)
        self.image_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_images_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Extract all images from a PDF with context
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of dicts with image info and context
        """
        pdf_path = Path(pdf_path)
        doc = fitz.open(pdf_path)
        extracted_images = []
        
        for page_num, page in enumerate(doc):
            # Get text from page for context
            page_text = page.get_text()
            
            # Extract images
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Save image
                    image_filename = f"{pdf_path.stem}_page{page_num+1}_img{img_index+1}.{image_ext}"
                    image_path = self.image_dir / image_filename
                    
                    with open(image_path, "wb") as img_file:
                        img_file.write(image_bytes)
                    
                    # Store metadata
                    extracted_images.append({
                        "path": str(image_path),
                        "page": page_num + 1,
                        "context": page_text[:500],  # Surrounding text
                        "source_pdf": pdf_path.name,
                        "type": "figure/chart"
                    })
                    
                except Exception as e:
                    print(f"⚠️  Could not extract image {img_index} from page {page_num}: {e}")
        
        doc.close()
        return extracted_images
    
    def describe_image_with_gemini(self, image_path: str) -> str:
        """
        Use Gemini Vision to describe images
        
        Args:
            image_path: Path to image file
            
        Returns:
            Description of the image
        """
        try:
            import google.generativeai as genai
            import time
            genai.configure(api_key=config.GOOGLE_API_KEY)
            
            # Use Gemini 1.5 Flash (supports vision and is faster/cheaper)
            model = genai.GenerativeModel('gemini-1.5-flash')
            img = Image.open(image_path)
            
            prompt = """Analyze this image from a NASA research paper. Describe:
1. What type of visualization is this (chart, diagram, photo, etc.)?
2. What data or information does it show?
3. Key findings or patterns visible
4. Any labels, legends, or annotations

Be technical and precise."""
            
            response = model.generate_content(
                [prompt, img],
                request_options={'timeout': 30}
            )
            
            time.sleep(1)  # Avoid rate limiting
            
            return response.text
            
        except Exception as e:
            print(f"⚠️  Could not describe image {Path(image_path).name}: {e}")
            return "Image description not available"


def process_pdf_multimodal(pdf_path: str) -> Dict:
    """Process a PDF with full multimodal extraction (images, text, metadata)"""
    import json
    processor = MultimodalProcessor()
    
    result = {
        "pdf_path": pdf_path,
        "images": [],
        "tables": [],
        "text": ""
    }
    
    if config.EXTRACT_IMAGES:
        result["images"] = processor.extract_images_from_pdf(pdf_path)
        
        # Describe images with AI if enabled
        if config.GOOGLE_API_KEY and getattr(config, 'DESCRIBE_IMAGES_WITH_AI', True):
            for img_data in result["images"]:
                img_data["description"] = processor.describe_image_with_gemini(img_data["path"])
        
        # Save metadata
        if result["images"]:
            _save_image_metadata(result["images"])
    
    return result


def _save_image_metadata(new_images: List[Dict]):
    """Save or append image metadata to JSON file"""
    import json
    from pathlib import Path
    
    metadata_file = Path(config.IMAGE_EXTRACTION_DIR) / "image_metadata.json"
    
    # Load existing metadata
    existing_images = []
    if metadata_file.exists():
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                existing_images = json.load(f)
        except:
            pass
    
    # Avoid duplicates
    existing_paths = {img['path'] for img in existing_images}
    for img in new_images:
        if img['path'] not in existing_paths:
            existing_images.append(img)
    
    # Save
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(existing_images, f, indent=2)


if __name__ == "__main__":
    # Test the processor
    import sys
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        result = process_pdf_multimodal(pdf_file)
        print(f"\n✅ Processed {result['pdf_path']}")
        print(f"   - {len(result['images'])} images extracted")
    else:
        print("Usage: python multimodal_processor.py <pdf_file>")

