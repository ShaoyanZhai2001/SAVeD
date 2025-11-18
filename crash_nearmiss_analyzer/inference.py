#!/usr/bin/env python3
import os
os.environ['ATTN_IMPLEMENTATION'] = 'eager'
os.environ['TRANSFORMERS_OFFLINE'] = '0'

import sys
import json
import torch
from pathlib import Path
from PIL import Image
import numpy as np
from decord import VideoReader, cpu
import argparse

def load_video_frames(video_path, num_frames=8):
    try:
        if not os.path.exists(video_path):
            print(f"ERROR: Video file not found: {video_path}")
            return None
            
        vr = VideoReader(video_path, ctx=cpu(0))
        total_frames = len(vr)
        
        if total_frames == 0:
            print(f"ERROR: Video has no frames: {video_path}")
            return None
        
        indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
        frames = vr.get_batch(indices).asnumpy()
        pil_frames = [Image.fromarray(frame) for frame in frames]
        
        return pil_frames
    except Exception as e:
        print(f"Error loading video {video_path}: {e}")
        return None

def test_single_video(model, tokenizer, image_processor, video_path, question, num_frames=8):
    print(f"\nProcessing: {os.path.basename(video_path)}")
    
    frames = load_video_frames(video_path, num_frames)
    if frames is None:
        return "Failed to load video"
    
    pixel_values = image_processor(frames, return_tensors='pt')['pixel_values']
    pixel_values = pixel_values.to(torch.float16).cuda()
    
    generation_config = {
        'max_new_tokens': 1000,
        'min_new_tokens': 200,
        'do_sample': False,
        'repetition_penalty': 1.15,
        'length_penalty': 1.0,
    }
    
    try:
        response = model.chat(
            tokenizer=tokenizer,
            pixel_values=pixel_values,
            question=question,
            generation_config=generation_config,
            num_patches_list=[num_frames],
            verbose=False
        )
        
        return response
        
    except Exception as e:
        import traceback
        error_msg = f"Generation error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        return error_msg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str, required=True)
    parser.add_argument('--crash-dir', type=str, required=True)
    parser.add_argument('--nearmiss-dir', type=str, required=True)
    parser.add_argument('--num-videos', type=int, default=10)
    parser.add_argument('--num-frames', type=int, default=32)
    parser.add_argument('--output-dir', type=str, default='inference_results')
    
    args = parser.parse_args()
    
    print("="*80)
    print("LOADING FINE-TUNED MODEL")
    print("="*80)
    
    from transformers import AutoModel, AutoTokenizer, AutoConfig
    import transformers.utils.import_utils as import_utils
    
    def patched_is_flash_attn_2_available():
        return False
    
    def patched_is_flash_attn_greater_or_equal_2_10():
        return False
    
    import_utils.is_flash_attn_2_available = patched_is_flash_attn_2_available
    import_utils.is_flash_attn_greater_or_equal_2_10 = patched_is_flash_attn_greater_or_equal_2_10
    
    print(f"Loading from: {args.model_path}")
    
    config = AutoConfig.from_pretrained(args.model_path, trust_remote_code=True)
    
    if hasattr(config, 'vision_config'):
        config.vision_config.use_flash_attn = False
        config.vision_config._attn_implementation = "eager"
    
    if hasattr(config, 'llm_config'):
        config.llm_config._attn_implementation = "eager"
        config.llm_config.attn_implementation = "eager"
    
    tokenizer = AutoTokenizer.from_pretrained(args.model_path, trust_remote_code=True, use_fast=False)
    
    model = AutoModel.from_pretrained(
        args.model_path,
        config=config,
        torch_dtype=torch.float16,
        trust_remote_code=True,
        device_map='cuda:0'
    )
    
    if hasattr(model, 'vision_model'):
        model.vision_model.config.use_flash_attn = False
        if hasattr(model.vision_model, 'encoder') and hasattr(model.vision_model.encoder, 'layers'):
            for layer in model.vision_model.encoder.layers:
                if hasattr(layer, 'attn'):
                    layer.attn.use_flash_attn = False
    
    if hasattr(model, 'language_model'):
        if hasattr(model.language_model, 'config'):
            model.language_model.config._attn_implementation = "eager"
        if hasattr(model.language_model, 'model') and hasattr(model.language_model.model, 'layers'):
            for layer in model.language_model.model.layers:
                if hasattr(layer, 'self_attn'):
                    layer.self_attn._flash_attn_uses_top_left_mask = False
                    if hasattr(layer.self_attn, 'config'):
                        layer.self_attn.config._attn_implementation = "eager"
    
    model.eval()
    
    from torchvision import transforms
    
    class SimpleImageProcessor:
        def __init__(self, image_size=448):
            self.image_mean = [0.485, 0.456, 0.406]
            self.image_std = [0.229, 0.224, 0.225]
            self.image_size = image_size
            
        def __call__(self, images, return_tensors='pt'):
            transform = transforms.Compose([
                transforms.Lambda(lambda img: img.convert('RGB') if img.mode != 'RGB' else img),
                transforms.Resize((self.image_size, self.image_size), 
                                interpolation=transforms.InterpolationMode.BICUBIC),
                transforms.ToTensor(),
                transforms.Normalize(mean=self.image_mean, std=self.image_std)
            ])
            
            processed = [transform(img) for img in images]
            pixel_values = torch.stack(processed)
            
            return {'pixel_values': pixel_values}
    
    image_processor = SimpleImageProcessor(image_size=448)
    
    print("✅ Model loaded successfully!\n")
    
    os.makedirs(args.output_dir, exist_ok=True)
    
    crash_question = """<image>
Analyze this driving scenario video. Provide ALL the following information in the EXACT format shown:

This is a crash scenario. Complete analysis:

**Environmental Conditions:**
- Light_condition: [Daylight/Nighttime/Dawn/Dusk]
- Weather: [Clear/Rainy/Foggy/Snowy/Other]

**Road Characteristics:**
- Surface_state: [Dry/Wet/Icy/Snowy/Slippery/Other]
- Road_type: [Highway/Urban_road/Rural_road/Road_segment/Signalized_intersection/Parking_lot/etc]
- Road_flat: [Flat/Uphill/Downhill/Curve]
- Lanes: [1/2/3/4+]
- Traffic_condition: [Light_traffic/Moderate_traffic/Heavy_traffic/Congested/etc]

**Pre-Crash Vehicle Movements:**
- Ego_pre_avoid_movement: [Proceeding_straight/Making_left_turn/Making_right_turn/Changing_lanes/Stopped/Backing/Parking/etc]
- Other_pre_avoid_movement: [Proceeding_straight/Making_left_turn/Making_right_turn/Changing_lanes/Stopped/Backing/Parking/etc]

**Crash Details:**
- Guilty: [Ego_vehicle/Other_vehicle/Both/Unknown]
- Crash_type: [Angle/Rear_end/Sideswipe/Head_on/Single_vehicle/Pedestrian/etc]
- Type_of_impact: [Front/Rear/Side/Front_to_side/Rear_to_side/Multiple/etc]
- Crash_with: [Passenger_vehicle/Truck/Van/Motorcycle/Pedestrian/Bicycle/Object/etc]
- Crash_vehicle_type: [Sedan/SUV/Truck/Van/Motorcycle/Bus/etc]
- Total_number_of_vehicles: [1/2/3/4+]
- Crash_reason: [Brief explanation]
- Other_most_damaged_area: [Front_center_bumper/Front_left_bumper/Front_right_bumper/Rear_center_bumper/Left_side/Right_side/Multiple/etc]
- Crash_severity: [Property_damage_only/Minor_injury/Moderate_injury/Severe_injury/Fatal/Unknown]

**Summary:**
- Note: [Additional observations]
- Description: [Brief narrative of crash sequence]"""

    nearmiss_question = """<image>
Analyze this driving scenario video. Provide ALL the following information in the EXACT format shown:

This is a near-miss scenario where a collision was successfully avoided. Complete analysis:

**Environmental Conditions:**
- Light_condition: [Daylight/Nighttime/Dawn/Dusk]
- Weather: [Clear/Rainy/Foggy/Snowy/Other]

**Road Characteristics:**
- Surface_state: [Dry/Wet/Icy/Snowy/Slippery/Other]
- Road_type: [Highway/Urban_road/Rural_road/Road_segment/Signalized_intersection/Parking_lot/etc]
- Road_flat: [Flat/Uphill/Downhill/Curve]
- Lanes: [1/2/3/4+]
- Traffic_condition: [Light_traffic/Moderate_traffic/Heavy_traffic/Congested/etc]

**Avoidance Details:**
- Guilty: [Ego_vehicle/Other_vehicle/Both/Unknown]
- Avoid_reason: [Explanation of near-miss and how collision was avoided]

**Summary:**
- Description: [Brief narrative of near-miss sequence]"""
    
    print("="*80)
    print("TESTING ON CRASH VIDEOS")
    print("="*80)
    
    all_crash_videos = [f for f in os.listdir(args.crash_dir) if f.endswith('.mp4')]
    def sort_key(filename):
        name = filename.replace('.mp4', '')
        try:
            return (0, int(name))
        except ValueError:
            return (1, name)
    
    crash_videos = sorted(all_crash_videos, key=sort_key)
    
    if args.num_videos > 0:
        crash_videos = crash_videos[:args.num_videos]
        print(f"Processing {len(crash_videos)} crash videos (limited by --num-videos)")
    else:
        print(f"Processing ALL {len(crash_videos)} crash videos")
    
    crash_results = []
    
    for idx, video_file in enumerate(crash_videos, 1):
        video_path = os.path.join(args.crash_dir, video_file)
        print(f"\n[{idx}/{len(crash_videos)}] {video_file}")
        print("-"*80)
        
        response = test_single_video(model, tokenizer, image_processor, video_path, crash_question, args.num_frames)
        print(f"Response:\n{response}")
        print("-"*80)
        
        crash_results.append({'video': video_file, 'response': response})
    
    crash_output = os.path.join(args.output_dir, 'crash_results.json')
    with open(crash_output, 'w', encoding='utf-8') as f:
        json.dump(crash_results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Crash results saved to: {crash_output}")
    
    print("\n" + "="*80)
    print("TESTING ON NEARMISS VIDEOS")
    print("="*80)
    
    all_nearmiss_videos = [f for f in os.listdir(args.nearmiss_dir) if f.endswith('.mp4')]
    nearmiss_videos = sorted(all_nearmiss_videos, key=sort_key)
    
    if args.num_videos > 0:
        nearmiss_videos = nearmiss_videos[:args.num_videos]
        print(f"Processing {len(nearmiss_videos)} nearmiss videos (limited by --num-videos)")
    else:
        print(f"Processing ALL {len(nearmiss_videos)} nearmiss videos")
    
    nearmiss_results = []
    
    for idx, video_file in enumerate(nearmiss_videos, 1):
        video_path = os.path.join(args.nearmiss_dir, video_file)
        print(f"\n[{idx}/{len(nearmiss_videos)}] {video_file}")
        print("-"*80)
        
        response = test_single_video(model, tokenizer, image_processor, video_path, nearmiss_question, args.num_frames)
        print(f"Response:\n{response}")
        print("-"*80)
        
        nearmiss_results.append({'video': video_file, 'response': response})
    
    nearmiss_output = os.path.join(args.output_dir, 'nearmiss_results.json')
    with open(nearmiss_output, 'w', encoding='utf-8') as f:
        json.dump(nearmiss_results, f, indent=2, ensure_ascii=False)
    print(f"\n✅ Nearmiss results saved to: {nearmiss_output}")
    
    print("\n" + "="*80)
    print("✅ TESTING COMPLETE!")
    print("="*80)
    print(f"Results saved to: {args.output_dir}/")

if __name__ == '__main__':
    main()
