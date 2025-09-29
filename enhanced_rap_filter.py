#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Chinese Rap & Hip-Hop Song Filter Script

This script provides advanced filtering for rap and hip-hop songs with
multiple detection methods and additional filtering options.
"""

import pandas as pd
import os
import sys
import re
import argparse

def detect_rap_hiphop(df, method='comprehensive'):
    """
    Detect rap and hip-hop songs using different methods
    
    Args:
        df (DataFrame): Input dataframe
        method (str): Detection method ('tag', 'lyrics', 'comprehensive')
    
    Returns:
        DataFrame: Filtered dataframe with rap/hip-hop songs
    """
    
    if method == 'tag':
        # Method 1: Filter by tag column only
        rap_hiphop_pattern = r'(rap|hip.?hop|hiphop|嘻哈|说唱|饶舌)'
        return df[df['tag'].str.contains(rap_hiphop_pattern, case=False, na=False)]
    
    elif method == 'lyrics':
        # Method 2: Filter by lyrics content (look for rap-related keywords)
        rap_keywords = [
            'rap', 'hip hop', 'hiphop', '嘻哈', '说唱', '饶舌', 'freestyle',
            'beat', 'rhyme', 'flow', 'mic', 'mc', 'dj', 'battle'
        ]
        
        # Create pattern for lyrics search
        lyrics_pattern = '|'.join(rap_keywords)
        return df[df['lyrics'].str.contains(lyrics_pattern, case=False, na=False)]
    
    elif method == 'comprehensive':
        # Method 3: Combine tag and lyrics filtering
        # First filter by tag
        tag_pattern = r'(rap|hip.?hop|hiphop|嘻哈|说唱|饶舌)'
        tag_filtered = df[df['tag'].str.contains(tag_pattern, case=False, na=False)]
        
        # Then filter by lyrics
        lyrics_keywords = [
            'rap', 'hip hop', 'hiphop', '嘻哈', '说唱', '饶舌', 'freestyle',
            'beat', 'rhyme', 'flow', 'mic', 'mc', 'dj', 'battle'
        ]
        lyrics_pattern = '|'.join(lyrics_keywords)
        lyrics_filtered = df[df['lyrics'].str.contains(lyrics_pattern, case=False, na=False)]
        
        # Combine both results
        combined = pd.concat([tag_filtered, lyrics_filtered]).drop_duplicates()
        return combined
    
    else:
        raise ValueError("Method must be 'tag', 'lyrics', or 'comprehensive'")

def filter_rap_hiphop_advanced(input_file, output_file, method='comprehensive', 
                               year_range=None, min_lyrics_length=None,
                               artist_filter=None):
    """
    Advanced rap and hip-hop song filtering
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
        method (str): Detection method
        year_range (tuple): Year range filter
        min_lyrics_length (int): Minimum lyrics length
        artist_filter (str): Artist name filter
    """
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file}")
        df = pd.read_csv(input_file)
        
        # Display basic info
        print(f"Total Chinese songs: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        
        # Check required columns
        required_columns = ['tag', 'lyrics']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"Error: Missing columns: {missing_columns}")
            return False
        
        # Display tag distribution
        print(f"\nTag distribution (top 20):")
        tag_counts = df['tag'].value_counts()
        print(tag_counts.head(20))
        
        # Detect rap and hip-hop songs
        print(f"\nDetecting rap/hip-hop songs using method: {method}")
        rap_hiphop_songs = detect_rap_hiphop(df, method)
        
        print(f"Rap/Hip-Hop songs found: {len(rap_hiphop_songs)}")
        
        if len(rap_hiphop_songs) == 0:
            print("No rap/hip-hop songs found")
            return False
        
        # Apply additional filters
        filtered_songs = rap_hiphop_songs.copy()
        
        # Year filter
        if year_range and 'year' in filtered_songs.columns:
            start_year, end_year = year_range
            filtered_songs = filtered_songs[
                (filtered_songs['year'] >= start_year) & 
                (filtered_songs['year'] <= end_year)
            ]
            print(f"After year filter ({start_year}-{end_year}): {len(filtered_songs)} songs")
        
        # Lyrics length filter
        if min_lyrics_length and 'lyrics' in filtered_songs.columns:
            filtered_songs = filtered_songs[filtered_songs['lyrics'].str.len() >= min_lyrics_length]
            print(f"After lyrics length filter (min {min_lyrics_length} chars): {len(filtered_songs)} songs")
        
        # Artist filter
        if artist_filter and 'artist' in filtered_songs.columns:
            filtered_songs = filtered_songs[filtered_songs['artist'].str.contains(artist_filter, case=False, na=False)]
            print(f"After artist filter ('{artist_filter}'): {len(filtered_songs)} songs")
        
        if len(filtered_songs) == 0:
            print("No songs match all filter criteria")
            return False
        
        # Display unique tags found
        print(f"\nRap/Hip-Hop tags found:")
        unique_tags = filtered_songs['tag'].value_counts()
        print(unique_tags)
        
        # Save filtered data
        filtered_songs.to_csv(output_file, index=False, encoding='utf-8')
        print(f"\nFiltered songs saved to: {output_file}")
        
        # Display sample
        print(f"\nSample of filtered songs:")
        sample_data = filtered_songs[['title', 'artist', 'year', 'tag']].head(10)
        print(sample_data.to_string(index=False))
        
        # Display statistics
        if 'year' in filtered_songs.columns:
            print(f"\nYear distribution:")
            year_dist = filtered_songs['year'].value_counts().sort_index()
            print(year_dist)
        
        if 'artist' in filtered_songs.columns:
            print(f"\nTop 10 artists:")
            artist_dist = filtered_songs['artist'].value_counts().head(10)
            print(artist_dist)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return False
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return False

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Enhanced Chinese Rap & Hip-Hop Filter')
    parser.add_argument('--input', default='chinese_songs.csv', 
                       help='Input CSV file path')
    parser.add_argument('--output', default='chinese_raphiphop.csv', 
                       help='Output CSV file path')
    parser.add_argument('--method', choices=['tag', 'lyrics', 'comprehensive'], 
                       default='comprehensive', help='Detection method')
    parser.add_argument('--year-start', type=int, help='Start year filter')
    parser.add_argument('--year-end', type=int, help='End year filter')
    parser.add_argument('--min-lyrics', type=int, help='Minimum lyrics length')
    parser.add_argument('--artist', help='Artist name filter')
    
    args = parser.parse_args()
    
    print("Enhanced Chinese Rap & Hip-Hop Song Filter Script")
    print("=" * 60)
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return False
    
    # Prepare year range
    year_range = None
    if args.year_start and args.year_end:
        year_range = (args.year_start, args.year_end)
    elif args.year_start:
        year_range = (args.year_start, 2024)
    elif args.year_end:
        year_range = (1990, args.year_end)
    
    # Filter songs
    success = filter_rap_hiphop_advanced(
        input_file=args.input,
        output_file=args.output,
        method=args.method,
        year_range=year_range,
        min_lyrics_length=args.min_lyrics,
        artist_filter=args.artist
    )
    
    if success:
        print(f"\n✅ Successfully filtered rap/hip-hop songs!")
        print(f"📁 Output file: {args.output}")
        
        # Display file info
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"📊 Output file size: {file_size:,} bytes")
    else:
        print("\n❌ Failed to filter rap/hip-hop songs")
        return False
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

