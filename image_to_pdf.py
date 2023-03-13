import sys
from tkinter import Tk
from tkinter.filedialog import askopenfilenames
from typing import Optional

from PIL import Image
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg


def images_picker(source_type: str) -> tuple:
    Tk().withdraw()

    file_types = [
        ('document', '*.svg')
    ] if source_type == 'svg' else [
        ('image', '*.jpeg'),
        ('image', '*.jpg'),
        ('image', '*.png'),
    ]
    images: tuple = askopenfilenames(filetypes=file_types)
    return images


def save_as_pdf(source_type: Optional[str]) -> None:
    picked_images: tuple = images_picker(source_type)

    if picked_images:
        file_path = '/'.join(picked_images[0].split('/')[:-1])
        file_name = ''.join(picked_images[0].split('/')[-1:]).split('.')[0]

        if 'svg' == source_type:
            for n, image in enumerate(picked_images, start=1):
                draw = svg2rlg(image)
                renderPDF.drawToFile(draw, f'{file_path}/{file_name} ({n}).pdf')
        else:
            image_list = [Image.open(image).convert('RGB') for image in picked_images]
            image_list[0].save(
                f'{file_path}/{file_name}.pdf',
                save_all=True,
                append_images=image_list[1:]
            )

        print('generated!')


def usage_message(n):
    usage = f'\n\nUsage:\n  python image_to_pdf.py --[options]\n'\
            f'\nOptions:\n  None (default)    generate with image files\n' \
            f'  --svg    generate with svg files\n\n' \
            f'no such option: {sys.argv[n] if len(sys.argv) > n else None}'
    return usage


format_argument = sys.argv[1] if len(sys.argv) > 1 else None

if format_argument:
    if '-' not in format_argument:
        raise Exception(usage_message(1))

    elif 'svg' not in format_argument:
        raise Exception(usage_message(1))

    format_argument = 'svg'

save_as_pdf(source_type=format_argument)
