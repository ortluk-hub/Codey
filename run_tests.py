#!/usr/bin/env python
"""Quick test runner script."""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Try imports
print("Testing imports...")
try:
    from cody import api_ui, tcp_server, llm, config, memory, sandbox, status
    print("  cody.* imports: OK")
except Exception as e:
    print(f"  cody.* imports: FAILED - {e}")

try:
    from codey import project
    print("  codey.* imports: OK")
except Exception as e:
    print(f"  codey.* imports: FAILED - {e}")

# Run tests
print("\nRunning tests...")
import unittest

loader = unittest.TestLoader()
suite = loader.discover('tests', pattern='test_*.py')
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

# Summary
print(f"\n{'='*60}")
print(f"Tests run: {result.testsRun}")
print(f"Failures: {len(result.failures)}")
print(f"Errors: {len(result.errors)}")
print(f"Success: {result.wasSuccessful()}")
