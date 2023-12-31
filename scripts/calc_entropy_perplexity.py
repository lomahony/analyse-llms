import argparse
import json
import numpy as np
import torch


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--calculation_output_path', required=True,
                        help='Path for where results from previous step were saved')
    parser.add_argument('--utf8_conversion_scalar', default=None, type=float)
    parser.add_argument('--output_path', default=None,
                        help='Path for where to save final results')
    return parser.parse_args()


def main():
    args = parse_args()
    perplexity_data = torch.load(args.calculation_output_path)
    aggregate_logprobs = np.concatenate(perplexity_data["all_logprobs"])
    perplexity = np.exp(-aggregate_logprobs.mean())
    result = {
        "entropy": float(-aggregate_logprobs.mean()),
        "perplexity": float(perplexity)
    }
    if args.utf8_conversion_scalar is not None:
        result["bpb"] = float(np.log2(perplexity) * args.utf8_conversion_scalar)
    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(json.dumps(result, indent=2))
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()