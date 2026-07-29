import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from tests import run_tests as sprint1_tests
from tests import test_services as service_tests

if __name__ == "__main__":
    print("==================================================")
    print("   RUNNING ALL IMPORT SYSTEM VERIFICATION TESTS")
    print("==================================================")
    
    print("\n--- 1. Testing Database Initialization & Audit Log (Sprint 1) ---")
    sprint1_tests.run()

    print("\n--- 2. Testing Business Logic & Calculations (Sprint 2, 3, 4) ---")
    service_tests.run_tests()

    print("\n==================================================")
    print(" 🎉 ALL SYSTEM VERIFICATION TESTS PASSED PERFECTLY!")
    print("==================================================")
