#!/usr/bin/env python3
import re

ROAD_TYPE_MAPPING = {
    'highway': 'Highway/Freeway', 'freeway': 'Highway/Freeway', 'highway/freeway': 'Highway/Freeway',
    'urban road': 'Road_segement', 'urban': 'Road_segement', 'city road': 'Road_segement', 'street': 'Road_segement',
    'rural road': 'Rural_road', 'rural': 'Rural_road', 'country road': 'Rural_road',
    'unpaved road': 'Unpaved_road', 'unpaved': 'Unpaved_road', 'dirt road': 'Unpaved_road',
    'parking lot': 'Parking_lot', 'parking': 'Parking_lot',
    'intersection': 'Signalized_intersection', 'signalized intersection': 'Signalized_intersection',
    'traffic light': 'Signalized_intersection',
    'non-signalized intersection': 'nonSignalized_intersection', 'unsignalized intersection': 'nonSignalized_intersection',
    'other': 'other', 'unknown': 'other'
}

CRASH_TYPE_MAPPING = {
    'angle': 'Angle', 'angle collision': 'Angle',
    'rear-end': 'Rear_end', 'rear end': 'Rear_end', 'rear': 'Rear_end', 'rear collision': 'Rear_end',
    'sideswipe': 'Sideswipe', 'side swipe': 'Sideswipe', 'side collision': 'Sideswipe',
    'head-on': 'Head_on', 'head on': 'Head_on', 'frontal': 'Head_on',
    'other': 'other', 'unknown': 'other'
}

TYPE_OF_IMPACT_MAPPING = {
    'front to side': 'Front_to_side', 'front-to-side': 'Front_to_side', 'side': 'Front_to_side',
    'front to rear': 'Front_to_rear', 'front-to-rear': 'Front_to_rear', 'rear': 'Front_to_rear',
    'sideswipe same direction': 'Sideswipe_same_direction', 'sideswipe opposite direction': 'Sideswipe_opposite_direction',
    'sideswipe': 'Sideswipe_same_direction',
    'head on': 'Head_on', 'head-on': 'Head_on', 'frontal': 'Head_on',
    'other': 'other'
}

CRASH_SEVERITY_MAPPING = {
    'property damage only': 'Property_damage_only', 'property damage': 'Property_damage_only', 'minor': 'Property_damage_only',
    'injury': 'Injury', 'injured': 'Injury', 'injuries': 'Injury',
    'fatal': 'Fatal', 'death': 'Fatal', 'fatality': 'Fatal',
    'other': 'other'
}

GUILTY_MAPPING = {
    'both': 'Both', 'both parties': 'Both', 'both at fault': 'Both_at_fault', 'both vehicles': 'Both',
    'ego vehicle': 'Yes', 'yes': 'Yes', 'ego': 'Yes', 'our vehicle': 'Yes',
    'no': 'No', 'other vehicle': 'No', 'not guilty': 'No', 'other': 'No',
    'unclear': 'Both', 'unknown': 'Both'
}

LIGHT_CONDITION_MAPPING = {
    'daylight': 'Daylight', 'daytime': 'Daylight', 'day': 'Daylight',
    'nighttime': 'Dark_lighted', 'night': 'Dark_lighted',
    'dark lighted': 'Dark_lighted', 'dark unlighted': 'Dark_unlighted', 'dark': 'Dark_lighted',
    'dawn': 'Dawn_dusk', 'dusk': 'Dawn_dusk', 'twilight': 'Dawn_dusk',
    'other': 'other'
}

WEATHER_MAPPING = {
    'clear': 'Clear', 'sunny': 'Clear',
    'cloudy': 'Cloudy', 'overcast': 'Cloudy',
    'rainy': 'Rainy', 'rain': 'Rainy', 'raining': 'Rainy',
    'foggy': 'Foggy', 'fog': 'Foggy',
    'snowy': 'Snowy', 'snow': 'Snowy', 'snowing': 'Snowy',
    'other': 'other'
}

