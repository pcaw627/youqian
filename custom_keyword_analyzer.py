#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Custom Keyword Frequency Analyzer

This script allows you to specify custom keywords and analyze their frequencies
over time from the Chinese rap/hip-hop dataset.
"""

import pandas as pd
import json
import re
import argparse
from collections import defaultdict, Counter
from datetime import datetime
import jieba
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CustomKeywordAnalyzer:
    def __init__(self):
        """Initialize the custom keyword analyzer"""
        # Initialize jieba for Chinese word segmentation
        jieba.initialize()
        
        # Store keyword frequencies by year
        self.keyword_frequencies = defaultdict(lambda: defaultdict(int))
        self.songs_processed = 0
        self.total_matches = 0
        
        # Statistics
        self.stats = {
            'total_songs': 0,
            'total_years': 0,
            'keywords_analyzed': 0
        }
    
    def is_chinese_character(self, char):
        """Check if a character is Chinese"""
        return '\u4e00' <= char <= '\u9fff'
    
    def is_english_word(self, word):
        """Check if a word is English"""
        return bool(re.match(r'^[a-zA-Z0-9\'"\.!?\-:;]+$', word))
    
    def extract_vocabulary(self, text):
        """Extract vocabulary from mixed Chinese-English text"""
        if not text or pd.isna(text):
            return []
        
        text = str(text).strip()
        if not text:
            return []
        
        vocabulary = []
        tokens = text.split()
        
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            
            has_chinese = any(self.is_chinese_character(char) for char in token)
            has_english = any((char.isalnum() or char in '\'".!?\-:;') and not self.is_chinese_character(char) for char in token)
            
            if has_chinese and has_english:
                chinese_part = ''.join([char for char in token if self.is_chinese_character(char)])
                english_part = ''.join([char for char in token if (char.isalnum() or char in '\'".!?\-:;') and not self.is_chinese_character(char)])
                
                if chinese_part:
                    chinese_words = jieba.lcut(chinese_part)
                    vocabulary.extend([word for word in chinese_words if len(word) >= 2])
                
                if english_part:
                    vocabulary.append(english_part.lower())
            
            elif has_chinese:
                chinese_words = jieba.lcut(token)
                vocabulary.extend([word for word in chinese_words if len(word) >= 2])
            
            elif has_english:
                cleaned_token = token.strip('\'".!?\-:;').lower()
                if len(cleaned_token) >= 2:
                    vocabulary.append(cleaned_token)
        
        # Filter vocabulary
        filtered_vocab = []
        for word in vocabulary:
            word = word.strip()
            if len(word) >= 2:
                if self.is_english_word(word) or self.is_chinese_character(word[0]):
                    filtered_vocab.append(word)
        
        return filtered_vocab
    
    def analyze_keywords(self, csv_file, keywords):
        """Analyze keyword frequencies over time"""
        try:
            logger.info(f"Reading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            
            logger.info(f"Total songs in dataset: {len(df)}")
            logger.info(f"Keywords to analyze: {keywords}")
            
            # Check required columns
            required_columns = ['year', 'lyrics']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing required columns: {missing_columns}")
                return False
            
            # Process each song
            for index, row in df.iterrows():
                try:
                    year = int(row['year']) if pd.notna(row['year']) else None
                    lyrics = row['lyrics'] if pd.notna(row['lyrics']) else ''
                    
                    if not year or not lyrics:
                        continue
                    
                    # Extract vocabulary from lyrics
                    vocab_words = self.extract_vocabulary(lyrics)
                    
                    if vocab_words:
                        # Count keyword frequencies
                        for keyword in keywords:
                            keyword_lower = keyword.lower()
                            matches = sum(1 for word in vocab_words if word.lower() == keyword_lower)
                            if matches > 0:
                                self.keyword_frequencies[keyword][year] += matches
                                self.total_matches += matches
                        
                        self.songs_processed += 1
                    
                    # Progress logging
                    if (index + 1) % 10000 == 0:
                        logger.info(f"Processed {index + 1} songs...")
                
                except Exception as e:
                    logger.warning(f"Error processing song {index}: {str(e)}")
                    continue
            
            self.stats['total_songs'] = len(df)
            self.stats['total_years'] = len(set(year for keyword_dict in self.keyword_frequencies.values() for year in keyword_dict.keys()))
            self.stats['keywords_analyzed'] = len(keywords)
            
            logger.info(f"Analysis complete!")
            logger.info(f"Processed {self.songs_processed} songs")
            logger.info(f"Total keyword matches: {self.total_matches}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"File not found: {csv_file}")
            return False
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return False
    
    def generate_frequency_data(self):
        """Generate frequency data for each keyword"""
        frequency_data = {}
        
        for keyword, year_frequencies in self.keyword_frequencies.items():
            frequency_tuples = [(year, freq) for year, freq in sorted(year_frequencies.items())]
            frequency_data[keyword] = frequency_tuples
        
        return frequency_data
    
    def save_results(self, output_file, keywords):
        """Save keyword frequency analysis results to JSON file"""
        try:
            frequency_data = self.generate_frequency_data()
            
            results = {
                'analysis_info': {
                    'total_songs_processed': self.songs_processed,
                    'total_keyword_matches': self.total_matches,
                    'keywords_analyzed': keywords,
                    'analysis_date': datetime.now().isoformat(),
                    'years_covered': self.stats['total_years']
                },
                'keyword_frequencies': frequency_data,
                'statistics': {
                    'total_unique_years': self.stats['total_years'],
                    'keywords_with_data': len([k for k, v in frequency_data.items() if v])
                }
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False
    
    def print_summary(self, keywords):
        """Print analysis summary"""
        print("\n" + "="*60)
        print("Custom Keyword Frequency Analysis Summary")
        print("="*60)
        
        print(f"Total songs processed: {self.songs_processed}")
        print(f"Total keyword matches: {self.total_matches}")
        print(f"Keywords analyzed: {len(keywords)}")
        
        frequency_data = self.generate_frequency_data()
        
        for keyword in keywords:
            if keyword in frequency_data and frequency_data[keyword]:
                freq_tuples = frequency_data[keyword]
                print(f"\n{keyword} - Frequency by year:")
                print("-" * 40)
                for year, freq in freq_tuples:
                    print(f"  {year}: {freq} occurrences")
                
                total_freq = sum(freq for _, freq in freq_tuples)
                print(f"  Total: {total_freq} occurrences")
            else:
                print(f"\n{keyword} - No occurrences found")


def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Custom Keyword Frequency Analyzer')
    parser.add_argument('--input', default='chinese_raphiphop.csv', 
                       help='Input CSV file path')
    parser.add_argument('--output', default='rap_keyword_freq.json', 
                       help='Output JSON file path')
    parser.add_argument('--keywords', nargs='+', 
                       default=['家', '钱', '爱情', '青春', '梦想'],
                       help='Keywords to analyze (space-separated)')
    
    args = parser.parse_args()
    
    print("Custom Keyword Frequency Analyzer")
    print("="*50)
    
    # Create analyzer
    analyzer = CustomKeywordAnalyzer()
    
    # Analyze keywords
    success = analyzer.analyze_keywords(args.input, args.keywords)
    
    if not success:
        print("❌ Failed to analyze keywords")
        return False
    
    # Save results
    analyzer.save_results(args.output, args.keywords)
    
    # Print summary
    analyzer.print_summary(args.keywords)
    
    print(f"\n✅ Analysis complete! Results saved to: {args.output}")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

