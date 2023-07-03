# Import plugins - Image to deal with pixel counting, math for math(duh), tqdm for the timer seen by the user
# pathlib as a robust method of acessing local files, and openpyxl for population of excel spreadsheets
from PIL import Image
import math as math
from tqdm import tqdm
from pathlib import Path
import openpyxl

"""
Streamlining ideas

if the tool doesn't find anything (the image in the folder or zones)- don't close, give a warning!

"""

# Define zone names and colours (RGB). Note that zone colours and names have to be defined at the same indice
ZoneNames =["RDZ1" , "NRZ", "ACZ1", "RDZ2", "PUZ4", "PUZ", "GRZ", "RCZ3", "PPRZ", "IN3Z", "IN1Z","MUZ","RGZ","C1Z","C2Z","UFZ","B2Z", "PCRZ", "SUZ","UGZ2","CCZ", "LDRZ", "GWZ2","CDZ3","CA","TRZ1","TRZ2","TRZ3","TRZ4", "The Sea (no zone)","FZ"]
ZoneColours = [(240,0,176),(255, 209, 204),(153, 204, 204),(255, 176, 0), (227, 227, 227), ( #"RDZ1" , "NRZ1", "ACZ1", "RDZ2", "PUZ4"
    255, 255, 153),(255, 181, 207),(204, 204, 0),(161, 219, 178), (191,89,26), (240,176,130),( #"PUZ", "GRZ", "RCZ3", "PPRZ", "IN3Z", "IN1Z"
    217,  77,  77),(255, 153,204),(240,217, 250), (194,140,178), (153,227,255), (224,181,242), ( #"MUZ","RGZ","C1Z","C2Z","UFZ","B2Z"
    97, 204, 38), (222, 250, 138),(238, 180, 180),(25, 255, 235),(255, 166, 153),(204, 204, 153),( #"PCRZ", "SUZ5?","UGZ2","CCZ", "LDRZ", "GWZ2"
    0,189,194),(255,255,255),(200,205,215),(110,120,145),(140,150,185),(215,225,235),(230,246,255),(# "CDZ3","CA","TRZ1 (formerly PUZ4)","TRZ2 (formerly RDZ1)","TRZ3 (formerly RDZ2)","TRZ4 (formerly PUZ4)", "The Sea (no zone) (literally the sea)
    222,255,237)] # FZ

# Fill arrays used with zeroes
Zone200Count = [0]*len(ZoneNames)
Zone70Count =  [0]*len(ZoneNames)
Zone200Prop =  [0]*len(ZoneNames)
Zone70Prop =   [0]*len(ZoneNames)
Zone200Area =  [0]*len(ZoneNames)
Zone70Area =   [0]*len(ZoneNames)

def exit_message(msg=""):
    if msg:
        print(msg)
    input("Press Enter to close")
    exit()

# Open the planning map image
script_location = Path(__file__).absolute().parent
file_location = script_location / 'image.png'
try:
    im = Image.open(file_location)
except:
    exit_message("Error: image.png not found")

# check if printed or exported
if im.width == 7016 and im.height == 4962:
    # printed as high res A2 png @ 1:2257
    print("Processing printed image")
    box = (1005, 479, 6891, 4265)
    im = im.crop(box) # crop to the map
    im.show()
    im.save(script_location / "crop.png")
    scale = 4.725 # pixels per m
else:
    print("Processing exported image")
    map_scales = [2257, 4514, 9028, 18056]
    print("Choose map scale: ")
    for i in range(len(map_scales)):
        print(f"{i+1}. 1:{map_scales[i]}")
    selected = input("Input scale [1-4] and press Enter: ")
    if not selected:
        selected = 1 # default to 1:2257
    map_scale = map_scales[int(selected)-1]
    print(f"Selected scale 1:{map_scale}")

    # calculate the pixel scale
    scale = 2.114*(2257.0/map_scale) # pixels per m

# Initialise EPR spreadsheet
sheet_name = 'EPR 2021 Mech Noise Limit, Assessment & Report tool (r5).xlsx'

# Define the centre of the circle
pixelX = round(im.width/2)
pixelY = round(im.height/2)

radius200 = round(200*scale)
radius70 = round(70*scale)
total200Pix = math.pi * radius200**2
total70Pix = math.pi * radius70**2

if (im.height < (radius200*2)):
    exit_message("Error: Exported image is too small")

# Define the area of the two circles in m2 (for error checking)
area200 = math.pi * 200**2
area70 = math.pi * 70**2

# Initialise
total200CountedPix = 0
total70CountedPix = 0

