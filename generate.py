#!/usr/bin/env python
# coding=utf8

# Generates S-12 PDF files from given OSM file.

import cairo
import json
import argparse
import re
import os

class Generator:

    CONFIG="config.json"

    def __init__(self):
        self.cfg = None
        self.read_config(self.CONFIG)

    def read_config(self, filename):
        f = open(filename, 'r')
        data = f.read()
        f.close()
        self.cfg = json.loads(data)

    def parse_input(self, filename):
        f = open(filename, 'r')
        content = f.read()
        f.close()
        numbers = []
        p_number = re.compile('tag k="number" v="(.*)"')
        p_name = re.compile('tag k="name" v="(.*)"')
        numbers = p_number.findall(content)
        names = p_name.findall(content)
        cards = []
        for i in range(0, len(names)):
            if len(names[i]) or len(numbers[i]):
                cards.append({ 'name': names[i], 'number': numbers[i] })
        return cards

    def generate(self, cards, output_directory):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        for card in cards:
            filename = os.path.join(output_directory, self._gen_filename(card))
            self._create_pdf(card, filename)

    def _gen_filename(self, card):
        filename = "%s%s.pdf" % (card['name'], card['number'])
        return filename

    def _create_pdf(self, card, filename):
        surface = cairo.PDFSurface(filename,
            self.cfg['paper']['width'], self.cfg['paper']['height'])
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(0.0, 0.0, 0.0)
        ctx.select_font_face(self.cfg['font']['face'], cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        ctx.set_font_size(self.cfg['font']['size'])

        ctx.move_to(self.cfg['name']['x'], self.cfg['name']['y'])
        ctx.show_text(card['name'])

        ctx.move_to(self.cfg['number']['x'], self.cfg['number']['y'])
        ctx.show_text(card['number'])
        surface.finish()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='S-12 generator')
    parser.add_argument('-i', '--osm_file', required=True)
    parser.add_argument('-d', '--directory', required=False, default=".")
    args = parser.parse_args()

    g = Generator()
    cards = g.parse_input(args.osm_file)
    g.generate(cards, args.directory)
    print "%d PDF files generated" % (len(cards))
    print "Now you can combine wanted PDF files into one:"
    print "pdftk *.pdf cat output output.pdf"

