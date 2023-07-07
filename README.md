# EPR Zoning Calculator

## Downloading

Go to the [latest release](https://github.com/OctaveAcoustics/epr-zoning/releases/latest) and download the .exe. Download the spreadsheet from the repository (or the Spreadsheet Tools sharepoint folder), and place in the same folder as the executable.

## How to use

Follow the steps for the chosen method. (Note: Print was removed May 2023 but is expected to be added back once the scale issue with the print output is fixed.)

### Export
1. Search property on https://mapshare.vic.gov.au/vicplan/ to centre it in the screen.
2. Turn up opacity of Zones layer and turn other layers off.
3. Set scale to fit 400m diameter circle on screen (200m radius from the property).
4. Export as PNG, save as "image.png", and place in the same folder as the executable/script.
5. Run EPRzoning.py and select the chosen scale when prompted.
6. If you get "Error: Exported image is too small", zoom out in VicPlan, re-export image and try again.
6. Check spreadsheet and fill in any missing zone types.

### Print
1. Search property on https://mapshare.vic.gov.au/vicplan/ to centre it in the screen.
2. Turn up opacity of Zones layer and turn other layers off.
3. Set scale to 1:2257.
4. Print as high resolution A2 PNG, save as "image.png", and place in the same folder as the executable/script.
5. Run EPRzoning.py.
6. Check spreadsheet and fill in any missing zone types.
