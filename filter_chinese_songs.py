#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese Song Filter Script

This script reads song_lyrics.csv, filters for Chinese songs (language="zh"),
and saves the results to a separate CSV file.
"""

import pandas as pd
import os
import sys

def filter_chinese_songs(input_file, output_file):
    """
    Filter CSV file for Chinese songs and save to new file
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)
        
        # Display basic info about the dataset
        print(f"Total rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Check if 'language' column exists
        if 'language' not in df.columns:
            print("Error: 'language' column not found in the CSV file")
            print("Available columns:", list(df.columns))
            return False
        
        # Display language distribution
        print("\nLanguage distribution:")
        language_counts = df['language'].value_counts()
        print(language_counts)
        
        # Filter for Chinese songs (language = "zh")
        chinese_songs = df[df['language'] == 'zh']
        
        print(f"\nChinese songs found: {len(chinese_songs)}")
        
        if len(chinese_songs) == 0:
            print("No Chinese songs found in the dataset")
            return False
        
        # Save filtered data to new CSV
        chinese_songs.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Chinese songs saved to: {output_file}")
        
        # Display sample of filtered data
        print("\nSample of Chinese songs:")
        print(chinese_songs.head())
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return False
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function"""
    print("Chinese Song Filter Script")
    print("=" * 40)
    
    # Define file paths
    input_file = "dataset/song_lyrics.csv"
    output_file = "chinese_songs.csv"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        print("Please make sure the file exists in the dataset folder")
        return False
    
    # Filter Chinese songs
    success = filter_chinese_songs(input_file, output_file)
    
    if success:
        print(f"\n✅ Successfully filtered Chinese songs!")
        print(f"📁 Output file: {output_file}")
        
        # Display file size info
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            print(f"📊 Output file size: {file_size:,} bytes")
    else:
        print("\n❌ Failed to filter Chinese songs")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

