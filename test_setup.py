"""
Test script to verify all components are working
Run this after installation to check setup
"""
import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    required_packages = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("streamlit", "Streamlit"),
        ("langchain", "LangChain"),
        ("openai", "OpenAI"),
        ("sentence_transformers", "SentenceTransformers"),
        ("faiss", "FAISS"),
        ("PyPDF2", "PyPDF2"),
        ("pydantic", "Pydantic"),
        ("numpy", "NumPy"),
        ("dotenv", "python-dotenv"),
    ]
    
    failed = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name}")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n✅ All packages installed successfully!")
    return True


def test_environment():
    """Test environment variables"""
    print("\nTesting environment variables...")
    
    # Try loading .env
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Please create .env file with your API key:")
        print("OPENAI_API_KEY=sk-your-key-here")
        return False
    
    if api_key == "your_openai_api_key_here":
        print("⚠️  Please replace placeholder API key in .env file")
        return False
    
    print("✓ OPENAI_API_KEY found")
    print(f"✓ Key starts with: {api_key[:7]}...")
    print("\n✅ Environment configured correctly!")
    return True


def test_embedding_model():
    """Test embedding model loading"""
    print("\nTesting embedding model...")
    
    try:
        from sentence_transformers import SentenceTransformer
        
        print("Loading model (this may take a moment on first run)...")
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        
        # Test encoding
        test_text = "This is a test sentence."
        embedding = model.encode(test_text)
        
        print(f"✓ Model loaded successfully")
        print(f"✓ Embedding dimension: {len(embedding)}")
        print("\n✅ Embedding model working!")
        return True
        
    except Exception as e:
        print(f"❌ Error loading embedding model: {str(e)}")
        return False


def test_openai_connection():
    """Test OpenAI API connection"""
    print("\nTesting OpenAI connection...")
    
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        
        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test simple completion
        print("Sending test request to OpenAI...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"✓ OpenAI response: {result}")
        print("\n✅ OpenAI connection working!")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {str(e)}")
        print("Check your API key and internet connection")
        return False


def test_faiss():
    """Test FAISS vector operations"""
    print("\nTesting FAISS...")
    
    try:
        import faiss
        import numpy as np
        
        # Create simple index
        dimension = 384
        index = faiss.IndexFlatL2(dimension)
        
        # Add some vectors
        vectors = np.random.random((10, dimension)).astype('float32')
        index.add(vectors)
        
        # Search
        query = np.random.random((1, dimension)).astype('float32')
        distances, indices = index.search(query, 3)
        
        print(f"✓ Created FAISS index with {index.ntotal} vectors")
        print(f"✓ Search returned {len(indices[0])} results")
        print("\n✅ FAISS working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ FAISS test failed: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("AI RESUME ANALYZER - INSTALLATION TEST")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Environment": test_environment(),
        "Embedding Model": test_embedding_model(),
        "FAISS": test_faiss(),
    }
    
    # Only test OpenAI if API key is configured
    if results["Environment"]:
        results["OpenAI Connection"] = test_openai_connection()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! 🎉")
        print("\nYou can now run the application:")
        print("1. Backend:  python -m backend.main")
        print("2. Frontend: streamlit run frontend/app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the application")
        print("See README.md for troubleshooting help")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
