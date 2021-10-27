#coding=utf-8
# Vistas de la interfaz de Voluntario
import os, sys, uuid, argparse
import cv2
from pathlib import Path
from shutil import copyfile
import glob
import PIL
from Models import NeuralModel, Soft_Light
from tqdm import tqdm
from facemakeup.custom_makeup import custom_hair_color
parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('input_image', metavar='Image', type=Path,
#                     help='The Image to Dye')
# parser.add_argument('color', metavar='Color', type=str,
#                     help='The color to dye the image')
# parser.add_argument('-o', "--output", default="generated.png",
#                     help='Output the image')
# parser.add_argument("--opacity", default=0.7, type=float,
#                     help='Opacity for the blend mode')
# custom code for arguments
parser.add_argument("--input_image", type=Path, default=None,
                    help='The Image to Dye')
parser.add_argument("--input_dir", type=Path,
                    help='The Image to Dye')
parser.add_argument("--color", type=str,
                    help='The Color of the image to dye')
parser.add_argument("--output", default="generated.png",
                    help='Output the image')
parser.add_argument("--opacity", default=0.7, type=float,
                    help='Opacity for the blend mode')
parser.add_argument("--lip_color", default ='red' ,
                    help='The Color of the image to dye')
                    
args = parser.parse_args()

COLORES = {"red":[255.,0.,0.],
"green":[0.,255.,0.], 
"blue" : [0.,0.,255.],
"pink":[255.,64.,195.], 
"white":[255.,255.,255.],
"black": [0.,0.,0.], 
"brown": [150.,75.,0.],
"light brown": [181.,101.,29.],
"espresso brown": [56., 32., 1.],
"reddish":[99.,61.,66.],
"Light Ash Blonde":[98.,94.,75.],
"Light Blonde":[250.,240.,190.],
"Light Golden Blonde":[255.,236.,139.],
"Medium Champagne":[109.,67.,44.],
"Butterscotch":[142.,116.,95.],
"Cool Brown":[215.,212.,208.],
"Light Brown":[97.,70.,50.],
"Light Golden Brown":[196.,156.,117.],
"Chocolate Brown":[87.,66.,55.],
"Dark Golden Brown":[69.,46.,42.],
"Espresso":[56., 32., 1.],
"Jet Black":[11.,11.,11.],
"Reddish Blonde":[111.,62.,34.],
"Light Auburn":[112.,65.,34.],
"Medium Auburn":[113.,49.,4.],
"Reddish Cinnamon":[121.,89.,111.]}
          
GENERATED = Path("./Output")
if not GENERATED.exists():
    GENERATED.mkdir()

def MainProgram(input_image, color, output_image, opacity,lip_color):
    UniqueID = uuid.uuid4().hex
    # ImgSaveFilename = (GENERATED/UniqueID).with_suffix(input_image.suffix)
    
    try:      
        image_ext = str(input_image).split('/')[-1].split('.')[-1]
        image_name = str(input_image).split('/')[-1].split('.')[-2]
        for colorName, colorRGB in tqdm(COLORES.items()):           
            ImgSaveFilename = (GENERATED/f"{image_name}_{colorName}_{UniqueID}.{image_ext}")
            image = cv2.imread(str(input_image))
            image_lip = custom_hair_color(image, lip_color=lip_color)
            # image_lip = custom_hair_color(image, hair_color='mahroon')

            
            # Img = PIL.Image.open(input_image)  # old code
            Img = PIL.Image.fromarray(image_lip)
            Img.save(ImgSaveFilename)
            OutFilename = ProcessImage(ImgSaveFilename, colorRGB, opacity)
            print(OutFilename)
            # copyfile(str(OutFilename), output_image)
            os.remove(ImgSaveFilename)
            print('Hair Colour and lipsing completed')
    except Exception as e:
        print("Program terminated due to")
        print(e)

def ProcessImage(ImageFileName, Color, opacity):
    # Pass through Neuro
    OutMask = NeuralModel.Forward(ImageFileName, Color)
    OutFileName = ImageFileName.with_name(str(ImageFileName.stem) + "Processed.png")

    # Color
    Soft_Light.ChangeColor(str(ImageFileName), str(OutMask), str(OutFileName), opacity)

    return OutFileName

if __name__ == "__main__":
    args = parser.parse_args()
    if args.input_image is None:
        img_list = os.listdir(args.input_dir)
        for img in img_list:
            img_path = os.path.join(args.input_dir, img)
            print(img_path)
            MainProgram(img_path, args.color, args.output, args.opacity,args.lip_color)
    else:
        MainProgram(args.input_image, args.color, args.output, args.opacity , args.lip_color)
