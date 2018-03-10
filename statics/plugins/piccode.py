from PIL import Image,ImageDraw,ImageFilter,ImageFont
import random
def piccode(width,height,complex=30,code_num = 6):
    '''
    生成随机验证图片
    :param width: 图片宽度
    :param height: 图片高度
    :param complex: 干扰复杂度
    :param code_num: 验证码个数
    :return:
    '''
    def rancolor():
        '''
        随机颜色
        :return:
        '''
        color = random.randint(0,255),random.randint(0,255),random.randint(0,255)
        return color


    # 创建图片、画笔
    img = Image.new(mode="RGB",size=(width,height),color=rancolor())
    draw = ImageDraw.ImageDraw(img,"RGB")

    #干扰
    for i in range(complex):
        # 画点
        draw.point(xy=[random.randint(0,width),random.randint(0,height)],
                   fill=(rancolor()))
    # 画线
    for i in range(4):
        draw.line(xy=(random.randint(0,width),random.randint(0,height),random.randint(0,width),random.randint(0,height)),
                  fill=(rancolor()),
                  width=random.randint(0,20))

    # 画字
    code_width = width/code_num
    code_list = []
    font = ImageFont.truetype('kumo.ttf',28)
    for i in range(code_num):
        text_code = chr(random.randint(97,122))
        code_list.append(text_code)
        draw.text(xy=[i*code_width,0],text=text_code,font=font)
    # 调节对比度
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img,''.join(code_list)



