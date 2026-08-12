"""Device/seed plumbing (needs torch)."""
import os
import torch

import config


def test_seed_constant():
    assert config.SEED == 0


def test_set_seeds_runs():
    config.set_seeds()


def test_force_cpu_env(monkeypatch):
    monkeypatch.setenv("FORCE_CPU", "1")
    assert config.get_device() == torch.device("cpu")


def test_get_device_returns_torch_device():
    assert isinstance(config.get_device(), torch.device)
