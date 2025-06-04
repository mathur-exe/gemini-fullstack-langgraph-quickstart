# Query Generation Testing

This directory contains test files for testing the query generation functionality from the backend agent.

## Files

- `test_query_generation.py` - Comprehensive interactive test script
- `simple_query_test.py` - Simple test script that can be run directly
- `README.md` - This documentation file

## Prerequisites

1. **Environment Setup**: Make sure you have the `venv` conda environment activated:
   ```bash
   conda activate venv
   ```

2. **API Key**: You need a Gemini API key. Create a `.env` file in the `backend` directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

3. **Dependencies**: Ensure all backend dependencies are installed by running from the backend directory:
   ```bash
   cd ../backend
   pip install -e .
   ```

## Usage

### Simple Query Test

The simplest way to test query generation:

```bash
# Test with sample queries
python simple_query_test.py

# Test with a custom query
python simple_query_test.py "What are the latest trends in machine learning?"
```

### Comprehensive Test

For more detailed testing with interactive options:

```bash
python test_query_generation.py
```

This script offers three testing modes:
1. Test a single custom query
2. Test all sample queries (10 predefined queries)
3. Test different query counts (1-5 queries per input)

## What the Tests Do

The test scripts:

1. **Load the backend agent modules** - Import the `generate_query` function and related components
2. **Create test states** - Simulate the agent state with user messages
3. **Generate queries** - Call the query generation function with sample inputs
4. **Display results** - Show the original query and generated search queries
5. **Handle errors** - Catch and display any errors that occur during testing

## Expected Output

When successful, you'll see output like:

```
[Test 1] Original Query: What are the latest developments in AI?
----------------------------------------
✅ Success! Generated queries:
  1. artificial intelligence latest developments 2024
  2. AI breakthrough technologies recent advances
  3. machine learning innovations current trends
```

## Sample Queries

The tests include these sample queries:
- AI and technology developments
- Stock market comparisons
- Environmental impacts
- Programming frameworks
- Health and wellness topics
- Climate change effects
- Cybersecurity trends
- Economic policies
- Gene editing technology
- Remote work productivity

## Troubleshooting

### Common Issues

1. **ImportError**: Make sure you're running from the correct directory and the backend source is accessible
2. **API Key Error**: Ensure `GEMINI_API_KEY` is set in the `.env` file in the backend directory
3. **Module Not Found**: Activate the `venv` conda environment and install backend dependencies

### Environment Variables

The test looks for the `.env` file in the backend directory. Make sure it contains:
```
GEMINI_API_KEY=your_actual_api_key
```

## Output Files

The comprehensive test script can save results to JSON files:
- `query_generation_test_results_YYYYMMDD_HHMMSS.json` - All test results
- `query_count_test_results.json` - Query count variation tests

These files contain detailed information about each test including:
- Original queries
- Generated queries
- Success/failure status
- Timestamps
- Error messages (if any) 