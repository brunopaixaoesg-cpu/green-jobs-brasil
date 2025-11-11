"""
Combined test suite runner for Green Jobs Brasil
Runs both smoke tests and pytest integration tests
"""
import sys
import os
import subprocess

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

def run_smoke_tests():
    """Run the legacy smoke tests"""
    print("\n" + "="*60)
    print("RUNNING SMOKE TESTS")
    print("="*60 + "\n")
    
    result = subprocess.run([sys.executable, "scripts/full_smoke_test.py"], 
                          capture_output=False)
    return result.returncode == 0

def run_pytest():
    """Run pytest integration tests"""
    print("\n" + "="*60)
    print("RUNNING PYTEST INTEGRATION TESTS")
    print("="*60 + "\n")
    
    result = subprocess.run([sys.executable, "-m", "pytest", "-v", "tests/"],
                          capture_output=False)
    return result.returncode == 0

def main():
    """Run all tests and report results"""
    smoke_passed = run_smoke_tests()
    pytest_passed = run_pytest()
    
    print("\n" + "="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    print(f"Smoke Tests:    {'✓ PASS' if smoke_passed else '✗ FAIL'}")
    print(f"Pytest Suite:   {'✓ PASS' if pytest_passed else '✗ FAIL'}")
    print("="*60 + "\n")
    
    if smoke_passed and pytest_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed - see output above")
        return 1

if __name__ == "__main__":
    sys.exit(main())
