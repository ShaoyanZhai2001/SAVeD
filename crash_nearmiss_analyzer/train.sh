#!/bin/bash

set -x

export OMP_NUM_THREADS=1
export DISABLE_ADDMM_CUDA_LT=1
export TORCH_CUDNN_USE_HEURISTIC_MODE_B=1
export PYTHONPATH="$(pwd):$(pwd)/../"
export TF_CPP_MIN_LOG_LEVEL=3

JOB_NAME=$(basename $0)_$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR=work_dirs/${JOB_NAME}

if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi
SCRIPT_NAME=$(basename "$0")
cp "$0" "${OUTPUT_DIR}/${SCRIPT_NAME}"

GPUS=${GPUS:-4}
MIRCO_BATCH_SIZE=${MIRCO_BATCH_SIZE:-1}
ACCUMULATIVE_COUNTS=${ACCUMULATIVE_COUNTS:-4}

torchrun --nproc_per_node=${GPUS} \
  --master_port=29500 \
  train_internvl2_modified.py \
  --model OpenGVLab/InternVL_2_5_HiCo_R16 \
  --datasets data/diy_ft_data.json \
  --num-workers 4 \
  --mirco-batch-size $MIRCO_BATCH_SIZE \
  --global-batch-size $((MIRCO_BATCH_SIZE*GPUS*ACCUMULATIVE_COUNTS)) \
  --vit_lr 2e-6 \
  --connector_lr 1e-5 \
  --lr 1e-5 \
  --wd 0.0 \
  --use-fast-tokenizer \
  --warmup-ratio 0.03 \
  --work-dir ${OUTPUT_DIR} \
  --log-interval 2 \
  --seed 42 \
  --checkpoint-interval 4000 \
  --checkpoint-drop-optimizer \
  --shard-strategy 'zero2' \
  --group-by-length \
  --min_num_frames 64 \
  --max_num_frames 256 \
  2>&1 | tee -a "${OUTPUT_DIR}/training_log.txt"

echo ""
echo "Training complete! Output saved to: ${OUTPUT_DIR}"
