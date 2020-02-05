import os
import shutil
import PyPDF2
from PIL import Image
import pytesseract
import time

pdf_file_path = 'data_for_parse/8416_4.pdf'
# todo Отсортировать файлы jpg и pdf


def sort_files_pdf_or_jpg(catalog):
    for d, s, files in os.walk(catalog):
        print(f'{files}')
        for file in files:
            root, ext = os.path.splitext(file)
            print(f'{root} | {ext}')
            if ext == 'jpg':
                yield extract_number(os.path.join(d, file))
                print('jpg')
            elif ext == 'pdf':
                yield extract_pdf_image(os.path.join(d, file))
                print('pdf')
            else:
                print('None')

# todo Извлечь jpg из pdf и сохранить в папке изображений




# todo Отсортировать файлы jpg и pdf


# todo Извлечь jpg из pdf и сохранить в папке изображений
def extract_pdf_image(pdf_path):
    try:
        pdf_file = PyPDF2.PdfFileReader(open(pdf_path, "rb"), strict=False)
    except PyPDF2.utils.PdfReadError as e:
        return None
    except FileNotFoundError as e:
        return None

    result = []

    for page_num in range(0, pdf_file.getNumPages()):
        page = pdf_file.getPage(page_num)
        page_obj = page['/Resources']['/XObject'].getObject()
        if page_obj['/Im0'].get('/Subtype') == "/Image":
            size = (page_obj['/Im0']['/Width'], page_obj['/Im0']['/Height'])
            data = page_obj['/Im0']._data
            if page_obj['/Im0']['/ColorSpace'] == '/DeviceRGB':
                mode = 'RGB'
            else:
                mode = 'P'

            if page_obj['/Im0']['/Filter'] == '/FlateDecode':
                file_type = 'png'
            elif page_obj['/Im0']['/Filter'] == '/DCTDecode':
                file_type = 'jpg'
            elif page_obj['/Im0']['/Filter'] == '/JPXDecode':
                file_type = 'jp2'
            else:
                file_type = 'bmp'

            result_strict = {
                'page': page_num,
                'size': size,
                'data': data,
                'mode': mode,
                'file_type': file_type,
            }
            result.append(result_strict)

    return result


def save_pdf_image(file_name, f_path, *pdf_strict):
    for item in pdf_strict:
        name = f"{file_name}_#_{item['page']}.{item['file_type']}"

        with open(f"{f_path}/{name}", "wb") as image:
            image.write(item['data'])




# todo не забыть про формат имен файлов

# todo Извлеч номер кассы из поля

def extract_number(file_path):
    img_obj = Image.open(file_path)
    text = pytesseract.image_to_string(img_obj, 'rus')
    pattern = 'заводской (серийный) номер'
    pattern2 = 'заводской номер'
    result = []
    for idx, line in enumerate(text.split('\n')):
        if line.lower().find(pattern2) + 1 or line.lower().find(pattern) + 1:
            eng_text = pytesseract.image_to_string(img_obj, 'eng')
            number = eng_text.split('\n')[idx].split(' ')[-1]
            result.append(number)

    # todo при отсутсвии распознавания вернуть соответсвующее сообщение или error
    return result

# todo сохранить все в БД MONGO
file_name = '8416_4'
image_path = "data_for_parse/image"
img_file_path = 'data_for_parse/image/16.03.2019  (2).jpg'


if __name__ == '__main__':
    # pdf_result = extract_pdf_image(pdf_file_path)
    # save_pdf_image(file_name, image_path, *pdf_result)
    # res = extract_number(img_file_path)
    sort_files_pdf_or_jpg('/home/egor/python/parsing/æèä_Å«óÑα¬á óÑß«ó')
    print(1)
