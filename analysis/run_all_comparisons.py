import argparse
import os
import subprocess
import sys
import time

# (label, invocation, args) — run from the repo root. The frozen pipeline
# scripts live at the root and run as files; packaged scripts run with -m.
PIPELINE_SCRIPTS = [
    ("02_evaluate.py", ["02_evaluate.py"], []),
    ("04_regrade.py", ["04_regrade.py"], ["--force"]),
    ("03_analyze.py", ["03_analyze.py"], []),
    ("make_robustness_check", ["-m", "analysis.make_robustness_check"], []),
    ("make_probe_direction_atlas", ["-m", "analysis.make_probe_direction_atlas"], []),
    ("make_atlas_figure", ["-m", "plots.make_atlas_figure"], []),
]


def run_pipeline(model_id: str, limit: int = None, skip_eval: bool = False):
    print("=" * 60)
    print(f"RUNNING PIPELINE FOR MODEL: {model_id}")
    print("=" * 60)

    # Set the environment variable for config.py
    env = os.environ.copy()
    env["MODEL_ID"] = model_id

    for script, invocation, args in PIPELINE_SCRIPTS:
        if skip_eval and script == "02_evaluate.py":
            print(f"\n>>> Skipping evaluation step for {model_id}...")
            continue

        cmd = [sys.executable] + invocation + args
        if script == "02_evaluate.py" and limit is not None:
            cmd.extend(["--limit", str(limit)])

        print(f"\n>>> Running: {' '.join(cmd)}")
        t_start = time.perf_counter()
        res = subprocess.run(cmd, env=env)
        dt = time.perf_counter() - t_start

        if res.returncode != 0:
            print(f"ERROR: {script} failed with exit code {res.returncode}")
            sys.exit(res.returncode)

        print(f"Finished {script} in {dt:.1f}s")

    print("\n" + "=" * 60)
    print(f"PIPELINE COMPLETED FOR MODEL: {model_id}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default=None,
                        help="Specific HF model ID to run (e.g. unsloth/gemma-2-2b-it)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit evaluation questions (useful for smoke tests)")
    parser.add_argument("--skip-eval", action="store_true",
                        help="Skip evaluation step (if responses and activations are already cached)")
    args = parser.parse_args()

    models_to_run = []
    if args.model:
        models_to_run = [args.model]
    else:
        # Default models comparison set
        models_to_run = [
            "unsloth/gemma-2-2b-it",
            "unsloth/Llama-3.2-3B-Instruct",
        ]

    for model in models_to_run:
        run_pipeline(model, limit=args.limit, skip_eval=args.skip_eval)


if __name__ == "__main__":
    main()
