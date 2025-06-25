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
- `fog/smog/smoke` may also include wildfire smoke or industrial smog that significantly impairs AV sensors or human view.



