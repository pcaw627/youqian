#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Rap/Hip-Hop Keyword Frequency Analyzer

This script analyzes the frequency of specific keywords over time from the
Chinese rap/hip-hop dataset and saves the results as JSON.
"""

import pandas as pd
import json
import re
from collections import defaultdict, Counter
from datetime import datetime
import jieba
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KeywordFrequencyAnalyzer:
    def __init__(self):
        """Initialize the keyword frequency analyzer"""
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
        """
        Check if a character is Chinese
        
        Args:
            char (str): Single character to check
            
        Returns:
            bool: True if Chinese character
        """
        return '\u4e00' <= char <= '\u9fff'
    
    def is_english_word(self, word):
        """
        Check if a word is English (contains English letters, numbers, and punctuation)
        
        Args:
            word (str): Word to check
            
        Returns:
            bool: True if English word
        """
        return bool(re.match(r'^[a-zA-Z0-9\'"\.!?\-:;]+$', word))
    
    def extract_vocabulary(self, text):
        """
        Extract vocabulary from mixed Chinese-English text
        
        Args:
            text (str): Input text with mixed languages
            
        Returns:
            list: List of vocabulary words
        """
        if not text or pd.isna(text):
            return []
        
        # Clean text - remove extra whitespace and special characters
        text = str(text).strip()
        if not text:
            return []
        
        vocabulary = []
        
        # Split text into tokens (space-separated)
        tokens = text.split()
        
        for token in tokens:
            # Clean token
            token = token.strip()
            if not token:
                continue
            
            # Check if token contains Chinese characters
            has_chinese = any(self.is_chinese_character(char) for char in token)
            has_english = any((char.isalnum() or char in '\'".!?\-:;') and not self.is_chinese_character(char) for char in token)
            
            if has_chinese and has_english:
                # Mixed token - split by character type
                chinese_part = ''.join([char for char in token if self.is_chinese_character(char)])
                english_part = ''.join([char for char in token if (char.isalnum() or char in '\'".!?\-:;') and not self.is_chinese_character(char)])
                
                # Process Chinese part with jieba
                if chinese_part:
                    chinese_words = jieba.lcut(chinese_part)
                    vocabulary.extend([word for word in chinese_words if len(word) >= 2])
                
                # Process English part (including numbers)
                if english_part:
                    vocabulary.append(english_part.lower())
            
            elif has_chinese:
                # Pure Chinese token - use jieba segmentation
                chinese_words = jieba.lcut(token)
                vocabulary.extend([word for word in chinese_words if len(word) >= 2])
            
            elif has_english:
                # Pure English token - clean and process
                cleaned_token = token.strip('\'".!?\-:;').lower()
                if len(cleaned_token) >= 2:
                    vocabulary.append(cleaned_token)
        
        # Filter vocabulary
        filtered_vocab = []
        for word in vocabulary:
            word = word.strip()
            if len(word) >= 2:  # Minimum length
                # Additional filtering
                if self.is_english_word(word) or self.is_chinese_character(word[0]):
                    filtered_vocab.append(word)
        
        return filtered_vocab
    
    def analyze_keywords(self, csv_file, keywords):
        """
        Analyze keyword frequencies over time
        
        Args:
            csv_file (str): Path to the CSV file
            keywords (list): List of keywords to analyze
            
        Returns:
            bool: Success status
        """
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
            
            # Display year distribution
            year_counts = df['year'].value_counts().sort_index()
            logger.info(f"Year distribution: {dict(year_counts.head(10))}")
            
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
                            # Count exact matches (case-insensitive)
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
            logger.info(f"Keywords analyzed: {len(keywords)}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"File not found: {csv_file}")
            return False
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return False
    
    def generate_frequency_data(self):
        """
        Generate frequency data for each keyword
        
        Returns:
            dict: Keyword frequency data by year
        """
        frequency_data = {}
        
        for keyword, year_frequencies in self.keyword_frequencies.items():
            # Convert to list of (year, frequency) tuples
            frequency_tuples = [(year, freq) for year, freq in sorted(year_frequencies.items())]
            frequency_data[keyword] = frequency_tuples
        
        return frequency_data
    
    def save_results(self, output_file='rap_keyword_freq.json', keywords=None):
        """
        Save keyword frequency analysis results to JSON file
        
        Args:
            output_file (str): Output JSON file path
            keywords (list): List of keywords analyzed
        """
        try:
            # Generate frequency data
            frequency_data = self.generate_frequency_data()
            
            # Prepare results
            results = {
                'analysis_info': {
                    'total_songs_processed': self.songs_processed,
                    'total_keyword_matches': self.total_matches,
                    'keywords_analyzed': keywords or list(frequency_data.keys()),
                    'analysis_date': datetime.now().isoformat(),
                    'years_covered': self.stats['total_years']
                },
                'keyword_frequencies': frequency_data,
                'statistics': {
                    'total_unique_years': self.stats['total_years'],
                    'keywords_with_data': len([k for k, v in frequency_data.items() if v])
                }
            }
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False
    
    def print_summary(self, keywords=None):
        """
        Print analysis summary
        
        Args:
            keywords (list): List of keywords to summarize
        """
        print("\n" + "="*60)
        print("Chinese Rap/Hip-Hop Keyword Frequency Analysis Summary")
        print("="*60)
        
        print(f"Total songs processed: {self.songs_processed}")
        print(f"Total keyword matches: {self.total_matches}")
        print(f"Keywords analyzed: {len(keywords) if keywords else 'All'}")
        
        # Show frequency data for each keyword
        frequency_data = self.generate_frequency_data()
        
        for keyword in (keywords or list(frequency_data.keys())):
            if keyword in frequency_data:
                freq_tuples = frequency_data[keyword]
                if freq_tuples:
                    print(f"\n{keyword} - Frequency by year:")
                    print("-" * 40)
                    for year, freq in freq_tuples:
                        print(f"  {year}: {freq} occurrences")
                    
                    # Show total frequency
                    total_freq = sum(freq for _, freq in freq_tuples)
                    print(f"  Total: {total_freq} occurrences")
                else:
                    print(f"\n{keyword} - No occurrences found")
            else:
                print(f"\n{keyword} - No data available")
    
    def get_keyword_stats(self):
        """
        Get keyword statistics
        
        Returns:
            dict: Keyword statistics
        """
        frequency_data = self.generate_frequency_data()
        
        stats = {
            'total_keywords': len(frequency_data),
            'keywords_with_data': len([k for k, v in frequency_data.items() if v]),
            'total_matches': self.total_matches,
            'songs_processed': self.songs_processed
        }
        
        # Add per-keyword statistics
        keyword_stats = {}
        for keyword, freq_tuples in frequency_data.items():
            if freq_tuples:
                total_freq = sum(freq for _, freq in freq_tuples)
                years_active = len(freq_tuples)
                avg_freq_per_year = total_freq / years_active if years_active > 0 else 0
                
                keyword_stats[keyword] = {
                    'total_frequency': total_freq,
                    'years_active': years_active,
                    'average_per_year': round(avg_freq_per_year, 2),
                    'year_range': (min(year for year, _ in freq_tuples), max(year for year, _ in freq_tuples)) if freq_tuples else None
                }
        
        stats['keyword_details'] = keyword_stats
        return stats


def main():
    """Main function"""
    print("Chinese Rap/Hip-Hop Keyword Frequency Analyzer")
    print("="*60)
    
    # Create analyzer
    analyzer = KeywordFrequencyAnalyzer()
    
    # Define keywords to analyze
    keywords = ["家", "钱", "爱情", "青春", "梦想", "工作", "生活", "未来", "朋友", "音乐", "生病", "外部"]
    
    # Analyze the dataset
    csv_file = "chinese_raphiphop.csv"
    
    try:
        # Analyze keywords
        success = analyzer.analyze_keywords(csv_file, keywords)
        
        if not success:
            print("❌ Failed to analyze keywords")
            return False
        
        # Generate and save results
        output_file = "rap_keyword_freq.json"
        analyzer.save_results(output_file, keywords)
        
        # Print summary
        analyzer.print_summary(keywords)
        
        # Display statistics
        stats = analyzer.get_keyword_stats()
        print(f"\n📊 Analysis Statistics:")
        print(f"   Keywords analyzed: {stats['total_keywords']}")
        print(f"   Keywords with data: {stats['keywords_with_data']}")
        print(f"   Total matches: {stats['total_matches']:,}")
        print(f"   Songs processed: {stats['songs_processed']:,}")
        
        print(f"\n✅ Analysis complete! Results saved to: {output_file}")
        return True
        
    except KeyboardInterrupt:
        print("\nUser interrupted the program")
        return False
    except Exception as e:
        logger.error(f"Program error: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

