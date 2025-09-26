#!/usr/bin/env python3
"""
Script to run tests with the correct virtual environment
"""
import subprocess
import sys
import os

def main():
    """Run tests with proper environment activation"""
    
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Command to activate environment and run pytest
    cmd = [
        "bash", "-c",
        "source ../bin/activate && python -m pytest " + " ".join(sys.argv[1:])
    ]
    
    print("🧪 Running tests with virtual environment...")
    print(f"📁 Working directory: {project_dir}")
    print(f"🔧 Command: {' '.join(sys.argv[1:]) if sys.argv[1:] else 'all tests'}")
    print()
    
    # Run the command
    try:
        result = subprocess.run(cmd, cwd=project_dir)
        sys.exit(result.returncode)
    except KeyboardInterrupt:
        print("\n❌ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
