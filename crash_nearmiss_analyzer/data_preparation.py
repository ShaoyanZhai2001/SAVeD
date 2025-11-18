#!/usr/bin/env python3
import pandas as pd
import json
import os

CRASH_COLUMNS = ['Light_condition', 'Weather', 'Road_surface_condition', 'Road_type', 
    'Road_flat', 'Lanes', 'Traffic_condition', 'Ego_pre_avoid_movement', 'Other_pre_avoid_movement', 
    'Guilty', 'Crash_type', 'Type_of_impact', 'Crash with', 'Crash_vehicle_type', 
    'Total_number_of_vehicles', 'Crash_reason', 'Other_most_damaged_area', 'Crash_severity', 'Note']

NEARMISS_COLUMNS = ['Light_condition', 'Weather', 'Road_surface_condition', 'Road_type',
    'Road_flat', 'Lanes', 'Traffic_condition', 'Guilty', 'Avoid_reason']

def clean_value(value):
    if pd.isna(value) or value == '' or str(value).lower() in ['nan', 'none', 'null']:
        return 'Unknown'
    return str(value).strip()

def create_crash_conversation(row, video_name):
    annotations = {col: clean_value(row.get(col, 'Unknown')) for col in CRASH_COLUMNS}
    
    response_parts = [
        "This is a crash scenario. Based on the video analysis:",
        "",
        "**Environmental Conditions:**",
        f"- Light condition: {annotations['Light_condition']}",
        f"- Weather: {annotations['Weather']}",
        f"- Road surface: {annotations['Road_surface_condition']}",
        "",
        "**Road Characteristics:**",
        f"- Road type: {annotations['Road_type']}",
        f"- Road flatness: {annotations['Road_flat']}",
        f"- Number of lanes: {annotations['Lanes']}",
        f"- Traffic condition: {annotations['Traffic_condition']}",
        "",
        "**Pre-Crash Movements:**",
        f"- Ego vehicle movement: {annotations['Ego_pre_avoid_movement']}",
        f"- Other vehicle movement: {annotations['Other_pre_avoid_movement']}",
        "",
        "**Crash Details:**",
        f"- Crash type: {annotations['Crash_type']}",
        f"- Type of impact: {annotations['Type_of_impact']}",
        f"- Crash with: {annotations['Crash with']}",
        f"- Other vehicle type: {annotations['Crash_vehicle_type']}",
        f"- Total vehicles involved: {annotations['Total_number_of_vehicles']}",
        "",
        "**Fault and Severity:**",
        f"- Guilty party: {annotations['Guilty']}",
        f"- Crash reason: {annotations['Crash_reason']}",
        f"- Most damaged area: {annotations['Other_most_damaged_area']}",
        f"- Crash severity: {annotations['Crash_severity']}",
    ]
    
    if annotations['Note'] != 'Unknown':
        response_parts.extend(["", f"**Additional Notes:** {annotations['Note']}"])
    
    response = "\n".join(response_parts)
    
    conversation = [
        {"from": "human", "value": "<image>\nAnalyze this driving scenario video. Describe the environmental conditions, road characteristics, vehicle movements, crash details, and severity."},
        {"from": "gpt", "value": response}
    ]
    
    return conversation

def create_nearmiss_conversation(row, video_name):
    annotations = {col: clean_value(row.get(col, 'Unknown')) for col in NEARMISS_COLUMNS}
    
    response_parts = [
        "This is a near-miss scenario where a collision was successfully avoided. Analysis:",
        "",
        "**Environmental Conditions:**",
        f"- Light condition: {annotations['Light_condition']}",
        f"- Weather: {annotations['Weather']}",
        f"- Road surface: {annotations['Road_surface_condition']}",
        "",
        "**Road Characteristics:**",
        f"- Road type: {annotations['Road_type']}",
        f"- Road flatness: {annotations['Road_flat']}",
        f"- Number of lanes: {annotations['Lanes']}",
        f"- Traffic condition: {annotations['Traffic_condition']}",
        "",
        "**Avoidance Details:**",
        f"- Guilty party (if applicable): {annotations['Guilty']}",
        f"- Reason for avoidance maneuver: {annotations['Avoid_reason']}",
        "",
        "The driver successfully avoided a potential collision through appropriate defensive driving actions."
    ]
    
    response = "\n".join(response_parts)
    
    conversation = [
        {"from": "human", "value": "<image>\nAnalyze this driving scenario video. Describe the environmental conditions, road characteristics, and explain why this was a near-miss and how the collision was avoided."},
        {"from": "gpt", "value": response}
    ]
    
    return conversation

