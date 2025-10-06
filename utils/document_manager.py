"""
Document Manager for NASA Research Assistant
Handles document uploads, metadata, and file operations
"""
import hashlib
import json
from pathlib import Path
from datetime import datetime
import config


def get_file_hash(file_content):
    """
    Calculate a unique hash for a file to detect duplicates
    
    Args:
        file_content: The file bytes
        
    Returns:
        MD5 hash string
    """
    return hashlib.md5(file_content).hexdigest()


def load_document_metadata():
    """
    Load the metadata file that stores info about uploaded documents
    
    Returns:
        Dictionary with document metadata (filename, URL, upload date, etc.)
    """
    # Store metadata in project root so it's tracked by Git (not in data/)
    metadata_file = Path(".document_metadata.json")
    
    try:
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        # If we can't load it, just return empty dict
        print(f"Warning: Could not load document metadata: {e}")
    
    return {}


def save_document_metadata(metadata_dict):
    """
    Save document metadata to disk
    
    Args:
        metadata_dict: The metadata dictionary to save
    """
    # Store metadata in project root so it's tracked by Git (not in data/)
    metadata_file = Path(".document_metadata.json")
    
    try:
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata_dict, f, indent=2)
    except Exception as e:
        print(f"Error saving document metadata: {e}")


def add_document_to_metadata(file_hash, filename, url):
    """
    Add a new document to the metadata store
    
    Args:
        file_hash: Unique hash of the file
        filename: Name of the file
        url: URL where the document can be found
        
    Returns:
        True if added, False if already exists
    """
    metadata = load_document_metadata()
    
    # Check if this file already exists
    if file_hash in metadata:
        return False
    
    # Add the new document
    metadata[file_hash] = {
        "filename": filename,
        "url": url,
        "ingested_at": datetime.now().isoformat()
    }
    
    save_document_metadata(metadata)
    return True


def get_document_url(filename):
    """
    Look up the URL for a document by its filename
    
    Args:
        filename: The document filename
        
    Returns:
        URL string or None if not found
    """
    metadata = load_document_metadata()
    
    # Search through all documents
    for file_hash, doc_info in metadata.items():
        if doc_info.get('filename') == filename:
            return doc_info.get('url')
    
    return None


def is_document_indexed(file_content):
    """
    Check if a document has already been indexed
    
    Args:
        file_content: The file bytes
        
    Returns:
        True if already indexed, False if new
    """
    file_hash = get_file_hash(file_content)
    metadata = load_document_metadata()
    return file_hash in metadata

