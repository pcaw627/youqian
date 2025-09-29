#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script showing vocabulary analysis functionality
"""

import json
from youqian import ChineseRapVocabularyAnalyzer

def demo_vocabulary_extraction():
    """Demo vocabulary extraction with sample lyrics"""
    print("🎵 Vocabulary Extraction Demo")
    print("=" * 40)
    
    analyzer = ChineseRapVocabularyAnalyzer()
    
    # Sample lyrics with mixed Chinese-English content
    sample_lyrics = [
        "有人喜欢我 oh shit 这是真的",
        "I love you 我爱你 rap music",
        "hip hop 嘻哈文化 freestyle battle",
        "beat 节拍 flow 节奏 MC 麦克风",
        "中文说唱 English rap 混合风格",
        "I'm the best 我是最好的 rapper",
        "DJ 唱片 music 音乐 culture 文化",
        "2023年 rap music 2024",
        "I'm 'the best' rapper 我是最好的",
        "hip-hop \"freestyle\" battle 嘻哈自由说唱",
        "MC's mic 麦克风 beat 123",
        "I'm #1 我是第一 rapper",
        "rap 'n' roll 摇滚说唱 DJ's mix",
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
    
    print("Sample lyrics and extracted vocabulary:")
    print("-" * 40)
    
    for i, lyrics in enumerate(sample_lyrics, 1):
        vocab = analyzer.extract_vocabulary(lyrics)
        print(f"{i}. Lyrics: '{lyrics}'")
        print(f"   Vocabulary: {vocab}")
        print(f"   Count: {len(vocab)} words")
        print()
    
    return True

def demo_json_output_format():
    """Demo the expected JSON output format"""
    print("📄 Expected JSON Output Format")
    print("=" * 40)
    
    # Sample output structure
    sample_output = {
        "analysis_info": {
            "total_songs_processed": 1000,
            "total_vocabulary_count": 50000,
            "years_analyzed": 5,
            "analysis_date": "2024-01-01T12:00:00",
            "top_words_per_year": 50
        },
        "yearly_rankings": {
            "2020": [
                {"word": "说唱", "frequency": 150},
                {"word": "rap", "frequency": 120},
                {"word": "音乐", "frequency": 100},
                {"word": "hip", "frequency": 80},
                {"word": "hop", "frequency": 75}
            ],
            "2021": [
                {"word": "freestyle", "frequency": 200},
                {"word": "battle", "frequency": 180},
                {"word": "beat", "frequency": 160},
                {"word": "flow", "frequency": 140},
                {"word": "MC", "frequency": 120}
            ]
        },
        "statistics": {
            "total_unique_words": 5000,
            "year_range": {
                "start": 2018,
                "end": 2023
            }
        }
    }
    
    print("Sample JSON structure:")
    print(json.dumps(sample_output, ensure_ascii=False, indent=2))
    
    return True

def main():
    """Run demo"""
    print("Chinese Rap/Hip-Hop Vocabulary Analysis Demo")
    print("=" * 50)
    
    demos = [
        ("Vocabulary Extraction", demo_vocabulary_extraction),
        ("JSON Output Format", demo_json_output_format),
    ]
    
    for demo_name, demo_func in demos:
        try:
            print(f"\n🎯 Running {demo_name}...")
            demo_func()
            print(f"✅ {demo_name} completed")
        except Exception as e:
            print(f"❌ {demo_name} failed: {str(e)}")
    
    print(f"\n🚀 To run the full analysis:")
    print(f"   python youqian.py")
    print(f"\n🧪 To test vocabulary extraction:")
    print(f"   python test_vocabulary_extraction.py")

if __name__ == "__main__":
    main()
