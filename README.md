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
[![Shared Fault](https://img.youtube.com/vi/IjFsu5mirkw/0.jpg)](https://www.youtube.com/watch?v=IjFsu5mirkw)  
⚖️ *Both the AV and the other driver made poor decisions leading to the crash. Mutual misjudgment observed.*

---

### 📌 Annotation Notes

- Annotate fault based on **behavioral evidence in the video**, not just outcomes.
- If the AV makes a legal maneuver but fails to detect/respond adequately, it may still be labeled at fault.
- In complex situations, label as `both` when mutual errors clearly contribute to the incident.



