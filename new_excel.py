import csv
import keyboard  # 引入keyboard库

# 定义字段和所有选项
fields = [
    ("URL", []),  # 自由填写
    ("time", []),  # 自由填写
    ("LIGHT_CONDITION 灯光情况", [
        "Dark – Lighted 黑暗-有灯光", "Dark - Not Lighted 黑暗-无灯光", "Dawn 黎明", "Daylight 白天", "Dusk 黄昏", "other"]),
    
    ("Weather 天气", [
        "Clear 晴天", "Cloudy 多云", "Fog Smog, Smoke 雾霾", "Rain 雨天", "Snow 雪天", "other"]),
    
    ("ROAD_SURFACE_CONDITION 道路状况", [
        "Dry 干燥", "Wet 湿滑", "Snow, Ice 雪地/冰面", "Oil Spill/Mud 油污泥泞" "other"]),
    
    ("Guilty 是否是过错方", [
        "Yes 是", "No 否", "Both at Fault", "other"]),
    
    ("Type_of_impact 碰撞类型", [
        "Front to Front 正面-正面", "Front to Rear 正面-追尾", "Rear to Rear 追尾-追尾", "front to side 头-追侧面",
        "Rear to Side 后-侧面", "Sideswipe, Opposite Direction 逆向擦碰", "Sideswipe, Same Direction 同向擦碰", "other"]),
    
    ("TOTAL_NUMBER_OF_VEHICLES 涉及车辆总数", ["0", "1", "2", "3", "4", "5", "over 5"]),
    
    ("Crash with 碰撞对象", [
        "Ped 行人", "Vehicle 车辆", "Bicycle 自行车", "Infrastructure 基础设施", "Animal 动物", "other"]),
    ("tesla model", [
        "s", "x", "3", "y", "truck", "idk"]),
    
    ("Most Damaged Area (AV) 自动驾驶车受损部位", [
        "Front Center Bumper 前中央保险杠", "Front Left Bumper 前左保险杠", "Front Right Bumper 前右保险杠",
        "Left Front Door 左前门", "Left Front Fender 左前挡泥板", "Left Rear Door 左后门", 
        "Left Rear Fender 左后挡泥板", "Overturn 翻车", "Rear Center Bumper 后中央保险杠", 
        "Rear Left Bumper 后左保险杠", "Rear Right Bumper 后右保险杠", "Right Front Door 右前门", 
        "Right Front Fender 右前挡泥板", "Right Rear Door 右后门", "Right Rear Fender 右后挡泥板",
        "Roof 车顶", "Undercarriage 底盘", "Windshield 挡风玻璃", "Rollover 翻滚", "Hit and Run 肇事逃逸", "other"]),
    
    ("Most Damaged Area (Other) 其他车受损部位", [
        "Front Center Bumper 前中央保险杠", "Front Left Bumper 前左保险杠", "Front Right Bumper 前右保险杠",
        "Left Front Door 左前门", "Left Front Fender 左前挡泥板", "Left Rear Door 左后门", 
        "Left Rear Fender 左后挡泥板", "Overturn 翻车", "Rear Center Bumper 后中央保险杠", 
        "Rear Left Bumper 后左保险杠", "Rear Right Bumper 后右保险杠", "Right Front Door 右前门", 
        "Right Front Fender 右前挡泥板", "Right Rear Door 右后门", "Right Rear Fender 右后挡泥板",
        "Roof 车顶", "Undercarriage 底盘", "Windshield 挡风玻璃", "Rollover 翻滚", "Hit and Run 肇事逃逸", "other"]),
    
    ("FSD or Not 是否使用自动驾驶", ["Autopilot 自动辅助驾驶", "FSD 完整自动驾驶", "idk", "other"]),
    
    ("Road_type 道路类型", [
        "Highway/Freeway 高速", "Local city 市区道路", "Signalized intersection 有红绿灯路口", "nonSignalized intersection 没有红绿灯路口", 
        "Parking lot 停车场", "Traffic Circle 环岛", "Rural Road 乡村道路", "Unpaved Road 土路", "Bridge 桥梁", "Tunnel 隧道", "workzone 工程区域", "other"]),
    
    ("Crash_type 碰撞类型", [
        "Angle 角度碰撞", "Head On 迎面碰撞", "Left Turn 左转事故", "Right Turn 右转事故", 
        "Sideswipe 擦碰", "Off Road 偏离道路", "Rear End 追尾", "Ped/Bicycle 行人/自行车", "other"]),
    
    ("Road_Flat 道路坡度", ["Yes 平坦", "Up 上坡", "Down 下坡", "other"]),
    
    ("hurt? 人员受伤", ["no", "Yes， not bad 受轻伤", "yes, bad 重伤", "dead 死亡", "idk不知道"]),
    
    ("Reason_碰撞原因", [
        "Failure to Yield 未礼让", "Following Too Closely 跟车太近", "Improper Lane Change 并线不当", 
        "Running Red Light 闯红灯", "Running Stop Sign 闯停车标志", "Improper Turn 转弯不当", 
        "Backing Without Caution 倒车不小心", "Wrong-way Driving 逆行", "Over-speeding 超速", 
        "Improper Passing 超车失误", "Slippery Road (Rain, Snow, Ice) 道路湿滑", 
        "Poor Visibility (Fog, Heavy Rain) 能见度低", "Road Surface Defect 路面破损", 
        "Animal on Road 道路有动物", "Sudden Pedestrian Movement 行人突然横穿", 
        "Unexpected AV Behavior 自动驾驶异常", "other"]),
    
    ("Crash_car_type 碰撞车辆类型", [
        "Big vehicle (BUS, TRUCK) 大型车", "Middle vehicle (Pickup/SUV) 中型车", "Small car 小型车", "Bike or Ped 自行车/行人", "other"]),
    
    ("What AV Pre Crash Movement 事发时AV的动作", [
        "Stopped 停止", "Proceeding Straight 直行", "Making Right Turn 右转", "Making Left Turn 左转", 
        "Making U-Turn 掉头", "Backing 倒车", "Passing 超车", "Changing Lanes 变道", 
        "Parking Maneuver 停车", "Entering Traffic 进入车流", "Crossing into Opposing Lane 驶入对向", 
        "Parked 停路边", "Traveling Wrong Way 逆行", "other"]),
    
    ("What another car Pre Crash Movement 事发时对方车动作", [
        "Stopped 停止", "Proceeding Straight 直行", "Making Right Turn 右转", "Making Left Turn 左转", 
        "Making U-Turn 掉头", "Backing 倒车", "Passing 超车", "Changing Lanes 变道", 
        "Parking Maneuver 停车", "Entering Traffic 进入车流", "Crossing into Opposing Lane 驶入对向", 
        "Parked 停路边", "Traveling Wrong Way 逆行", "other"]),
    
    ("What AV did to Avoid Crash AV为了避撞的动作", ["Right turn 右转", "Left turn 左转", "Decelerating 减速", "Accelerating 加速", "No Action 无动作", "other"]),
    
    ("What another car did to Avoid Crash 对方为了避撞的动作", ["Right turn 右转", "Left turn 左转", "Decelerating 减速", "Accelerating 加速", "No Action 无动作", "other"]),
    
    ("AV Avoid Time (s) AV避撞提前几秒", []),  # 自由填写秒数
    ("Another Car Avoid Time (s) 另一车避撞提前几秒", []),
    
    ("Location of Crash 事故地点描述", []),  # 自由填写
    
    ("单向几条车道", ["1lane 1条", "2lane2条", "3lane3条", "over 4 lane条及以上"]),
    
    ("交通流 Traffic Flow", ["Congested 拥堵", "Red Light Stopped 红灯停车", "Moderate Traffic 车辆适中", "Light Traffic 车辆较少", "other"]),
    
    ("How Much to Fix 维修费用估算", []),  # 自由填写
    ("备注", []),  # 自由填写
]

