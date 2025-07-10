from huggingface_hub import snapshot_download
import os

# Download entire repository
repo_path = snapshot_download(
    repo_id="StampyAI/alignment-research-dataset",
    local_dir="./alignment-research-dataset",
    repo_type="dataset"
)

print(f"Dataset downloaded to: {repo_path}")
