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

#Detects whether the first color is significantly darker than the second color based on the tolerance percentage
def detect_darker_color(possibleDarkerColor, lightColor, tolerancePercentage):
    if possibleDarkerColor[0] + possibleDarkerColor[1] + possibleDarkerColor[2] < (lightColor[0] + lightColor[1] + lightColor[2]) * tolerancePercentage:
        return True
    else:
        return False
        
def recursiveFindHighlightBlock(image, color, tolerance, x, y, xStep, yStep, topLeft, bottomRight, visitedMatrix):
    if x < 0 or y < 0 or x >= image.width or y >= image.height or visitedMatrix[x][y]:
        return
    if not compareColors(image.getpixel((x,y)), color, tolerance):
        visitedMatrix[x][y] = True
        return

    visitedMatrix[x][y] = True
    
    #print("Old: " + str(topLeft) + ", " + str(bottomRight))
    changed = False
    
    if x < topLeft[0]:
        topLeft[0] = x
        changed = True
    if y < topLeft[1]:
        topLeft[1] = y
        changed = True
    if x > bottomRight[0]:
        bottomRight[0] = x
        changed = True
    if y > bottomRight[1]:
        bottomRight[1] = y
        changed = True
    
    #if changed:
    #    print("New: " + str(topLeft) + ", " + str(bottomRight))
    
    recursiveFindHighlightBlock(image, color, tolerance, x + xStep, y, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x - xStep, y, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x, y + yStep, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x, y - yStep, xStep, yStep, topLeft, bottomRight, visitedMatrix)
        

#Does a scan of an image with a step size depending on image size and uses Google Vision OCR on highlighted words
#TODO: Adjust code to handle multiple highlighted words
def find_highlighted_words(path):
    selected_image = PIL.Image.open(path)
    image_width = selected_image.width
    image_height = selected_image.height
    colorList = []
    
    colorScanTolerance = 100
    highlightColorTolerance = 50
    overflowTextContrastTolerance = 0.9
    overflowTextHeightMultiplier = 0.35
    
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
                if compareColors(selected_image.getpixel((x,y)), color[0],colorScanTolerance):
                    color[0][0] = round(color[0][0]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[0] / color[1])
                    color[0][1] = round(color[0][1]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[1] / color[1])
                    color[0][2] = round(color[0][2]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[2] / color[1])
                    color[1] += 1
                    colorMatch = True
                    break;
            if not colorMatch:
                colorList.append([list(selected_image.getpixel((x,y))), 1])
            
        
    print("Color frequency: ")
    for i in colorList:
        print(i)
    
    #Finds coordinates of top left and bottom right of each color
    coordinatesList = []
    for color in colorList:
        coordinatesList.append([color[0], image_width, image_height, 0, 0])
        
    for x in range(0, image_width, stepSizeX):
        for y in range(0, image_height, stepSizeY):
            for color in coordinatesList:
                if compareColors(selected_image.getpixel((x,y)), color[0], highlightColorTolerance):
                    if x < color[1]:
                        color[1] = x
                    if x > color[3]:
                        color[3] = x
                    if y < color[2]:
                        color[2] = y
                    if y > color[4]:
                        color[4] = y
                        
    print("Initial highlight coordinates: ")
    for i in coordinatesList:
        print(i)
        
    
    #TODO: Separate multiple highlighted words 
    
    tempCoordinatesList = []
    for color in coordinatesList:
        #visitedMatrix = [[False] * image_width for _ in range(image_height)]
        print("Color: " + str(color[0]))
        visitedMatrix = [[False] * image_height for _ in range(image_width)]
        for x in range(color[1], color[3], stepSizeX * 6):
            for y in range(color[2], color[4], stepSizeY * 6):
                topLeft = [color[3],color[4]]
                bottomRight = [color[1],color[2]]
                if not (visitedMatrix[x][y]):
                    recursiveFindHighlightBlock(selected_image, color[0], highlightColorTolerance, x, y, stepSizeX * 6, stepSizeY * 6, topLeft, bottomRight, visitedMatrix)
                if not ([color[0],topLeft[0],topLeft[1],bottomRight[0],bottomRight[1]] in tempCoordinatesList) and not (topLeft[0] == color[3] and topLeft[1] == color[4] and bottomRight[0] == color[1] and bottomRight[1] == color[2]) and not (topLeft[0] == bottomRight[0] or topLeft[1] == bottomRight[1]):
                    #print("individualBlock is " + str(topLeft) + ", " + str(bottomRight))
                    #print("fullBlock is (" + str(color[1]) + "," + str(color[2]) + ") , (" + str(color[3]) + "," + str(color[4]) + ")")
                    tempCoordinatesList.append([color[0],topLeft[0],topLeft[1],bottomRight[0],bottomRight[1]])
    
    coordinatesList = tempCoordinatesList

    
    print("Separated highlight coordinates: ")
    for i in coordinatesList:
        print(i)

    print("done")
    
    #Scans coordinate blocks to filter out unhighlighted text
    for color in coordinatesList:
        totalStepCount = 0
        matchingStepCount = 0
        for x in range(color[1], color[3], stepSizeX):
            for y in range(color[2], color[4], stepSizeY):
                totalStepCount += 1
                if compareColors(selected_image.getpixel((x,y)), color[0], highlightColorTolerance):
                    matchingStepCount += 1
        if (matchingStepCount / totalStepCount) < 0.5:
            coordinatesList.remove(color)
           
    print("Filtered highlight coordinates: ")
    for i in coordinatesList:
        print(i)
    
    
    #Checks for text sticking out of the highlight and adjusts highlight coordinates to account for it
    for color in coordinatesList:
        for x in range(color[1], color[3], stepSizeX):
            if detect_darker_color(selected_image.getpixel((x,color[2])), color[0], overflowTextContrastTolerance):
                color[2] = color[2] - ((color[4] - color[2]) * overflowTextHeightMultiplier)
            if detect_darker_color(selected_image.getpixel((x,color[4])), color[0], overflowTextContrastTolerance):
                color[4] = color[4] + ((color[4] - color[2]) * overflowTextHeightMultiplier)
                


    #Colors areas outside of coordinate blocks white and saves as new images for each coordinate block
    imageCount = 0
    for color in coordinatesList:
        imageCount += 1
        imageCopy = Image.new(selected_image.mode, selected_image.size)
        pixels = imageCopy.load()
        for x in range(0, image_width):
            for y in range(0, image_height):
                if(x < color[1] or x > color[3] or y < color[2] or y > color[4]):
                    pixels[x,y] = (255, 255, 255)
                else:
                    pixels[x,y] = selected_image.getpixel((x,y))
        imageCopy.save("./Images/Processing Images/" + str(imageCount) + ".jpg")
    
    
    #Uses Google Vision OCR on each saved image
    imageCount = 0
    for color in coordinatesList:
        imageCount += 1
        detect_document("./Images/Processing Images/" + str(imageCount) + ".jpg")
    

def detect_document(path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../../../StudyBuddyResources/service_account_token.json"
    
    client = vision.ImageAnnotatorClient()
    
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    #"""
    if len(response.full_text_annotation.pages) == 1 and len(response.full_text_annotation.pages[0].blocks) == 1 and len(response.full_text_annotation.pages[0].blocks[0].paragraphs) == 1 and len(response.full_text_annotation.pages[0].blocks[0].paragraphs[0].words) == 1:
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
    #"""
    """                        
    print(path)
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
    """
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

find_highlighted_words("Images/MultipleHighlightsImage.jpg")
#detect_document("Images/Processing Images/2.jpg")