def process_crash_data(csv_path, video_dir, output_jsonl):
    print(f"Processing crash data from {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} crash samples")
    
    output_data = []
    
    for idx, row in df.iterrows():
        if 'video_id' in row:
            video_name = f"{row['video_id']}.mp4"
        elif 'filename' in row:
            video_name = row['filename']
        elif 'Video_name' in row:
            video_name = row['Video_name']
        else:
            video_name = f"{idx + 1}.mp4"
        
        video_path = os.path.join(video_dir, video_name)
        if not os.path.exists(video_path):
            print(f"Warning: Video not found - {video_path}")
            continue
        
        duration = row.get('duration', 8.0)
        conversation = create_crash_conversation(row, video_name)
        
        entry = {
            "id": f"crash_{idx + 1}",
            "video": video_name,
            "duration": float(duration),
            "conversations": conversation
        }
        
        output_data.append(entry)
    
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for entry in output_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Wrote {len(output_data)} crash samples to {output_jsonl}")
    return len(output_data)

def process_nearmiss_data(csv_path, video_dir, output_jsonl):
    print(f"Processing nearmiss data from {csv_path}")
    
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} nearmiss samples")
    
    output_data = []
    
    for idx, row in df.iterrows():
        if 'video_id' in row:
            video_name = f"{row['video_id']}.mp4"
        elif 'filename' in row:
            video_name = row['filename']
        elif 'Video_name' in row:
            video_name = row['Video_name']
        else:
            video_name = f"{idx + 1}.mp4"
        
        video_path = os.path.join(video_dir, video_name)
        if not os.path.exists(video_path):
            print(f"Warning: Video not found - {video_path}")
            continue
        
        duration = row.get('duration', 8.0)
        conversation = create_nearmiss_conversation(row, video_name)
        
        entry = {
            "id": f"nearmiss_{idx + 1}",
            "video": video_name,
            "duration": float(duration),
            "conversations": conversation
        }
        
        output_data.append(entry)
    
    with open(output_jsonl, 'w', encoding='utf-8') as f:
        for entry in output_data:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    print(f"Wrote {len(output_data)} nearmiss samples to {output_jsonl}")
    return len(output_data)

def main():
    base_dir = "/path/to/your/data"
    
    crash_csv = os.path.join(base_dir, "AV_crash_modified_r.csv")
    crash_video_dir = os.path.join(base_dir, "crash")
    crash_output = os.path.join(base_dir, "crash_ft.jsonl")
    
    crash_count = process_crash_data(crash_csv, crash_video_dir, crash_output)
    
    nearmiss_csv = os.path.join(base_dir, "AV_nearmiss_modified_r.csv")
    nearmiss_video_dir = os.path.join(base_dir, "nearmiss")
    nearmiss_output = os.path.join(base_dir, "nearmiss_ft.jsonl")
    
    nearmiss_count = process_nearmiss_data(nearmiss_csv, nearmiss_video_dir, nearmiss_output)
    
    combined_output = "diy_ft_data.json"
    
    combined_data = {
        "crash": {
            "annotation": crash_output,
            "root": crash_video_dir,
            "video_read_type": "decord"
        },
        "nearmiss": {
            "annotation": nearmiss_output,
            "root": nearmiss_video_dir,
            "video_read_type": "decord"
        }
    }
    
    with open(combined_output, 'w', encoding='utf-8') as f:
        json.dump(combined_data, f, indent=2)
    
    print(f"\n✅ Data preparation complete!")
    print(f"   - Crash samples: {crash_count}")
    print(f"   - Nearmiss samples: {nearmiss_count}")
    print(f"   - Total samples: {crash_count + nearmiss_count}")
    print(f"   - Combined config: {combined_output}")

if __name__ == "__main__":
    main()
