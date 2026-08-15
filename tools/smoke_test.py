import os
import time

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import MODEL_ID, get_device, set_seeds

os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.0"


def main():
    set_seeds()
    device = get_device()
    print(f"Device: {device}")

    print(f"\nLoading tokenizer from {MODEL_ID}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    print(f"Loading model from {MODEL_ID}...")
    t_load_start = time.perf_counter()
    try:
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            dtype=torch.float32,
            device_map=device,
        )
    except Exception as e:
        if "mps" in str(e).lower() and device.type == "mps":
            print(f"MPS load failed ({e}), falling back to CPU")
            device = torch.device("cpu")
            model = AutoModelForCausalLM.from_pretrained(
                MODEL_ID,
                dtype=torch.float32,
                device_map=device,
            )
        else:
            raise
    t_load = time.perf_counter() - t_load_start
    print(f"Model loaded in {t_load:.1f}s")

    num_params = model.num_parameters()
    mem_bytes = num_params * 4  # float32
    print(f"Parameters: {num_params:,} ({num_params/1e9:.2f}B)")
    print(f"Estimated memory (float32): {mem_bytes / 1e9:.2f} GB")

    num_layers = model.config.num_hidden_layers
    mid_layer = num_layers // 2
    print(f"\nTransformer layers: {num_layers}, hooking layer {mid_layer}")

    captured_hidden = {}

    def hook_fn(module, input, output):
        if isinstance(output, tuple):
            captured_hidden["tensor"] = output[0].detach().cpu()
        else:
            captured_hidden["tensor"] = output.detach().cpu()

    hook_target = model.model.layers[mid_layer]
    handle = hook_target.register_forward_hook(hook_fn)

    question = "Who wrote 'One Hundred Years of Solitude'?"
    messages = [{"role": "user", "content": question}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    inputs = tokenizer(text, return_tensors="pt").to(device)
    input_len = inputs["input_ids"].shape[1]

    print(f"\nPrompt: {question}")
    print(f"Input tokens: {input_len}")
    print("Generating...")

    t_gen_start = time.perf_counter()
    with torch.no_grad():
        try:
            output_ids = model.generate(
                **inputs,
                max_new_tokens=128,
                do_sample=False,
            )
        except Exception as e:
            if device.type == "mps":
                print(f"MPS generation failed ({e}), retrying on CPU")
                model = model.to("cpu")
                inputs = {k: v.to("cpu") for k, v in inputs.items()}
                device = torch.device("cpu")
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=128,
                    do_sample=False,
                )
            else:
                raise
    t_gen_total = time.perf_counter() - t_gen_start

    new_tokens = output_ids.shape[1] - input_len
    tokens_per_sec = new_tokens / t_gen_total if t_gen_total > 0 else 0

    answer = tokenizer.decode(output_ids[0][input_len:], skip_special_tokens=True)
    print(f"\nAnswer: {answer}")
    print(f"\n--- Performance ---")
    print(f"Total generation time: {t_gen_total:.2f}s")
    print(f"New tokens: {new_tokens}")
    print(f"Tokens/sec: {tokens_per_sec:.1f}")

    print(f"\n--- Hidden State Capture ---")
    if "tensor" in captured_hidden:
        shape = captured_hidden["tensor"].shape
        print(f"Captured hidden state from layer {mid_layer}: {shape}")
        print(f"  (batch, seq_len, hidden_dim) = ({shape[0]}, {shape[1]}, {shape[2]})")
    else:
        print("WARNING: No hidden state captured!")

    handle.remove()
    del captured_hidden

    print("\nSmoke test passed.")


if __name__ == "__main__":
    main()
