#!/usr/bin/env python3
import json
import csv
import re
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from terminology_mapping import normalize_predictions

CRASH_FIELDS = ['video', 'Light_condition', 'Weather', 'Road_surface_condition', 'Road_type', 
    'Road_flat', 'Lanes', 'Traffic_condition', 'Ego_pre_avoid_movement', 'Other_pre_avoid_movement', 
    'Guilty', 'Crash_type', 'Type_of_impact', 'Crash_with', 'Crash_vehicle_type', 
    'Total_number_of_vehicles', 'Crash_reason', 'Other_most_damaged_area', 'Crash_severity', 'Note']

NEARMISS_FIELDS = ['video', 'Light_condition', 'Weather', 'Road_surface_condition', 'Road_type',
    'Road_flat', 'Lanes', 'Traffic_condition', 'Guilty', 'Avoid_reason']

CATEGORICAL_FIELDS = {'Light_condition', 'Weather', 'Road_surface_condition', 'Road_type', 'Road_flat', 
    'Lanes', 'Crash_type', 'Type_of_impact', 'Crash_with', 'Crash_vehicle_type', 
    'Total_number_of_vehicles', 'Crash_severity'}

TEXT_FIELDS = {'Ego_pre_avoid_movement', 'Other_pre_avoid_movement', 'Crash_reason', 
    'Other_most_damaged_area', 'Note', 'Avoid_reason', 'Traffic_condition', 'Guilty'}

def parse_field_value(response_text, field_name):
    patterns = [
        rf'-\s*{field_name}:\s*(.+?)(?:\n|$)',
        rf'-\s*{field_name.replace("_", " ")}:\s*(.+?)(?:\n|$)',
        rf'{field_name}:\s*(.+?)(?:\n|$)',
        rf'{field_name.replace("_", " ")}:\s*(.+?)(?:\n|$)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, response_text, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            value = re.sub(r'\*\*', '', value)
            value = re.sub(r'\s+', ' ', value)
            return value
    
    return ""

def parse_crash_response(response):
    result = {}
    field_mappings = {
        'Light_condition': ['Light condition', 'Light_condition'],
        'Weather': ['Weather'],
        'Road_surface_condition': ['Road surface condition', 'Road_surface_condition', 'Surface condition'],
        'Road_type': ['Road type', 'Road_type'],
        'Road_flat': ['Road flatness', 'Road_flat', 'Flatness'],
        'Lanes': ['Number of lanes', 'Lanes'],
        'Traffic_condition': ['Traffic condition', 'Traffic_condition', 'Traffic'],
        'Ego_pre_avoid_movement': ['Ego vehicle movement', 'Ego_pre_avoid_movement', 'Ego movement'],
        'Other_pre_avoid_movement': ['Other vehicle movement', 'Other_pre_avoid_movement', 'Other movement'],
        'Guilty': ['Guilty party', 'Guilty'],
        'Crash_type': ['Crash type', 'Crash_type'],
        'Type_of_impact': ['Type of impact', 'Type_of_impact', 'Impact type'],
        'Crash_with': ['Crash with', 'Crash_with'],
        'Crash_vehicle_type': ['Crash vehicle type', 'Crash_vehicle_type', 'Vehicle type'],
        'Total_number_of_vehicles': ['Total vehicles involved', 'Total_number_of_vehicles', 'Vehicles involved'],
        'Crash_reason': ['Crash reason', 'Crash_reason', 'Reason'],
        'Other_most_damaged_area': ['Most damaged area', 'Other_most_damaged_area', 'Damaged area'],
        'Crash_severity': ['Crash severity', 'Crash_severity', 'Severity'],
        'Note': ['Note', 'Additional notes', 'Notes']
    }
    
    for field, variations in field_mappings.items():
        value = ""
        for var in variations:
            value = parse_field_value(response, var)
            if value:
                break
        result[field] = value
    
    return result

def parse_nearmiss_response(response):
    result = {}
    field_mappings = {
        'Light_condition': ['Light condition', 'Light_condition'],
        'Weather': ['Weather'],
        'Road_surface_condition': ['Road surface condition', 'Road_surface_condition', 'Surface condition'],
        'Road_type': ['Road type', 'Road_type'],
        'Road_flat': ['Road flatness', 'Road_flat', 'Flatness'],
        'Lanes': ['Number of lanes', 'Lanes'],
        'Traffic_condition': ['Traffic condition', 'Traffic_condition', 'Traffic'],
        'Guilty': ['Guilty party', 'Guilty'],
        'Avoid_reason': ['Avoid reason', 'Avoid_reason', 'Reason for avoidance']
    }
    
    for field, variations in field_mappings.items():
        value = ""
        for var in variations:
            value = parse_field_value(response, var)
            if value:
                break
        result[field] = value
    
    return result

def parse_json_to_csv(json_file, output_csv, scenario_type='crash'):
    print(f"\n{'='*80}")
    print(f"PARSING {scenario_type.upper()} RESULTS")
    print(f"{'='*80}")
    
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data)} videos from {json_file}")
    
    parsed_data = []
    for item in data:
        video = item['video']
        response = item['response']
        
        if scenario_type == 'crash':
            fields = parse_crash_response(response)
        else:
            fields = parse_nearmiss_response(response)
        
        fields['video'] = video
        parsed_data.append(fields)
    
    if scenario_type == 'crash':
        df = pd.DataFrame(parsed_data, columns=CRASH_FIELDS)
    else:
        df = pd.DataFrame(parsed_data, columns=NEARMISS_FIELDS)
    
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} rows to {output_csv}")
    
    print(f"\n{'='*80}")
    print(f"APPLYING TERMINOLOGY NORMALIZATION")
    print(f"{'='*80}")
    df_normalized = normalize_predictions(df, scenario_type=scenario_type)
    print(f"✅ Normalization applied")
    
    normalized_csv = output_csv.replace('formatted-', 'formatted-normalized-')
    df_normalized.to_csv(normalized_csv, index=False)
    print(f"✅ Saved normalized version to {normalized_csv}")
    
    return df_normalized

