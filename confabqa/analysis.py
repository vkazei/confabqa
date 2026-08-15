"""Importable interface to the frozen 03_analyze.py pipeline."""
from confabqa._loader import load_script

analyze = load_script("analyze", "03_analyze.py")

load_all = analyze.load_all
prompt_features = analyze.prompt_features
prompt_feature_matrix = analyze.prompt_feature_matrix
