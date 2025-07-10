import json
from datasets import load_dataset
from pathlib import Path
import os


def load_stampy_dataset_to_dict(data_dir):
    """
    Load from local JSONL files if you've downloaded them manually.
    """
    merged_dict = {}
    seen_ids = set()
    
    # List of expected JSONL files based on the dataset structure
    jsonl_files = [
        'agentmodels.jsonl', 'agisf.jsonl', 'aisafety.info.jsonl',
        'alignmentforum.jsonl', 'arbital.jsonl', 'arxiv.jsonl',
        'blogs.jsonl', 'distill.jsonl', 'eaforum.jsonl',
        'lesswrong.jsonl', 'special_docs.jsonl', 'youtube.jsonl'
    ]
    
    data_path = Path(data_dir)
    
    for jsonl_file in jsonl_files:
        file_path = data_path / jsonl_file
        
        if file_path.exists():
            print(f"Processing {jsonl_file}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        item = json.loads(line.strip())
                        
                        # Check for valid item and avoid duplicates
                        if item and 'id' in item and item['id'] not in seen_ids:
                            # Filter out items with empty text
                            if item.get('text') and item['text'] not in [None, '', 'n/a']:
                                merged_dict[item['id']] = item
                                seen_ids.add(item['id'])
                                
                    except json.JSONDecodeError as e:
                        print(f"Error parsing line {line_num} in {jsonl_file}: {e}")
                        continue
        else:
            print(f"Warning: {jsonl_file} not found in {data_dir}")
    
    print(f"Loaded {len(merged_dict)} unique documents")
    return merged_dict

def explore_dataset_structure(merged_dict, num_samples=3):
    """
    Explore the structure of the merged dataset.
    """
    print("\n=== Dataset Structure ===")
    print(f"Total documents: {len(merged_dict)}")
    
    # Get some sample documents
    sample_ids = list(merged_dict.keys())[:num_samples]
    
    for i, doc_id in enumerate(sample_ids):
        print(f"\n--- Sample Document {i+1} ---")
        doc = merged_dict[doc_id]
        print(f"ID: {doc['id']}")
        print(f"Source: {doc.get('source', 'N/A')}")
        print(f"Title: {doc.get('title', 'N/A')}")
        print(f"Text length: {len(doc.get('text', ''))}")
        print(f"Authors: {doc.get('authors', [])}")
        print(f"Available keys: {list(doc.keys())}")
        
        # Show first 200 characters of text
        text = doc.get('text', '')
        if text:
            print(f"Text preview: {text[:200]}...")

def filter_by_source(merged_dict, source_types=None):
    """
    Filter the dataset by source type(s).
    
    Args:
        merged_dict: The full dataset dictionary
        source_types: List of source types to include (e.g., ['arxiv', 'alignmentforum'])
    
    Returns:
        Filtered dictionary
    """
    if not source_types:
        return merged_dict
    
    filtered_dict = {}
    for doc_id, doc in merged_dict.items():
        if doc.get('source') in source_types:
            filtered_dict[doc_id] = doc
    
    print(f"Filtered to {len(filtered_dict)} documents from sources: {source_types}")
    return filtered_dict

def save_merged_dataset(merged_dict, output_path):
    """
    Save the merged dataset to a JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged_dict, f, indent=2, ensure_ascii=False)
    print(f"Saved merged dataset to {output_path}")

# Main usage example
if __name__ == "__main__":
    # Load the dataset
    merged_dict = load_stampy_dataset_to_dict("./alignment-research-dataset/")
    
    # Explore the structure
    explore_dataset_structure(merged_dict)
    
    # Example: Filter by specific sources
    arxiv_docs = filter_by_source(merged_dict, ['arxiv'])
    alignment_forum_docs = filter_by_source(merged_dict, ['alignmentforum'])
    
    # Save if needed
    # save_merged_dataset(merged_dict, 'stampy_alignment_dataset.json')
    
    print("\n=== Usage Examples ===")
    print("# Access a specific document:")
    print("doc = merged_dict['some_document_id']")
    print("\n# Iterate through all documents:")
    print("for doc_id, doc_content in merged_dict.items():")
    print("    print(f'Processing {doc_id}: {doc_content[\"title\"]}')")
    print("\n# Get all document texts for processing:")
    print("all_texts = [doc['text'] for doc in merged_dict.values()]")