def load_ground_truth(csv_file, scenario_type='crash'):
    print(f"\n{'='*80}")
    print(f"LOADING {scenario_type.upper()} GROUND TRUTH")
    print(f"{'='*80}")
    
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} rows from {csv_file}")
    
    df['video'] = df.index + 1
    df['video'] = df['video'].astype(str) + '.mp4'
    
    if scenario_type == 'crash':
        available_fields = [f for f in CRASH_FIELDS if f in df.columns or f == 'video']
        df = df[available_fields]
    else:
        available_fields = [f for f in NEARMISS_FIELDS if f in df.columns or f == 'video']
        df = df[available_fields]
    
    print(f"Available fields: {available_fields}")
    
    return df

def calculate_semantic_similarity(pred_text, gt_text, model):
    if not pred_text or not gt_text:
        return 0.0
    
    pred_text = str(pred_text).strip()
    gt_text = str(gt_text).strip()
    
    if not pred_text or not gt_text:
        return 0.0
    
    embeddings = model.encode([pred_text, gt_text])
    similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    
    return float(similarity)

def evaluate_predictions(pred_df, gt_df, scenario_type='crash'):
    print(f"\n{'='*80}")
    print(f"EVALUATING {scenario_type.upper()} PREDICTIONS")
    print(f"{'='*80}")
    
    print("Loading sentence transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Model loaded")
    
    merged = pd.merge(pred_df, gt_df, on='video', suffixes=('_pred', '_gt'), how='inner')
    print(f"\nMatched {len(merged)} videos between predictions and ground truth")
    
    if len(merged) == 0:
        print("❌ No matching videos found! Check video naming convention.")
        return
    
    results = []
    
    if scenario_type == 'crash':
        eval_fields = [f for f in CRASH_FIELDS if f != 'video']
    else:
        eval_fields = [f for f in NEARMISS_FIELDS if f != 'video']
    
    for field in eval_fields:
        pred_col = f"{field}_pred"
        gt_col = f"{field}_gt"
        
        if gt_col not in merged.columns:
            print(f"⚠️  {field}: Not in ground truth, skipping")
            continue
        
        print(f"\nEvaluating: {field}")
        
        if field in CATEGORICAL_FIELDS:
            matched = 0
            total = 0
            for _, row in merged.iterrows():
                pred_val = str(row[pred_col]).strip().lower()
                gt_val = str(row[gt_col]).strip().lower()
                
                if pred_val and gt_val and pred_val != 'nan' and gt_val != 'nan':
                    total += 1
                    if pred_val == gt_val:
                        matched += 1
            
            accuracy = (matched / total * 100) if total > 0 else 0.0
            print(f"  Exact Match: {matched}/{total} = {accuracy:.2f}%")
            
            if total > 0:
                results.append({
                    'field': field,
                    'type': 'categorical',
                    'metric': 'exact_match',
                    'score': accuracy,
                    'matched': matched,
                    'total': total
                })
        
        elif field in TEXT_FIELDS:
            similarities = []
            for _, row in merged.iterrows():
                pred_val = str(row[pred_col]).strip()
                gt_val = str(row[gt_col]).strip()
                
                if pred_val and gt_val and pred_val != 'nan' and gt_val != 'nan':
                    sim = calculate_semantic_similarity(pred_val, gt_val, model)
                    similarities.append(sim)
            
            avg_similarity = np.mean(similarities) * 100 if similarities else 0.0
            print(f"  Semantic Similarity: {avg_similarity:.2f}% (avg over {len(similarities)} samples)")
            
            if len(similarities) > 0:
                results.append({
                    'field': field,
                    'type': 'text',
                    'metric': 'cosine_similarity',
                    'score': avg_similarity,
                    'matched': len(similarities),
                    'total': len(similarities)
                })
    
    print(f"\n{'='*80}")
    print(f"OVERALL RESULTS ({scenario_type.upper()})")
    print(f"{'='*80}")
    
    categorical_scores = [r['score'] for r in results if r['type'] == 'categorical']
    text_scores = [r['score'] for r in results if r['type'] == 'text']
    
    if categorical_scores:
        print(f"Average Exact Match (Categorical): {np.mean(categorical_scores):.2f}%")
    if text_scores:
        print(f"Average Semantic Similarity (Text): {np.mean(text_scores):.2f}%")
    
    all_scores = categorical_scores + text_scores
    if all_scores:
        print(f"Overall Average Score: {np.mean(all_scores):.2f}%")
    
    results_df = pd.DataFrame(results)
    results_file = f"evaluation_{scenario_type}.csv"
    results_df.to_csv(results_file, index=False)
    print(f"\n✅ Detailed results saved to {results_file}")
    
    return results_df

