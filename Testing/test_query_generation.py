#!/usr/bin/env python3
"""
Test script for the query generation functionality in the backend agent.

This script tests the generate_query function which takes user questions
and generates optimized search queries using Gemini 2.0 Flash.
"""

import os
import sys
from typing import List, Dict
import json
from datetime import datetime

# Add the backend source to the Python path
backend_src_path = os.path.join(os.path.dirname(__file__), "..", "backend", "src")
sys.path.insert(0, backend_src_path)

# Import the required modules from the agent
from agent.graph import generate_query
from agent.state import OverallState, QueryGenerationState
from agent.tools_and_schemas import SearchQueryList
from agent.configuration import Configuration
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph
from langgraph.types import RunnableConfig
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class QueryGenerationTester:
    """Test class for the query generation functionality."""
    
    def __init__(self):
        """Initialize the tester with sample queries."""
        self.sample_queries = [
            "What are the latest developments in artificial intelligence for 2024?",
            "How does Tesla's stock performance compare to traditional automakers?",
            "What are the environmental impacts of cryptocurrency mining?",
            "Explain the differences between React and Vue.js frameworks",
            "What are the health benefits of intermittent fasting?",
            "How is climate change affecting global food security?",
            "What are the latest trends in cybersecurity threats?",
            "Compare the economic policies of different countries during COVID-19",
            "What are the potential risks and benefits of gene editing technology?",
            "How has remote work affected productivity in tech companies?"
        ]
        
        # Check if API key is available
        if not os.getenv("GEMINI_API_KEY"):
            print("Warning: GEMINI_API_KEY not found. Please set it in your .env file.")
            print("You can create a .env file in the backend directory with:")
            print("GEMINI_API_KEY=your_api_key_here")
            
    def create_test_state(self, user_query: str, num_queries: int = 3) -> OverallState:
        """Create a test state with the given user query."""
        return {
            "messages": [HumanMessage(content=user_query)],
            "initial_search_query_count": num_queries,
            "research_loop_count": 0,
            "sources_gathered": [],
            "search_query": [],
            "web_research_result": [],
        }
    
    def create_test_config(self) -> RunnableConfig:
        """Create a test configuration."""
        return RunnableConfig(
            configurable={
                "query_generator_model": "gemini-2.0-flash-exp",
                "reasoning_model": "gemini-2.0-flash-thinking-exp-1219",
                "number_of_initial_queries": 3,
                "max_research_loops": 3,
            }
        )
    
    def test_single_query(self, user_query: str, num_queries: int = 3) -> Dict:
        """Test query generation for a single user query."""
        print(f"\n{'='*60}")
        print(f"Testing Query Generation")
        print(f"{'='*60}")
        print(f"Original Query: {user_query}")
        print(f"Requested number of queries: {num_queries}")
        print("-" * 60)
        
        try:
            # Create test state and config
            state = self.create_test_state(user_query, num_queries)
            config = self.create_test_config()
            
            # Generate queries
            result = generate_query(state, config)
            
            # Display results
            print(f"✅ Success! Generated {len(result['query_list'])} queries:")
            for i, query in enumerate(result['query_list'], 1):
                print(f"  {i}. {query}")
            
            return {
                "success": True,
                "original_query": user_query,
                "generated_queries": result['query_list'],
                "num_generated": len(result['query_list']),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return {
                "success": False,
                "original_query": user_query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def test_all_sample_queries(self) -> List[Dict]:
        """Test query generation for all sample queries."""
        print(f"\n{'='*80}")
        print(f"TESTING QUERY GENERATION FUNCTIONALITY")
        print(f"{'='*80}")
        print(f"Testing {len(self.sample_queries)} sample queries...")
        
        results = []
        successful_tests = 0
        
        for i, query in enumerate(self.sample_queries, 1):
            print(f"\n[Test {i}/{len(self.sample_queries)}]")
            result = self.test_single_query(query)
            results.append(result)
            
            if result["success"]:
                successful_tests += 1
        
        # Summary
        print(f"\n{'='*80}")
        print(f"TEST SUMMARY")
        print(f"{'='*80}")
        print(f"Total tests: {len(self.sample_queries)}")
        print(f"Successful: {successful_tests}")
        print(f"Failed: {len(self.sample_queries) - successful_tests}")
        print(f"Success rate: {(successful_tests/len(self.sample_queries)*100):.1f}%")
        
        return results
    
    def test_different_query_counts(self, test_query: str = None) -> List[Dict]:
        """Test query generation with different numbers of requested queries."""
        if test_query is None:
            test_query = "What are the latest developments in artificial intelligence?"
        
        print(f"\n{'='*80}")
        print(f"TESTING DIFFERENT QUERY COUNTS")
        print(f"{'='*80}")
        print(f"Using test query: {test_query}")
        
        results = []
        query_counts = [1, 2, 3, 4, 5]
        
        for count in query_counts:
            print(f"\n[Testing with {count} requested queries]")
            result = self.test_single_query(test_query, count)
            results.append(result)
        
        return results
    
    def save_results_to_file(self, results: List[Dict], filename: str = None):
        """Save test results to a JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_generation_test_results_{timestamp}.json"
        
        filepath = os.path.join(os.path.dirname(__file__), filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📁 Results saved to: {filepath}")
        return filepath


def main():
    """Main function to run the query generation tests."""
    print("🚀 Starting Query Generation Tests...")
    
    # Check if GEMINI_API_KEY is set
    if not os.getenv("GEMINI_API_KEY"):
        print("\n❌ Error: GEMINI_API_KEY environment variable is not set!")
        print("Please create a .env file in the backend directory with:")
        print("GEMINI_API_KEY=your_api_key_here")
        return
    
    tester = QueryGenerationTester()
    
    # Option 1: Test a single custom query
    print("\n" + "="*50)
    print("OPTION 1: Test a custom query")
    print("="*50)
    custom_query = input("Enter a custom query to test (or press Enter to skip): ").strip()
    
    if custom_query:
        tester.test_single_query(custom_query)
    
    # Option 2: Test all sample queries
    print("\n" + "="*50)
    print("OPTION 2: Test all sample queries")
    print("="*50)
    test_all = input("Test all sample queries? (y/n): ").strip().lower()
    
    if test_all == 'y':
        results = tester.test_all_sample_queries()
        
        # Save results
        save_results = input("\nSave results to file? (y/n): ").strip().lower()
        if save_results == 'y':
            tester.save_results_to_file(results)
    
    # Option 3: Test different query counts
    print("\n" + "="*50)
    print("OPTION 3: Test different query counts")
    print("="*50)
    test_counts = input("Test different query counts? (y/n): ").strip().lower()
    
    if test_counts == 'y':
        results = tester.test_different_query_counts()
        tester.save_results_to_file(results, "query_count_test_results.json")
    
    print("\n🎉 Testing completed!")


if __name__ == "__main__":
    main() 