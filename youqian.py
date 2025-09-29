#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Rap/Hip-Hop Vocabulary Analysis System

This system analyzes Chinese rap/hip-hop songs from CSV data, extracts vocabulary
from lyrics (handling both Chinese characters and English words), and creates
yearly frequency rankings.
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

class ChineseRapVocabularyAnalyzer:
    def __init__(self):
        """Initialize the vocabulary analyzer"""
        # Initialize jieba for Chinese word segmentation
        jieba.initialize()
        
        # Store vocabulary data by year
        self.vocab_by_year = defaultdict(Counter)
        self.songs_processed = 0
        self.total_vocab_count = 0
        
        # Statistics
        self.stats = {
            'total_songs': 0,
            'total_years': 0,
            'vocab_processing_time': 0
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
        Check if a word is English (contains English letters, numbers, quotes, and punctuation)
        
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
    
    def analyze_csv_file(self, csv_file):
        """
        Analyze the CSV file and extract vocabulary by year
        
        Args:
            csv_file (str): Path to the CSV file
        """
        try:
            logger.info(f"Reading CSV file: {csv_file}")
            df = pd.read_csv(csv_file)
            
            logger.info(f"Total songs in dataset: {len(df)}")
            logger.info(f"Columns: {list(df.columns)}")
            
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
                        # Count vocabulary by year
                        for word in vocab_words:
                            self.vocab_by_year[year][word] += 1
                            self.total_vocab_count += 1
                        
                        self.songs_processed += 1
                    
                    # Progress logging
                    if (index + 1) % 10000 == 0:
                        logger.info(f"Processed {index + 1} songs...")
                
                except Exception as e:
                    logger.warning(f"Error processing song {index}: {str(e)}")
                    continue
            
            self.stats['total_songs'] = len(df)
            self.stats['total_years'] = len(self.vocab_by_year)
            
            logger.info(f"Analysis complete!")
            logger.info(f"Processed {self.songs_processed} songs")
            logger.info(f"Total vocabulary count: {self.total_vocab_count}")
            logger.info(f"Years covered: {len(self.vocab_by_year)}")
            
            return True
            
        except FileNotFoundError:
            logger.error(f"File not found: {csv_file}")
            return False
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            return False
    
    def generate_yearly_rankings(self, top_n=50):
        """
        Generate yearly vocabulary rankings
        
        Args:
            top_n (int): Number of top words to include per year
            
        Returns:
            dict: Yearly vocabulary rankings
        """
        rankings = {}
        
        for year in sorted(self.vocab_by_year.keys()):
            # Get top N words for this year
            top_words = self.vocab_by_year[year].most_common(top_n)
            rankings[year] = top_words
        
        return rankings
    
    def save_results(self, output_file='rap_vocabulary_analysis.json', top_n=50):
        """
        Save analysis results to JSON file
        
        Args:
            output_file (str): Output JSON file path
            top_n (int): Number of top words per year
        """
        try:
            # Generate rankings
            rankings = self.generate_yearly_rankings(top_n)
            
            # Prepare results
            results = {
                'analysis_info': {
                    'total_songs_processed': self.songs_processed,
                    'total_vocabulary_count': self.total_vocab_count,
                    'years_analyzed': len(self.vocab_by_year),
                    'analysis_date': datetime.now().isoformat(),
                    'top_words_per_year': top_n
                },
                'yearly_rankings': {},
                'statistics': {
                    'total_unique_words': sum(len(counter) for counter in self.vocab_by_year.values()),
                    'year_range': {
                        'start': min(self.vocab_by_year.keys()) if self.vocab_by_year else None,
                        'end': max(self.vocab_by_year.keys()) if self.vocab_by_year else None
                    }
                }
            }
            
            # Convert rankings to the required format
            for year, word_counts in rankings.items():
                results['yearly_rankings'][str(year)] = [
                    {'word': word, 'frequency': count} 
                    for word, count in word_counts
                ]
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Results saved to: {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
            return False
    
    def print_summary(self, top_n=20):
        """
        Print analysis summary
        
        Args:
            top_n (int): Number of top words to display per year
        """
        print("\n" + "="*60)
        print("Chinese Rap/Hip-Hop Vocabulary Analysis Summary")
        print("="*60)
        
        print(f"Total songs processed: {self.songs_processed}")
        print(f"Total vocabulary count: {self.total_vocab_count}")
        print(f"Years analyzed: {len(self.vocab_by_year)}")
        
        if self.vocab_by_year:
            print(f"Year range: {min(self.vocab_by_year.keys())} - {max(self.vocab_by_year.keys())}")
        
        # Show top words for each year
        for year in sorted(self.vocab_by_year.keys()):
            print(f"\n{year} - Top {top_n} vocabulary:")
            print("-" * 40)
            
            top_words = self.vocab_by_year[year].most_common(top_n)
            for i, (word, count) in enumerate(top_words, 1):
                print(f"{i:2d}. {word:<15} (frequency: {count})")
    
    def get_vocabulary_stats(self):
        """
        Get vocabulary statistics
        
        Returns:
            dict: Vocabulary statistics
        """
        stats = {
            'total_years': len(self.vocab_by_year),
            'total_unique_words': sum(len(counter) for counter in self.vocab_by_year.values()),
            'total_word_occurrences': sum(sum(counter.values()) for counter in self.vocab_by_year.values()),
            'songs_processed': self.songs_processed
        }
        
        if self.vocab_by_year:
            stats['year_range'] = {
                'start': min(self.vocab_by_year.keys()),
                'end': max(self.vocab_by_year.keys())
            }
        
        return stats


def main():
    """Main function"""
    print("Chinese Rap/Hip-Hop Vocabulary Analysis System")
    print("="*60)
    
    # Create analyzer
    analyzer = ChineseRapVocabularyAnalyzer()
    
    # Analyze the CSV file
    csv_file = "chinese_raphiphop.csv"
    
    try:
        # Analyze the dataset
        success = analyzer.analyze_csv_file(csv_file)
        
        if not success:
            print("❌ Failed to analyze the CSV file")
            return False
        
        # Generate and save results
        output_file = "rap_vocabulary_analysis.json"
        analyzer.save_results(output_file, top_n=50)
        
        # Print summary
        analyzer.print_summary(top_n=20)
        
        # Display statistics
        stats = analyzer.get_vocabulary_stats()
        print(f"\n📊 Analysis Statistics:")
        print(f"   Years analyzed: {stats['total_years']}")
        print(f"   Unique words: {stats['total_unique_words']:,}")
        print(f"   Total word occurrences: {stats['total_word_occurrences']:,}")
        print(f"   Songs processed: {stats['songs_processed']:,}")
        
        if 'year_range' in stats:
            print(f"   Year range: {stats['year_range']['start']} - {stats['year_range']['end']}")
        
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