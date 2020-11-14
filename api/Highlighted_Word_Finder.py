#PIL is from the Pillow library
import io
import os
import PIL
from PIL import Image
from google.cloud import vision

#Returns whether the two colors are similar enough based on the tolerance parameter
def compareColors(colorList_1,colorList_2,tolerance):
    
    redDistance = abs(colorList_1[0] - colorList_2[0])
    blueDistance = abs(colorList_1[1] - colorList_2[1])
    greenDistance = abs(colorList_1[2] - colorList_2[2])
    
    RGBdistance = (redDistance**2 + blueDistance**2 + greenDistance**2)**(0.5)
    
    if RGBdistance < tolerance:
        return True
    else:
        return False

#Does a scan of an image with a step size depending on image size and uses Google Vision OCR on highlighted words
def find_highlighted_words(path):
    selected_image = PIL.Image.open(path)
    image_width = selected_image.height
    image_height = selected_image.width
    colorList = []
    
    colorScanTolerance = 105
    highlightColorTolerance = 50
    
    stepSizeX = 1
    stepSizeY = 1
    
    if selected_image.height > 200:
        stepSizeX = round(image_width / 200)
    if selected_image.width > 200:
        stepSizeY = round(image_height / 200)
    
    #Scans for colors in the image and records their frequency
    for x in range(0, image_width, stepSizeX):
        for y in range(0, image_height, stepSizeY):
            colorMatch = False
            for color in colorList:
                if compareColors(selected_image.getpixel((y,x)), color[0],colorScanTolerance):
                    color[0][0] = round(color[0][0]*((color[1]-1)/color[1]) + selected_image.getpixel((y,x))[0] / color[1])
                    color[0][1] = round(color[0][1]*((color[1]-1)/color[1]) + selected_image.getpixel((y,x))[1] / color[1])
                    color[0][2] = round(color[0][2]*((color[1]-1)/color[1]) + selected_image.getpixel((y,x))[2] / color[1])
                    color[1] += 1
                    colorMatch = True
                    break;
            if not colorMatch:
                colorList.append([list(selected_image.getpixel((y,x))), 1])
            
        
    for i in colorList:
        print(i)
    
    #Finds coordinates of top left and bottom right of each color
    coordinatesList = []
    for color in colorList:
        coordinatesList.append([color[0], image_width, image_height, 0, 0])
        
    for x in range(0, image_width, stepSizeX):
        for y in range(0, image_height, stepSizeY):
            for color in coordinatesList:
                if compareColors(selected_image.getpixel((y,x)), color[0], highlightColorTolerance):
                    if x < color[1]:
                        color[1] = x
                    if x > color[3]:
                        color[3] = x
                    if y < color[2]:
                        color[2] = y
                    if y > color[4]:
                        color[4] = y
                        
    for i in coordinatesList:
        print(i)
    
    #TODO: Scan coordinate blocks to filter out unhighlighted text
    for color in coordinatesList:
        totalStepCount = 0
        matchingStepCount = 0
        for x in range(color[1], color[3], stepSizeX):
            for y in range(color[2], color[4], stepSizeY):
                totalStepCount += 1
                if compareColors(selected_image.getpixel((y,x)), color[0], highlightColorTolerance):
                    matchingStepCount += 1
        if (matchingStepCount / totalStepCount) < 0.5:
            coordinatesList.remove(color)
            
    for i in coordinatesList:
        print(i)
    
    #TODO: Scan to adjust highlight coordinates to account for text sticking out of the highlight
    
    
    #TODO: Color areas outside of coordinate blocks white and save as new images for each coordinate block
    
    
    #TODO: Use Google Vision OCR on each saved image
    
    

def detect_document(path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service_account_token.json"
    
    client = vision.ImageAnnotatorClient()
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock confidence: {}\n'.format(block.confidence))

            for paragraph in block.paragraphs:
                print('Paragraph confidence: {}'.format(
                    paragraph.confidence))

                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    print('Word text: {} (confidence: {})'.format(
                        word_text, word.confidence))

                    for symbol in word.symbols:
                        print('\tSymbol: {} (confidence: {})'.format(
                            symbol.text, symbol.confidence))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

find_highlighted_words("Images/IMG_3200.jpg")
#detect_document("Images/IMG_3200.jpg")
