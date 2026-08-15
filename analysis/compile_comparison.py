import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
FIGURES_DIR = PROJECT_DIR / "figures"
FIGURES_DIR.mkdir(exist_ok=True)

MODEL_NAMES = {
    "qwen3_1_7b": "Qwen3-1.7B",
    "gemma_2_2b": "Gemma 2 2B",
    "llama_3_2_3b": "Llama 3.2 3B",
}


def load_summaries():
    summaries = {}
    for key, label in MODEL_NAMES.items():
        path = DATA_DIR / f"{key}_summary.json"
        if path.exists():
            with open(path) as f:
                summaries[key] = json.load(f)
            print(f"Loaded summary for {label}")
        else:
            print(f"Summary not found for {label} ({path.name})")
    return summaries


def build_markdown_table(summaries):
    if not summaries:
        return "No summaries loaded."

    lines = []
    lines.append("# Cross-Model Comparison Summary\n")
    lines.append("| Metric / Probe | " + " | ".join(MODEL_NAMES[k] for k in summaries) + " |")
    lines.append("|:---| " + " | ".join("---:" for _ in summaries) + " |")

    # 1. Dataset stats
    lines.append("| **Dataset Size (n)** | " + " | ".join(str(summaries[k]["n"]) for k in summaries) + " |")
    lines.append("| **Overall Accuracy** | " + " | ".join(f"{summaries[k]['judge_counts']['correct'] / summaries[k]['n']:.1%}" for k in summaries) + " |")
    lines.append("| **Pre-cutoff Accuracy** | " + " | ".join(f"{summaries[k]['by_cutoff']['pre']['accuracy']:.1%}" for k in summaries) + " |")
    lines.append("| **Post-cutoff Accuracy** | " + " | ".join(f"{summaries[k]['by_cutoff']['post']['accuracy']:.1%}" for k in summaries) + " |")

    # 2. Refusal stats
    refusal_rates = []
    for k in summaries:
        c = summaries[k].get("cutoff_x_judge", {})
        ref = c.get("post__refusal", 0)
        wrg = c.get("post__wrong", 0)
        total_wrong = ref + wrg
        rate = ref / total_wrong if total_wrong else 0.0
        refusal_rates.append(f"{rate:.1%} ({ref}/{total_wrong})")
    lines.append("| **Refusal Rate on Post-cutoff Failures** | " + " | ".join(refusal_rates) + " |")

    lines.append("| " + " | ".join(" " for _ in range(len(summaries) + 1)) + " |")
    lines.append("| *PROBE ACCURACIES (PEAK % [PEAK LAYER] vs BASELINE)* | " + " | ".join(" " for _ in summaries) + " |")

    # 3. Probes
    probe_targets = [
        ("correct", "Correctness (all items)"),
        ("cutoff", "Cutoff (all items)"),
        ("refusal_vs_wrong", "Refusal-vs-Wrong (subset)"),
        ("correct_within_pre", "Correct within Pre-cutoff"),
        ("correct_within_obscure", "Correct within Obscure"),
    ]

    for target_key, target_label in probe_targets:
        row_vals = []
        for k in summaries:
            p = summaries[k]["probes"].get(target_key, {})
            if p:
                peak_acc = p["peak_acc"]
                peak_layer = p["peak_layer"]
                base = p["baseline"]
                margin = p["margin_pp"]
                row_vals.append(f"**{peak_acc:.1%}** [L{peak_layer}]<br>(base {base:.1%}, +{margin:.1f} pp)")
            else:
                row_vals.append("N/A")
        lines.append(f"| **{target_label}** | " + " | ".join(row_vals) + " |")

    lines.append("| " + " | ".join(" " for _ in range(len(summaries) + 1)) + " |")
    lines.append("| *PROMPT FEATURE BASELINE COMPARISONS* | " + " | ".join(" " for _ in summaries) + " |")

    # 4. Prompt baselines
    baseline_targets = [
        ("correct", "correct", "text_plus_domain_plus_cat", "Correctness vs +category"),
        ("refusal_vs_wrong", "refusal_vs_wrong", "tfidf", "Refusal-vs-Wrong vs TF-IDF"),
        ("correct_within_pre", "correct_within_pre", "text_plus_domain_plus_cat", "Within-Pre Correct vs +category"),
    ]

    for target_key, base_key, baseline_type, label in baseline_targets:
        row_vals = []
        for k in summaries:
            p = summaries[k]["probes"].get(target_key, {})
            if p:
                peak_acc = p["peak_acc"]
                base_acc = p["prompt_feature_baselines"][baseline_type]["mean_acc"]
                diff = (peak_acc - base_acc) * 100
                row_vals.append(f"Probe **{peak_acc:.1%}** vs Base **{base_acc:.1%}**<br>({diff:+.1f} pp)")
            else:
                row_vals.append("N/A")
        lines.append(f"| **{label}** | " + " | ".join(row_vals) + " |")

    return "\n".join(lines)


def plot_comparative_curves(summaries):
    if not summaries:
        return

    n_models = len(summaries)
    fig, axes = plt.subplots(1, n_models, figsize=(5 * n_models, 4.5), sharey=True)
    if n_models == 1:
        axes = [axes]

    targets = [
        ("correct", "correctness", "#2ca02c", "o"),
        ("cutoff", "pre/post cutoff", "#ff7f0e", "s"),
        ("refusal_vs_wrong", "refusal-vs-wrong", "#9467bd", "D"),
    ]

    for idx, (key, label) in enumerate(summaries.items()):
        ax = axes[idx]
        sum_data = summaries[key]
        num_layers = len(sum_data["probes"]["correct"]["per_layer_acc"])
        layers = np.arange(num_layers)

        for target_key, target_label, color, marker in targets:
            p = sum_data["probes"].get(target_key, {})
            if p:
                accs = np.array(p["per_layer_acc"])
                stds = np.array(p["per_layer_std"])
                ax.plot(layers, accs, marker=marker, color=color, label=target_label, linewidth=1.5, markersize=5)
                ax.fill_between(layers, accs - stds, accs + stds, color=color, alpha=0.12)
                # Dotted baseline
                base = p["baseline"]
                ax.axhline(base, color=color, linestyle=":", alpha=0.5)

        ax.set_title(f"{MODEL_NAMES[key]} (L={num_layers - 1})", fontsize=11)
        ax.set_xlabel("Layer Index (0=embeddings)")
        ax.set_ylim(0.48, 1.02)
        ax.grid(True, alpha=0.25)
        if idx == 0:
            ax.set_ylabel("5-Fold CV Accuracy")
            ax.legend(loc="lower left", fontsize=8.5)

    fig.suptitle("Comparative Per-Layer Probing Accuracy across Architectures", fontsize=12, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    out_png = FIGURES_DIR / "comparative_probes.png"
    fig.savefig(out_png, dpi=140)
    plt.close(fig)
    print(f"Wrote {out_png}")


def main():
    summaries = load_summaries()
    if not summaries:
        print("No summary JSONs found. Exiting.")
        return

    table_md = build_markdown_table(summaries)
    out_md = DATA_DIR / "comparison_table.md"
    out_md.write_text(table_md)
    print(f"Wrote {out_md}")

    plot_comparative_curves(summaries)


if __name__ == "__main__":
    main()
