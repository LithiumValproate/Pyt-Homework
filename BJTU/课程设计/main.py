# -*- coding: utf-8 -*-

import datetime

# --- 配置参数 ---
# 地铁计价规则
METRO_CONFIG = {
    "start_km": 4,
    "start_price": 2,
    "rules": [
        {"from": 4, "to": 12, "step": 4, "price": 1},
        {"from": 12, "to": 24, "step": 6, "price": 1},
        {"from": 24, "to": float('inf'), "step": 8, "price": 1}
    ],
    "avg_speed": 35  # km/h
}

# 城际计价规则
INTERCITY_CONFIG = {
    "start_km": 10,
    "start_price": 5,
    "rules": [
        {"from": 10, "to": 50, "step": 10, "price": 3},
        {"from": 50, "to": float('inf'), "step": 20, "price": 5}
    ],
    "avg_speed": 80  # km/h
}

# 其他规则
SAME_STATION_FREE_MINUTES = 20
TRANSFER_DISCOUNT = 1.5
TRANSFER_MAX_MINUTES = 60
MAX_FARE = 15  # 用于计算超时费用


# --- 核心计价函数 ---

def calculate_base_fare(distance, config):
    # 根据里程和配置计算基础票价
    if distance <= 0:
        return 0
    if distance <= config["start_km"]:
        return config["start_price"]

    price = config["start_price"]
    remaining_distance = distance - config["start_km"]

    # 查找规则并应用
    for rule in config["rules"]:
        # 当前规则段内的可计算里程
        distance_in_rule = min(remaining_distance, rule["to"] - rule["from"])
        if distance_in_rule > 0:
            # 向上取整计算费用
            price += -(-distance_in_rule // rule["step"]) * rule["price"]
            remaining_distance -= distance_in_rule
        if remaining_distance <= 0:
            break

    return price


def calculate_ticket_price(
        distance_km,
        trip_type="metro",
        user_type="adult",
        is_business_class=False,
        monthly_spent=0,
        entry_time=None,
        exit_time=None,
        is_same_station=False,
        is_transfer=False
):
    """
    计算最终票价的核心函数

    :param distance_km: 行程距离 (公里)
    :param trip_type: 行程类型 ('metro', 'intercity')
    :param user_type: 用户类型 ('adult', 'student', 'senior_peak', 'senior_offpeak', 'child', 'disabled')
    :param is_business_class: 是否为11号线商务车厢
    :param monthly_spent: 当月已消费金额
    :param entry_time: 进站时间 (datetime object)
    :param exit_time: 出站时间 (datetime object)
    :param is_same_station: 是否同站进出
    :param is_transfer: 是否为换乘行程
    :return: 最终票价 (元) 和 说明
    """

    # 1. 计算基础票价
    config = METRO_CONFIG if trip_type == "metro" else INTERCITY_CONFIG
    base_fare = calculate_base_fare(distance_km, config)
    final_price = base_fare
    explanation = [f"行程类型: {trip_type}, 距离: {distance_km}km, 基础票价: {base_fare:.2f}元"]

    # 2. 检查同站进出免费
    if is_same_station:
        duration_minutes = (exit_time - entry_time).total_seconds() / 60
        if duration_minutes <= SAME_STATION_FREE_MINUTES:
            explanation.append(
                f"同站进出且时长({duration_minutes:.1f}分钟)小于{SAME_STATION_FREE_MINUTES}分钟, 免收费用。")
            return 0, explanation
        else:
            explanation.append(
                f"同站进出但时长({duration_minutes:.1f}分钟)超过{SAME_STATION_FREE_MINUTES}分钟, 按单程最低票价收费。")
            final_price = config["start_price"]  # 如果同站超时，按最低票价

    # 3. 检查超时
    if entry_time and exit_time and not is_same_station:
        duration_minutes = (exit_time - entry_time).total_seconds() / 60
        allowed_minutes = (distance_km / config["avg_speed"]) * 60 + 45
        if duration_minutes > allowed_minutes:
            explanation.append(
                f"乘车超时(实际: {duration_minutes:.1f}分钟 > 规定: {allowed_minutes:.1f}分钟), 加收网络服务费{MAX_FARE:.2f}元。")
            return MAX_FARE, explanation

    # 4. 计算换乘优惠
    if is_transfer:
        final_price -= TRANSFER_DISCOUNT
        explanation.append(f"享受换乘优惠: -{TRANSFER_DISCOUNT:.2f}元")
        # 确保票价不为负
        final_price = max(0, final_price)

    # 5. 应用特殊人群折扣
    discount = 1.0
    if user_type == "student":
        discount = 0.5
        explanation.append("学生优惠: 5折")
    elif user_type == "senior_peak":
        discount = 0.5
        explanation.append("老人高峰时段优惠: 5折")
    elif user_type in ["senior_offpeak", "child", "disabled"]:
        explanation.append(f"{user_type} 免费乘坐。")
        return 0, explanation

    final_price *= discount

    # 6. 应用常旅客折扣
    if user_type == 'adult':  # 假设只有普通成人享受常旅客优惠
        if monthly_spent > 400:
            final_price *= 0.8
            explanation.append(f"月消费超400元, 享受8折优惠。")
        elif monthly_spent > 200:
            final_price *= 0.85
            explanation.append(f"月消费超200元, 享受8.5折优惠。")
        elif monthly_spent > 100:
            final_price *= 0.9
            explanation.append(f"月消费超100元, 享受9折优惠。")

    # 7. 计算商务车厢附加费
    if is_business_class:
        business_surcharge = base_fare * 2  # 附加费是基础票价的2倍
        final_price += business_surcharge
        explanation.append(f"11号线商务车厢附加费: +{business_surcharge:.2f}元")

    # 最终价格四舍五入到分
    final_price = round(final_price, 2)
    explanation.append(f"最终票价: {final_price:.2f}元")

    return final_price, "\n".join(explanation)


# --- 模拟场景 ---
if __name__ == "__main__":
    print("--- 场景1: 普通成人乘坐地铁 ---")
    price, desc = calculate_ticket_price(distance_km=15, trip_type="metro", user_type="adult")
    print(desc)
    print("-" * 30)

    print("--- 场景2: 学生乘坐城际铁路 ---")
    price, desc = calculate_ticket_price(distance_km=60, trip_type="intercity", user_type="student")
    print(desc)
    print("-" * 30)

    print("--- 场景3: 老人高峰期乘坐地铁 ---")
    price, desc = calculate_ticket_price(distance_km=8, trip_type="metro", user_type="senior_peak")
    print(desc)
    print("-" * 30)

    print("--- 场景4: 成人乘坐11号线商务车厢 (有月度消费) ---")
    price, desc = calculate_ticket_price(distance_km=35, trip_type="metro", user_type="adult", is_business_class=True,
                                         monthly_spent=250)
    print(desc)
    print("-" * 30)

    print("--- 场景5: 同站进出 (15分钟) ---")
    now = datetime.datetime.now()
    entry = now - datetime.timedelta(minutes=15)
    price, desc = calculate_ticket_price(distance_km=0, is_same_station=True, entry_time=entry, exit_time=now)
    print(desc)
    print("-" * 30)

    print("--- 场景6: 长时间短距离 (超时) ---")
    entry = datetime.datetime.now() - datetime.timedelta(hours=3)
    exit_t = datetime.datetime.now()
    price, desc = calculate_ticket_price(distance_km=5, trip_type="metro", user_type="adult", entry_time=entry,
                                         exit_time=exit_t)
    print(desc)
    print("-" * 30)

    print("--- 场景7: 地铁换乘城际 ---")
    # 分开计算再组合
    metro_dist = 10
    intercity_dist = 40
    # 地铁部分
    metro_fare, _ = calculate_ticket_price(metro_dist, "metro", "adult")
    # 城际部分 (享受换乘优惠)
    intercity_fare, _ = calculate_ticket_price(intercity_dist, "intercity", "adult", is_transfer=True)
    total_fare = metro_fare + intercity_fare
    print(f"地铁里程: {metro_dist}km, 票价: {metro_fare:.2f}元")
    print(f"城际里程: {intercity_dist}km, 享受换乘优惠后票价: {intercity_fare:.2f}元")
    print(f"总票价: {total_fare:.2f}元")
    print("-" * 30)
