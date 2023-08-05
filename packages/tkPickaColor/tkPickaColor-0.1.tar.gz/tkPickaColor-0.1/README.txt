************
TkPickaColor
************
This widget provides a more full featured color-chooser for Linux Tkinter users. The widget is invoked by...
  from tkPickaColor import tkpickacolor
  tkpickacolor.askColors()

askColors returns a list of up-to eight color strings that the user has selected.

The screen has seven display or functional areas:

* The spectrum selector

* The value selector

* a color swatch

* color chips

* a manual color entry field

* Favorites palette

* Harmonies palette

.. image:: VIEWME.jpg

The spectrum selector
*********************
  Dragging the cursor (left-click & hold) over the spectrum changes swatche's hue and saturation.

  * Pressing Ctrl-left or -right an arrow changes the swatch's hue

  * Pressing a Ctrl-up or -down arrow changes the swatch's saturation


The value selector
******************
  Dragging the cursor (with left-click & hold) changes the swatch's color *value* level.

  * Pressing a Alt-left or -right arrow changes the swatch's color value.

The swatch
**********
  The swatch displays a larger color sample with the text of hsv levels.

  * Left-clicking sends swatch's color to a chip. (also Alt-C)

  * Right-clicking sends the swatch's color to the harmonies palette. (also Alt-P)

  * Ctrl-left-clicking copies the current color to memory.

The color chips
***************
  The eight chips at the screen's bottom display the colors to be returned to the calling program. These are returned as the rgb strings used by Tkinter ("#ABCDEF") when the "Ok" menu button is pressed (alt-O)

  * Left-clicking swaps the colors of adjoining chips.

  * Right-clicking deletes a chip's color.

  .. note::
    When all eight chips are assigned a color and a new color is to be added, the left chip's color is deleted, all the remaining colors are shifted one place to the left, and the new color is added to the right most chip.

The manual entry field
**********************
  The yellow entry field allows typing a six-digit hexadecimal number (from 0 to F). If a correct value is entered the swatch's color is changed to match. If an incorrect value is entered the prior value is returned and the swatch is unchanged.

  .. Hint::
    Three identical pairs of hexadecimal numbers (e.g.. 4B4B4B) will create a gray. "#FFFFFF" = white, "#000000" = black, "#FF0000" = red, "#00FF00" = green,"#0000FF" = blue,

The Favorites palette
*********************
  Here user favorites, that are saved over sessions, are displayed. Once a color has been copied from the swatch or the harmonies palette it may be pasted to a favorite square with a control-left-click. The Favorites menu allows the palette to be saved, deleted (cleared), and reloaded from the last save copy. Tidy moves the empty squares to the end of the palette.

  * Left-clicking a favorite sends the color to a chip.

  * Right-clicking a favorite sets the swatch's color.

  * Cntrl-left-clicking paste the color in memory to the selected square.

  * Cntrl-right-clicking clears a color from the selected square.


The Harmonies palettes
**********************
  These palettes show tints and shades for various colors (see comment below).

  * Left-clicking a color sends it to a chip.

  * Right-clicking a color sets the swatch's color.

  * Ctrl-left-click copies the current color to memory.

Miscellanea
=========== 
    
  The spectrum is a gif image 360 pixels wide and 100 pixels high. The x, y cursor coordinates over the image is mapped to the hue (0-360) and saturation levels of a color (0-100) in hvs color space (see below). Similarly, the values graphics's x coordinates are mapped to the 0-100 levels of the color's value component.

  **Color spaces**. Computer based colors may be represented in different models of three-dimensional color spaces. The two used here are the red-green-blue color space (rgb) and the hue-saturation-value form (hsv). These colors are written in shorthand formulas.

  The **RGB** color space is written as three numeric values, one each for the red, green, and blue elements that are combined to create a color. (Actually sometimes more than three values are used including one indicating transparency). These values range from 0 (00) to 255 (FF). Tkinter uses hexadecimal strings combining these three numbers and run from '#000000' to '#FFFFFF'. Other representations include decimal strings ('00 00 00' to '255 255 255') or as tuples, e.g..(255, 255, 255).

  The **HSV** space describes colors with 360 *hues*, 100 levels of *saturation*, and 100 of *value*. These are written as tuples, that is from (0, 0, 0) to (360, 100, 100). Roughly, hues are the colors, saturation describes a color's intensity, similar to the results of adding white paint to a color of paint in the analog world. "Value is a measure of where a particular color lies along the lightness–darkness axis" (ref: Freedictionary.com)

  The colors of the Harmonies palettes are created in hsv space conceptually as though the spectrum's hues are arranged in a circle and then rotated by certain degrees. For example, a complementary color (which is directly across the circle from an original) is calculated by rotating the hue 180-degrees. The tints are created by holding a color's hue and saturation constant and varying the values. Similarly the shades are calculated by varying a color's saturation. Note that these palettes may not have any value in a color-theory sense, because this calculation is simply translated to the red-green-blue color space from the artist's "color wheel" in red-yellow-blue color space. 
