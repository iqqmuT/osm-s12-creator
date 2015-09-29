# osm-s12-creator

## Usage
`python generate.py -i OSM_FILE.osm -d output_dir`

This will create PDF file for each area in OSM_FILE.osm. You can combine all PDF files into one big PDF file with `pdftk` tool:

`pdftk *.pdf cat output output.pdf`

## Requirements
Pycairo (Python Cairo)
