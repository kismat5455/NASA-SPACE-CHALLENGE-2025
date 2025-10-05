"""
Quick Start Script for NASA RAG System
Checks setup and guides user through initial configuration
"""
import os
import sys


def check_python_version():
    """Check if Python version is adequate"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'llama_index',
        'google.generativeai',
        'streamlit',
        'dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('_', '.'))
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print("\n⚠️  Missing packages detected!")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def check_api_key():
    """Check if API key is configured"""
    print("\n🔑 Checking API key...")
    
    if not os.path.exists('.env'):
        print("  ❌ .env file not found")
        print("\n📝 To set up your API key:")
        print("  1. Get your key from: https://makersuite.google.com/app/apikey")
        print("  2. Create a .env file with: GOOGLE_API_KEY=your_key_here")
        return False
    
    # Try to load and check
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        print("  ❌ API key not configured properly")
        print("\n📝 To set up your API key:")
        print("  1. Get your key from: https://makersuite.google.com/app/apikey")
        print("  2. Edit .env file and add: GOOGLE_API_KEY=your_actual_key")
        return False
    
    print(f"  ✅ API key configured ({api_key[:10]}...)")
    return True


def check_documents():
    """Check if documents are available"""
    print("\n📚 Checking documents...")
    
    if not os.path.exists('data'):
        print("  ❌ data/ folder not found")
        return False
    
    files = [f for f in os.listdir('data') if f.endswith(('.pdf', '.txt', '.docx', '.md'))]
    
    if not files:
        print("  ⚠️  No documents found in data/ folder")
        print("     Add PDF, TXT, DOCX, or MD files to get started")
        print("     (A sample document has been provided)")
        return False
    
    print(f"  ✅ Found {len(files)} document(s)")
    for f in files[:5]:  # Show first 5
        print(f"     - {f}")
    if len(files) > 5:
        print(f"     ... and {len(files) - 5} more")
    
    return True


def check_index():
    """Check if vector index exists"""
    print("\n🗃️  Checking vector index...")
    
    if not os.path.exists('vector_store'):
        print("  ⚠️  No index found - run: python document_ingestion.py")
        return False
    
    files = os.listdir('vector_store')
    if not files:
        print("  ⚠️  Index folder empty - run: python document_ingestion.py")
        return False
    
    print(f"  ✅ Index exists")
    return True


def main():
    """Main setup check"""
    print("=" * 60)
    print("🚀 NASA RAG System - Quick Start Check")
    print("=" * 60)
    
    checks = {
        "Python Version": check_python_version(),
        "Dependencies": False,
        "API Key": False,
        "Documents": False,
        "Vector Index": False
    }
    
    # Only check dependencies if Python version is OK
    if checks["Python Version"]:
        checks["Dependencies"] = check_dependencies()
    
    # Only check API key if dependencies are installed
    if checks["Dependencies"]:
        checks["API Key"] = check_api_key()
        checks["Documents"] = check_documents()
        checks["Vector Index"] = check_index()
    
    print("\n" + "=" * 60)
    print("📊 Setup Status")
    print("=" * 60)
    
    for check, status in checks.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check}")
    
    print("=" * 60)
    
    if all(checks.values()):
        print("\n🎉 Everything is set up! You're ready to go!")
        print("\n🚀 Next Steps:")
        print("   1. Run web interface: streamlit run app.py")
        print("   2. Or run CLI: python query_engine.py")
    else:
        print("\n⚠️  Setup incomplete. Please follow the steps above.")
        print("\n📖 For detailed instructions, see:")
        print("   - README.md")
        print("   - setup_guide.md")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

