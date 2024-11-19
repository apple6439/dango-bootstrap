import random
import string
import time


def generate_order_number(prefix='ORD', length=6):
    """生成一个随机订单号，带有前缀和时间戳

    参数:
    prefix -- 订单号的前缀 (默认为 'ORD')
    length -- 随机部分的长度 (默认为6)

    返回:
    随机生成的订单号字符串
    """
    characters = string.ascii_uppercase + string.digits
    # 生成随机部分
    random_part = ''.join(random.choice(characters) for _ in range(length))
    # 获取当前时间戳
    timestamp = int(time.time())
    # 返回组合后的订单号
    return f"{prefix}-{timestamp}-{random_part}"


if __name__ == "__main__":
    print(generate_order_number())
    print(generate_order_number(length=8))
