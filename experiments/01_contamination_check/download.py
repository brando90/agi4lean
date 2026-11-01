"""Download the training sets and eval sets used by contam.py from Hugging Face (public, no token).
Usage: python download.py --out DATA_DIR   (about 4.7 GB; the file list is hard-coded below)
"""
import argparse, json, os, subprocess, urllib.request
from concurrent.futures import ThreadPoolExecutor
AI4M = "state_info_informalization minif2f_dataset willy_mix_1 stateInfoInformalizationBig regexInformalizationData miniF2FInformalizations michael-af mma-dataset gpt4-more gpt-4fp_minif2f_mix minif2f_real regex_gpt4 claudedataset-2 250ktokendataset 102k_token_clean_claude_dataset leandojo-informalized less-code-top-1M zipfit-AF-TOP1M dsir-TOP1M-AF zipfit-TOP1M-AF less-proofnet-lean4-top1M less-proofnet-lean4-ranked math-select-less-llama8b".split()
UDACA = "AF AF-with-metaData Isa-MMA MMA-with-Text Isa-AF-MMA Split-Isa-AF-MMA AF-split Code-Mixed-Dataset ZIPFIT-train DSIR-train proofnet-lean4 minif2f-lean4 proofnet-v2-lean4 proofnet-v3-lean4".split()
repos = [f"AI4M/{n}" for n in AI4M] + [f"UDACA/{n}" for n in UDACA] + ["hoskinson-center/proofnet", "cat-searcher/minif2f-lean4"]
def walk(r, p=""):
    d = json.load(urllib.request.urlopen(f"https://huggingface.co/api/datasets/{r}/tree/main" + (f"/{p}" if p else "")))
    for x in d:
        if x["type"] == "directory": yield from walk(r, x["path"])
        else: yield r, x["path"]
ap = argparse.ArgumentParser(); ap.add_argument("--out", required=True); a = ap.parse_args()
jobs = [j for r in repos for j in walk(r) if not j[1].endswith((".gitattributes", ".png", ".py"))]
def go(j):
    r, p = j; dst = f"{a.out}/{r.replace('/', '__')}/{p}"; os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst): subprocess.run(["curl", "-sfL", "--retry", "3", "-o", dst, f"https://huggingface.co/datasets/{r}/resolve/main/{p}"])
with ThreadPoolExecutor(8) as ex: list(ex.map(go, jobs))
