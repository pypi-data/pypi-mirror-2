"""
Color handling functions.
"""

__license__ = """
Copyright (C) 2006-2007  Gabor Csardi <csardi@rmki.kfki.hu>,
Tamas Nepusz <ntamas@rmki.kfki.hu>

MTA RMKI, Konkoly-Thege Miklos st. 29-33, Budapest 1121, Hungary

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc.,  51 Franklin Street, Fifth Floor, Boston, MA 
02110-1301 USA
"""

from math import ceil

__all__ = ["Palette", "GradientPalette", "AdvancedGradientPalette", \
    "PrecalculatedPalette", "ClusterColoringPalette", \
    "color_name_to_rgb", "palettes", "known_colors"]

class Palette(object):
    """Base class of color palettes.

    Color palettes are mappings that assign integers from the range
    0..M{n-1} to colors (3-tuples). M{n} is called the size or length
    of the palette. C{igraph} comes with a number of predefined palettes,
    so this class is useful for you only if you want to define your
    own palette. This can be done by subclassing this class and implementing
    the L{Palette._get} method as necessary.

    Palettes can also be used as lists or dicts, for the C{__getitem__}
    method is overridden properly to call L{Palette.get}.
    """
    def __init__(self, n):
        self._length = n
        self._cache = {}

    def _get_length(self): return self._length
    length = property(_get_length, "the length of the palette")
    def __len__(self): return self._length

    def clear_cache(self):
        """Clears the result cache.
        
        The return values of L{Palette.get} are cached. Use this method
        to clear the cache.
        """
        self._cache = {}

    def get(self, v):
        """Returns the given color from the palette.

        Values are cached: if the specific value given has already been
        looked upon, its value will be returned from the cache instead of
        calculating it again. Use L{Palette.clear_cache} to clear the cache
        if necessary.

        @note: you shouldn't override this method in subclasses, override
          L{_get} instead. If you override this method, lookups in the
          L{known_colors} dict won't work, so you won't be able to refer to
          colors by names or RGB triplets, only by integer indices. The
          caching functionality will disappear as well. However,
          feel free to override this method if this is exactly the behaviour
          you want.

        @param v: the color to be retrieved. If it is an integer, it is
          passed to L{Palette._get} to be translated to an RGB triplet.
          Otherwise it is passed to L{color_name_to_rgb()} to determine the
          RGB values.

        @return: the color as an RGB triplet"""
        if isinstance(v, list): v=tuple(v)
        try:
            return self._cache[v]
        except KeyError:
            pass
        if isinstance(v, int) or isinstance(v, long):
            if v<0: raise ValueError, "color index must be non-negative"
            if v>=self._length: raise ValueError, "color index too large"
            result=self._get(v)
        else:
            result=color_name_to_rgb(v)
        self._cache[v]=result
        return result

    def _get(self, v):
        """Override this method in a subclass to create a custom palette.

        You can safely assume that v is an integer in the range 0..M{n-1}
        where M{n} is the size of the palette.

        @param v: numerical index of the color to be retrieved
        @return: a 3-tuple containing the RGB values"""
        raise ValueError, "abstract class"

    __getitem__ = get


class GradientPalette(Palette):
    """Base class for gradient palettes

    Gradient palettes contain a gradient between two given colors.

    Example:
    
      >>> pal = GradientPalette("red", "blue",4)
      >>> pal.get(2)
      (0.5, 0., 0.5)
    """
    def __init__(self, color1, color2, n=256):
        """Creates a gradient palette.

        @param color1: the color where the gradient starts.
        @param color2: the color where the gradient ends.
        @param n: the number of colors in the palette.
        """
        Palette.__init__(self, n)
        self._color1 = color_name_to_rgb(color1)
        self._color2 = color_name_to_rgb(color2)

    def _get(self, v):
        ratio = float(v)/(len(self)-1)
        return tuple([self._color1[x]*(1-ratio)+self._color2[x]*ratio for x in range(3)])


class AdvancedGradientPalette(GradientPalette):
    """Advanced gradient that consists of more than two base colors.
    
    Example:
    
      >>> pal = AdvancedGradientPalette(["red", "black", "blue"], n=8)
      >>> pal.get(2)
      (0.5, 0., 0.)
      >>> pal.get(7)
      (0., 0., 0.75)
    """

    def __init__(self, colors, indices=None, n=256):
        """Creates an advanced gradient palette

        @param colors: the colors in the gradient.
        @param indices: the color indices belonging to the given colors. If
          C{None}, the colors are distributed equally
        @param n: the total number of colors in the palette
        """
        Palette.__init__(self, n)

        if indices is None:
            indices = list(range(len(colors)))
            d = float(n-1) / (len(indices)-1)
            for i in xrange(len(colors)): indices[i] *= d
        elif not hasattr(indices, "__iter__"):
            indices = map(float, indices)
        d = zip(*sorted(zip(indices, colors)))
        self._colors = [color_name_to_rgb(c) for c in d[1]]
        self._indices = d[0]
        self._k = len(self._indices)-1
        self._dists = [self._indices[i+1]-self._indices[i] for i in xrange(self._k)]

    def _get(self, v):
        # Find where does v belong
        for i in xrange(self._k):
            if self._indices[i] <= v and self._indices[i+1] >= v:
                dist = self._dists[i]
                ratio = float(v-self._indices[i])/dist
                return tuple([self._colors[i][x]*(1-ratio)+self._colors[i+1][x]*ratio for x in range(3)])
        return (0., 0., 0.)


class PrecalculatedPalette(Palette):
    """A palette that returns colors from a pre-calculated list of colors"""

    def __init__(self, l):
        """Creates the palette backed by the given list. The list must contain
        RGB triplets or color names, which will be resolved first by
        L{color_name_to_rgb()}."""
        Palette.__init__(self, len(l))
        for idx, color in enumerate(l):
            if isinstance(color, (str, unicode)):
                color = color_name_to_rgb(color)
            self._cache[idx] = color

    def _get(self, v):
        """This method will only be called if the requested color index is
        outside the size of the palette. In that case, we throw an exception"""
        raise ValueError, "palette index outside bounds: %s" % v


class ClusterColoringPalette(PrecalculatedPalette):
    """A palette suitable for coloring vertices when plotting a clustering.

    This palette tries to make sure that the colors are easily distinguishable.
    This is achieved by using a set of base colors and their lighter and darker
    variants, depending on the number of elements in the palette.

    When the desired size of the palette is less than or equal to the number of
    base colors (denoted by M{n}), only the bsae colors will be used. When the
    size of the palette is larger than M{n} but less than M{2*n}, the base colors
    and their lighter variants will be used. Between M{2*n} and M{3*n}, the
    base colors and their lighter and darker variants will be used. Above M{3*n},
    more darker and lighter variants will be generated, but this makes the individual
    colors less and less distinguishable.
    """

    def __init__(self, n):
        base_colors = ["red", "green", "blue", "yellow", "magenta", "cyan", "#808080"]
        base_colors = map(color_name_to_rgb, base_colors)

        num_base_colors = len(base_colors)
        colors = base_colors[:]

        blocks_to_add = ceil(float(n - num_base_colors) / num_base_colors)
        ratio = 1.0 / (ceil(blocks_to_add / 2.0) + 1)

        adding_darker = True
        r = ratio
        while len(colors) < n:
            if adding_darker:
                new_block = [darken(color, r) for color in base_colors]
            else:
                new_block = [lighten(color, r) for color in base_colors]
                r += ratio
            colors.extend(new_block)
            adding_darker = not adding_darker

        colors = colors[0:n]
        PrecalculatedPalette.__init__(self, colors)


def _clamp(value, min, max):
    """Clamps the given value between min and max"""
    if value>max: return max
    if value<min: return min
    return value

def color_name_to_rgb(color, palette=None):
    """Converts a color given in one of the supported color formats to R-G-B values.

    Examples:

      >>> color_name_to_rgb("red")
      (1., 0., 0.)
      >>> color_name_to_rgb("#ff8000")
      (1., 0.50196078431372548, 0.)
      >>> color_name_to_rgb("#08f")
      (0., 0.53333333333333333, 1.)
      >>> color_name_to_rgb("rgb(100%, 50%, 0%)")
      (1., 0.5, 0.)

    @param color: the color to be converted in one of the following formats:
      - B{CSS color specification}: C{#rrggbb} or C{#rgb} or C{rgb(red, green, blue)}
        where the red-green-blue components are given as hexadecimal numbers in the
        first two cases and as decimals (in the range of 0-255) or percentages
        (0-100) in the third case. Of course these are given as strings.
      - B{Valid HTML color names}, i.e. those that are present in the HTML 4.0
        specification
      - B{Valid X11 color names}, see U{http://en.wikipedia.org/wiki/X11_color_names}
      - B{Red-green-blue components} given separately in either a comma-, slash- or
        whitespace-separated string or a list or a tuple, in the range of 0-255
      - B{A single palette index} given either as a string or a number. Uses
        the palette given in the C{palette} parameter of the method call.
    @param palette: the palette to be used if a single number is passed to
      the method. Must be an instance of L{colors.Palette}.

    @return: the R-G-B values corresponding to the given color in a 3-tuple.
      Since these colors are primarily used by Cairo routines, the tuples
      contain floats in the range 0.0-1.0
    """
    global known_colors

    if not isinstance(color, basestring):
        try:
            components = [c/255. for c in color]
        except TypeError:
            # A single index is given as a number
            try:
                components = palette.get(color)
            except AttributeError:
                raise ValueError, "palette index used when no palette was given"
    else:
        if color[0] == '#':
            color = color[1:]
            if len(color) == 3:
                components = [int(i, 16) * 17. / 255. for i in color]
            elif len(color) == 6:
                components = [int(color[(2*i):(2*i+2)], 16) / 255. for i in range(3)]
        else:
            if color.startswith("rgb(") and color[-1] == ")": color = color[4:-1]
            if " " in color or "/" in color or "," in color:
                color = color.replace(",", " ")
                color = color.replace("/", " ")
                components = color.split()
                for idx, c in enumerate(components):
                    if c[-1] == "%":
                        components[idx] = float(c[:-1])/100.
                    else:
                        components[idx] = float(c)/255.
            else:
                try:
                    components = palette.get(int(color))
                except ValueError:
                    components = known_colors[color.lower()]
                except AttributeError:
                    components = known_colors[color.lower()]

    # At this point, the components are floats
    return tuple([_clamp(val, 0., 1.) for val in components])


