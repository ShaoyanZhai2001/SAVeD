# Crash & Nearmiss Video Analyzer

Fine-tuned InternVL 2.5 model for analyzing driving scenarios (crash/nearmiss classification and detailed annotation extraction).

## Quick Start

```bash
pip install -r requirements.txt

python inference.py \
  --model-path /path/to/model \
  --crash-dir /path/to/crash/videos \
  --nearmiss-dir /path/to/nearmiss/videos \
  --num-videos 10 \
  --num-frames 32 \
  --output-dir results
```

## Files

**Inference & Evaluation:**
- **inference.py**: Run model on videos
- **evaluation.py**: Compare predictions vs ground truth
- **terminology_mapping.py**: Normalize outputs

**Training (Modified from Original XTuner):**
- **train_internvl2_modified.py**: FULL training script (1113 lines) with TITAN RTX patches
- **train.sh**: Training launch script
- **training_modifications.txt**: Complete documentation of all modifications
- **data_preparation.py**: Prepare training data from CSV

**IMPORTANT**: This training code is heavily modified from the original XTuner/VideoChat-Flash
to support TITAN RTX (Turing) GPUs. See training_modifications.txt for details.

**Documentation:**
- **requirements.txt**: Dependencies
- **instructions.txt**: Full documentation
- **README.md**: This file

## Model Details

- Base: InternVL 2.5 HiCo R16
- Training: 1,642 videos (1040 crash, 602 nearmiss)
- Input: 8-32 frames @ 448x448
- Output: 19 crash fields or 9 nearmiss fields

## Extracted Fields

**Crash (19)**: Light_condition, Weather, Road_surface_condition, Road_type, Road_flat, Lanes, Traffic_condition, Ego_pre_avoid_movement, Other_pre_avoid_movement, Guilty, Crash_type, Type_of_impact, Crash_with, Crash_vehicle_type, Total_number_of_vehicles, Crash_reason, Other_most_damaged_area, Crash_severity, Note

**Nearmiss (9)**: Light_condition, Weather, Road_surface_condition, Road_type, Road_flat, Lanes, Traffic_condition, Guilty, Avoid_reason

## Requirements

- GPU: 16GB+ VRAM
- Python 3.8+
- PyTorch 2.0+
- transformers 4.45.1

See **instructions.txt** for full documentation.
