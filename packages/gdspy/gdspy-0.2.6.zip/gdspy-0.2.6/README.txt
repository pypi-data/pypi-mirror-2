########################################################################
##                                                                    ##
##  Copyright 2009-2010 Lucas Heitzmann Gabrielli                     ##
##                                                                    ##
##  This file is part of gdspy.                                       ##
##                                                                    ##
##  gdspy is free software: you can redistribute it and/or modify it  ##
##  under the terms of the GNU General Public License as published    ##
##  by the Free Software Foundation, either version 3 of the          ##
##  License, or any later version.                                    ##
##                                                                    ##
##  gdspy is distributed in the hope that it will be useful, but      ##
##  WITHOUT ANY WARRANTY; without even the implied warranty of        ##
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the     ##
##  GNU General Public License for more details.                      ##
##                                                                    ##
##  You should have received a copy of the GNU General Public         ##
##  License along with gdspy.  If not, see                            ##
##  <http://www.gnu.org/licenses/>.                                   ##
##                                                                    ##
########################################################################

Version: 0.2.6
Author: Lucas Heitzmann Gabrielli


1. Installation

You will need to have the Python programming language installed in your
system (tested in version 2.6):
  * http://www.python.org/

You will also need the modules numpy, and, optionally, Python Imaging
Library (needed only if you want to output the geometry to an image
file):
  * http://numpy.scipy.org/
  * http://www.pythonware.com/products/pil/index.htm

To install gdspy execute the following command in the folder where you
uncompressed the gdspy distribution:

    python setup.py install


2. Usage

The file gdspy-sample.py is a sample script to show the features
provided by this module.  The complete module reference can be found in
the html folder or online at:
  * http://gdspy.sourceforge.net/


3. History of changes

Version 0.2.6 (February 28, 2011)
  * When saving a GDSII file, ValueError is raised if cell names are
  duplicated.
  * Save screenshot from LayoutViewer.
  * gds_image accepts cells, instead of lists.
  * Outlines supported by gds_image.
  * LayoutViewer stores bounding box information for all visited layers to
  save rendering time.

Version 0.2.5 (December 10, 2010)
  * Empty cells no longer break the LayoutViewer.
  * Removed the gds_view function, superseded by the LayoutViewer, along
  with all dependencies to matplotlib.
  * Fixed a bug in boolean which affected polygons with series of
  collinear vertices.
  * Added a function to slice polygons along straight lines parallel to
  an axis.

Version 0.2.4 (September 04, 2010)
  * Added shortcut to Extents in LayoutViewer: 'Home' or 'a' keys.
  * PolygonSet is the new base class for Round, which might bring some
  incompatibility issues with older scripts.
  * Round elements, PolyPath, L1Path, and Path arc, turn and parametric
  sections are now automatically fractured into pieces defined by a
  maximal number of points.
  * Default value for max_points in boolean changed to 199.
  * Removed the flag to disable the warning about polygons with more
  than 199 vertices.  The warning is shown only for Polygon and
  PolygonSet.
  * Fixed a bug impeding parallel parametric paths to change their
  distance to each other.

Version 0.2.3 (August 09, 2010)
  * Added the PolyPath class to easily create paths with sharp corners.
  * Allow None as item in the colors parameter of LayoutViewer to make
  layers invisible.
  * Added color outline mode to LayoutViewer (change outline color with
  the shift key pressed)
  * Increased the scroll region of the LayoutViewer canvas
  * Added a fast scroll mode: control + drag 2nd mouse button
  * Created a new sample script

Version 0.2.2 (July 29, 2010)
  * Changed the cursor inside LayoutViewer to standard arrow.
  * Fixed bugs with the windows version of LayoutViewer (mouse wheel and
  ruler tool).

Version 0.2.1 (July 29, 2010)
  * Bug fix: gds_image displays an error message instead of crashing
  when PIL is not found.
  * Added class LayoutViewer, which uses Tkinter (included in all python
  distributions) to display the GDSII layout with better controls then
  the gds_view function. This eliminates the matplotlib requirement for
  the viewer functionality.
  * New layer colors extending layers 0 to 63.