def darken(color, ratio=0.5):
    """Creates a darker version of a color given by an RGB triplet.
    
    This is done by mixing the original color with black using the given
    ratio. A ratio of 1.0 will yield a completely black color, a ratio
    of 0.0 will yield the original color.
    """
    r, g, b = color
    ratio = 1.0 - ratio
    r *= ratio
    g *= ratio
    b *= ratio
    return r, g, b

def lighten(color, ratio=0.5):
    """Creates a lighter version of a color given by an RGB triplet.
    
    This is done by mixing the original color with white using the given
    ratio. A ratio of 1.0 will yield a completely white color, a ratio
    of 0.0 will yield the original color.
    """
    r, g, b = color
    r += (1.0 - r) * ratio
    g += (1.0 - g) * ratio
    b += (1.0 - b) * ratio
    return r, g, b

known_colors = \
{   'alice blue': (0.94117647058823528, 0.97254901960784312, 1.0),
    'aliceblue': (0.94117647058823528, 0.97254901960784312, 1.0),
    'antique white': (   0.98039215686274506,
                         0.92156862745098034,
                         0.84313725490196079),
    'antiquewhite': (   0.98039215686274506,
                        0.92156862745098034,
                        0.84313725490196079),
    'antiquewhite1': (1.0, 0.93725490196078431, 0.85882352941176465),
    'antiquewhite2': (   0.93333333333333335,
                         0.87450980392156863,
                         0.80000000000000004),
    'antiquewhite3': (   0.80392156862745101,
                         0.75294117647058822,
                         0.69019607843137254),
    'antiquewhite4': (   0.54509803921568623,
                         0.51372549019607838,
                         0.47058823529411764),
    'aqua': (0.0, 1.0, 1.0),
    'aquamarine': (0.49803921568627452, 1.0, 0.83137254901960789),
    'aquamarine1': (0.49803921568627452, 1.0, 0.83137254901960789),
    'aquamarine2': (   0.46274509803921571,
                       0.93333333333333335,
                       0.77647058823529413),
    'aquamarine3': (   0.40000000000000002,
                       0.80392156862745101,
                       0.66666666666666663),
    'aquamarine4': (   0.27058823529411763,
                       0.54509803921568623,
                       0.45490196078431372),
    'azure': (0.94117647058823528, 1.0, 1.0),
    'azure1': (0.94117647058823528, 1.0, 1.0),
    'azure2': (0.8784313725490196, 0.93333333333333335, 0.93333333333333335),
    'azure3': (0.75686274509803919, 0.80392156862745101, 0.80392156862745101),
    'azure4': (0.51372549019607838, 0.54509803921568623, 0.54509803921568623),
    'beige': (0.96078431372549022, 0.96078431372549022, 0.86274509803921573),
    'bisque': (1.0, 0.89411764705882357, 0.7686274509803922),
    'bisque1': (1.0, 0.89411764705882357, 0.7686274509803922),
    'bisque2': (0.93333333333333335, 0.83529411764705885, 0.71764705882352942),
    'bisque3': (0.80392156862745101, 0.71764705882352942, 0.61960784313725492),
    'bisque4': (0.54509803921568623, 0.49019607843137253, 0.41960784313725491),
    'black': (0.0, 0.0, 0.0),
    'blanched almond': (1.0, 0.92156862745098034, 0.80392156862745101),
    'blanchedalmond': (1.0, 0.92156862745098034, 0.80392156862745101),
    'blue': (0.0, 0.0, 1.0),
    'blue violet': (   0.54117647058823526,
                       0.16862745098039217,
                       0.88627450980392153),
    'blue1': (0.0, 0.0, 1.0),
    'blue2': (0.0, 0.0, 0.93333333333333335),
    'blue3': (0.0, 0.0, 0.80392156862745101),
    'blue4': (0.0, 0.0, 0.54509803921568623),
    'blueviolet': (   0.54117647058823526,
                      0.16862745098039217,
                      0.88627450980392153),
    'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117),
    'brown1': (1.0, 0.25098039215686274, 0.25098039215686274),
    'brown2': (0.93333333333333335, 0.23137254901960785, 0.23137254901960785),
    'brown3': (0.80392156862745101, 0.20000000000000001, 0.20000000000000001),
    'brown4': (0.54509803921568623, 0.13725490196078433, 0.13725490196078433),
    'burlywood': (   0.87058823529411766,
                     0.72156862745098038,
                     0.52941176470588236),
    'burlywood1': (1.0, 0.82745098039215681, 0.60784313725490191),
    'burlywood2': (   0.93333333333333335,
                      0.77254901960784317,
                      0.56862745098039214),
    'burlywood3': (   0.80392156862745101,
                      0.66666666666666663,
                      0.49019607843137253),
    'burlywood4': (   0.54509803921568623,
                      0.45098039215686275,
                      0.33333333333333331),
    'cadet blue': (   0.37254901960784315,
                      0.61960784313725492,
                      0.62745098039215685),
    'cadetblue': (   0.37254901960784315,
                     0.61960784313725492,
                     0.62745098039215685),
    'cadetblue1': (0.59607843137254901, 0.96078431372549022, 1.0),
    'cadetblue2': (   0.55686274509803924,
                      0.89803921568627454,
                      0.93333333333333335),
    'cadetblue3': (   0.47843137254901963,
                      0.77254901960784317,
                      0.80392156862745101),
    'cadetblue4': (   0.32549019607843138,
                      0.52549019607843139,
                      0.54509803921568623),
    'chartreuse': (0.49803921568627452, 1.0, 0.0),
    'chartreuse1': (0.49803921568627452, 1.0, 0.0),
    'chartreuse2': (0.46274509803921571, 0.93333333333333335, 0.0),
    'chartreuse3': (0.40000000000000002, 0.80392156862745101, 0.0),
    'chartreuse4': (0.27058823529411763, 0.54509803921568623, 0.0),
    'chocolate': (   0.82352941176470584,
                     0.41176470588235292,
                     0.11764705882352941),
    'chocolate1': (1.0, 0.49803921568627452, 0.14117647058823529),
    'chocolate2': (   0.93333333333333335,
                      0.46274509803921571,
                      0.12941176470588237),
    'chocolate3': (   0.80392156862745101,
                      0.40000000000000002,
                      0.11372549019607843),
    'chocolate4': (   0.54509803921568623,
                      0.27058823529411763,
                      0.074509803921568626),
    'coral': (1.0, 0.49803921568627452, 0.31372549019607843),
    'coral1': (1.0, 0.44705882352941179, 0.33725490196078434),
    'coral2': (0.93333333333333335, 0.41568627450980394, 0.31372549019607843),
    'coral3': (0.80392156862745101, 0.35686274509803922, 0.27058823529411763),
    'coral4': (0.54509803921568623, 0.24313725490196078, 0.18431372549019609),
    'cornflower blue': (   0.39215686274509803,
                           0.58431372549019611,
                           0.92941176470588238),
    'cornflowerblue': (   0.39215686274509803,
                          0.58431372549019611,
                          0.92941176470588238),
    'cornsilk': (1.0, 0.97254901960784312, 0.86274509803921573),
    'cornsilk1': (1.0, 0.97254901960784312, 0.86274509803921573),
    'cornsilk2': (   0.93333333333333335,
                     0.90980392156862744,
                     0.80392156862745101),
    'cornsilk3': (   0.80392156862745101,
                     0.78431372549019607,
                     0.69411764705882351),
    'cornsilk4': (   0.54509803921568623,
                     0.53333333333333333,
                     0.47058823529411764),
    'cyan': (0.0, 1.0, 1.0),
    'cyan1': (0.0, 1.0, 1.0),
    'cyan2': (0.0, 0.93333333333333335, 0.93333333333333335),
    'cyan3': (0.0, 0.80392156862745101, 0.80392156862745101),
    'cyan4': (0.0, 0.54509803921568623, 0.54509803921568623),
    'dark blue': (0.0, 0.0, 0.54509803921568623),
    'dark cyan': (0.0, 0.54509803921568623, 0.54509803921568623),
    'dark goldenrod': (   0.72156862745098038,
                          0.52549019607843139,
                          0.043137254901960784),
    'dark gray': (   0.66274509803921566,
                     0.66274509803921566,
                     0.66274509803921566),
    'dark green': (0.0, 0.39215686274509803, 0.0),
    'dark grey': (   0.66274509803921566,
                     0.66274509803921566,
                     0.66274509803921566),
    'dark khaki': (   0.74117647058823533,
                      0.71764705882352942,
                      0.41960784313725491),
    'dark magenta': (0.54509803921568623, 0.0, 0.54509803921568623),
    'dark olive green': (   0.33333333333333331,
                            0.41960784313725491,
                            0.18431372549019609),
    'dark orange': (1.0, 0.5490196078431373, 0.0),
    'dark orchid': (   0.59999999999999998,
                       0.19607843137254902,
                       0.80000000000000004),
    'dark red': (0.54509803921568623, 0.0, 0.0),
    'dark salmon': (   0.9137254901960784,
                       0.58823529411764708,
                       0.47843137254901963),
    'dark sea green': (   0.5607843137254902,
                          0.73725490196078436,
                          0.5607843137254902),
    'dark slate blue': (   0.28235294117647058,
                           0.23921568627450981,
                           0.54509803921568623),
    'dark slate gray': (   0.18431372549019609,
                           0.30980392156862746,
                           0.30980392156862746),
    'dark slate grey': (   0.18431372549019609,
                           0.30980392156862746,
                           0.30980392156862746),
    'dark turquoise': (0.0, 0.80784313725490198, 0.81960784313725488),
    'dark violet': (0.58039215686274515, 0.0, 0.82745098039215681),
    'darkblue': (0.0, 0.0, 0.54509803921568623),
    'darkcyan': (0.0, 0.54509803921568623, 0.54509803921568623),
    'darkgoldenrod': (   0.72156862745098038,
                         0.52549019607843139,
                         0.043137254901960784),
    'darkgoldenrod1': (1.0, 0.72549019607843135, 0.058823529411764705),
    'darkgoldenrod2': (   0.93333333333333335,
                          0.67843137254901964,
                          0.054901960784313725),
    'darkgoldenrod3': (   0.80392156862745101,
                          0.58431372549019611,
                          0.047058823529411764),
    'darkgoldenrod4': (   0.54509803921568623,
                          0.396078431372549,
                          0.031372549019607843),
    'darkgray': (   0.66274509803921566,
                    0.66274509803921566,
                    0.66274509803921566),
    'darkgreen': (0.0, 0.39215686274509803, 0.0),
    'darkgrey': (   0.66274509803921566,
                    0.66274509803921566,
                    0.66274509803921566),
    'darkkhaki': (   0.74117647058823533,
                     0.71764705882352942,
                     0.41960784313725491),
    'darkmagenta': (0.54509803921568623, 0.0, 0.54509803921568623),
    'darkolivegreen': (   0.33333333333333331,
                          0.41960784313725491,
                          0.18431372549019609),
    'darkolivegreen1': (0.792156862745098, 1.0, 0.4392156862745098),
    'darkolivegreen2': (   0.73725490196078436,
                           0.93333333333333335,
                           0.40784313725490196),
    'darkolivegreen3': (   0.63529411764705879,
                           0.80392156862745101,
                           0.35294117647058826),
    'darkolivegreen4': (   0.43137254901960786,
                           0.54509803921568623,
                           0.23921568627450981),
    'darkorange': (1.0, 0.5490196078431373, 0.0),
    'darkorange1': (1.0, 0.49803921568627452, 0.0),
    'darkorange2': (0.93333333333333335, 0.46274509803921571, 0.0),
    'darkorange3': (0.80392156862745101, 0.40000000000000002, 0.0),
    'darkorange4': (0.54509803921568623, 0.27058823529411763, 0.0),
    'darkorchid': (   0.59999999999999998,
                      0.19607843137254902,
                      0.80000000000000004),
    'darkorchid1': (0.74901960784313726, 0.24313725490196078, 1.0),
    'darkorchid2': (   0.69803921568627447,
                       0.22745098039215686,
                       0.93333333333333335),
    'darkorchid3': (   0.60392156862745094,
                       0.19607843137254902,
                       0.80392156862745101),
    'darkorchid4': (   0.40784313725490196,
                       0.13333333333333333,
                       0.54509803921568623),
    'darkred': (0.54509803921568623, 0.0, 0.0),
    'darksalmon': (   0.9137254901960784,
                      0.58823529411764708,
                      0.47843137254901963),
    'darkseagreen': (   0.5607843137254902,
                        0.73725490196078436,
                        0.5607843137254902),
    'darkseagreen1': (0.75686274509803919, 1.0, 0.75686274509803919),
    'darkseagreen2': (   0.70588235294117652,
                         0.93333333333333335,
                         0.70588235294117652),
    'darkseagreen3': (   0.60784313725490191,
                         0.80392156862745101,
                         0.60784313725490191),
    'darkseagreen4': (   0.41176470588235292,
                         0.54509803921568623,
                         0.41176470588235292),
    'darkslateblue': (   0.28235294117647058,
                         0.23921568627450981,
                         0.54509803921568623),
    'darkslategray': (   0.18431372549019609,
                         0.30980392156862746,
                         0.30980392156862746),
    'darkslategray1': (0.59215686274509804, 1.0, 1.0),
    'darkslategray2': (   0.55294117647058827,
                          0.93333333333333335,
                          0.93333333333333335),
    'darkslategray3': (   0.47450980392156861,
                          0.80392156862745101,
                          0.80392156862745101),
    'darkslategray4': (   0.32156862745098042,
                          0.54509803921568623,
                          0.54509803921568623),
    'darkslategrey': (   0.18431372549019609,
                         0.30980392156862746,
                         0.30980392156862746),
    'darkturquoise': (0.0, 0.80784313725490198, 0.81960784313725488),
    'darkviolet': (0.58039215686274515, 0.0, 0.82745098039215681),
    'deep pink': (1.0, 0.078431372549019607, 0.57647058823529407),
    'deep sky blue': (0.0, 0.74901960784313726, 1.0),
    'deeppink': (1.0, 0.078431372549019607, 0.57647058823529407),
    'deeppink1': (1.0, 0.078431372549019607, 0.57647058823529407),
    'deeppink2': (   0.93333333333333335,
                     0.070588235294117646,
                     0.53725490196078429),
    'deeppink3': (   0.80392156862745101,
                     0.062745098039215685,
                     0.46274509803921571),
    'deeppink4': (   0.54509803921568623,
                     0.039215686274509803,
                     0.31372549019607843),
    'deepskyblue': (0.0, 0.74901960784313726, 1.0),
    'deepskyblue1': (0.0, 0.74901960784313726, 1.0),
    'deepskyblue2': (0.0, 0.69803921568627447, 0.93333333333333335),
    'deepskyblue3': (0.0, 0.60392156862745094, 0.80392156862745101),
    'deepskyblue4': (0.0, 0.40784313725490196, 0.54509803921568623),
    'dim gray': (   0.41176470588235292,
                    0.41176470588235292,
                    0.41176470588235292),
    'dim grey': (   0.41176470588235292,
                    0.41176470588235292,
                    0.41176470588235292),
    'dimgray': (0.41176470588235292, 0.41176470588235292, 0.41176470588235292),
    'dimgrey': (0.41176470588235292, 0.41176470588235292, 0.41176470588235292),
    'dodger blue': (0.11764705882352941, 0.56470588235294117, 1.0),
    'dodgerblue': (0.11764705882352941, 0.56470588235294117, 1.0),
    'dodgerblue1': (0.11764705882352941, 0.56470588235294117, 1.0),
    'dodgerblue2': (   0.10980392156862745,
                       0.52549019607843139,
                       0.93333333333333335),
    'dodgerblue3': (   0.094117647058823528,
                       0.45490196078431372,
                       0.80392156862745101),
    'dodgerblue4': (   0.062745098039215685,
                       0.30588235294117649,
                       0.54509803921568623),
    'firebrick': (   0.69803921568627447,
                     0.13333333333333333,
                     0.13333333333333333),
    'firebrick1': (1.0, 0.18823529411764706, 0.18823529411764706),
    'firebrick2': (   0.93333333333333335,
                      0.17254901960784313,
                      0.17254901960784313),
    'firebrick3': (   0.80392156862745101,
                      0.14901960784313725,
                      0.14901960784313725),
    'firebrick4': (   0.54509803921568623,
                      0.10196078431372549,
                      0.10196078431372549),
    'floral white': (1.0, 0.98039215686274506, 0.94117647058823528),
    'floralwhite': (1.0, 0.98039215686274506, 0.94117647058823528),
    'forest green': (   0.13333333333333333,
                        0.54509803921568623,
                        0.13333333333333333),
    'forestgreen': (   0.13333333333333333,
                       0.54509803921568623,
                       0.13333333333333333),
    'fuchsia': (1.0, 0.0, 1.0),
    'gainsboro': (   0.86274509803921573,
                     0.86274509803921573,
                     0.86274509803921573),
    'ghost white': (0.97254901960784312, 0.97254901960784312, 1.0),
    'ghostwhite': (0.97254901960784312, 0.97254901960784312, 1.0),
    'gold': (1.0, 0.84313725490196079, 0.0),
    'gold1': (1.0, 0.84313725490196079, 0.0),
    'gold2': (0.93333333333333335, 0.78823529411764703, 0.0),
    'gold3': (0.80392156862745101, 0.67843137254901964, 0.0),
    'gold4': (0.54509803921568623, 0.45882352941176469, 0.0),
    'goldenrod': (   0.85490196078431369,
                     0.6470588235294118,
                     0.12549019607843137),
    'goldenrod1': (1.0, 0.75686274509803919, 0.14509803921568629),
    'goldenrod2': (   0.93333333333333335,
                      0.70588235294117652,
                      0.13333333333333333),
    'goldenrod3': (   0.80392156862745101,
                      0.60784313725490191,
                      0.11372549019607843),
    'goldenrod4': (   0.54509803921568623,
                      0.41176470588235292,
                      0.078431372549019607),
    'gray': (0.74509803921568629, 0.74509803921568629, 0.74509803921568629),
    'gray0': (0.0, 0.0, 0.0),
    'gray1': (   0.011764705882352941,
                 0.011764705882352941,
                 0.011764705882352941),
    'gray10': (0.10196078431372549, 0.10196078431372549, 0.10196078431372549),
    'gray100': (1.0, 1.0, 1.0),
    'gray11': (0.10980392156862745, 0.10980392156862745, 0.10980392156862745),
    'gray12': (0.12156862745098039, 0.12156862745098039, 0.12156862745098039),
    'gray13': (0.12941176470588237, 0.12941176470588237, 0.12941176470588237),
    'gray14': (0.14117647058823529, 0.14117647058823529, 0.14117647058823529),
    'gray15': (0.14901960784313725, 0.14901960784313725, 0.14901960784313725),
    'gray16': (0.16078431372549021, 0.16078431372549021, 0.16078431372549021),
    'gray17': (0.16862745098039217, 0.16862745098039217, 0.16862745098039217),
    'gray18': (0.1803921568627451, 0.1803921568627451, 0.1803921568627451),
    'gray19': (0.18823529411764706, 0.18823529411764706, 0.18823529411764706),
    'gray2': (   0.019607843137254902,
                 0.019607843137254902,
                 0.019607843137254902),
    'gray20': (0.20000000000000001, 0.20000000000000001, 0.20000000000000001),
    'gray21': (0.21176470588235294, 0.21176470588235294, 0.21176470588235294),
    'gray22': (0.2196078431372549, 0.2196078431372549, 0.2196078431372549),
    'gray23': (0.23137254901960785, 0.23137254901960785, 0.23137254901960785),
    'gray24': (0.23921568627450981, 0.23921568627450981, 0.23921568627450981),
    'gray25': (0.25098039215686274, 0.25098039215686274, 0.25098039215686274),
    'gray26': (0.25882352941176473, 0.25882352941176473, 0.25882352941176473),
    'gray27': (0.27058823529411763, 0.27058823529411763, 0.27058823529411763),
    'gray28': (0.27843137254901962, 0.27843137254901962, 0.27843137254901962),
    'gray29': (0.29019607843137257, 0.29019607843137257, 0.29019607843137257),
    'gray3': (   0.031372549019607843,
                 0.031372549019607843,
                 0.031372549019607843),
    'gray30': (0.30196078431372547, 0.30196078431372547, 0.30196078431372547),
    'gray31': (0.30980392156862746, 0.30980392156862746, 0.30980392156862746),
    'gray32': (0.32156862745098042, 0.32156862745098042, 0.32156862745098042),
    'gray33': (0.32941176470588235, 0.32941176470588235, 0.32941176470588235),
    'gray34': (0.3411764705882353, 0.3411764705882353, 0.3411764705882353),
    'gray35': (0.34901960784313724, 0.34901960784313724, 0.34901960784313724),
    'gray36': (0.36078431372549019, 0.36078431372549019, 0.36078431372549019),
    'gray37': (0.36862745098039218, 0.36862745098039218, 0.36862745098039218),
    'gray38': (0.38039215686274508, 0.38039215686274508, 0.38039215686274508),
    'gray39': (0.38823529411764707, 0.38823529411764707, 0.38823529411764707),
    'gray4': (   0.039215686274509803,
                 0.039215686274509803,
                 0.039215686274509803),
    'gray40': (0.40000000000000002, 0.40000000000000002, 0.40000000000000002),
    'gray41': (0.41176470588235292, 0.41176470588235292, 0.41176470588235292),
    'gray42': (0.41960784313725491, 0.41960784313725491, 0.41960784313725491),
    'gray43': (0.43137254901960786, 0.43137254901960786, 0.43137254901960786),
    'gray44': (0.4392156862745098, 0.4392156862745098, 0.4392156862745098),
    'gray45': (0.45098039215686275, 0.45098039215686275, 0.45098039215686275),
    'gray46': (0.45882352941176469, 0.45882352941176469, 0.45882352941176469),
    'gray47': (0.47058823529411764, 0.47058823529411764, 0.47058823529411764),
    'gray48': (0.47843137254901963, 0.47843137254901963, 0.47843137254901963),
    'gray49': (0.49019607843137253, 0.49019607843137253, 0.49019607843137253),
    'gray5': (   0.050980392156862744,
                 0.050980392156862744,
                 0.050980392156862744),
    'gray50': (0.49803921568627452, 0.49803921568627452, 0.49803921568627452),
    'gray51': (0.50980392156862742, 0.50980392156862742, 0.50980392156862742),
    'gray52': (0.52156862745098043, 0.52156862745098043, 0.52156862745098043),
    'gray53': (0.52941176470588236, 0.52941176470588236, 0.52941176470588236),
    'gray54': (0.54117647058823526, 0.54117647058823526, 0.54117647058823526),
    'gray55': (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
    'gray56': (0.5607843137254902, 0.5607843137254902, 0.5607843137254902),
    'gray57': (0.56862745098039214, 0.56862745098039214, 0.56862745098039214),
    'gray58': (0.58039215686274515, 0.58039215686274515, 0.58039215686274515),
    'gray59': (0.58823529411764708, 0.58823529411764708, 0.58823529411764708),
    'gray6': (   0.058823529411764705,
                 0.058823529411764705,
                 0.058823529411764705),
    'gray60': (0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
    'gray61': (0.61176470588235299, 0.61176470588235299, 0.61176470588235299),
    'gray62': (0.61960784313725492, 0.61960784313725492, 0.61960784313725492),
    'gray63': (0.63137254901960782, 0.63137254901960782, 0.63137254901960782),
    'gray64': (0.63921568627450975, 0.63921568627450975, 0.63921568627450975),
    'gray65': (0.65098039215686276, 0.65098039215686276, 0.65098039215686276),
    'gray66': (0.6588235294117647, 0.6588235294117647, 0.6588235294117647),
    'gray67': (0.6705882352941176, 0.6705882352941176, 0.6705882352941176),
    'gray68': (0.67843137254901964, 0.67843137254901964, 0.67843137254901964),
    'gray69': (0.69019607843137254, 0.69019607843137254, 0.69019607843137254),
    'gray7': (   0.070588235294117646,
                 0.070588235294117646,
                 0.070588235294117646),
    'gray70': (0.70196078431372544, 0.70196078431372544, 0.70196078431372544),
    'gray71': (0.70980392156862748, 0.70980392156862748, 0.70980392156862748),
    'gray72': (0.72156862745098038, 0.72156862745098038, 0.72156862745098038),
    'gray73': (0.72941176470588232, 0.72941176470588232, 0.72941176470588232),
    'gray74': (0.74117647058823533, 0.74117647058823533, 0.74117647058823533),
    'gray75': (0.74901960784313726, 0.74901960784313726, 0.74901960784313726),
    'gray76': (0.76078431372549016, 0.76078431372549016, 0.76078431372549016),
    'gray77': (0.7686274509803922, 0.7686274509803922, 0.7686274509803922),
    'gray78': (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
    'gray79': (0.78823529411764703, 0.78823529411764703, 0.78823529411764703),
    'gray8': (   0.078431372549019607,
                 0.078431372549019607,
                 0.078431372549019607),
    'gray80': (0.80000000000000004, 0.80000000000000004, 0.80000000000000004),
    'gray81': (0.81176470588235294, 0.81176470588235294, 0.81176470588235294),
    'gray82': (0.81960784313725488, 0.81960784313725488, 0.81960784313725488),
    'gray83': (0.83137254901960789, 0.83137254901960789, 0.83137254901960789),
    'gray84': (0.83921568627450982, 0.83921568627450982, 0.83921568627450982),
    'gray85': (0.85098039215686272, 0.85098039215686272, 0.85098039215686272),
    'gray86': (0.85882352941176465, 0.85882352941176465, 0.85882352941176465),
    'gray87': (0.87058823529411766, 0.87058823529411766, 0.87058823529411766),
    'gray88': (0.8784313725490196, 0.8784313725490196, 0.8784313725490196),
    'gray89': (0.8901960784313725, 0.8901960784313725, 0.8901960784313725),
    'gray9': (   0.090196078431372548,
                 0.090196078431372548,
                 0.090196078431372548),
    'gray90': (0.89803921568627454, 0.89803921568627454, 0.89803921568627454),
    'gray91': (0.90980392156862744, 0.90980392156862744, 0.90980392156862744),
    'gray92': (0.92156862745098034, 0.92156862745098034, 0.92156862745098034),
    'gray93': (0.92941176470588238, 0.92941176470588238, 0.92941176470588238),
    'gray94': (0.94117647058823528, 0.94117647058823528, 0.94117647058823528),
    'gray95': (0.94901960784313721, 0.94901960784313721, 0.94901960784313721),
    'gray96': (0.96078431372549022, 0.96078431372549022, 0.96078431372549022),
    'gray97': (0.96862745098039216, 0.96862745098039216, 0.96862745098039216),
    'gray98': (0.98039215686274506, 0.98039215686274506, 0.98039215686274506),
    'gray99': (0.9882352941176471, 0.9882352941176471, 0.9882352941176471),
    'green': (0.0, 1.0, 0.0),
    'green yellow': (0.67843137254901964, 1.0, 0.18431372549019609),
    'green1': (0.0, 1.0, 0.0),
    'green2': (0.0, 0.93333333333333335, 0.0),
    'green3': (0.0, 0.80392156862745101, 0.0),
    'green4': (0.0, 0.54509803921568623, 0.0),
    'greenyellow': (0.67843137254901964, 1.0, 0.18431372549019609),
    'grey': (0.74509803921568629, 0.74509803921568629, 0.74509803921568629),
    'grey0': (0.0, 0.0, 0.0),
    'grey1': (   0.011764705882352941,
                 0.011764705882352941,
                 0.011764705882352941),
    'grey10': (0.10196078431372549, 0.10196078431372549, 0.10196078431372549),
    'grey100': (1.0, 1.0, 1.0),
    'grey11': (0.10980392156862745, 0.10980392156862745, 0.10980392156862745),
    'grey12': (0.12156862745098039, 0.12156862745098039, 0.12156862745098039),
    'grey13': (0.12941176470588237, 0.12941176470588237, 0.12941176470588237),
    'grey14': (0.14117647058823529, 0.14117647058823529, 0.14117647058823529),
    'grey15': (0.14901960784313725, 0.14901960784313725, 0.14901960784313725),
    'grey16': (0.16078431372549021, 0.16078431372549021, 0.16078431372549021),
    'grey17': (0.16862745098039217, 0.16862745098039217, 0.16862745098039217),
    'grey18': (0.1803921568627451, 0.1803921568627451, 0.1803921568627451),
    'grey19': (0.18823529411764706, 0.18823529411764706, 0.18823529411764706),
    'grey2': (   0.019607843137254902,
                 0.019607843137254902,
                 0.019607843137254902),
    'grey20': (0.20000000000000001, 0.20000000000000001, 0.20000000000000001),
    'grey21': (0.21176470588235294, 0.21176470588235294, 0.21176470588235294),
    'grey22': (0.2196078431372549, 0.2196078431372549, 0.2196078431372549),
    'grey23': (0.23137254901960785, 0.23137254901960785, 0.23137254901960785),
    'grey24': (0.23921568627450981, 0.23921568627450981, 0.23921568627450981),
    'grey25': (0.25098039215686274, 0.25098039215686274, 0.25098039215686274),
    'grey26': (0.25882352941176473, 0.25882352941176473, 0.25882352941176473),
    'grey27': (0.27058823529411763, 0.27058823529411763, 0.27058823529411763),
    'grey28': (0.27843137254901962, 0.27843137254901962, 0.27843137254901962),
    'grey29': (0.29019607843137257, 0.29019607843137257, 0.29019607843137257),
    'grey3': (   0.031372549019607843,
                 0.031372549019607843,
                 0.031372549019607843),
    'grey30': (0.30196078431372547, 0.30196078431372547, 0.30196078431372547),
    'grey31': (0.30980392156862746, 0.30980392156862746, 0.30980392156862746),
    'grey32': (0.32156862745098042, 0.32156862745098042, 0.32156862745098042),
    'grey33': (0.32941176470588235, 0.32941176470588235, 0.32941176470588235),
    'grey34': (0.3411764705882353, 0.3411764705882353, 0.3411764705882353),
    'grey35': (0.34901960784313724, 0.34901960784313724, 0.34901960784313724),
    'grey36': (0.36078431372549019, 0.36078431372549019, 0.36078431372549019),
    'grey37': (0.36862745098039218, 0.36862745098039218, 0.36862745098039218),
    'grey38': (0.38039215686274508, 0.38039215686274508, 0.38039215686274508),
    'grey39': (0.38823529411764707, 0.38823529411764707, 0.38823529411764707),
    'grey4': (   0.039215686274509803,
                 0.039215686274509803,
                 0.039215686274509803),
    'grey40': (0.40000000000000002, 0.40000000000000002, 0.40000000000000002),
    'grey41': (0.41176470588235292, 0.41176470588235292, 0.41176470588235292),
    'grey42': (0.41960784313725491, 0.41960784313725491, 0.41960784313725491),
    'grey43': (0.43137254901960786, 0.43137254901960786, 0.43137254901960786),
    'grey44': (0.4392156862745098, 0.4392156862745098, 0.4392156862745098),
    'grey45': (0.45098039215686275, 0.45098039215686275, 0.45098039215686275),
    'grey46': (0.45882352941176469, 0.45882352941176469, 0.45882352941176469),
    'grey47': (0.47058823529411764, 0.47058823529411764, 0.47058823529411764),
    'grey48': (0.47843137254901963, 0.47843137254901963, 0.47843137254901963),
    'grey49': (0.49019607843137253, 0.49019607843137253, 0.49019607843137253),
    'grey5': (   0.050980392156862744,
                 0.050980392156862744,
                 0.050980392156862744),
    'grey50': (0.49803921568627452, 0.49803921568627452, 0.49803921568627452),
    'grey51': (0.50980392156862742, 0.50980392156862742, 0.50980392156862742),
    'grey52': (0.52156862745098043, 0.52156862745098043, 0.52156862745098043),
    'grey53': (0.52941176470588236, 0.52941176470588236, 0.52941176470588236),
    'grey54': (0.54117647058823526, 0.54117647058823526, 0.54117647058823526),
    'grey55': (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
    'grey56': (0.5607843137254902, 0.5607843137254902, 0.5607843137254902),
    'grey57': (0.56862745098039214, 0.56862745098039214, 0.56862745098039214),
    'grey58': (0.58039215686274515, 0.58039215686274515, 0.58039215686274515),
    'grey59': (0.58823529411764708, 0.58823529411764708, 0.58823529411764708),
    'grey6': (   0.058823529411764705,
                 0.058823529411764705,
                 0.058823529411764705),
    'grey60': (0.59999999999999998, 0.59999999999999998, 0.59999999999999998),
    'grey61': (0.61176470588235299, 0.61176470588235299, 0.61176470588235299),
    'grey62': (0.61960784313725492, 0.61960784313725492, 0.61960784313725492),
    'grey63': (0.63137254901960782, 0.63137254901960782, 0.63137254901960782),
    'grey64': (0.63921568627450975, 0.63921568627450975, 0.63921568627450975),
    'grey65': (0.65098039215686276, 0.65098039215686276, 0.65098039215686276),
    'grey66': (0.6588235294117647, 0.6588235294117647, 0.6588235294117647),
    'grey67': (0.6705882352941176, 0.6705882352941176, 0.6705882352941176),
    'grey68': (0.67843137254901964, 0.67843137254901964, 0.67843137254901964),
    'grey69': (0.69019607843137254, 0.69019607843137254, 0.69019607843137254),
    'grey7': (   0.070588235294117646,
                 0.070588235294117646,
                 0.070588235294117646),
    'grey70': (0.70196078431372544, 0.70196078431372544, 0.70196078431372544),
    'grey71': (0.70980392156862748, 0.70980392156862748, 0.70980392156862748),
    'grey72': (0.72156862745098038, 0.72156862745098038, 0.72156862745098038),
    'grey73': (0.72941176470588232, 0.72941176470588232, 0.72941176470588232),
    'grey74': (0.74117647058823533, 0.74117647058823533, 0.74117647058823533),
    'grey75': (0.74901960784313726, 0.74901960784313726, 0.74901960784313726),
    'grey76': (0.76078431372549016, 0.76078431372549016, 0.76078431372549016),
    'grey77': (0.7686274509803922, 0.7686274509803922, 0.7686274509803922),
    'grey78': (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
    'grey79': (0.78823529411764703, 0.78823529411764703, 0.78823529411764703),
    'grey8': (   0.078431372549019607,
                 0.078431372549019607,
                 0.078431372549019607),
    'grey80': (0.80000000000000004, 0.80000000000000004, 0.80000000000000004),
    'grey81': (0.81176470588235294, 0.81176470588235294, 0.81176470588235294),
    'grey82': (0.81960784313725488, 0.81960784313725488, 0.81960784313725488),
    'grey83': (0.83137254901960789, 0.83137254901960789, 0.83137254901960789),
    'grey84': (0.83921568627450982, 0.83921568627450982, 0.83921568627450982),
    'grey85': (0.85098039215686272, 0.85098039215686272, 0.85098039215686272),
    'grey86': (0.85882352941176465, 0.85882352941176465, 0.85882352941176465),
    'grey87': (0.87058823529411766, 0.87058823529411766, 0.87058823529411766),
    'grey88': (0.8784313725490196, 0.8784313725490196, 0.8784313725490196),
    'grey89': (0.8901960784313725, 0.8901960784313725, 0.8901960784313725),
    'grey9': (   0.090196078431372548,
                 0.090196078431372548,
                 0.090196078431372548),
    'grey90': (0.89803921568627454, 0.89803921568627454, 0.89803921568627454),
    'grey91': (0.90980392156862744, 0.90980392156862744, 0.90980392156862744),
    'grey92': (0.92156862745098034, 0.92156862745098034, 0.92156862745098034),
    'grey93': (0.92941176470588238, 0.92941176470588238, 0.92941176470588238),
    'grey94': (0.94117647058823528, 0.94117647058823528, 0.94117647058823528),
    'grey95': (0.94901960784313721, 0.94901960784313721, 0.94901960784313721),
    'grey96': (0.96078431372549022, 0.96078431372549022, 0.96078431372549022),
    'grey97': (0.96862745098039216, 0.96862745098039216, 0.96862745098039216),
    'grey98': (0.98039215686274506, 0.98039215686274506, 0.98039215686274506),
    'grey99': (0.9882352941176471, 0.9882352941176471, 0.9882352941176471),
    'honeydew': (0.94117647058823528, 1.0, 0.94117647058823528),
    'honeydew1': (0.94117647058823528, 1.0, 0.94117647058823528),
    'honeydew2': (0.8784313725490196, 0.93333333333333335, 0.8784313725490196),
    'honeydew3': (   0.75686274509803919,
                     0.80392156862745101,
                     0.75686274509803919),
    'honeydew4': (   0.51372549019607838,
                     0.54509803921568623,
                     0.51372549019607838),
    'hot pink': (1.0, 0.41176470588235292, 0.70588235294117652),
    'hotpink': (1.0, 0.41176470588235292, 0.70588235294117652),
    'hotpink1': (1.0, 0.43137254901960786, 0.70588235294117652),
    'hotpink2': (   0.93333333333333335,
                    0.41568627450980394,
                    0.65490196078431373),
    'hotpink3': (   0.80392156862745101,
                    0.37647058823529411,
                    0.56470588235294117),
    'hotpink4': (0.54509803921568623, 0.22745098039215686, 0.3843137254901961),
    'indian red': (   0.80392156862745101,
                      0.36078431372549019,
                      0.36078431372549019),
    'indianred': (   0.80392156862745101,
                     0.36078431372549019,
                     0.36078431372549019),
    'indianred1': (1.0, 0.41568627450980394, 0.41568627450980394),
    'indianred2': (   0.93333333333333335,
                      0.38823529411764707,
                      0.38823529411764707),
    'indianred3': (   0.80392156862745101,
                      0.33333333333333331,
                      0.33333333333333331),
    'indianred4': (   0.54509803921568623,
                      0.22745098039215686,
                      0.22745098039215686),
    'ivory': (1.0, 1.0, 0.94117647058823528),
    'ivory1': (1.0, 1.0, 0.94117647058823528),
    'ivory2': (0.93333333333333335, 0.93333333333333335, 0.8784313725490196),
    'ivory3': (0.80392156862745101, 0.80392156862745101, 0.75686274509803919),
    'ivory4': (0.54509803921568623, 0.54509803921568623, 0.51372549019607838),
    'khaki': (0.94117647058823528, 0.90196078431372551, 0.5490196078431373),
    'khaki1': (1.0, 0.96470588235294119, 0.5607843137254902),
    'khaki2': (0.93333333333333335, 0.90196078431372551, 0.52156862745098043),
    'khaki3': (0.80392156862745101, 0.77647058823529413, 0.45098039215686275),
    'khaki4': (0.54509803921568623, 0.52549019607843139, 0.30588235294117649),
    'lavender': (   0.90196078431372551,
                    0.90196078431372551,
                    0.98039215686274506),
    'lavender blush': (1.0, 0.94117647058823528, 0.96078431372549022),
    'lavenderblush': (1.0, 0.94117647058823528, 0.96078431372549022),
    'lavenderblush1': (1.0, 0.94117647058823528, 0.96078431372549022),
    'lavenderblush2': (   0.93333333333333335,
                          0.8784313725490196,
                          0.89803921568627454),
    'lavenderblush3': (   0.80392156862745101,
                          0.75686274509803919,
                          0.77254901960784317),
    'lavenderblush4': (   0.54509803921568623,
                          0.51372549019607838,
                          0.52549019607843139),
    'lawn green': (0.48627450980392156, 0.9882352941176471, 0.0),
    'lawngreen': (0.48627450980392156, 0.9882352941176471, 0.0),
    'lemon chiffon': (1.0, 0.98039215686274506, 0.80392156862745101),
    'lemonchiffon': (1.0, 0.98039215686274506, 0.80392156862745101),
    'lemonchiffon1': (1.0, 0.98039215686274506, 0.80392156862745101),
    'lemonchiffon2': (   0.93333333333333335,
                         0.9137254901960784,
                         0.74901960784313726),
    'lemonchiffon3': (   0.80392156862745101,
                         0.78823529411764703,
                         0.6470588235294118),
    'lemonchiffon4': (   0.54509803921568623,
                         0.53725490196078429,
                         0.4392156862745098),
    'light blue': (   0.67843137254901964,
                      0.84705882352941175,
                      0.90196078431372551),
    'light coral': (   0.94117647058823528,
                       0.50196078431372548,
                       0.50196078431372548),
    'light cyan': (0.8784313725490196, 1.0, 1.0),
    'light goldenrod': (   0.93333333333333335,
                           0.8666666666666667,
                           0.50980392156862742),
    'light goldenrod yellow': (   0.98039215686274506,
                                  0.98039215686274506,
                                  0.82352941176470584),
    'light gray': (   0.82745098039215681,
                      0.82745098039215681,
                      0.82745098039215681),
    'light green': (   0.56470588235294117,
                       0.93333333333333335,
                       0.56470588235294117),
    'light grey': (   0.82745098039215681,
                      0.82745098039215681,
                      0.82745098039215681),
    'light pink': (1.0, 0.71372549019607845, 0.75686274509803919),
    'light salmon': (1.0, 0.62745098039215685, 0.47843137254901963),
    'light sea green': (   0.12549019607843137,
                           0.69803921568627447,
                           0.66666666666666663),
    'light sky blue': (   0.52941176470588236,
                          0.80784313725490198,
                          0.98039215686274506),
    'light slate blue': (0.51764705882352946, 0.4392156862745098, 1.0),
    'light slate gray': (   0.46666666666666667,
                            0.53333333333333333,
                            0.59999999999999998),
    'light slate grey': (   0.46666666666666667,
                            0.53333333333333333,
                            0.59999999999999998),
    'light steel blue': (   0.69019607843137254,
                            0.7686274509803922,
                            0.87058823529411766),
    'light yellow': (1.0, 1.0, 0.8784313725490196),
    'lightblue': (   0.67843137254901964,
                     0.84705882352941175,
                     0.90196078431372551),
    'lightblue1': (0.74901960784313726, 0.93725490196078431, 1.0),
    'lightblue2': (   0.69803921568627447,
                      0.87450980392156863,
                      0.93333333333333335),
    'lightblue3': (   0.60392156862745094,
                      0.75294117647058822,
                      0.80392156862745101),
    'lightblue4': (   0.40784313725490196,
                      0.51372549019607838,
                      0.54509803921568623),
    'lightcoral': (   0.94117647058823528,
                      0.50196078431372548,
                      0.50196078431372548),
    'lightcyan': (0.8784313725490196, 1.0, 1.0),
    'lightcyan1': (0.8784313725490196, 1.0, 1.0),
    'lightcyan2': (   0.81960784313725488,
                      0.93333333333333335,
                      0.93333333333333335),
    'lightcyan3': (   0.70588235294117652,
                      0.80392156862745101,
                      0.80392156862745101),
    'lightcyan4': (   0.47843137254901963,
                      0.54509803921568623,
                      0.54509803921568623),
    'lightgoldenrod': (   0.93333333333333335,
                          0.8666666666666667,
                          0.50980392156862742),
    'lightgoldenrod1': (1.0, 0.92549019607843142, 0.54509803921568623),
    'lightgoldenrod2': (   0.93333333333333335,
                           0.86274509803921573,
                           0.50980392156862742),
    'lightgoldenrod3': (   0.80392156862745101,
                           0.74509803921568629,
                           0.4392156862745098),
    'lightgoldenrod4': (   0.54509803921568623,
                           0.50588235294117645,
                           0.29803921568627451),
    'lightgoldenrodyellow': (   0.98039215686274506,
                                0.98039215686274506,
                                0.82352941176470584),
    'lightgray': (   0.82745098039215681,
                     0.82745098039215681,
                     0.82745098039215681),
    'lightgreen': (   0.56470588235294117,
                      0.93333333333333335,
                      0.56470588235294117),
    'lightgrey': (   0.82745098039215681,
                     0.82745098039215681,
                     0.82745098039215681),
    'lightpink': (1.0, 0.71372549019607845, 0.75686274509803919),
    'lightpink1': (1.0, 0.68235294117647061, 0.72549019607843135),
    'lightpink2': (   0.93333333333333335,
                      0.63529411764705879,
                      0.67843137254901964),
    'lightpink3': (   0.80392156862745101,
                      0.5490196078431373,
                      0.58431372549019611),
    'lightpink4': (   0.54509803921568623,
                      0.37254901960784315,
                      0.396078431372549),
    'lightsalmon': (1.0, 0.62745098039215685, 0.47843137254901963),
    'lightsalmon1': (1.0, 0.62745098039215685, 0.47843137254901963),
    'lightsalmon2': (   0.93333333333333335,
                        0.58431372549019611,
                        0.44705882352941179),
    'lightsalmon3': (   0.80392156862745101,
                        0.50588235294117645,
                        0.3843137254901961),
    'lightsalmon4': (   0.54509803921568623,
                        0.3411764705882353,
                        0.25882352941176473),
    'lightseagreen': (   0.12549019607843137,
                         0.69803921568627447,
                         0.66666666666666663),
    'lightskyblue': (   0.52941176470588236,
                        0.80784313725490198,
                        0.98039215686274506),
    'lightskyblue1': (0.69019607843137254, 0.88627450980392153, 1.0),
    'lightskyblue2': (   0.64313725490196083,
                         0.82745098039215681,
                         0.93333333333333335),
    'lightskyblue3': (   0.55294117647058827,
                         0.71372549019607845,
                         0.80392156862745101),
    'lightskyblue4': (   0.37647058823529411,
                         0.4823529411764706,
                         0.54509803921568623),
    'lightslateblue': (0.51764705882352946, 0.4392156862745098, 1.0),
    'lightslategray': (   0.46666666666666667,
                          0.53333333333333333,
                          0.59999999999999998),
    'lightslategrey': (   0.46666666666666667,
                          0.53333333333333333,
                          0.59999999999999998),
    'lightsteelblue': (   0.69019607843137254,
                          0.7686274509803922,
                          0.87058823529411766),
    'lightsteelblue1': (0.792156862745098, 0.88235294117647056, 1.0),
    'lightsteelblue2': (   0.73725490196078436,
                           0.82352941176470584,
                           0.93333333333333335),
    'lightsteelblue3': (   0.63529411764705879,
                           0.70980392156862748,
                           0.80392156862745101),
    'lightsteelblue4': (   0.43137254901960786,
                           0.4823529411764706,
                           0.54509803921568623),
    'lightyellow': (1.0, 1.0, 0.8784313725490196),
    'lightyellow1': (1.0, 1.0, 0.8784313725490196),
    'lightyellow2': (   0.93333333333333335,
                        0.93333333333333335,
                        0.81960784313725488),
    'lightyellow3': (   0.80392156862745101,
                        0.80392156862745101,
                        0.70588235294117652),
    'lightyellow4': (   0.54509803921568623,
                        0.54509803921568623,
                        0.47843137254901963),
    'lime': (0.0, 1.0, 0.0),
    'lime green': (   0.19607843137254902,
                      0.80392156862745101,
                      0.19607843137254902),
    'limegreen': (   0.19607843137254902,
                     0.80392156862745101,
                     0.19607843137254902),
    'linen': (0.98039215686274506, 0.94117647058823528, 0.90196078431372551),
    'magenta': (1.0, 0.0, 1.0),
    'magenta1': (1.0, 0.0, 1.0),
    'magenta2': (0.93333333333333335, 0.0, 0.93333333333333335),
    'magenta3': (0.80392156862745101, 0.0, 0.80392156862745101),
    'magenta4': (0.54509803921568623, 0.0, 0.54509803921568623),
    'maroon': (0.69019607843137254, 0.18823529411764706, 0.37647058823529411),
    'maroon1': (1.0, 0.20392156862745098, 0.70196078431372544),
    'maroon2': (0.93333333333333335, 0.18823529411764706, 0.65490196078431373),
    'maroon3': (0.80392156862745101, 0.16078431372549021, 0.56470588235294117),
    'maroon4': (0.54509803921568623, 0.10980392156862745, 0.3843137254901961),
    'medium aquamarine': (   0.40000000000000002,
                             0.80392156862745101,
                             0.66666666666666663),
    'medium blue': (0.0, 0.0, 0.80392156862745101),
    'medium orchid': (   0.72941176470588232,
                         0.33333333333333331,
                         0.82745098039215681),
    'medium purple': (   0.57647058823529407,
                         0.4392156862745098,
                         0.85882352941176465),
    'medium sea green': (   0.23529411764705882,
                            0.70196078431372544,
                            0.44313725490196076),
    'medium slate blue': (   0.4823529411764706,
                             0.40784313725490196,
                             0.93333333333333335),
    'medium spring green': (0.0, 0.98039215686274506, 0.60392156862745094),
    'medium turquoise': (   0.28235294117647058,
                            0.81960784313725488,
                            0.80000000000000004),
    'medium violet red': (   0.7803921568627451,
                             0.082352941176470587,
                             0.52156862745098043),
    'mediumaquamarine': (   0.40000000000000002,
                            0.80392156862745101,
                            0.66666666666666663),
    'mediumblue': (0.0, 0.0, 0.80392156862745101),
    'mediumorchid': (   0.72941176470588232,
                        0.33333333333333331,
                        0.82745098039215681),
    'mediumorchid1': (0.8784313725490196, 0.40000000000000002, 1.0),
    'mediumorchid2': (   0.81960784313725488,
                         0.37254901960784315,
                         0.93333333333333335),
    'mediumorchid3': (   0.70588235294117652,
                         0.32156862745098042,
                         0.80392156862745101),
    'mediumorchid4': (   0.47843137254901963,
                         0.21568627450980393,
                         0.54509803921568623),
    'mediumpurple': (   0.57647058823529407,
                        0.4392156862745098,
                        0.85882352941176465),
    'mediumpurple1': (0.6705882352941176, 0.50980392156862742, 1.0),
    'mediumpurple2': (   0.62352941176470589,
                         0.47450980392156861,
                         0.93333333333333335),
    'mediumpurple3': (   0.53725490196078429,
                         0.40784313725490196,
                         0.80392156862745101),
    'mediumpurple4': (   0.36470588235294116,
                         0.27843137254901962,
                         0.54509803921568623),
    'mediumseagreen': (   0.23529411764705882,
                          0.70196078431372544,
                          0.44313725490196076),
    'mediumslateblue': (   0.4823529411764706,
                           0.40784313725490196,
                           0.93333333333333335),
    'mediumspringgreen': (0.0, 0.98039215686274506, 0.60392156862745094),
    'mediumturquoise': (   0.28235294117647058,
                           0.81960784313725488,
                           0.80000000000000004),
    'mediumvioletred': (   0.7803921568627451,
                           0.082352941176470587,
                           0.52156862745098043),
    'midnight blue': (   0.098039215686274508,
                         0.098039215686274508,
                         0.4392156862745098),
    'midnightblue': (   0.098039215686274508,
                        0.098039215686274508,
                        0.4392156862745098),
    'mint cream': (0.96078431372549022, 1.0, 0.98039215686274506),
    'mintcream': (0.96078431372549022, 1.0, 0.98039215686274506),
    'misty rose': (1.0, 0.89411764705882357, 0.88235294117647056),
    'mistyrose': (1.0, 0.89411764705882357, 0.88235294117647056),
    'mistyrose1': (1.0, 0.89411764705882357, 0.88235294117647056),
    'mistyrose2': (   0.93333333333333335,
                      0.83529411764705885,
                      0.82352941176470584),
    'mistyrose3': (   0.80392156862745101,
                      0.71764705882352942,
                      0.70980392156862748),
    'mistyrose4': (   0.54509803921568623,
                      0.49019607843137253,
                      0.4823529411764706),
    'moccasin': (1.0, 0.89411764705882357, 0.70980392156862748),
    'navajo white': (1.0, 0.87058823529411766, 0.67843137254901964),
    'navajowhite': (1.0, 0.87058823529411766, 0.67843137254901964),
    'navajowhite1': (1.0, 0.87058823529411766, 0.67843137254901964),
    'navajowhite2': (   0.93333333333333335,
                        0.81176470588235294,
                        0.63137254901960782),
    'navajowhite3': (   0.80392156862745101,
                        0.70196078431372544,
                        0.54509803921568623),
    'navajowhite4': (   0.54509803921568623,
                        0.47450980392156861,
                        0.36862745098039218),
    'navy': (0.0, 0.0, 0.50196078431372548),
    'navy blue': (0.0, 0.0, 0.50196078431372548),
    'navyblue': (0.0, 0.0, 0.50196078431372548),
    'old lace': (   0.99215686274509807,
                    0.96078431372549022,
                    0.90196078431372551),
    'oldlace': (0.99215686274509807, 0.96078431372549022, 0.90196078431372551),
    'olive': (0.5, 0.5, 0.0),
    'olive drab': (   0.41960784313725491,
                      0.55686274509803924,
                      0.13725490196078433),
    'olivedrab': (   0.41960784313725491,
                     0.55686274509803924,
                     0.13725490196078433),
    'olivedrab1': (0.75294117647058822, 1.0, 0.24313725490196078),
    'olivedrab2': (   0.70196078431372544,
                      0.93333333333333335,
                      0.22745098039215686),
    'olivedrab3': (   0.60392156862745094,
                      0.80392156862745101,
                      0.19607843137254902),
    'olivedrab4': (   0.41176470588235292,
                      0.54509803921568623,
                      0.13333333333333333),
    'orange': (1.0, 0.6470588235294118, 0.0),
    'orange red': (1.0, 0.27058823529411763, 0.0),
    'orange1': (1.0, 0.6470588235294118, 0.0),
    'orange2': (0.93333333333333335, 0.60392156862745094, 0.0),
    'orange3': (0.80392156862745101, 0.52156862745098043, 0.0),
    'orange4': (0.54509803921568623, 0.35294117647058826, 0.0),
    'orangered': (1.0, 0.27058823529411763, 0.0),
    'orangered1': (1.0, 0.27058823529411763, 0.0),
    'orangered2': (0.93333333333333335, 0.25098039215686274, 0.0),
    'orangered3': (0.80392156862745101, 0.21568627450980393, 0.0),
    'orangered4': (0.54509803921568623, 0.14509803921568629, 0.0),
    'orchid': (0.85490196078431369, 0.4392156862745098, 0.83921568627450982),
    'orchid1': (1.0, 0.51372549019607838, 0.98039215686274506),
    'orchid2': (0.93333333333333335, 0.47843137254901963, 0.9137254901960784),
    'orchid3': (0.80392156862745101, 0.41176470588235292, 0.78823529411764703),
    'orchid4': (0.54509803921568623, 0.27843137254901962, 0.53725490196078429),
    'pale goldenrod': (   0.93333333333333335,
                          0.90980392156862744,
                          0.66666666666666663),
    'pale green': (   0.59607843137254901,
                      0.98431372549019602,
                      0.59607843137254901),
    'pale turquoise': (   0.68627450980392157,
                          0.93333333333333335,
                          0.93333333333333335),
    'pale violet red': (   0.85882352941176465,
                           0.4392156862745098,
                           0.57647058823529407),
    'palegoldenrod': (   0.93333333333333335,
                         0.90980392156862744,
                         0.66666666666666663),
    'palegreen': (   0.59607843137254901,
                     0.98431372549019602,
                     0.59607843137254901),
    'palegreen1': (0.60392156862745094, 1.0, 0.60392156862745094),
    'palegreen2': (   0.56470588235294117,
                      0.93333333333333335,
                      0.56470588235294117),
    'palegreen3': (   0.48627450980392156,
                      0.80392156862745101,
                      0.48627450980392156),
    'palegreen4': (   0.32941176470588235,
                      0.54509803921568623,
                      0.32941176470588235),
    'paleturquoise': (   0.68627450980392157,
                         0.93333333333333335,
                         0.93333333333333335),
    'paleturquoise1': (0.73333333333333328, 1.0, 1.0),
    'paleturquoise2': (   0.68235294117647061,
                          0.93333333333333335,
                          0.93333333333333335),
    'paleturquoise3': (   0.58823529411764708,
                          0.80392156862745101,
                          0.80392156862745101),
    'paleturquoise4': (   0.40000000000000002,
                          0.54509803921568623,
                          0.54509803921568623),
    'palevioletred': (   0.85882352941176465,
                         0.4392156862745098,
                         0.57647058823529407),
    'palevioletred1': (1.0, 0.50980392156862742, 0.6705882352941176),
    'palevioletred2': (   0.93333333333333335,
                          0.47450980392156861,
                          0.62352941176470589),
    'palevioletred3': (   0.80392156862745101,
                          0.40784313725490196,
                          0.53725490196078429),
    'palevioletred4': (   0.54509803921568623,
                          0.27843137254901962,
                          0.36470588235294116),
    'papaya whip': (1.0, 0.93725490196078431, 0.83529411764705885),
    'papayawhip': (1.0, 0.93725490196078431, 0.83529411764705885),
    'peach puff': (1.0, 0.85490196078431369, 0.72549019607843135),
    'peachpuff': (1.0, 0.85490196078431369, 0.72549019607843135),
    'peachpuff1': (1.0, 0.85490196078431369, 0.72549019607843135),
    'peachpuff2': (   0.93333333333333335,
                      0.79607843137254897,
                      0.67843137254901964),
    'peachpuff3': (   0.80392156862745101,
                      0.68627450980392157,
                      0.58431372549019611),
    'peachpuff4': (   0.54509803921568623,
                      0.46666666666666667,
                      0.396078431372549),
    'peru': (0.80392156862745101, 0.52156862745098043, 0.24705882352941178),
    'pink': (1.0, 0.75294117647058822, 0.79607843137254897),
    'pink1': (1.0, 0.70980392156862748, 0.77254901960784317),
    'pink2': (0.93333333333333335, 0.66274509803921566, 0.72156862745098038),
    'pink3': (0.80392156862745101, 0.56862745098039214, 0.61960784313725492),
    'pink4': (0.54509803921568623, 0.38823529411764707, 0.42352941176470588),
    'plum': (0.8666666666666667, 0.62745098039215685, 0.8666666666666667),
    'plum1': (1.0, 0.73333333333333328, 1.0),
    'plum2': (0.93333333333333335, 0.68235294117647061, 0.93333333333333335),
    'plum3': (0.80392156862745101, 0.58823529411764708, 0.80392156862745101),
    'plum4': (0.54509803921568623, 0.40000000000000002, 0.54509803921568623),
    'powder blue': (   0.69019607843137254,
                       0.8784313725490196,
                       0.90196078431372551),
    'powderblue': (   0.69019607843137254,
                      0.8784313725490196,
                      0.90196078431372551),
    'purple': (0.62745098039215685, 0.12549019607843137, 0.94117647058823528),
    'purple1': (0.60784313725490191, 0.18823529411764706, 1.0),
    'purple2': (0.56862745098039214, 0.17254901960784313, 0.93333333333333335),
    'purple3': (0.49019607843137253, 0.14901960784313725, 0.80392156862745101),
    'purple4': (0.33333333333333331, 0.10196078431372549, 0.54509803921568623),
    'red': (1.0, 0.0, 0.0),
    'red1': (1.0, 0.0, 0.0),
    'red2': (0.93333333333333335, 0.0, 0.0),
    'red3': (0.80392156862745101, 0.0, 0.0),
    'red4': (0.54509803921568623, 0.0, 0.0),
    'rosy brown': (   0.73725490196078436,
                      0.5607843137254902,
                      0.5607843137254902),
    'rosybrown': (0.73725490196078436, 0.5607843137254902, 0.5607843137254902),
    'rosybrown1': (1.0, 0.75686274509803919, 0.75686274509803919),
    'rosybrown2': (   0.93333333333333335,
                      0.70588235294117652,
                      0.70588235294117652),
    'rosybrown3': (   0.80392156862745101,
                      0.60784313725490191,
                      0.60784313725490191),
    'rosybrown4': (   0.54509803921568623,
                      0.41176470588235292,
                      0.41176470588235292),
    'royal blue': (   0.25490196078431371,
                      0.41176470588235292,
                      0.88235294117647056),
    'royalblue': (   0.25490196078431371,
                     0.41176470588235292,
                     0.88235294117647056),
    'royalblue1': (0.28235294117647058, 0.46274509803921571, 1.0),
    'royalblue2': (   0.2627450980392157,
                      0.43137254901960786,
                      0.93333333333333335),
    'royalblue3': (   0.22745098039215686,
                      0.37254901960784315,
                      0.80392156862745101),
    'royalblue4': (   0.15294117647058825,
                      0.25098039215686274,
                      0.54509803921568623),
    'saddle brown': (   0.54509803921568623,
                        0.27058823529411763,
                        0.074509803921568626),
    'saddlebrown': (   0.54509803921568623,
                       0.27058823529411763,
                       0.074509803921568626),
    'salmon': (0.98039215686274506, 0.50196078431372548, 0.44705882352941179),
    'salmon1': (1.0, 0.5490196078431373, 0.41176470588235292),
    'salmon2': (0.93333333333333335, 0.50980392156862742, 0.3843137254901961),
    'salmon3': (0.80392156862745101, 0.4392156862745098, 0.32941176470588235),
    'salmon4': (0.54509803921568623, 0.29803921568627451, 0.22352941176470589),
    'sandy brown': (   0.95686274509803926,
                       0.64313725490196083,
                       0.37647058823529411),
    'sandybrown': (   0.95686274509803926,
                      0.64313725490196083,
                      0.37647058823529411),
    'sea green': (0.1803921568627451, 0.54509803921568623, 0.3411764705882353),
    'seagreen': (0.1803921568627451, 0.54509803921568623, 0.3411764705882353),
    'seagreen1': (0.32941176470588235, 1.0, 0.62352941176470589),
    'seagreen2': (   0.30588235294117649,
                     0.93333333333333335,
                     0.58039215686274515),
    'seagreen3': (   0.2627450980392157,
                     0.80392156862745101,
                     0.50196078431372548),
    'seagreen4': (0.1803921568627451, 0.54509803921568623, 0.3411764705882353),
    'seashell': (1.0, 0.96078431372549022, 0.93333333333333335),
    'seashell1': (1.0, 0.96078431372549022, 0.93333333333333335),
    'seashell2': (   0.93333333333333335,
                     0.89803921568627454,
                     0.87058823529411766),
    'seashell3': (   0.80392156862745101,
                     0.77254901960784317,
                     0.74901960784313726),
    'seashell4': (   0.54509803921568623,
                     0.52549019607843139,
                     0.50980392156862742),
    'sienna': (0.62745098039215685, 0.32156862745098042, 0.17647058823529413),
    'sienna1': (1.0, 0.50980392156862742, 0.27843137254901962),
    'sienna2': (0.93333333333333335, 0.47450980392156861, 0.25882352941176473),
    'sienna3': (0.80392156862745101, 0.40784313725490196, 0.22352941176470589),
    'sienna4': (0.54509803921568623, 0.27843137254901962, 0.14901960784313725),
    'silver': (0.75, 0.75, 0.75),
    'sky blue': (   0.52941176470588236,
                    0.80784313725490198,
                    0.92156862745098034),
    'skyblue': (0.52941176470588236, 0.80784313725490198, 0.92156862745098034),
    'skyblue1': (0.52941176470588236, 0.80784313725490198, 1.0),
    'skyblue2': (   0.49411764705882355,
                    0.75294117647058822,
                    0.93333333333333335),
    'skyblue3': (   0.42352941176470588,
                    0.65098039215686276,
                    0.80392156862745101),
    'skyblue4': (0.29019607843137257, 0.4392156862745098, 0.54509803921568623),
    'slate blue': (   0.41568627450980394,
                      0.35294117647058826,
                      0.80392156862745101),
    'slate gray': (   0.4392156862745098,
                      0.50196078431372548,
                      0.56470588235294117),
    'slate grey': (   0.4392156862745098,
                      0.50196078431372548,
                      0.56470588235294117),
    'slateblue': (   0.41568627450980394,
                     0.35294117647058826,
                     0.80392156862745101),
    'slateblue1': (0.51372549019607838, 0.43529411764705883, 1.0),
    'slateblue2': (   0.47843137254901963,
                      0.40392156862745099,
                      0.93333333333333335),
    'slateblue3': (   0.41176470588235292,
                      0.34901960784313724,
                      0.80392156862745101),
    'slateblue4': (   0.27843137254901962,
                      0.23529411764705882,
                      0.54509803921568623),
    'slategray': (   0.4392156862745098,
                     0.50196078431372548,
                     0.56470588235294117),
    'slategray1': (0.77647058823529413, 0.88627450980392153, 1.0),
    'slategray2': (   0.72549019607843135,
                      0.82745098039215681,
                      0.93333333333333335),
    'slategray3': (   0.62352941176470589,
                      0.71372549019607845,
                      0.80392156862745101),
    'slategray4': (   0.42352941176470588,
                      0.4823529411764706,
                      0.54509803921568623),
    'slategrey': (   0.4392156862745098,
                     0.50196078431372548,
                     0.56470588235294117),
    'snow': (1.0, 0.98039215686274506, 0.98039215686274506),
    'snow1': (1.0, 0.98039215686274506, 0.98039215686274506),
    'snow2': (0.93333333333333335, 0.9137254901960784, 0.9137254901960784),
    'snow3': (0.80392156862745101, 0.78823529411764703, 0.78823529411764703),
    'snow4': (0.54509803921568623, 0.53725490196078429, 0.53725490196078429),
    'spring green': (0.0, 1.0, 0.49803921568627452),
    'springgreen': (0.0, 1.0, 0.49803921568627452),
    'springgreen1': (0.0, 1.0, 0.49803921568627452),
    'springgreen2': (0.0, 0.93333333333333335, 0.46274509803921571),
    'springgreen3': (0.0, 0.80392156862745101, 0.40000000000000002),
    'springgreen4': (0.0, 0.54509803921568623, 0.27058823529411763),
    'steel blue': (   0.27450980392156865,
                      0.50980392156862742,
                      0.70588235294117652),
    'steelblue': (   0.27450980392156865,
                     0.50980392156862742,
                     0.70588235294117652),
    'steelblue1': (0.38823529411764707, 0.72156862745098038, 1.0),
    'steelblue2': (   0.36078431372549019,
                      0.67450980392156867,
                      0.93333333333333335),
    'steelblue3': (   0.30980392156862746,
                      0.58039215686274515,
                      0.80392156862745101),
    'steelblue4': (   0.21176470588235294,
                      0.39215686274509803,
                      0.54509803921568623),
    'tan': (0.82352941176470584, 0.70588235294117652, 0.5490196078431373),
    'tan1': (1.0, 0.6470588235294118, 0.30980392156862746),
    'tan2': (0.93333333333333335, 0.60392156862745094, 0.28627450980392155),
    'tan3': (0.80392156862745101, 0.52156862745098043, 0.24705882352941178),
    'tan4': (0.54509803921568623, 0.35294117647058826, 0.16862745098039217),
    'teal': (0.0, 0.5, 0.5),
    'thistle': (0.84705882352941175, 0.74901960784313726, 0.84705882352941175),
    'thistle1': (1.0, 0.88235294117647056, 1.0),
    'thistle2': (   0.93333333333333335,
                    0.82352941176470584,
                    0.93333333333333335),
    'thistle3': (   0.80392156862745101,
                    0.70980392156862748,
                    0.80392156862745101),
    'thistle4': (0.54509803921568623, 0.4823529411764706, 0.54509803921568623),
    'tomato': (1.0, 0.38823529411764707, 0.27843137254901962),
    'tomato1': (1.0, 0.38823529411764707, 0.27843137254901962),
    'tomato2': (0.93333333333333335, 0.36078431372549019, 0.25882352941176473),
    'tomato3': (0.80392156862745101, 0.30980392156862746, 0.22352941176470589),
    'tomato4': (0.54509803921568623, 0.21176470588235294, 0.14901960784313725),
    'turquoise': (   0.25098039215686274,
                     0.8784313725490196,
                     0.81568627450980391),
    'turquoise1': (0.0, 0.96078431372549022, 1.0),
    'turquoise2': (0.0, 0.89803921568627454, 0.93333333333333335),
    'turquoise3': (0.0, 0.77254901960784317, 0.80392156862745101),
    'turquoise4': (0.0, 0.52549019607843139, 0.54509803921568623),
    'violet': (0.93333333333333335, 0.50980392156862742, 0.93333333333333335),
    'violet red': (   0.81568627450980391,
                      0.12549019607843137,
                      0.56470588235294117),
    'violetred': (   0.81568627450980391,
                     0.12549019607843137,
                     0.56470588235294117),
    'violetred1': (1.0, 0.24313725490196078, 0.58823529411764708),
    'violetred2': (   0.93333333333333335,
                      0.22745098039215686,
                      0.5490196078431373),
    'violetred3': (   0.80392156862745101,
                      0.19607843137254902,
                      0.47058823529411764),
    'violetred4': (   0.54509803921568623,
                      0.13333333333333333,
                      0.32156862745098042),
    'wheat': (0.96078431372549022, 0.87058823529411766, 0.70196078431372544),
    'wheat1': (1.0, 0.90588235294117647, 0.72941176470588232),
    'wheat2': (0.93333333333333335, 0.84705882352941175, 0.68235294117647061),
    'wheat3': (0.80392156862745101, 0.72941176470588232, 0.58823529411764708),
    'wheat4': (0.54509803921568623, 0.49411764705882355, 0.40000000000000002),
    'white': (1.0, 1.0, 1.0),
    'white smoke': (   0.96078431372549022,
                       0.96078431372549022,
                       0.96078431372549022),
    'whitesmoke': (   0.96078431372549022,
                      0.96078431372549022,
                      0.96078431372549022),
    'yellow': (1.0, 1.0, 0.0),
    'yellow green': (   0.60392156862745094,
                        0.80392156862745101,
                        0.19607843137254902),
    'yellow1': (1.0, 1.0, 0.0),
    'yellow2': (0.93333333333333335, 0.93333333333333335, 0.0),
    'yellow3': (0.80392156862745101, 0.80392156862745101, 0.0),
    'yellow4': (0.54509803921568623, 0.54509803921568623, 0.0),
    'yellowgreen': (   0.60392156862745094,
                       0.80392156862745101,
                       0.19607843137254902)}

palettes = {
    "gray": GradientPalette("black", "white"),
    "red-blue": GradientPalette("red", "blue")
}


