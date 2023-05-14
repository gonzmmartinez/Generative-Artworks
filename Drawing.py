from PIL import Image, ImageDraw, ImageFont
import random
import colorsys
import math

def random_color():
    h = random.random()
    s = 1
    v = 1

    float_rgb = colorsys.hsv_to_rgb(h, s, v)
    rgb = [int(x * 255) for x in float_rgb]

    return tuple(rgb)

def interpolate(start_color, end_color, factor: float):
    recip = 1 - factor
    return (
        int(start_color[0] * recip + end_color[0] * factor),
        int(start_color[1] * recip + end_color[1] * factor),
        int(start_color[2] * recip + end_color[2] * factor)
    )

def generate_art(path: str,artist_name: str):
    target_size_px = 1000
    scale_factor = 2
    image_size_px = target_size_px * scale_factor
    padding_px = int(image_size_px * 0.1)
    image_bg_color = (0, 0, 0, 0)
    start_color = (255,255,255)
    end_color = (255,255,255)
    image = Image.new('RGBA',
                      size=(image_size_px, image_size_px),
                      color=image_bg_color)

    # Dibujar lineas.
    draw = ImageDraw.Draw(image)
    points = []

    #Generar puntos
    limit = 250
    count = 0
    while len(points) <= 100:
        random_point = (random.randint(padding_px, image_size_px - padding_px),
                        random.randint(padding_px, image_size_px - padding_px))

        if (len(points)>=1):
            if (math.dist(points[count-1], random_point) <= limit):
                points.append(random_point)
                count += 1
            else:
                pass
        else:
            points.append(random_point)
            count += 1

    #Dibujar los puntos
    n_points = len(points) - 1
    for i, point in enumerate(points):
        point1 = point

        if (i == n_points):
            point2 = points[-1]
        else:
            point2 = points[i + 1]

        line_xy = (point1, point2)
        color_factor = i / n_points
        line_color = interpolate(start_color, end_color, color_factor)
        thickness = random.randint(5,10)
        draw.line(line_xy, fill=line_color, width = thickness)

    # Write artists name
    # create a drawing context
    draw = ImageDraw.Draw(image)

    # write the text
    for k in range(10):
        # set the font size and type
        font = ImageFont.truetype("arial.ttf", random.randint(50, 750))
        # set a random position
        text_color = (255, 255, 255, random.randint(85,255))
        position = (random.randint(0,1500),random.randint(0,1500))
        draw.text((position), artist_name, fill=text_color, font=font)

    image = image.resize((target_size_px, target_size_px), resample = Image.LANCZOS)
    image.save(path)

#if __name__ == "__main__":
#    generate_art(f"E:\Code\Projects\Gen2\Generaciones\Generation.png","Hola")