def main():
    crash_json = "test_results_all/crash_results.json"
    nearmiss_json = "test_results_all/nearmiss_results.json"
    
    crash_gt = "/media/rv/Disk 0/for-vlm-crash/AV_crash_modified_r.csv"
    nearmiss_gt = "/media/rv/Disk 0/for-vlm-crash/AV_nearmiss_modified_r.csv"
    
    formatted_crash_csv = "formatted-crash.csv"
    formatted_nearmiss_csv = "formatted-nearmiss.csv"
    
    print("STEP 1: PARSING MODEL OUTPUTS TO CSV")
    print("="*80)
    
    crash_df = parse_json_to_csv(crash_json, formatted_crash_csv, scenario_type='crash')
    nearmiss_df = parse_json_to_csv(nearmiss_json, formatted_nearmiss_csv, scenario_type='nearmiss')
    
    print("\n\nSTEP 2: LOADING GROUND TRUTH")
    print("="*80)
    
    crash_gt_df = load_ground_truth(crash_gt, scenario_type='crash')
    nearmiss_gt_df = load_ground_truth(nearmiss_gt, scenario_type='nearmiss')
    
    print("\n\nSTEP 3: EVALUATING NORMALIZED PREDICTIONS")
    print("="*80)
    
    print("\n" + "🔍 CRASH EVALUATION WITH NORMALIZATION")
    print("="*80)
    crash_results = evaluate_predictions(crash_df, crash_gt_df, scenario_type='crash')
    
    print("\n" + "🔍 NEARMISS EVALUATION WITH NORMALIZATION")
    print("="*80)
    nearmiss_results = evaluate_predictions(nearmiss_df, nearmiss_gt_df, scenario_type='nearmiss')
    
    print("\n" + "="*80)
    print("✅ EVALUATION COMPLETE WITH TERMINOLOGY NORMALIZATION!")
    print("="*80)

if __name__ == "__main__":
    main()
