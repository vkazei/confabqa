"""Importable interface to the frozen 02_evaluate.py pipeline."""
from confabqa._loader import load_script

evaluate = load_script("evaluate", "02_evaluate.py")

evaluate_question = evaluate.evaluate_question
grade = evaluate.grade
