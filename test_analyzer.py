#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 网易云音乐分析器
Test script for NetEase Cloud Music Analyzer
"""

import sys
import os
from youqian import NetEaseMusicAnalyzer

def test_keyword_extraction():
    """Test keyword extraction functionality"""
    print("Testing keyword extraction functionality...")
    
    analyzer = NetEaseMusicAnalyzer()
    
    # Test text
    test_lyrics = """
    家是温暖的港湾
    钱不是万能的
    爱情让人心动
    青春岁月如歌
    梦想照亮前路
    """
    
    keywords = analyzer.extract_keywords(test_lyrics)
    print(f"Extracted keywords: {keywords}")
    
    # Verify if expected keywords are found
    expected_keywords = ['家', '钱', '爱情', '青春', '梦想']
    found_keywords = [kw for kw in expected_keywords if kw in keywords]
    
    print(f"Found expected keywords: {found_keywords}")
    return len(found_keywords) >= 2  # At least find 2 expected keywords

def test_year_analysis():
    """Test yearly analysis functionality"""
    print("\nTesting yearly analysis functionality...")
    
    analyzer = NetEaseMusicAnalyzer()
    
    # Simulate adding some data
    test_songs = [
        {'year': 2020, 'keywords': ['家', '钱', '爱情']},
        {'year': 2020, 'keywords': ['家', '梦想', '青春']},
        {'year': 2021, 'keywords': ['钱', '工作', '生活']},
        {'year': 2021, 'keywords': ['爱情', '钱', '未来']},
    ]
    
    for song in test_songs:
        for keyword in song['keywords']:
            analyzer.keywords_by_year[song['year']][keyword] += 1
    
    # Generate rankings
    rankings = analyzer.generate_rankings()
    
    print("2020 keywords:")
    for keyword, count in rankings[2020][:5]:
        print(f"  {keyword}: {count}")
    
    print("2021 keywords:")
    for keyword, count in rankings[2021][:5]:
        print(f"  {keyword}: {count}")
    
    return len(rankings) >= 2

def main():
    """Run all tests"""
    print("Starting NetEase Cloud Music Analyzer tests...")
    print("="*50)
    
    tests = [
        ("Keyword Extraction", test_keyword_extraction),
        ("Yearly Analysis", test_year_analysis),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} - PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {str(e)}")
    
    print(f"\nTest Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
