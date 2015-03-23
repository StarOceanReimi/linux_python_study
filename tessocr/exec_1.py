import cv2.cv as cv
import tesseract

TESSDATA_PATH = '/usr/local/share/tessdata'

api = tesseract.TessBaseAPI()
api.Init(TESSDATA_PATH, 'eng', tesseract.OEM_DEFAULT)
api.SetPageSegMode(tesseract.PSM_AUTO)

def image_text(imagepath):
    image = cv.LoadImage(imagepath, cv.CV_LOAD_IMAGE_GRAYSCALE)
    tesseract.SetCvImage(image, api)
    text = api.GetUTF8Text()
    conf = api.MeanTextConf()
    return text, conf

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    print image_text(args[0])

