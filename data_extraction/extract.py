#!/usr/bin/env python3
"""
Script to extract all lines containing a search term from a text file.
Searches are case-insensitive by default.
Can blacklist image lines to avoid processing image data/references.
"""

# Configuration parameters
DEFAULT_OUTPUT_FILE = None  # If None, will generate based on input filename
DEFAULT_SEARCH_TERM = "Talent"
BLACKLIST_IMAGE_LINES = True  # Skip lines that appear to contain image data/references
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp', '.ico', '.tiff'}
IMAGE_KEYWORDS = {'base64', 'data:image', 'blob:', 'image/', 'img src', 'background-image'}

import os
import argparse
from pathlib import Path


def extract_card_lines(input_file, output_file=None, search_term=None, case_sensitive=False, show_line_numbers=True, blacklist_images=None):
    """
    Extract all lines containing the search term from the input file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output file (optional)
        search_term (str): Term to search for (optional, uses default if None)
        case_sensitive (bool): Whether to perform case-sensitive search
        show_line_numbers (bool): Whether to include line numbers in output
        blacklist_images (bool): Whether to skip lines that appear to contain image data
    """
    # Use default values if not provided
    if output_file is None:
        output_file = DEFAULT_OUTPUT_FILE
    if search_term is None:
        search_term = DEFAULT_SEARCH_TERM
    if blacklist_images is None:
        blacklist_images = BLACKLIST_IMAGE_LINES
    
    def is_image_line(line):
        """Check if a line appears to contain image data or references."""
        if not blacklist_images:
            return False
        
        line_lower = line.lower()
        
        # Check for image file extensions
        for ext in IMAGE_EXTENSIONS:
            if ext in line_lower:
                return True
        
        # Check for image-related keywords
        for keyword in IMAGE_KEYWORDS:
            if keyword in line_lower:
                return True
        
        # Check for very long lines that might be base64 encoded images
        if len(line.strip()) > 1000 and any(char in line for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='):
            # Likely base64 data
            return True
        
        return False
    
    try:
        # Check if input file exists
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found.")
            return False
        
        # Get file size
        file_size = os.path.getsize(input_file) / (1024 * 1024)  # Convert to MB
        print(f"Processing file: {input_file} ({file_size:.2f} MB)")
        
        # Prepare output
        if output_file is None:
            # Generate output filename
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_{search_term}_lines{input_path.suffix}"
        
        matched_lines = []
        skipped_image_lines = 0
        total_lines = 0
        
        # Read and process file
        print(f"Searching for lines containing '{search_term}'...")
        if blacklist_images:
            print("Image lines will be skipped.")
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
            for line_num, line in enumerate(infile, 1):
                total_lines = line_num
                
                # Skip image lines if blacklisting is enabled
                if is_image_line(line):
                    skipped_image_lines += 1
                    continue
                
                # Check if line contains search term
                if case_sensitive:
                    if search_term in line:
                        matched_lines.append((line_num, line.rstrip()))
                else:
                    if search_term.lower() in line.lower():
                        matched_lines.append((line_num, line.rstrip()))
                
                # Progress indicator for large files
                if line_num % 10000 == 0:
                    print(f"  Processed {line_num:,} lines...", end='\r')
        
        print(f"\nTotal lines processed: {total_lines:,}")
        print(f"Lines containing '{search_term}': {len(matched_lines):,}")
        if blacklist_images and skipped_image_lines > 0:
            print(f"Image lines skipped: {skipped_image_lines:,}")
        
        # Write results to output file
        if matched_lines:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                outfile.write(f"# Lines containing '{search_term}' from {input_file}\n")
                outfile.write(f"# Total matches: {len(matched_lines)}\n")
                if blacklist_images and skipped_image_lines > 0:
                    outfile.write(f"# Image lines skipped: {skipped_image_lines}\n")
                outfile.write("#" + "="*60 + "\n\n")
                
                for line_num, line in matched_lines:
                    if show_line_numbers:
                        outfile.write(f"[Line {line_num:6d}] {line}\n")
                    else:
                        outfile.write(f"{line}\n")
            
            print(f"\nResults saved to: {output_file}")
            
            # Show file size of output
            output_size = os.path.getsize(output_file) / 1024  # Convert to KB
            if output_size > 1024:
                print(f"Output file size: {output_size/1024:.2f} MB")
            else:
                print(f"Output file size: {output_size:.2f} KB")
                
            # Show first few matches as preview
            print("\nFirst 5 matches:")
            for i, (line_num, line) in enumerate(matched_lines[:5]):
                preview = line[:100] + "..." if len(line) > 100 else line
                print(f"  Line {line_num}: {preview}")
            
            if len(matched_lines) > 5:
                print(f"  ... and {len(matched_lines) - 5} more matches")
        else:
            print(f"\nNo lines containing '{search_term}' were found.")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Extract all lines containing a search term from a text file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input file"
    )
    parser.add_argument(
        "-o", "--output",
        help=f"Path to the output file (default: input_file_[search_term]_lines.ext)",
        default=None
    )
    parser.add_argument(
        "-t", "--search-term",
        help=f"Term to search for (default: '{DEFAULT_SEARCH_TERM}')",
        default=None
    )
    parser.add_argument(
        "-c", "--case-sensitive",
        action="store_true",
        help="Perform case-sensitive search (default: case-insensitive)"
    )
    parser.add_argument(
        "-n", "--no-line-numbers",
        action="store_true",
        help="Don't include line numbers in output"
    )
    parser.add_argument(
        "-s", "--stats-only",
        action="store_true",
        help="Only show statistics, don't create output file"
    )
    parser.add_argument(
        "--no-blacklist-images",
        action="store_true",
        help="Don't skip image lines (default: skip image lines)"
    )
    
    args = parser.parse_args()
    
    # Determine search term
    search_term = args.search_term if args.search_term is not None else DEFAULT_SEARCH_TERM
    
    # Determine blacklist setting
    blacklist_images = not args.no_blacklist_images
    
    if args.stats_only:
        # Just count matches without creating output file
        count = 0
        skipped = 0
        
        def is_image_line_stats(line):
            """Local version of image detection for stats mode."""
            if not blacklist_images:
                return False
            
            line_lower = line.lower()
            
            # Check for image file extensions
            for ext in IMAGE_EXTENSIONS:
                if ext in line_lower:
                    return True
            
            # Check for image-related keywords
            for keyword in IMAGE_KEYWORDS:
                if keyword in line_lower:
                    return True
            
            # Check for very long lines that might be base64 encoded images
            if len(line.strip()) > 1000 and any(char in line for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='):
                return True
            
            return False
        
        with open(args.input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                if is_image_line_stats(line):
                    skipped += 1
                    continue
                    
                if args.case_sensitive:
                    if search_term in line:
                        count += 1
                else:
                    if search_term.lower() in line.lower():
                        count += 1
        
        print(f"Total lines containing '{search_term}': {count}")
        if blacklist_images and skipped > 0:
            print(f"Image lines skipped: {skipped}")
    else:
        extract_card_lines(
            args.input_file,
            args.output,
            search_term,
            args.case_sensitive,
            not args.no_line_numbers,
            blacklist_images
        )


if __name__ == "__main__":
    main()