# loop through the square defined by the diameter of the 200m circle. Note tqdm here is the progress bar seen in the command prompt
for j in tqdm(range(pixelY-radius200,pixelY+radius200)):
    for i in range(pixelX-radius200,pixelX+radius200):

        # Retreive the RGB info for the current pixel in the nested loop
        currentPix = im.getpixel((i,j))[0:3]

        # Check if the pixel is within the 200m circle
        if ((math.fabs(i-pixelX))**2 + (math.fabs(j-pixelY))**2) < radius200**2:
            for zone in range(0,len(ZoneNames)):

                # If the pixel is within the circle, check if the colour matches anything in the ZoneColours array. If it does, add a count to its respective indice.
                # Also, colour the output pixel to show that it's been found.
                if(currentPix == (ZoneColours[zone])):
                    Zone200Count[zone]+=1
                    im.putpixel((i,j),(255,255,255))
                    total200CountedPix+=1

        # Do the same but for the 70m circle (yes I know we're double dipping on the pixels for 70m and 70m within the 200m and it would be easy to do both at the same time, but leave me alone)
        if ((math.fabs(i-pixelX))**2 + (math.fabs(j-pixelY))**2) < radius70**2:
            for zone in range(0,len(ZoneNames)):
                if(currentPix == (ZoneColours[zone])):
                    Zone70Count[zone]+=1
                    im.putpixel((i,j),(150,150,150))
                    total70CountedPix+=1


# Find the 'error' in the counting. Check how many pixels were found over the possible theortical maximum (mostly zone boundaries and zone titles)
Zone70error = [x/total70Pix for x in Zone70Count]
Zone200error = [x/total200Pix for x in Zone200Count]
error200 = sum(Zone200error)
error70 = sum(Zone70error)

# Display and save final image
im.show()
im.save(script_location / "final_output.png")

# Turn this into a proportion
Zone70Prop = [x/total70CountedPix for x in Zone70Count]
Zone200Prop = [x/total200CountedPix for x in Zone200Count]

# Calculate the area in m2 from each individual pixel counted
Zone70Area = [x*area70 for x in Zone70Prop]
Zone200Area = [x*area200 for x in Zone200Prop]

# Open/write txt file with information in it
f = open(script_location /'output.txt','w')
f.write('')

# Display calculated areas for each zone
print("\n")
print("Done!\n ")
f.write("Done!\n")

print("For 70m circle:")
f.write("For 70m circle:\n")
for zone in range(0,len(ZoneNames)):
    if(Zone70Count[zone] != 0):
        print(ZoneNames[zone],"has an area of",Zone70Area[zone],"m2")
        f.write(str(ZoneNames[zone]) + " has an area of " + str(Zone70Area[zone]) + " m2\n")

print("\n")
f.write("\n")

print("for 200m circle")
f.write("for 200m circle\n")

for zone in range(0,len(ZoneNames)):
    if(Zone200Count[zone] != 0):
        print(ZoneNames[zone],"has an area of",Zone200Area[zone],"m2")
        f.write(str(ZoneNames[zone]) + " has an area of " + str(Zone200Area[zone]) + " m2\n")
        if(ZoneNames[zone] == "PUZ1,2 or 3"):
            print("Careful, there are PUZ1, 2,  3, 5, 6 or 7 zones in the circle's radius. Check to see what zone number they represent, and if there are any double ups!")
            f.write("Careful, there are PUZ1, 2, 3, 5, 6 or 7 zones in the circle's radius. Check to see what zone number they represent, and if there are any double ups!\n")

print("\n")
f.write("\n")

print("The percentage of identified pixels in 70m circle is", error70*100,"%")
f.write("The percentage of identified pixels in 70m circle is " + str(error70*100) + "%\n")

print("The percentage of identified pixels in 200m circle is", error200*100,"%")
f.write("The percentage of identified pixels in 200m circle is " + str(error200*100) + "%\n")

print("\n")
f.write("\n")

# open epr excel sheet
sheet_location = script_location / sheet_name

if (sheet_location.exists()):
    print("Found EPR Excel workbook. Populating spreadsheet now...")
    book = openpyxl.load_workbook(script_location / sheet_name)
    sheet = book['EPR2021 Assessment & Report']
    count = 0

    # empty input areas
    for cell in range(5,25):
            sheet['B' + str(cell)].value = None
            sheet['D' + str(cell)].value = None
            sheet['E' + str(cell)].value = None
            sheet['G' + str(cell)].value = None

    # populate zone and area in spreadsheet (yes i'm using a counter, you do it instead)
    for zone in range(0,len(ZoneNames)):
        if(Zone70Count[zone] != 0):
            sheet['B' + str(count+5)].value = ZoneNames[zone]
            sheet['D' + str(count+5)].value = Zone70Area[zone]
            count = count + 1
    count = 0

    for zone in range(0,len(ZoneNames)):

        if(Zone200Count[zone] != 0):
            sheet['E' + str(count+5)].value = ZoneNames[zone]
            sheet['G' + str(count+5)].value = Zone200Area[zone]
            count = count + 1

    # save sheet
    book.save(script_location / sheet_name)
    print("Spreadsheet populated!")
else:
    print("EPR Excel workbook not found. Spreadsheet not populated.")

# Do some housekeeping
print("\n")
f.write("\n")
f.close()

# wait for input from the user before closing the command prompt, in case they want to read anything
exit_message()