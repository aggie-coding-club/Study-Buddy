#PIL is from the Pillow library
import io
import os
import PIL
from PIL import Image
from google.cloud import vision


def find_highlights(path):
    selected_image = PIL.Image.open(path)
    highlightedWords = []
    
    stepSizeX = 1
    stepSizeY = 1
    
    if selected_image.height > 200:
        stepSizeX = round(selected_image.height / 200)
    if selected_image.width > 200:
        stepSizeY = round(selected_image.width / 200)
    
    searcherX = 0
    searcherY = 0
    
    print(stepSizeX)
    print(stepSizeY)
    
    #Find the number of highlighted words
    #while not (searcherX == selected_image.width and searcherY == selected_image.height):
    #    print(selected_image.getpixel((10,10)))

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

find_highlights("Images/IMG_3200.jpg")
#detect_document("Images/IMG_3200.jpg")
