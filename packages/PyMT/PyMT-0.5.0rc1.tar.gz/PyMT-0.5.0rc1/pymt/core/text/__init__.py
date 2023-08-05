'''
Text: Handle drawing of text
'''

__all__ = ('LabelBase', 'Label')

import pymt
import re
import os
from pymt.core import core_select_lib
from pymt.baseobject import BaseObject

DEFAULT_FONT = 'Liberation Sans,Bitstream Vera Sans,Free Sans,Arial, Sans'

label_font_cache = {}

class LabelBase(BaseObject):
    '''Core text label.
    This is the abstract class used for different backend to render text.

    .. warning::
        The core text label can't be changed at runtime, you must recreate one.

    :Parameters:
        `font_size`: int, default to 12
            Font size of the text
        `font_name`: str, default to DEFAULT_FONT
            Font name of the text
        `bold`: bool, default to False
            Activate "bold" text style
        `italic`: bool, default to False
            Activate "italic" text style
        `size`: list, default to (None, None)
            Add constraint to render the text (inside a bounding box)
            If no size is given, the label size will be adapted from the text size.
        `anchor_x`: str, default to "left"
            Indicate what represent the X position inside the bounding box.
            Can be one of "left", "center", "right".
        `anchor_y`: str, default to "bottom"
            Indicate what represent the Y position inside the bounding box.
            Can be one of "top", "middle", "bottom".
        `padding`: int, default to None
            If it's a integer, it will set padding_x and padding_y
        `padding_x`: int, default to 0
            Left/right padding
        `padding_y`: int, default to 0
            Top/bottom padding
        `halign`: str, default to "left"
            Horizontal text alignement inside bounding box
        `valign`: str, default to "bottom"
            Vertical text alignement inside bounding box
        `color`: list, default to (1, 1, 1, 1)
            Text color in (R, G, B, A)
    '''

    __slots__ = ('options', 'texture', '_label', 'color', 'usersize')

    _cache_glyphs = {}

    def __init__(self, label, **kwargs):
        kwargs.setdefault('font_size', 12)
        kwargs.setdefault('font_name', DEFAULT_FONT)
        kwargs.setdefault('bold', False)
        kwargs.setdefault('italic', False)
        kwargs.setdefault('size', (None, None))
        kwargs.setdefault('anchor_x', 'left')
        kwargs.setdefault('anchor_y', 'bottom')
        kwargs.setdefault('halign', 'left')
        kwargs.setdefault('valign', 'bottom')
        kwargs.setdefault('padding', None)
        kwargs.setdefault('padding_x', 0)
        kwargs.setdefault('padding_y', 0)
        kwargs.setdefault('color', (1, 1, 1, 1))

        padding = kwargs.get('padding', None)
        if type(padding) in (tuple, list):
            kwargs['padding_x'] = float(padding[0])
            kwargs['padding_y'] = float(padding[1])
        elif padding is not None:
            kwargs['padding_x'] = float(padding)
            kwargs['padding_y'] = float(padding)

        uw, uh = kwargs['size']
        if uw != None:
            kwargs['size'] = uw - kwargs['padding_x'] * 2, uh

        super(LabelBase, self).__init__(**kwargs)

        self._label     = None

        self.color      = kwargs.get('color')
        self.usersize   = kwargs.get('size')
        self.options    = kwargs
        self.texture    = None

        if 'font_name' in self.options:
            fontname = self.options['font_name']
            if fontname in label_font_cache:
                if label_font_cache[fontname] is not None:
                    self.options['font_name'] = label_font_cache[fontname]
            else:
                filename = os.path.join(pymt.pymt_data_dir, fontname)
                if os.path.exists(filename):
                    label_font_cache[fontname] = filename
                    self.options['font_name'] = filename
                else:
                    label_font_cache[fontname] = None

        self.label      = label

    def get_extents(self, text):
        '''Return a tuple with (width, height) for a text.'''
        return (0, 0)

    def _render_begin(self):
        pass

    def _render_text(self, text, x, y):
        pass

    def _render_end(self):
        pass

    def render(self, real=False):
        '''Return a tuple(width, height) to create the image
        with the user constraints.

        2 differents methods are used:
          * if user don't set width, splitting line
            and calculate max width + height
          * if user set a width, blit per glyph
        '''

        uw, uh = self.usersize
        w, h = 0, 0
        x, y = 0, 0
        if real:
            self._render_begin()

        # no width specified, faster method
        if uw is None:
            for line in self.label.split('\n'):
                lw, lh = self.get_extents(line)
                if real:
                    x = 0
                    if self.options['halign'] == 'center':
                        x = int((self.width - lw) / 2.)
                    elif self.options['halign'] == 'right':
                        x = int(self.width - lw)
                    self._render_text(line, x, y)
                    y += int(lh)
                else:
                    w = max(w, int(lw))
                    h += int(lh)

        # constraint
        else:
            # precalculate id/name
            if not self.fontid in self._cache_glyphs:
                self._cache_glyphs[self.fontid] = {}
            cache = self._cache_glyphs[self.fontid]

            if not real:
                # verify that each glyph have size
                glyphs = list(set(self.label))
                for glyph in glyphs:
                    if not glyph in cache:
                        cache[glyph] = self.get_extents(glyph)

            # first, split lines
            glyphs = []
            lines = []
            lw = lh = 0
            for word in re.split(r'( |\n)', self.label):

                # calculate the word width
                ww, wh = 0, 0
                for glyph in word:
                    gw, gh = cache[glyph]
                    ww += gw
                    wh = max(gh, wh)

                # is the word fit on the uw ?
                if ww > uw:
                    lines.append(((ww, wh), word))
                    lw = lh = x = 0
                    continue

                # get the maximum height for this line
                lh = max(wh, lh)

                # is the word fit on the line ?
                if (word == '\n' or x + ww > uw) and lw != 0:

                    # no, push actuals glyph
                    lines.append(((lw, lh), glyphs))
                    glyphs = []

                    # reset size
                    lw = lh = x = 0

                    # new line ? don't render
                    if word == '\n':
                        continue

                # advance the width
                lw += ww
                x  += ww
                lh = max(wh, lh)
                glyphs += list(word)

            # got some char left ?
            if lw != 0:
                lines.append(((lw, lh), glyphs))

            if not real:
                h = sum([size[1] for size, glyphs in lines])
                w = uw
            else:
                # really render now.
                y = 0
                for size, glyphs in lines:
                    x = 0
                    if self.options['halign'] == 'center':
                        x = int((self.width - size[0]) / 2.)
                    elif self.options['halign'] == 'right':
                        x = int(self.width - size[0])
                    for glyph in glyphs:
                        lw, lh = cache[glyph]
                        if glyph != '\n':
                            self._render_text(glyph, x, y)
                        x += lw
                    y += size[1]

        if not real:
            # was only the first pass
            # return with/height
            w = int(max(w, 1))
            h = int(max(h, 1))
            return w, h

        # get data from provider
        data = self._render_end()
        assert(data)

        # create texture is necessary
        if self.texture is None:
            self.texture = pymt.Texture.create(*self.size)
            self.texture.flip_vertical()
        elif self.width > self.texture.width or self.height > self.texture.height:
            self.texture = pymt.Texture.create(*self.size)
            self.texture.flip_vertical()
        else:
            self.texture = self.texture.get_region(0, 0, self.width, self.height)

        # update texture
        self.texture.blit_data(data)


    def refresh(self):
        '''Force re-rendering of the label'''
        # first pass, calculating width/height
        sz = self.render()
        self._size = sz
        # second pass, render for real
        self.render(real=True)
        self._size = sz[0] + self.options['padding_x'] * 2, \
                     sz[1] + self.options['padding_y'] * 2

    def draw(self):
        '''Draw the label'''
        if self.texture is None:
            return
        if not len(self.label):
            # it's a empty label, don't waste time to draw it
            return

        x, y = self.pos
        w, h = self.size
        anchor_x = self.options['anchor_x']
        anchor_y = self.options['anchor_y']
        padding_x = self.options['padding_x']
        padding_y = self.options['padding_y']

        if anchor_x == 'left':
            x += padding_x
        elif anchor_x in ('center', 'middle'):
            x -= w * 0.5
        elif anchor_x == 'right':
            x -= w + padding_x

        if anchor_y == 'bottom':
            y += padding_y
        elif anchor_y in ('center', 'middle'):
            y -= h * 0.5
        elif anchor_y == 'top':
            y -= h - padding_y

        alpha = 1
        if len(self.options['color']) > 3:
            alpha = self.options['color'][3]
        pymt.set_color(1, 1, 1, alpha, blend=True)
        pymt.drawTexturedRectangle(
            texture=self.texture,
            pos=(int(x), int(y)), size=self.texture.size)

    def _get_label(self):
        return self._label
    def _set_label(self, label):
        if label == self._label:
            return
        # try to automaticly decode unicode
        try:
            self._label = label.decode('utf8')
        except:
            try:
                self._label = str(label)
            except:
                self._label = label
        self.refresh()
    label = property(_get_label, _set_label, doc='Get/Set the label text')
    text = property(_get_label, _set_label, doc='Get/Set the label text')

    @property
    def content_width(self):
        '''Return the content width'''
        if self.texture is None:
            return 0
        return self.texture.width + 2 * self.options['padding_x']

    @property
    def content_height(self):
        '''Return the content height'''
        if self.texture is None:
            return 0
        return self.texture.height + 2 * self.options['padding_y']

    @property
    def content_size(self):
        '''Return the content size (width, height)'''
        if self.texture is None:
            return (0, 0)
        return (self.content_width, self.content_height)

    @property
    def fontid(self):
        '''Return an uniq id for all font parameters'''
        return str([self.options[x] for x in (
            'font_size', 'font_name', 'bold', 'italic')])

# Load the appropriate provider
Label = core_select_lib('text', (
    ('pygame', 'text_pygame', 'LabelPygame'),
    ('cairo', 'text_cairo', 'LabelCairo'),
    ('pil', 'text_pil', 'LabelPIL'),
))

