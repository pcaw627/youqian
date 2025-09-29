#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Song Filter Script

This script provides advanced filtering options for the song_lyrics.csv file,
including language filtering, year filtering, and keyword filtering.
"""

import pandas as pd
import os
import sys
import argparse
from datetime import datetime

def filter_songs(input_file, output_file, language=None, year_range=None, 
                 min_lyrics_length=None, keyword_filter=None):
    """
    Advanced song filtering function
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        language (str): Language filter (e.g., 'zh', 'en')
        year_range (tuple): Year range filter (start_year, end_year)
        min_lyrics_length (int): Minimum lyrics length
        keyword_filter (str): Keyword to search in lyrics
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)
        
        # Display basic info
        print(f"Total rows: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Apply filters
        filtered_df = df.copy()
        
        # Language filter
        if language:
            if 'language' in df.columns:
                filtered_df = filtered_df[filtered_df['language'] == language]
                print(f"After language filter ('{language}'): {len(filtered_df)} rows")
            else:
                print("Warning: 'language' column not found")
        
        # Year filter
        if year_range and 'year' in df.columns:
            start_year, end_year = year_range
            filtered_df = filtered_df[
                (filtered_df['year'] >= start_year) & 
                (filtered_df['year'] <= end_year)
            ]
            print(f"After year filter ({start_year}-{end_year}): {len(filtered_df)} rows")
        
        # Lyrics length filter
        if min_lyrics_length and 'lyrics' in df.columns:
            filtered_df = filtered_df[filtered_df['lyrics'].str.len() >= min_lyrics_length]
            print(f"After lyrics length filter (min {min_lyrics_length} chars): {len(filtered_df)} rows")
        
        # Keyword filter
        if keyword_filter and 'lyrics' in df.columns:
            filtered_df = filtered_df[filtered_df['lyrics'].str.contains(keyword_filter, case=False, na=False)]
            print(f"After keyword filter ('{keyword_filter}'): {len(filtered_df)} rows")
        
        if len(filtered_df) == 0:
            print("No songs match the filter criteria")
            return False
        
        # Save filtered data
        filtered_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Filtered songs saved to: {output_file}")
        
        # Display sample
        print("\nSample of filtered songs:")
        print(filtered_df.head())
        
        # Display statistics
        if 'year' in filtered_df.columns:
            print(f"\nYear distribution:")
            print(filtered_df['year'].value_counts().sort_index())
        
        if 'language' in filtered_df.columns:
            print(f"\nLanguage distribution:")
            print(filtered_df['language'].value_counts())
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return False
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Advanced Song Filter')
    parser.add_argument('--input', default='dataset/song_lyrics.csv', 
                       help='Input CSV file path')
    parser.add_argument('--output', default='filtered_songs.csv', 
                       help='Output CSV file path')
    parser.add_argument('--language', help='Filter by language (e.g., zh, en)')
    parser.add_argument('--year-start', type=int, help='Start year filter')
    parser.add_argument('--year-end', type=int, help='End year filter')
    parser.add_argument('--min-lyrics', type=int, help='Minimum lyrics length')
    parser.add_argument('--keyword', help='Keyword to search in lyrics')
    
    args = parser.parse_args()
    
    print("Advanced Song Filter Script")
    print("=" * 40)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return False
    
    # Prepare year range
    year_range = None
    if args.year_start and args.year_end:
        year_range = (args.year_start, args.year_end)
    elif args.year_start:
        year_range = (args.year_start, datetime.now().year)
    elif args.year_end:
        year_range = (1900, args.year_end)
    
    # Filter songs
    success = filter_songs(
        input_file=args.input,
        output_file=args.output,
        language=args.language,
        year_range=year_range,
        min_lyrics_length=args.min_lyrics,
        keyword_filter=args.keyword
    )
    
    if success:
        print(f"\n✅ Successfully filtered songs!")
        print(f"📁 Output file: {args.output}")
    else:
        print("\n❌ Failed to filter songs")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

