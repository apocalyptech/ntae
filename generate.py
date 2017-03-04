#!/usr/bin/python
# vim: set expandtab tabstop=4 shiftwidth=4:

import os
import jinja2
from PIL import Image

class VariantImage(object):
    """
    A single NTAE variant image
    """

    def __init__(self, filename, sheet):
        """
        Loads ourselves and sets up some convenience vars.  Will generate
        a thumbnail automatically if one isn't found.
        """

        # Basic vars
        self.filename = filename
        self.image_file = os.path.join(sheet.directory, filename)
        self.thumb_file = os.path.join(sheet.thumbdir, filename)

        # Attribution vars
        self.attributions = []

        # Open the image to get width/height
        im = Image.open(self.image_file)
        self.width = im.width
        self.height = im.height

        # Create a thumbnail if we need to
        if not os.path.exists(self.thumb_file):
            print('Generating %s' % (self.thumb_file))
            im.thumbnail((200, 200))
            im.save(self.thumb_file)

        # Close the image
        im.close()

    def add_attribution(self, info_filename):
        """
        Adds some attribution information to ourselves, from a text
        file.
        """

        with open(info_filename, 'r') as df:
            for line in df.readlines():
                self.attributions.append(line.strip().split(': '))

    def has_attributions(self):
        """
        Jinja convenience function
        """
        return len(self.attributions) > 0

class Variant(object):
    """
    A variant of a sheet
    """

    def __init__(self, sheet, ident, desc):
        self.sheet = sheet
        self.ident = ident
        self.desc = desc
        self.front = []
        self.back = []
        self.prefix_front = '%s_fr_' % (ident)
        self.prefix_back = '%s_bk_' % (ident)
        self.read_and_thumbnail_files()

    def read_and_thumbnail_files(self):
        """
        Looks in our directory for any files which match, and also
        generates thumbnails for any file we find.  Also also populates
        our 'sizes' dict.  This is rather inefficient since os.listdir()
        will get called against a sheet directory for every single
        variant the sheet has, but of course given the data size we have,
        we can be as inefficient as we want.  Yay?

        All the actual work actually happens in the VariantImage class.
        """

        # Read in our files
        for filename in sorted(os.listdir(self.sheet.directory)):
            if filename[:len(self.prefix_front)] == self.prefix_front:
                if filename[-4:] == '.txt':
                    self.front[-1].add_attribution(os.path.join(self.sheet.directory, filename))
                else:
                    self.front.append(VariantImage(filename, self.sheet))
            elif filename[:len(self.prefix_back)] == self.prefix_back:
                if filename[-4:] == '.txt':
                    self.back[-1].add_attribution(os.path.join(self.sheet.directory, filename))
                else:
                    self.back.append(VariantImage(filename, self.sheet))

    def loop_images(self):
        """
        Convenience function for Jinja to simplify templating a bit.
        Returns a list of tuples, and will be of the following form:
            [ ('Front', self.front) ]
        or:
            [ ('Front', self.front), ('Back', self.back) ]
        """
        l = [ ('Front', self.front) ]
        if len(self.back) > 0:
            l.append(('Back', self.back))
        return l

    def has_front(self):
        """
        Convenience function for Jinja
        """
        return len(self.front) > 0

    def has_back(self):
        """
        Convenience function for Jinja
        """
        return len(self.back) > 0

class Sheet(object):
    """
    A sheet - there are seven here (one for each song, one cover,
    one credits)
    """

    def __init__(self, directory, name):
        self.directory = directory
        self.thumbdir = os.path.join(directory, 'thumbs')
        self.name = name
        self.variants = []
        if not os.path.exists(self.thumbdir):
            os.mkdir(self.thumbdir)

    def add_variant(self, ident, desc):
        var = Variant(self, ident, desc)
        self.variants.append(var)
        return var

class App(object):

    def __init__(self):

        self.sheets = []

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
        self.template = env.get_template('main.html')

    def run(self):

        warning = self.new_sheet('warning', 'Envelope Warning')
        warning.add_variant('common', 'Identical on all packages')

        cover = self.new_sheet('00_cover', 'Cover')
        cover.add_variant('clear', 'Clear Transparency')

        track01 = self.new_sheet('01_branches_bones', '01. Branches/Bones')
        track01.add_variant('blue', 'Blue with black text')
        track01.add_variant('white', 'White with black text')

        track02 = self.new_sheet('02_dear_world', '02. Dear World,')
        track02.add_variant('black', 'Black with white text')
        track02.add_variant('green', 'Green with black text')
        track02.add_variant('white', 'White with black text')

        track03 = self.new_sheet('03_shes_gone_away', '03. She\'s Gone Away')
        track03.add_variant('black', 'Black with white text')
        track03.add_variant('red', 'Red with blue text')

        track04 = self.new_sheet('04_the_idea_of_you', '04. The Idea of You')
        track04.add_variant('bluered', 'Blue with red text')
        track04.add_variant('white', 'White with black text')

        track05 = self.new_sheet('05_burning_bright', '05. Burning Bright (Field on Fire)')
        track05.add_variant('white', 'White with black text')
        track05.add_variant('multicolor', 'White with multicolored text')
        track05.add_variant('blackred', 'Black with red text')

        credits = self.new_sheet('06_credits', 'Credits')
        credits.add_variant('white', 'White with black text, portrait (has a faint NIN logo / Halo designation on back)')
        credits.add_variant('blue', 'Blue/Purple with white text, portrait (has a faint NIN logo / Halo designation on back)')
        credits.add_variant('black', 'Black with white text, landscape (NIN logo / Halo designation may be present but extremely faint)')

        page_content = self.template.render({
            'sheets': self.sheets,
        })
        with open('index.html', 'w') as df:
            df.write(page_content)

        print('Wrote out index.html!')

    def new_sheet(self, directory, name):

        sheet = Sheet(directory, name)
        self.sheets.append(sheet)
        return sheet

if __name__ == '__main__':
    app = App()
    app.run()
