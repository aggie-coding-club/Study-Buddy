#PIL is from the Pillow library
import io
import os
import PIL
from PIL import Image
from google.cloud import vision
import requests

#TODOs
#Use JSON text coordinates to find highlights
#Filter out background and text colors

#Returns true or false depending on whether the two colors are similar enough based on the tolerance parameter
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
        
#Recursive function for finding the top left coordinates and bottom right coordinates of individual blocks of highlighting
def recursiveFindHighlightBlock(image, color, tolerance, x, y, xStep, yStep, topLeft, bottomRight, visitedMatrix):
    if x < 0 or y < 0 or x >= image.width or y >= image.height or visitedMatrix[x][y]:
        return
    if not compareColors(image.getpixel((x,y)), color, tolerance):
        visitedMatrix[x][y] = True
        return

    visitedMatrix[x][y] = True
    
    if x < topLeft[0]:
        topLeft[0] = x
    if y < topLeft[1]:
        topLeft[1] = y
    if x > bottomRight[0]:
        bottomRight[0] = x
    if y > bottomRight[1]:
        bottomRight[1] = y
    
    recursiveFindHighlightBlock(image, color, tolerance, x + xStep, y, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x - xStep, y, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x, y + yStep, xStep, yStep, topLeft, bottomRight, visitedMatrix)
    recursiveFindHighlightBlock(image, color, tolerance, x, y - yStep, xStep, yStep, topLeft, bottomRight, visitedMatrix)
        

#Scans image with a step size depending on image size and uses Google Vision OCR and Google Dictionary API on highlighted words
def findHighlightedWordDefinitions(path):
    selected_image = PIL.Image.open(path)
    
    #Variables for image width and height
    image_width = selected_image.width
    image_height = selected_image.height
    
    #colorList's format is [[R,G,B], # of pixel instances]
    colorList = []
    
    colorScanTolerance = 100
    highlightColorTolerance = 50
    
    #Sets initial scan step size to 1
    stepSizeX = 1
    stepSizeY = 1
    
    #Adjusts scan step size to be 1/200 of the width/height of the image in case the image is massive
    if selected_image.width > 200:
        stepSizeX = round(image_width / 200)
    if selected_image.height > 200:
        stepSizeY = round(image_height / 200)
    
    #Scans for colors in the image, averages out RGB values, and records their frequency
    #Scans the whole image with step sizes based on stepSizeX and stepSizeY
    for x in range(0, image_width, stepSizeX):
        for y in range(0, image_height, stepSizeY):
            colorMatch = False
            #For each pixel scanned, look through the color list and compare the current pixel's color.
            #If there's a color that's close enough, average together the colorList color's RGB values 
            #and the current pixel's RGB values. Also +1 to the number of instances of that color.
            for color in colorList:
                if compareColors(selected_image.getpixel((x,y)), color[0],colorScanTolerance):
                    color[0][0] = round(color[0][0]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[0] / color[1])
                    color[0][1] = round(color[0][1]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[1] / color[1])
                    color[0][2] = round(color[0][2]*((color[1]-1)/color[1]) + selected_image.getpixel((x,y))[2] / color[1])
                    color[1] += 1
                    colorMatch = True
                    break;
            #Otherwise, if the current pixel's color isn't close to one already in the list, add it onto the list
            if not colorMatch:
                colorList.append([list(selected_image.getpixel((x,y))), 1])

    print("Color frequency: ")
    for i in colorList:
        print(i)
    

    
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
    
    
    #Uses Google Vision OCR on each saved image and find definitions for highlighted words
    imageCount = 0
    wordList = []
    definitionList = []
    
    for color in coordinatesList:
        imageCount += 1
        wordList.append(detect_document("./Images/Processing Images/" + str(imageCount) + ".jpg"))
        
    wordList = list(dict.fromkeys(wordList))
    
    for word in wordList:
        definitionList.append([word, findDefinition(word)])
        
    while [None, None] in definitionList:
        definitionList.remove([None, None])
        
    for i in definitionList:
        print(i)
    
    #Returns list of lists with the inner lists' first element being the word and its second element being a list of definitions
    return definitionList
            
        
    
#Google Vision function that returns words in an image as strings as long as they're only single words
def detect_document(path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="acc-study-buddy-2ca6d1c6098d.json"
    
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
                                
                        return word_text
    else:
        return
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

#Gives bounding boxes and other information
def detect_text(path):
    """Detects text in the file."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="acc-study-buddy-2ca6d1c6098d.json"
    
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))
        
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
                
    return texts


#Requests dictionary data from Google Dictionary and returns a list of definitions for a given word
def findDefinition(word):
    if not (type(word) is str):
        return
    queryResult = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en/" + word)
    editedResult = queryResult.text.replace("\",\"","},{")
    response = editedResult.split("},{")
    definitionList = []
    

    
    for i in range(len(response)):
        if "definitions\":" in response[i]:
            response[i] = response[i][13:]
    


    for i in response:
        if "definition" in i:
            definitionIndex = 1
            while "[{\"definition\"" in i.split(":")[definitionIndex]:
                definitionIndex += 1
            temp = i.split("\":\"")[definitionIndex]
            if "\"}]}]}]" in temp:
                temp = temp[:-7]
            if temp[-2:] == ".\"":
                temp = temp[:-1]

            definitionList.append(temp)
    
    return definitionList


#findHighlightedWordDefinitions("Images/MultipleHighlightsImage.jpg")
detect_text("Images/MultipleHighlightsImage.jpg")
#detect_document("Images/Processing Images/2.jpg")
#findDefinition("type")