csv_file = "output_labels_almost.csv"

# 如果第一次运行，创建文件并写标题行
try:
    with open(csv_file, "x", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([field[0] for field in fields])
except FileExistsError:
    pass  # 文件存在就跳过

print("\n🚀 开始标注完整记录，每次填写一条～\n")

# 用于保存上一个问题的索引
history = []

# 循环标注
while True:
    row = []
    for idx, (field_name, options) in enumerate(fields):
        history.append(idx)  # 保存当前字段的索引
        if options:  # 如果有固定选项
            print(f"\n请选择 {field_name}:")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            while True:
                print("按Esc键返回上一个问题")
                try:
                    choice = int(input("输入对应的数字: "))
                    if 1 <= choice <= len(options):
                        break
                    else:
                        print("⚠️ 请输入有效的数字范围！")
                except ValueError:
                    print("⚠️ 请输入数字！")
                if keyboard.is_pressed("esc"):
                    print("⏪ 返回上一个问题")
                    history.pop()  # 移除当前的问题
                    break
            selected_option = options[choice - 1]
        else:  # 自由填写
            selected_option = input(f"\n请输入 {field_name}: ").strip()
        row.append(selected_option)

    # 保存到CSV
    with open(csv_file, "a", newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    print("记录已保存！\n")

    # 提问是否继续
    if keyboard.is_pressed("esc"):
        print("⏪ 退出标注")
        break
