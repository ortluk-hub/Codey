#!/usr/bin/env bash
# Test script for Cody tool usage and LLM routing

set -e

BASE_URL="http://localhost:8000"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Cody Tool Usage & Routing Tests${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Test 1: Simple math (should use local-tool)
echo -e "${YELLOW}Test 1: Simple math (expect: local-tool)${NC}"
echo "Request: What is 2 + 2 * 10?"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 2 + 2 * 10?"}')
echo "Response: $RESPONSE"
echo ""

# Test 2: String manipulation (should use local-tool)
echo -e "${YELLOW}Test 2: String reverse (expect: local-tool)${NC}"
echo "Request: Reverse the string hello"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Reverse the string hello"}')
echo "Response: $RESPONSE"
echo ""

# Test 3: Complex explanation (should use cloud)
echo -e "${YELLOW}Test 3: Python decorator (expect: ollama-cloud)${NC}"
echo "Request: Explain what a Python decorator is"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain what a Python decorator is"}')
echo "Response: $RESPONSE"
echo ""

# Test 4: Sum calculation (should use local-tool)
echo -e "${YELLOW}Test 4: Sum 1 to 100 (expect: local-tool)${NC}"
echo "Request: Calculate the sum of numbers 1 to 100"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate the sum of numbers 1 to 100"}')
echo "Response: $RESPONSE"
echo ""

# Test 5: Coding help (should use cloud)
echo -e "${YELLOW}Test 5: Write a function (expect: ollama-cloud)${NC}"
echo "Request: Write a Python function to check if a number is prime"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function to check if a number is prime"}')
echo "Response: $RESPONSE"
echo ""

# Test 6: Simple division (should use local-tool)
echo -e "${YELLOW}Test 6: Simple division (expect: local-tool)${NC}"
echo "Request: What is 100 divided by 4?"
RESPONSE=$(curl -s -X POST "$BASE_URL/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is 100 divided by 4?"}')
echo "Response: $RESPONSE"
echo ""

# Test 7: Sandbox /run endpoint
echo -e "${YELLOW}Test 7: Direct sandbox execution${NC}"
echo "Request: Run print(42)"
RESPONSE=$(curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"code": "print(42)"}')
echo "Response: $RESPONSE"
echo ""

# Test 8: Health check
echo -e "${YELLOW}Test 8: Health check${NC}"
RESPONSE=$(curl -s "$BASE_URL/health")
echo "Response: $RESPONSE"
echo ""

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  All tests completed!${NC}"
echo -e "${BLUE}========================================${NC}"
