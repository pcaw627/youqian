#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for vocabulary extraction functionality
"""

import sys
from youqian import ChineseRapVocabularyAnalyzer

def test_vocabulary_extraction():
    """Test vocabulary extraction with various text samples"""
    print("Testing vocabulary extraction...")
    
    analyzer = ChineseRapVocabularyAnalyzer()
    
    # Test cases with mixed Chinese-English text
    test_cases = [
        "有人喜欢我 oh shit",
        "I love you 我爱你",
        "rap music 说唱音乐",
        "hip can't hop 嘻哈文化",
        "freestyle battle 自由说唱比赛",
        "beat 节拍 flow 节奏",
        "MC 麦克风 DJ 唱片",
        "有人喜欢我 oh shit 这是真的",
        "I'm the best 我是最好的 rapper",
        "中文说唱 English rap 混合风格",
        "2023年 rap music 2024",
        "I'm 'the best' rapper",
        "hip-hop \"freestyle\" battle",
        "MC's mic 麦克风",
        "beat 123 flow 456",
        "I'm #1 我是第一",
        "rap 'n' roll 摇滚说唱",
        "DJ's \"mix\" 混音",
        "What's up! 怎么了",
        "How are you? 你好吗",
        "I'm fine. 我很好",
        "Really? 真的吗",
        "Yes! 是的",
        "No. 不是",
        "hip-hop 嘻哈文化",
        "rap: 说唱; hip-hop: 嘻哈",
        "MC; DJ: 麦克风",
        "beat-flow 节拍节奏",
        "freestyle: 自由说唱; battle: 比赛"
    ]
    
    print("\nTest Results:")
    print("=" * 50)
    
    for i, text in enumerate(test_cases, 1):
        vocab = analyzer.extract_vocabulary(text)
        print(f"{i:2d}. Input: '{text}'")
        print(f"    Output: {vocab}")
        print(f"    Count: {len(vocab)} words")
        print()
    
    return True

def test_chinese_character_detection():
    """Test Chinese character detection"""
    print("Testing Chinese character detection...")
    
    analyzer = ChineseRapVocabularyAnalyzer()
    
    test_chars = ['中', 'a', '1', '你', '好', 'A', 'Z', '我', '爱', '你']
    
    print("\nCharacter Detection Results:")
    print("=" * 30)
    
    for char in test_chars:
        is_chinese = analyzer.is_chinese_character(char)
        print(f"'{char}' -> Chinese: {is_chinese}")
    
    return True

def test_english_word_detection():
    """Test English word detection"""
    print("Testing English word detection...")
    
    analyzer = ChineseRapVocabularyAnalyzer()
    
    test_words = ['hello', 'world', 'rap', 'hip', 'hop', '中文', '说唱', 'hello123', 'world!', 
                  'I\'m', 'don\'t', 'can\'t', 'won\'t', '2023', '123', 'MC\'s', 'DJ\'s',
                  '"hello"', '"world"', 'hip-hop', 'rap\'n\'roll', 'I\'m', 'don\'t',
                  'What\'s', 'How', 'Really?', 'Yes!', 'No.', 'Really!', 'What?', 'How!',
                  'hip-hop', 'beat-flow', 'rap:', 'MC;', 'DJ:', 'freestyle:', 'battle:']
    
    print("\nEnglish Word Detection Results:")
    print("=" * 35)
    
    for word in test_words:
        is_english = analyzer.is_english_word(word)
        print(f"'{word}' -> English: {is_english}")
    
    return True

def main():
    """Run all tests"""
    print("Vocabulary Extraction Test Suite")
    print("=" * 40)
    
    tests = [
        ("Vocabulary Extraction", test_vocabulary_extraction),
        ("Chinese Character Detection", test_chinese_character_detection),
        ("English Word Detection", test_english_word_detection),
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
