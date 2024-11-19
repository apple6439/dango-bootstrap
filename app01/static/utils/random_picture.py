from PIL import Image, ImageDraw, ImageFont
from random import randint, choice


# img = Image.new(mode='RGB', size=(120, 30), color=(255, 255, 255))
# draw = ImageDraw.Draw(img, mode='RGB')
# font = ImageFont.truetype('华文宋体.ttf', 18)
# draw.text((0, 0), '高薪春', 'red', font=font)
# with open('../img/code.png', 'wb') as f:
#     img.save(f, format='png')


def create_image():
    random_code = []

    def get_random_code():
        # 随机数字
        number = str(randint(0, 9))
        # 随机大写字母
        upper = chr(randint(65, 90))
        # 随机小写字母
        lower = chr(randint(97, 122))
        # 在生成的大小写字母和数字中随机获取一个
        code = choice([number, upper, lower])
        return code

    def get_color():
        # 随机的颜色
        return (randint(0, 255), randint(0, 255), randint(0, 255))

    # 创建图片对象
    image = Image.new(mode="RGB", size=(145, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('fonts/msyh.ttc', 24)  # 确保路径正确

    # 制作图片噪点
    for i in range(100):
        draw.point([randint(0, 180), randint(0, 30)], fill=get_color())

    for i in range(10):
        draw.line([randint(0, 180), randint(0, 30), randint(0, 180), randint(0, 30)], fill=get_color())

    x = randint(0, 180)
    y = randint(0, 30)
    for i in range(10):
        draw.arc([x, y, x + 1, y + 1], 0, 90, fill=get_color())

    # 生成验证码
    for i in range(5):
        c = get_random_code()
        random_code.append(c)
        draw.text((5 + 30 * i, 2), text=c, fill=get_color(), font=font)

    code_string = ''.join(random_code)
    return image, code_string


create_image()