ROAD_FLAT_MAPPING = {
    'flat': 'Flat', 'level': 'Flat',
    'slope': 'Slope', 'sloped': 'Slope', 'incline': 'Slope', 'hill': 'Slope',
    'curve': 'Curve', 'curved': 'Curve', 'bend': 'Curve',
    'other': 'other'
}

TRAFFIC_CONDITION_KEYWORDS = {
    'light': ['light', 'sparse', 'few', 'empty', 'quiet'],
    'moderate': ['moderate', 'medium', 'normal', 'average'],
    'heavy': ['heavy', 'congested', 'dense', 'busy', 'traffic jam']
}

def normalize_text(text):
    if not text or str(text).strip().lower() in ['nan', 'none', '']:
        return ''
    text = str(text).strip().lower()
    text = re.sub(r'[_\-]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def apply_mapping(value, mapping_dict):
    if not value:
        return ''
    
    normalized = normalize_text(value)
    
    if normalized in mapping_dict:
        return mapping_dict[normalized]
    
    for key, mapped_value in mapping_dict.items():
        if key in normalized or normalized in key:
            return mapped_value
    
    return value.strip()

def normalize_road_type(value):
    return apply_mapping(value, ROAD_TYPE_MAPPING)

def normalize_crash_type(value):
    return apply_mapping(value, CRASH_TYPE_MAPPING)

def normalize_type_of_impact(value):
    return apply_mapping(value, TYPE_OF_IMPACT_MAPPING)

def normalize_crash_severity(value):
    return apply_mapping(value, CRASH_SEVERITY_MAPPING)

def normalize_guilty(value):
    if not value:
        return ''
    
    normalized = normalize_text(value)
    
    if 'not' in normalized or 'no (' in normalized or normalized == 'no':
        if 'both' in normalized:
            return 'Both'
        return 'No'
    
    if 'both' in normalized or 'two' in normalized or 'each' in normalized:
        return 'Both'
    
    if 'ego' in normalized or 'our' in normalized or 'yes' in normalized:
        return 'Yes'
    
    return apply_mapping(value, GUILTY_MAPPING)

def normalize_light_condition(value):
    return apply_mapping(value, LIGHT_CONDITION_MAPPING)

def normalize_weather(value):
    return apply_mapping(value, WEATHER_MAPPING)

def normalize_road_flat(value):
    return apply_mapping(value, ROAD_FLAT_MAPPING)

def normalize_lanes(value):
    if not value:
        return ''
    
    match = re.search(r'\d+', str(value))
    if match:
        return match.group()
    
    return str(value).strip()

def normalize_traffic_condition(value):
    if not value:
        return ''
    
    normalized = normalize_text(value)
    
    for category, keywords in TRAFFIC_CONDITION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in normalized:
                return f"{category.capitalize()}_traffic"
    
    return value.strip()

def normalize_predictions(df, scenario_type='crash'):
    df = df.copy()
    
    if 'Light_condition' in df.columns:
        df['Light_condition'] = df['Light_condition'].apply(normalize_light_condition)
    
    if 'Weather' in df.columns:
        df['Weather'] = df['Weather'].apply(normalize_weather)
    
    if 'Road_type' in df.columns:
        df['Road_type'] = df['Road_type'].apply(normalize_road_type)
    
    if 'Road_flat' in df.columns:
        df['Road_flat'] = df['Road_flat'].apply(normalize_road_flat)
    
    if 'Lanes' in df.columns:
        df['Lanes'] = df['Lanes'].apply(normalize_lanes)
    
    if 'Traffic_condition' in df.columns:
        df['Traffic_condition'] = df['Traffic_condition'].apply(normalize_traffic_condition)
    
    if 'Guilty' in df.columns:
        df['Guilty'] = df['Guilty'].apply(normalize_guilty)
    
    if scenario_type == 'crash':
        if 'Crash_type' in df.columns:
            df['Crash_type'] = df['Crash_type'].apply(normalize_crash_type)
        
        if 'Type_of_impact' in df.columns:
            df['Type_of_impact'] = df['Type_of_impact'].apply(normalize_type_of_impact)
        
        if 'Crash_severity' in df.columns:
            df['Crash_severity'] = df['Crash_severity'].apply(normalize_crash_severity)
    
    return df
