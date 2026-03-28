from huggingface_hub import HfApi, create_repo
import os

# You need to set your HF token first:
# Run: huggingface-cli login
# Or set: HF_TOKEN environment variable

REPO_ID = input("Enter your HF Space name (e.g. your-username/sql-practice): ").strip()

api = HfApi()

# Create the Space (static SDK)
try:
    create_repo(repo_id=REPO_ID, repo_type="space", space_sdk="static", exist_ok=True)
    print(f"✅ Space created: https://huggingface.co/spaces/{REPO_ID}")
except Exception as e:
    print(f"Space may already exist or error: {e}")

# Upload all files
deploy_dir = os.path.dirname(os.path.abspath(__file__))
files = ["README.md", "index.html", "app.js", "questions.js"]

for f in files:
    filepath = os.path.join(deploy_dir, f)
    if os.path.exists(filepath):
        api.upload_file(
            path_or_fileobj=filepath,
            path_in_repo=f,
            repo_id=REPO_ID,
            repo_type="space",
        )
        print(f"  ✅ Uploaded {f}")

print(f"\n🚀 Live at: https://huggingface.co/spaces/{REPO_ID}")
