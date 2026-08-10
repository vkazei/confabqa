import shutil
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent
DATA_DIR = PROJECT_DIR / "data"

# Qwen3 target dir name is 'qwen3_1_7b'
MODEL_SUBDIR = "qwen3_1_7b"

resp_src = DATA_DIR / "responses"
resp_dst = DATA_DIR / "responses" / MODEL_SUBDIR
act_src = DATA_DIR / "activations"
act_dst = DATA_DIR / "activations" / MODEL_SUBDIR
fig_src = PROJECT_DIR / "figures"
fig_dst = PROJECT_DIR / "figures" / MODEL_SUBDIR

print("Creating directories...")
resp_dst.mkdir(parents=True, exist_ok=True)
act_dst.mkdir(parents=True, exist_ok=True)
fig_dst.mkdir(parents=True, exist_ok=True)

# 1. Move responses (*.json files from resp_src to resp_dst)
print("Moving responses...")
for f in resp_src.glob("*.json"):
    shutil.move(str(f), str(resp_dst / f.name))

# 2. Move activations (*.pt files from act_src to act_dst)
print("Moving activations...")
for f in act_src.glob("*.pt"):
    shutil.move(str(f), str(act_dst / f.name))

# 3. Move summary.json -> data/qwen3_1_7b_summary.json
summary_src = DATA_DIR / "summary.json"
summary_dst = DATA_DIR / f"{MODEL_SUBDIR}_summary.json"
if summary_src.exists():
    print(f"Moving summary.json to {summary_dst.name}...")
    shutil.move(str(summary_src), str(summary_dst))

# 4. Move figures (excluding 08_qwen_architecture.png and 09_probe_pipeline.png)
print("Moving figures...")
for f in fig_src.glob("*.*"):
    if f.name not in ("08_qwen_architecture.png", "09_probe_pipeline.png"):
        shutil.move(str(f), str(fig_dst / f.name))

print("Migration completed successfully!")
