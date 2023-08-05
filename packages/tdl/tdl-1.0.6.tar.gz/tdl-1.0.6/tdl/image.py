"""
    This module could still be unstable
"""
import ctypes

from color import _tcodcolor, _tcodcolorget
from tcod import _lib

class Image(object):

    __slots__ = ('_as_parameter_',)

    def __init__(self, width, height):
        self._as_parameter_ = _lib.TCOD_image_new(width, height)

    def __del__(self):
        try:
            _lib.TCOD_image_delete(self)
        except StandardError: # try to ignore most errors
            pass

    def clear(self, color):
        """Clear the image to a color.
        """
        _lib.TCOD_image_clear(_tcodcolor(color))

    def get_size(self):
        """Return the size of the image as (width, height)
        """
        width, height = ctypes.c_int(), ctypes.c_int()
        _lib.TCOD_image_get_size(self, width, height)
        return width.value, height.value

    def save(self, filepath):
        """Saves the image to the filepath as a .bmp file.

        filepath must be a string to a file but not a file object
        """
        assert isinstance(filepath, str)
        _lib.TCOD_image_save(self, filepath)

    def get_pixel(self, x, y):
        """Get a pixel from the image.
        """
        return _tcodcolorget(_lib.TCOD_image_get_pixel(self, x, y))

    def get_mipmap_pixel(self, x1, y1, x2, y2):
        """Get a mipmapped pixel that starts at x1 and y2 and ends at x2 and y2.
        """
        return _tcodcolorget(_lib.TCOD_image_get_mipmap_pixel(self, x1, y1, x2, y2))

    def set_pixel(self, x, y, color):
        """Set the pixel at x and y to color.

        This is slow.
        """
        _lib.TCOD_image_put_pixel(self, x, y, _tcodcolor(color))

    def set_keycolor(self, color):
        """Set the color that will be transparent.
        """
        _lib.TCOD_image_set_key_color(self, _tcodcolor(color))

    def get_visible(self, x, y):
        """Checks if the pixel at x and y is visible or transparent.

        Returns True if visible.
        """
        return not _lib.TCOD_image_is_pixel_transparent(self, x, y)

class _ImageFromStruct(Image):

    def __init__(self, struct):
        self._as_parameter_ = struct

def load(filepath):
    """Loads a .bmp file and returns an Image.
    """
    return _ImageFromStruct(_lib.TCOD_image_load(filepath))

__all__ = [var for var in locals().keys() if not '_' in var[0]]