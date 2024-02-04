import cv2
import uuid
from PIL import Image


def find_maximum_contour(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.equalizeHist(gray_img)
    gray_img = cv2.GaussianBlur(gray_img, (3, 3), 4)
    gray_img = cv2.Canny(gray_img, 115, 255)
    contours, hierarchy = cv2.findContours(gray_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_axes = (0, 0)
    max_contour = None

    for k, contour in enumerate(contours):
        min_rect = cv2.minAreaRect(contour)
        if min_rect[1][0] * min_rect[1][1] > min_axes[0] * min_axes[1]:
            max_contour = contour
            min_axes = min_rect[1]

    return max_contour


def rotate_image(img, rect):
    angle = rect[2]
    center = rect[0]

    if rect[1][0] < rect[1][1]:
        angle -= 90

    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated_image = cv2.warpAffine(img, rotation_matrix, (img.shape[1], img.shape[0]))

    return rotated_image


def crop_image(img, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = img[y:y + h, x:x + w]
    return cropped_image


def rotate_and_crop(source_path="", dest_path=""):
    img = cv2.imread(source_path)

    contour = find_maximum_contour(img)
    min_rect = cv2.minAreaRect(contour)
    img = rotate_image(img, min_rect)

    contour = find_maximum_contour(img)
    img = crop_image(img, contour)

    img = cv2.resize(img, (800, 500), interpolation=cv2.INTER_AREA)

    cv2.imwrite(dest_path, img)


def paste_watermark(source_path="", dest_path=""):
    img = Image.open(source_path)
    icon = Image.open('./static/asset/watermark/watermark.png')

    width, height = img.size
    if width < height:
        img = img.transpose(Image.Transpose.ROTATE_90)
    img = img.resize((800, 500))

    img.paste(icon, (0, 0), icon)
    img.save(dest_path)


def id_card_processed_pipline(id_card):
    fid = uuid.uuid4()
    file_path = f'./static/asset/id_card/{fid}.jpg'
    id_card.save(file_path)

    rotate_and_crop(file_path, file_path)
    paste_watermark(file_path, file_path)
    return file_path
