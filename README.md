# SAVeD
Social media-based Autonomous Vehicle event Dataset

> 🧠 *Note: We respect YouTube content ownership. Only URLs and timestamps are shared.*
> ## 🔍 1. Example: Variable `LIGHT_CONDITION`

This variable describes the lighting condition of the scene during the crash or near-miss. It is classified into:

| Value                | Description                                             |
|----------------------|---------------------------------------------------------|
| `daylight`           | Scene is clearly visible under natural sunlight         |
| `dark with light`    | Night scene with streetlights or headlights             |
| `dark without light` | Completely dark environment with no external lighting   |

---

### 🎬 Video Examples (Click image to view)

#### 1. `daylight`
[![Daylight](https://img.youtube.com/vi/UHwEqBDFl34/0.jpg)](https://youtu.be/UHwEqBDFl34?t=65)  
*AV proceeds through a sunny city intersection.*

---

#### 2. `dark with light`
[![Dark with Light](https://img.youtube.com/vi/RPhR3nNWauY/0.jpg)](https://youtu.be/RPhR3nNWauY?t=149)  
*AV approaches a well-lit intersection at night.*

---

#### 3. `dark without light`
[![Dark without Light](https://img.youtube.com/vi/O8zvM-DPifw/0.jpg)](https://youtu.be/O8zvM-DPifw?t=154)  
*AV drives on a completely unlit road at night with limited visibility.*
---

## 🌦️ 2. Variable: `WEATHER` — Weather Condition

### 📘 Definition  
This variable captures the atmospheric conditions at the time of the event, which may affect AV sensor performance, visibility, and maneuverability.

---

### 🧩 Label Options

| Value      | Description                             |
|------------|-----------------------------------------|
| `clear`    | Sunny or mostly clear weather            |
| `cloudy`   | Overcast or partially cloudy sky         |
| `fog/smog/smoke` | Reduced visibility due to fog, smog, or smoke |
| `rain`     | Rainfall present during the event        |
| `snow`     | Snowfall or snowy road conditions        |

---

### 🎬 Video Examples (Click to View)

#### 1. `clear`
[![Clear](https://img.youtube.com/vi/Yk0JQaupWX0/0.jpg)](https://youtu.be/Yk0JQaupWX0?t=661)  
☀️ *Sunny day with excellent visibility. AV drives under clear weather conditions.*

---

#### 2. `cloudy`
[![Cloudy](https://img.youtube.com/vi/mzgvgvqh2QE/0.jpg)](https://youtu.be/mzgvgvqh2QE?t=4)  
⛅ *Overcast weather with gray sky. No precipitation but reduced sunlight.*

---

#### 3. `fog/smog/smoke`
[![Fog](https://img.youtube.com/vi/F94gFrOjQTA/0.jpg)](https://youtu.be/F94gFrOjQTA?t=7)  
🌫️ *AV drives through foggy conditions. Visibility is significantly reduced due to smog or haze.*

---

#### 4. `rain`
[![Rain](https://img.youtube.com/vi/9LuxEM7000g/0.jpg)](https://youtu.be/9LuxEM7000g?t=467)  
🌧️ *AV navigates in moderate to heavy rain. Raindrops visible on the camera lens.*

---

#### 5. `snow`
[![Snow](https://img.youtube.com/vi/ojU66krutns/0.jpg)](https://youtu.be/ojU66krutns)  
❄️ *AV operates in snowy conditions. Snow accumulates on road and surroundings.*

---

### 📌 Annotation Notes

- If multiple weather phenomena are present (e.g., rain + fog), annotate with the **most dominant** condition that affects visibility or driving.

---

## 🛣️ 3. Variable: `ROAD_SURFACE_CONDITION` — Road Surface Condition

### 📘 Definition  
This variable describes the surface condition of the roadway at the time of the event, which directly impacts vehicle control, traction, and braking efficiency.

---

### 🧩 Label Options

| Value        | Description                                         |
|--------------|-----------------------------------------------------|
| `dry`        | Normal, dry pavement with no moisture               |
| `wet`        | Surface appears damp or soaked due to rain or water |
| `snow/ice`   | Snow-covered or icy roadway, may reduce traction    |

---

### 🎬 Video Examples (Click to View)

#### 1. `dry`
[![Dry](https://img.youtube.com/vi/HD0dz8G-2sM/0.jpg)](https://youtu.be/HD0dz8G-2sM?t=2606)  
🚗 *AV operates on a dry and clear roadway. No visible moisture or precipitation.*

---

#### 2. `wet`
[![Wet](https://img.youtube.com/vi/66IApMK6F5Y/0.jpg)](https://youtu.be/66IApMK6F5Y?t=1051)  
🌧️ *Pavement is visibly wet due to recent or ongoing rain. Reflections and water film present.*

---

#### 3. `snow/ice`
[![Snow/Ice](https://img.youtube.com/vi/PKHfruXYmVY/0.jpg)](https://youtu.be/PKHfruXYmVY?t=170)  
❄️ *Road surface is covered in snow or ice. Potential for slipping and traction loss.*

---

### 📌 Annotation Notes

- When wet spots or melting snow are visible but not dominant, annotate based on the **overall driving condition**.
- If a road transitions during the video (e.g., snow melts), label based on **when the event occurs**, not general driving condition.


---

## ⚖️ 4. Variable: `GUILTY` — Fault Attribution

### 📘 Definition  
This variable indicates which party is considered at fault for the incident based on video evidence and contextual cues. It helps evaluate AV decision-making in safety-critical scenarios.

---

### 🧩 Label Options

| Value              | Description                                               |
|--------------------|-----------------------------------------------------------|
| `AV`               | The autonomous vehicle was primarily at fault             |
| `non-AV`           | The other road user was primarily at fault                |
| `both`             | Both parties contributed to the incident                  |

---

### 🎬 Video Examples (Click to View)

#### 1. `AV` — AV is at fault
[![AV Guilty](https://img.youtube.com/vi/6jSMxcnTklo/0.jpg)](https://youtu.be/6jSMxcnTklo?t=123)  
⚠️ *AV failed to yield and collided with cross traffic. Video clearly shows AV's improper judgment.*

---

#### 2. `non-AV` — Other party is at fault
[![Non-AV Guilty](https://img.youtube.com/vi/PKHfruXYmVY/0.jpg)](https://youtu.be/PKHfruXYmVY?t=825)  
✅ *Another vehicle unexpectedly enters AV's lane, causing a collision. AV behavior appears compliant.*

---

#### 3. `both` — Shared fault
[![Shared Fault](https://img.youtube.com/vi/IjFsu5mirkw/0.jpg)](https://youtu.be/IjFsu5mirkw?t=179)  
⚖️ *Both the AV and the other driver made poor decisions leading to the crash. Mutual misjudgment observed.*

---

### 📌 Annotation Notes

- Annotate fault based on **behavioral evidence in the video**, not just outcomes.
- If the AV makes a legal maneuver but fails to detect/respond adequately, it may still be labeled at fault.
- In complex situations, label as `both` when mutual errors clearly contribute to the incident.


---

## 💥 Variable: `TYPE_OF_IMPACT` — Collision Configuration

### 📘 Definition  
This variable describes the relative direction and position of the vehicles involved at the moment of impact. It helps classify crash geometry and impact severity.

---

### 🧩 Label Options

| Value                          | Description                                       |
|--------------------------------|---------------------------------------------------|
| `front_to_front`               | Two vehicles collided head-on                     |
| `front_to_rear`                | One vehicle rear-ended another                   |
| `front_to_side`                | Front of one vehicle hit the side of another     |
| `rear_to_rear`                 | Rear-to-rear collision (e.g., chain reaction)     |
| `rear_to_side`                 | Rear of one vehicle hit the side of another      |
| `sideswipe_opposite`          | Glancing contact in opposite directions          |
| `sideswipe_same`              | Glancing contact in the same direction (lane drift) |

---

### 🎬 Video Examples (Click to View)

#### 1. `front_to_front`
[![Front to Front](https://img.youtube.com/vi/6jSMxcnTklo/0.jpg)](https://youtu.be/6jSMxcnTklo?t=489)  
🚗🚗 *Two vehicles directly collide head-on.*

---

#### 2. `front_to_rear`
[![Front to Rear](https://img.youtube.com/vi/HD0dz8G-2sM/0.jpg)](https://youtu.be/HD0dz8G-2sM?t=2752)  
🚗➡️🚗 *AV crashes into the rear of a stopped or slower vehicle.*

---

#### 3. `front_to_side`
[![Front to Side](https://img.youtube.com/vi/yboO0LyliHY/0.jpg)](https://youtu.be/yboO0LyliHY?t=328)  
🚗➡️🚙 *Front of the AV collides into the side of a cross-traffic vehicle.*

---

#### 4. `rear_to_rear`
[![Rear to Rear](https://img.youtube.com/vi/IjFsu5mirkw/0.jpg)](https://youtu.be/IjFsu5mirkw?t=179)  
🚙↩️↩️🚙 *Rear bump occurs between two following vehicles.*

---

#### 5. `rear_to_side`
[![Rear to Side](https://img.youtube.com/vi/Nh4sTJjKfq0/0.jpg)](https://youtu.be/Nh4sTJjKfq0?t=351)  
🚙↩️➡️🚗 *Rear of one vehicle strikes the side of another (often at low speed).*

---

#### 6. `sideswipe_opposite`
[![Sideswipe Opposite](https://img.youtube.com/vi/66IApMK6F5Y/0.jpg)](https://youtu.be/66IApMK6F5Y?t=435)  
↔️ *Vehicles traveling in opposite directions brush against each other.*

---

#### 7. `sideswipe_same`
[![Sideswipe Same](https://img.youtube.com/vi/_KMALXm8-hs/0.jpg)](https://youtu.be/_KMALXm8-hs?t=492)  
➡️➡️ *Vehicles traveling in the same direction make lateral contact (e.g., lane drift).*

---

### 📌 Annotation Notes

- Focus on the **first point of contact** between vehicles, not secondary impacts.
- For multi-vehicle crashes, annotate the **main AV-to-object contact**.
- “Sideswipe” does not imply high damage but indicates motion alignment and partial contact.

---

## 🚗 Variable: `TOTAL_NUMBER_OF_VEHICLES` — Total Number of Vehicles Involved

### 📘 Definition  
This variable counts the total number of vehicles directly involved in the crash event. It helps characterize the scale and complexity of the incident.

- A "vehicle involved" refers to any road user that physically contacted or directly contributed to the collision sequence.

---

### 🧮 Example

#### Multi-Vehicle Crash — 3 Vehicles Involved  
[![Three Vehicles](https://img.youtube.com/vi/ecGSJVRCvC4/0.jpg)](https://youtu.be/ecGSJVRCvC4?t=17)  
🚗🚗🚗 *This crash involves three vehicles in a chain-reaction rear-end collision. All three vehicles sustained some level of damage.*

---

### 📌 Annotation Notes

- Do **not** count vehicles that simply witnessed the crash or stopped nearby.
- For sideswipe crashes involving several glancing contacts, count **all physically contacted** vehicles.
- In rare edge cases with trailers or towed equipment, count each **motor vehicle unit** separately。

---

## 🧱 Variable: `CRASH_WITH` — Object of Collision

### 📘 Definition  
This variable identifies what the autonomous vehicle (AV) collided with during the incident. It distinguishes among road users, static obstacles, and infrastructure elements.

---

### 🧩 Label Options

| Value           | Description                                            |
|------------------|--------------------------------------------------------|
| `vehicle`        | Collision with another moving or parked vehicle        |
| `bicycle`        | Collision with a cyclist or stationary bicycle         |
| `animal`         | Collision with a wild or domestic animal               |
| `infrastructure` | Collision with objects like poles, fences, or barriers |

---

### 🎬 Video Examples (Click to View)

#### 1. `vehicle` — AV collides with another car
[![Vehicle Collision](https://img.youtube.com/vi/1pZZPvgmas0/0.jpg)](https://youtu.be/1pZZPvgmas0?t=20)  
🚗💥🚗 *AV collides with another vehicle during a merge maneuver.*

---

#### 2. `bicycle` — AV hits a bicycle or cyclist
[![Bicycle Collision](https://img.youtube.com/vi/2-Oxtnh6noA/0.jpg)](https://youtu.be/2-Oxtnh6noA?t=446)  
🚲💥 *AV strikes a moving cyclist on the crosswalk.*

---

#### 3. `animal` — AV collides with an animal
[![Animal Collision](https://img.youtube.com/vi/okj2SdV6vDE/0.jpg)](https://youtu.be/okj2SdV6vDE?t=496)  
🦌 *AV crashes into an animal that suddenly enters the road.*

---

#### 4. `infrastructure` — AV hits road infrastructure
[![Infrastructure Collision](https://img.youtube.com/vi/7sWL7IKVL7Q/0.jpg)](https://youtu.be/7sWL7IKVL7Q?t=719)  
🛑 *AV collides with a fixed object such as a pole or barrier.*

---

### 📌 Annotation Notes

- In multi-object crashes, label based on **initial point of contact**.
- If the AV swerves and hits infrastructure while avoiding another object, use **the actual collision target**.
- “Infrastructure” includes curbs, cones, signs, fences, and poles.

---

## 🚘 Variable: `AV_MODEL` — Size Category of Autonomous Vehicle

### 📘 Definition  
This variable classifies the **autonomous vehicle (AV)** by its size category, rather than its specific make or model. This helps in analyzing visibility, stopping distances, and crash severity potential.

> ⚠️ **Note**: Since many videos are from first-person AV camera views, **visual identification may not be possible**. Please refer to **on-screen captions or text** for vehicle model details whenever available.

---

### 🧩 Label Options

| Value     | Description                                 | Includes                        |
|-----------|---------------------------------------------|---------------------------------|
| `small`   | Compact vehicles                            | sedan, coupe                    |
| `medium`  | Mid-size vehicles                           | SUV, pickup truck              |
| `large`   | Heavy or commercial vehicles                | truck, bus, van                |
| `unknown` | Model or size not visible or mentioned      | —                               |

---

### 🎬 Video Example

#### `medium` — Pickup Truck (identified via caption)
[![Pickup Truck](https://img.youtube.com/vi/nDHxO6HrHGc/0.jpg)](https://youtu.be/nDHxO6HrHGc?t=1056)  
🛻 *This AV is a pickup truck. The caption at timestamp 17:36 explicitly mentions the model. Classified as `medium`.*

---

### 📌 Annotation Notes

- Use **captions or speaker narration** as the primary source of vehicle type.
- If only the **vehicle’s shadow or mirror** is visible, **label as `unknown`**.
- If captions state the AV is a "bus" or "semi-truck," label as `large`.

---

## 🧱 Notes on Collision Damage Variables: Primary Impact Area

### 📘 Definition  
The following two variables describe the **primary damaged area** of the autonomous vehicle (AV) resulting from a collision.

These variables are designed to help characterize crash dynamics, system vulnerabilities, and AV structural exposure. They only capture the **first and most significant point of damage** on the AV.

---

### ⚠️ Important Annotation Rule

If the incident involves **multiple impacts**, only the **first damaged region** of the AV should be recorded, regardless of secondary collisions or resulting deformations.

This rule ensures labeling consistency and prioritizes the initial failure or exposure point in crash analysis.

---

<p align="center">
  <img src="SAVeD/main_damage_area.png" width="500"/>
  <br>
  <em>Figure: Illustration of main damage areas of an autonomous vehicle (AV).<br>
  Only the first damaged area should be labeled, even in cases with multiple collisions.</em>
</p>

---

