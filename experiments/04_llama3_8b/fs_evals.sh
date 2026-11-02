# Like-for-like 3-shot evals: base on MiniF2F; each fine-tune with the same 3-shot prompt on ProofNet and MiniF2F.
cd /lfs/skampere1/0/brando9/at2363 && . ./env.sh
mkdir -p results/passk_fs
run() { # gpu name adapter tasks...
  g=$1; n=$2; ad=$3; shift 3
  ADARG=""; [ "$ad" != "none" ] && ADARG="--adapter $ad"
  CUDA_VISIBLE_DEVICES=$g $PY passk.py $ADARG --name $n --format fewshot --tasks "$@" --n 100 --ks 1 5 10 50 100 --out results/passk_fs --lean-bin $L --mathlib $M --gpu-util 0.85 --workers 16 > logs/passk_fs_$n.log 2>&1
}
( run 3 base none minif2f_lean4:test; run 3 gpt4more runs/gpt4more/adapter proofnet_lean4:test minif2f_lean4:test ) &
( run 5 mma runs/mma/adapter proofnet_lean4:test minif2f_lean4:test; run 5 otf2 runs/otf2/adapter proofnet_lean4:test minif2f_lean4:test ) &
wait