Version 0.2.0 (July 19, 2010)
  * Fixed a bug on the turn method of Path.
  * Fixed a bug on the boolean function that would give an error when
  not using Polygon or PolygonSet as input objects.
  * Added the method get_polygons to Cell, CellReference and CellArray.
  * Added a copy method to Cell.
  * Added a flatten method to Cell to remove references (or array
  references) to other cells.
  * Fracture boolean output polygons based on the number of vertices to
  respect the 199 GDSII limit.
                                       
Version 0.1.9 (June 04, 2010)
  * Added L1Path class for Manhattan geometry (L1 norm) paths.

Version 0.1.8 (May 10, 2010)
  * Removed the argument fill from the function gds_view and added a
  more flexible one: style.
  * Fixed a rounding error on the boolean operator affecting polygons
  with holes.
  * Added a rotate method to PolygonSet.
  * Added a warning when PolygonSet has more than 199 points
  * Added a flag to disable the warning about polygons with more than
  199 points.
  * Added a turn method to Path, which is easier to use than arc.
  * Added a direction attribute to Path to keep the information used by
  the segment and turn methods.

Version 0.1.7 (April 12, 2010)
  * New visualization option: save the geometry directly to an image
  file (lower memory use).
  * New functionality added: boolean operations on polygons (polygon
  clipping).
  * All classes were adapted to work with the boolean operations.
  * The attribute size in the initializer of class Text does not have a
  default value any longer.
  * The name of the argument format in the function gds_view was changed
  to fill (to avoid confusion with the built-in function format).

Version 0.1.6 (December 15,  2009)
  * Sample script now include comments and creates an easier to
  understand GDSII example.
  * Improved floating point to integer rounding, which fixes the unit
  errors at the last digit of the precision in the GDSII file.
  * Fixed the font for character 5.
  * Added a flag to gds_view to avoid the automatic call to
  matplotlib.pyplot.show()
  * In gds_view, if a layer number is greater than the number of formats
  defined, the formats are cycled.

Version 0.1.5a (November 15, 2009)
  * Class Text correctly interprets '\n' and '\t' characters.
  * Better documentation format, using the Sphinx engine and the numpy
  format.

Version 0.1.4 (October 5, 2009)
  * Class Text re-written with a different font with no overlaps and
  correct size.

Version 0.1.3a (July 29 2009)
  * Fixed the function to_gds of class Rectangle.

Version 0.1.3 (July 27, 2009)
  * Added the datatype field to all elements of the GDSII structure.

Version 0.1.2 (July 11, 2009)
  * Added the gds_view function to display the GDSII structure using the
  matplotlib module.
  * Fixed a rotation bug in the CellArray class.
  * Module published under the GNU General Public License (GPL)

Version 0.1.1 (May 12, 2009)
  * Added attribute cell_list to class Cell to hold a list of all Cell
  created.
  * Set the default argument cells=Cell.cell_list in the function
  gds_print.
  * Added member to calculate the area for each element type.
  * Added member to calculate the total area of a Cell or the area by
  layer.
  * Included the possibility of creating objects in user-defined units,
  not only nanometers.

Version 0.1.0 (May 1, 2009)
  * Initial release.

########################################################################
##                                                                    ##
##  The Python Imaging Library (PIL) is                               ##
##                                                                    ##
##      Copyright © 1997-2006 by Secret Labs AB                       ##
##      Copyright © 1995-2006 by Fredrik Lundh                        ##
##                                                                    ##
##  By obtaining, using, and/or copying this software and/or its      ##
##  associated documentation, you agree that you have read,           ##
##  understood, and will comply with the following terms and          ##
##  conditions:                                                       ##
##                                                                    ##
##  Permission to use, copy, modify, and distribute this software     ##
##  and its associated documentation for any purpose and without fee  ##
##  is hereby granted, provided that the above copyright notice       ##
##  appears in all copies, and that both that copyright notice and    ##
##  this permission notice appear in supporting documentation, and    ##
##  that the name of Secret Labs AB or the author not be used in      ##
##  advertising or publicity pertaining to distribution of the        ##
##  software without specific, written prior permission.              ##
##                                                                    ##
##  SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH       ##
##  REGARD TO THIS SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF      ##
##  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL SECRET LABS AB OR  ##
##  THE AUTHOR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL   ##
##  DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,     ##
##  DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR  ##
##  OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE   ##
##  USE OR PERFORMANCE OF THIS SOFTWARE.                              ##
##                                                                    ##
########################################################################
