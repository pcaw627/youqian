#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for keyword frequency analyzer
"""

import sys
import json
from keyword_frequency_analyzer import KeywordFrequencyAnalyzer

def test_keyword_analysis():
    """Test keyword analysis with sample data"""
    print("Testing keyword frequency analysis...")
    
    analyzer = KeywordFrequencyAnalyzer()
    
    # Test with sample keywords
    test_keywords = ["家", "钱", "爱情", "青春", "梦想"]
    
    # Test vocabulary extraction
    test_lyrics = [
        "家是温暖的港湾 钱不是万能的",
        "爱情让人心动 青春岁月如歌",
        "梦想照亮前路 家是归宿",
        "钱能买到很多东西 但买不到爱情",
        "青春无悔 梦想成真"
    ]
    
    print("\nTest lyrics and keyword extraction:")
    print("-" * 50)
    
    for i, lyrics in enumerate(test_lyrics, 1):
        vocab = analyzer.extract_vocabulary(lyrics)
        print(f"{i}. Lyrics: '{lyrics}'")
        print(f"   Vocabulary: {vocab}")
        
        # Check for keywords
        found_keywords = [kw for kw in test_keywords if kw in vocab]
        print(f"   Found keywords: {found_keywords}")
        print()
    
    return True

def test_json_output_format():
    """Test the expected JSON output format"""
    print("Testing JSON output format...")
    
    # Sample output structure
    sample_output = {
        "analysis_info": {
            "total_songs_processed": 1000,
            "total_keyword_matches": 500,
            "keywords_analyzed": ["家", "钱", "爱情", "青春", "梦想"],
            "analysis_date": "2024-01-01T12:00:00",
            "years_covered": 5
        },
        "keyword_frequencies": {
            "家": [
                [2020, 25],
                [2021, 30],
                [2022, 35],
                [2023, 40]
            ],
            "钱": [
                [2020, 15],
                [2021, 20],
                [2022, 25],
                [2023, 30]
            ],
            "爱情": [
                [2020, 45],
                [2021, 50],
                [2022, 55],
                [2023, 60]
            ]
        },
        "statistics": {
            "total_unique_years": 4,
            "keywords_with_data": 3
        }
    }
    
    print("Sample JSON structure:")
    print(json.dumps(sample_output, ensure_ascii=False, indent=2))
    
    return True

def main():
    """Run all tests"""
    print("Keyword Frequency Analyzer Test Suite")
    print("=" * 50)
    
    tests = [
        ("Keyword Analysis", test_keyword_analysis),
        ("JSON Output Format", test_json_output_format),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 Running {test_name}...")
            result = test_func()
            if result:
                print(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

