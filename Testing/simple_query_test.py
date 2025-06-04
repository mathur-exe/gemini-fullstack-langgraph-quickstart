#!/usr/bin/env python3
"""
Simple test script for query generation functionality.

This script provides a quick way to test the query generation without interactive prompts.
It can be run directly to test sample queries or imported to test specific queries.
"""

import os
import sys
from typing import List, Dict

# Add the backend source to the Python path
backend_src_path = os.path.join(os.path.dirname(__file__), "..", "backend", "src")
sys.path.insert(0, backend_src_path)

from agent.graph import generate_query
from agent.state import OverallState
from langchain_core.messages import HumanMessage
from langgraph.types import RunnableConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_query_generation(user_query: str, num_queries: int = 3) -> Dict:
    """
    Test the query generation functionality with a given user query.
    
    Args:
        user_query: The original user question
        num_queries: Number of queries to generate (default: 3)
    
    Returns:
        Dictionary containing the results of the test
    """
    
    # Create test state
    state = {
        "messages": [HumanMessage(content=user_query)],
        "initial_search_query_count": num_queries,
        "research_loop_count": 0,
        "sources_gathered": [],
        "search_query": [],
        "web_research_result": [],
    }
    
    # Create test configuration with updated model
    config = RunnableConfig(
        configurable={
            "query_generator_model": "gemini-2.5-flash-preview-05-20",
            "reasoning_model": "gemini-2.5-flash-preview-05-20", 
            "number_of_initial_queries": num_queries,
            "max_research_loops": 3,
        }
    )
    
    try:
        # Generate queries
        result = generate_query(state, config)
        
        return {
            "success": True,
            "original_query": user_query,
            "generated_queries": result['query_list'],
            "num_generated": len(result['query_list']),
        }
        
    except Exception as e:
        return {
            "success": False,
            "original_query": user_query,
            "error": str(e),
        }


def run_sample_tests():
    """Run tests with sample queries and display results."""
    
    sample_queries = [
        "What are the latest developments in AI?",
        "How does Tesla compare to other car companies?", 
        "What are the benefits of renewable energy?",
        "Explain machine learning algorithms",
        "What is the future of cryptocurrency?"
    ]
    
    print("🚀 Testing Query Generation Functionality")
    print("=" * 60)
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ Error: GEMINI_API_KEY environment variable not set!")
        print("Please set your Gemini API key in the .env file")
        return
    
    successful_tests = 0
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n[Test {i}] Original Query: {query}")
        print("-" * 40)
        
        result = test_query_generation(query)
        
        if result["success"]:
            print("✅ Success! Generated queries:")
            for j, gen_query in enumerate(result["generated_queries"], 1):
                print(f"  {j}. {gen_query}")
            successful_tests += 1
        else:
            print(f"❌ Failed: {result['error']}")
    
    print(f"\n{'=' * 60}")
    print(f"Summary: {successful_tests}/{len(sample_queries)} tests passed")
    print("=" * 60)


if __name__ == "__main__":
    # Check if a custom query was provided as command line argument
    if len(sys.argv) > 1:
        custom_query = " ".join(sys.argv[1:])
        print(f"Testing custom query: {custom_query}")
        result = test_query_generation(custom_query)
        
        if result["success"]:
            print(f"\n✅ Generated {len(result['generated_queries'])} queries:")
            for i, query in enumerate(result["generated_queries"], 1):
                print(f"  {i}. {query}")
        else:
            print(f"❌ Error: {result['error']}")
    else:
        # Run sample tests
        run_sample_tests() 