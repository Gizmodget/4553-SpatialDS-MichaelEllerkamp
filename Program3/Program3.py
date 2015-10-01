"""
@author - Michael Ellerkamp
@date -  09/29/2015
@description - This program uses pantograph to create graphics in a web browser
The scene created consists of 3 polygons and 3 points. The goal of the program
was to create shapes that react the the edges of the screen and other shapes in
the scene. Behavior consists of collision, motion, and color change. 
@resources - I found code and methods at http://pythonhelper.com and used some polygon code.
"""
"""Point and Rectangle classes.
This code is in the public domain.
Point  -- point with (x,y) coordinates
Rect  -- two points, forming a rectangle
"""
import pantograph
import math
import sys
import itertools

class Point:

    """A point identified by (x,y) coordinates.
    supports: +, -, *, /, str, repr
    length  -- calculate length of vector to point from origin
    distance_to  -- calculate distance between two points
    as_tuple  -- construct tuple (x,y)
    clone  -- construct a duplicate
    integerize  -- convert x & y to integers
    floatize  -- convert x & y to floats
    move_to  -- reset x & y
    slide  -- move (in place) +dx, +dy, as spec'd by point
    slide_xy  -- move (in place) +dx, +dy
    rotate  -- rotate around the origin
    rotate_about  -- rotate around another point
    """

    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __add__(self, p):
        """Point(x1+x2, y1+y2)"""
        return Point(self.x+p.x, self.y+p.y)

    def __sub__(self, p):
        """Point(x1-x2, y1-y2)"""
        return Point(self.x-p.x, self.y-p.y)

    def __mul__( self, scalar ):
        """Point(x1*x2, y1*y2)"""
        return Point(self.x*scalar, self.y*scalar)

    def __div__(self, scalar):
        """Point(x1/x2, y1/y2)"""
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def distance_to(self, p):
        """Calculate the distance between two points."""
        return (self - p).length()

    def as_tuple(self):
        """(x, y)"""
        return (self.x, self.y)

    def clone(self):
        """Return a full copy of this point."""
        return Point(self.x, self.y)

    def integerize(self):
        """Convert co-ordinate values to integers."""
        self.x = int(self.x)
        self.y = int(self.y)

    def floatize(self):
        """Convert co-ordinate values to floats."""
        self.x = float(self.x)
        self.y = float(self.y)

    def move_to(self, x, y):
        """Reset x & y coordinates."""
        self.x = x
        self.y = y

    def slide(self, p):
        '''Move to new (x+dx,y+dy).
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + p.x
        self.y = self.y + p.y

    def slide_xy(self, dx, dy):
        '''Move to new (x+dx,y+dy).
        Can anyone think up a better name for this function?
        slide? shift? delta? move_by?
        '''
        self.x = self.x + dx
        self.y = self.y + dy

    def rotate(self, rad):
        """Rotate counter-clockwise by rad radians.
        Positive y goes *up,* as in traditional mathematics.
        Interestingly, you can use this in y-down computer graphics, if
        you just remember that it turns clockwise, rather than
        counter-clockwise.
        The new position is returned as a new Point.
        """
        s, c = [f(rad) for f in (math.sin, math.cos)]
        x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
        return Point(x,y)

    def rotate_about(self, p, theta):
        """Rotate counter-clockwise around a point, by theta degrees.
        Positive y goes *up,* as in traditional mathematics.
        The new position is returned as a new Point.
        """
        result = self.clone()
        result.slide(-p.x, -p.y)
        result.rotate(theta)
        result.slide(p.x, p.y)
        return result

    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction

    def update_position(self, canvas):
        """driver.update creates a clear rectangle the size of the browser
        We pass that rectangle to the update position method of our shapes and 
        call the rectangle canvas. This method reads when a point hits the edge
        of the canvas and changes the direction of the point in order to prevent
        the point from going out of  bounds as well as handles the basic movement
        of the point. Each of the 8 cardinal directions are implemented by 
        changing the x and/or y coordinate of the point by +/- 1.
        """
        if self.x <= 0:
            if self.direction == "SW":
                self.direction = "SE"
            if self.direction == "W":
                self.direction = "E"
            if self.direction == "NW":
                self.direction = "NE"
        if self.x >= canvas.width:
            if self.direction == "SE":
                self.direction = "SW"
            if self.direction == "E":
                self.direction = "W"
            if self.direction == "NE":
                self.direction = "NW"
        if self.y <= 0:
            if self.direction == "NW":
                self.direction = "SW"
            if self.direction == "N":
                self.direction = "S"
            if self.direction == "NE":
                self.direction = "SE"
        if self.y >= canvas.height:
            if self.direction == "SW":
                self.direction = "NW"
            if self.direction == "S":
                self.direction = "N"
            if self.direction == "SE":
                self.direction = "NE"
        if self.direction == "N":
            self.y -= 1
        if self.direction == "NE":
            self.y -= 1
            self.x += 1
        if self.direction == "E":
            self.x += 1
        if self.direction == "SE":
            self.x += 1
            self.y += 1
        if self.direction == "S":
            self.y += 1
        if self.direction == "SW":
            self.x -= 1
            self.y += 1
        if self.direction == "W":
            self.x -= 1
        if self.direction == "NW":
            self.y -= 1
            self.x -= 1



class Rect:

    """A rectangle identified by two points.
    The rectangle stores left, top, right, and bottom values.
    Coordinates are based on screen coordinates.
    origin                               top
       +-----> x increases                |
       |                           left  -+-  right
       v                                  |
    y increases                         bottom
    set_points  -- reset rectangle coordinates
    contains  -- is a point inside?
    overlaps  -- does a rectangle overlap?
    top_left  -- get top-left corner
    bottom_right  -- get bottom-right corner
    expanded_by  -- grow (or shrink)
    """

    def __init__(self, pt1, pt2):
        """Initialize a rectangle from two points."""
        self.set_points(pt1, pt2)

    def set_points(self, pt1, pt2):
        """Reset the rectangle coordinates."""
        (x1, y1) = pt1.as_tuple()
        (x2, y2) = pt2.as_tuple()
        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

    def contains(self, pt):
        """Return true if a point is inside the rectangle."""
        x,y = pt.as_tuple()
        return (self.left <= x <= self.right and
                self.top <= y <= self.bottom)

    def overlaps(self, other):
        """Return true if a rectangle overlaps this rectangle."""
        return (self.right > other.left and self.left < other.right and
                self.top < other.bottom and self.bottom > other.top)

    def top_left(self):
        """Return the top-left corner as a Point."""
        return Point(self.left, self.top)

    def bottom_right(self):
        """Return the bottom-right corner as a Point."""
        return Point(self.right, self.bottom)

    def expanded_by(self, n):
        """Return a rectangle with extended borders.
        Create a new rectangle that is wider and taller than the
        immediate one. All sides are extended by "n" points.
        """
        p1 = Point(self.left-n, self.top-n)
        p2 = Point(self.right+n, self.bottom+n)
        return Rect(p1, p2)

    def __str__( self ):
        return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,                                         self.right,self.bottom)

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__,                             Point(self.left, self.top),                             Point(self.right, self.bottom))

class Polygon:

    def __init__(self, pts=[]):
        """Initialize a polygon from list of points."""
        self.set_points(pts)

    def set_points(self, pts):
        """Reset the poly coordinates."""

        self.minX = sys.maxint
        self.minY = sys.maxint
        self.maxX = sys.maxint * -1
        self.maxY = sys.maxint * -1

        self.points = []
        #self.mbr = Rect()
        for p in pts:
            x,y = p

            if x < self.minX:
                self.minX = x
            if x > self.maxX:
                self.maxX = x
            if y < self.minY:
                self.minY = y
            if y > self.maxY:
                self.maxY = y

            self.points.append(Point(x,y))

        self.mbr = Rect(Point(self.minX,self.minY),Point(self.maxX,self.maxY))

    def get_points(self):
        generic = []
        for p in self.points:
            generic.append(p.as_tuple())
        return generic
    def set_direction(self,direction):
        assert direction in ['N','NE','E','SE','S','SW','W','NW']

        self.direction = direction
    def update_position(self, canvas):
        """similar to update_position for the point class, the points of the
        polygon are saved as tuples thus requiring the use of creating a new 
        tuple list and sending it back into set_points([(,)])
        This method uses the canvas rectangle to identify borders and changes
        the overall direction of the polygon to prevent any part of it from
        going out of bounds. The direction is bound to the polygon and all
        points of the polygon receive the same modifications based on the
        polygon's direction. Updates are done by adding new tuple points to the
        points list and then sent back into the rectangle as it's new points.
        """
        pts = []
        for P in self.get_points():
            if P[0] <= 0:
                if self.direction == "SW":
                    self.direction = "SE"
                if self.direction == "W":
                    self.direction = "E"
                if self.direction == "NW":
                    self.direction = "NE"
            if P[0] >= canvas.width:
                if self.direction == "SE":
                    self.direction = "SW"
                if self.direction == "E":
                    self.direction = "W"
                if self.direction == "NE":
                    self.direction = "NW"
            if P[1] <= 0:
                if self.direction == "NW":
                    self.direction = "SW"
                if self.direction == "N":
                    self.direction = "S"
                if self.direction == "NE":
                    self.direction = "SE"
            if P[1] >= canvas.height:
                if self.direction == "SW":
                    self.direction = "NW"
                if self.direction == "S":
                    self.direction = "N"
                if self.direction == "SE":
                    self.direction = "NE"
        for P in self.get_points():
            if self.direction == "N":
                pts.append((P[0],P[1]-1))                
#                P.y -= 1
            if self.direction == "NE":
                pts.append((P[0]+1,P[1]-1))
#                P.y -= 1
#                P.x += 1
            if self.direction == "E":
                pts.append((P[0]+1,P[1]))
#                P.x += 1
            if self.direction == "SE":
                pts.append((P[0]+1,P[1]+1))
#                P.x += 1
#                P.y += 1
            if self.direction == "S":
                pts.append((P[0],P[1]+1))
#                P.y += 1
            if self.direction == "SW":
                pts.append((P[0]-1,P[1]+1))
#                P.x -= 1
#                P.y += 1
            if self.direction == "W":
                pts.append((P[0]-1,P[1]))
#                P.x -= 1
            if self.direction == "NW":
                pts.append((P[0]-1,P[1]-1))
#                P.y -= 1
#                P.x -= 1        
        self.set_points(pts)
    # determine if a point is inside a given polygon or not
    # Polygon is a list of (x,y) pairs.
    def point_inside_polygon(self, p):

        n = len(self.points)
        inside =False

        p1x,p1y = self.points[0].as_tuple()
        for i in range(n+1):
            p2x,p2y = self.points[i % n].as_tuple()
            if p.y > min(p1y,p2y):
                if p.y <= max(p1y,p2y):
                    if p.x <= max(p1x,p2x):
                        if p1y != p2y:
                            xinters = (p.y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                        if p1x == p2x or p.x <= xinters:
                            inside = not inside
            p1x,p1y = p2x,p2y

        return inside

    def __str__( self ):
        return "<Polygon \n Points: %s \n Mbr: %s>" % ("".join(str(self.points)),str(self.mbr))

    def __repr__(self):
        return "%s %s" % (self.__class__.__name__,''.join(str(self.points)))


class Driver(pantograph.PantographHandler):

    def setup(self):
        """The intial creation of the shapes and setting their direction"""
        self.poly2 = Polygon([(145, 60),  (201, 69),  (265, 46),  (333, 61),  (352, 99),  (370, 129),  (474, 138),  (474, 178),  (396, 225),  (351, 275),  (376, 312),  (382, 356),  (338, 368),  (287, 302),  (224, 304),  (128, 338),  (110, 316),  (129, 270),  (83, 231),  (65, 51), (83, 163),  (103, 201),  (90, 74), (126, 162)])
        self.poly2.set_direction("E")
        self.poly1 = Polygon([(905, 328),(877, 367),(944, 413),(1004, 384),(1019, 307),(953, 248),(880, 250),(865, 278),(883, 325)])
        self.poly1.set_direction("SW")
        self.poly3 = Polygon([(900, 600), (950,650), (1000, 500)])
        self.poly3.set_direction("N")
        self.p1 = Point(485, 138)
        self.p1.set_direction("SE")
        self.p2 = Point(self.width/2, self.height/2)
        self.p2.set_direction("NW")
        self.p3 = Point(86,163)
        self.p3.set_direction("SE")
        #a separate list for each different type of shape for collision purposes.
        self.polys = [self.poly1, self.poly2, self.poly3]
        self.points = [self.p1, self.p2, self.p3]
    def drawShapes(self):
        """The actual visual creation of the shapes"""
        self.draw_polygon(self.poly3.get_points() , color = "#000")
        self.draw_polygon(self.poly2.get_points() , color = "#000")
        self.draw_polygon(self.poly1.get_points() , color = "#000")
        self.draw_rect(0, 0, self.width, self.height, color= "#000")
        """These statements are used to determine if a point is inside any of the
        3 polygons and if so changes the point's color"""
        if  (self.poly2.point_inside_polygon(self.p1) or self.poly1.point_inside_polygon(self.p1)
         or self.poly3.point_inside_polygon(self.p1)):
            color = "#0F0"
        else:
            color = "#F00"
        self.fill_oval(self.p1.x, self.p1.y, 7, 7, color)

        if  (self.poly2.point_inside_polygon(self.p2) or self.poly1.point_inside_polygon(self.p2)
        or self.poly3.point_inside_polygon(self.p2)):
            color = "#0F0"
        else:
            color = "#F00"
        self.fill_oval(self.p2.x, self.p2.y, 7, 7, color)
        if  (self.poly2.point_inside_polygon(self.p3) or self.poly1.point_inside_polygon(self.p3)
        or self.poly3.point_inside_polygon(self.p3)):
            color = "#0F0"
        else:
            color = "#F00"
        self.fill_oval(self.p3.x, self.p3.y, 7, 7, color)
    def changeDirection():
        pass

    def hitWall():
        pass

    def update(self):
        #creates a rectangle in the shape of the web browser
        self.clear_rect(0, 0, self.width, self.height)
        #method calls to give movement to our shapes
        self.p1.update_position(self)
        self.p2.update_position(self)
        self.p3.update_position(self)
        self.poly1.update_position(self)
        self.poly2.update_position(self)
        self.poly3.update_position(self)
        """iterates between all shapes in a list to check for collision
        for points the formula for distance between 2 points was used.
        Points having radius 7 making any distances less than 14 a collision
        Polygons used a minimum bounding rectangle and the overlaps method call
        to determine collision. """
        for (a, b) in itertools.combinations(self.points, 2):
            if a.distance_to(b) < 14:
                directtmp = a.direction
                a.direction = b.direction
                b.direction = directtmp
        for (a, b) in itertools.combinations(self.polys, 2):
            if a.mbr.overlaps(b.mbr):
                directtmp = a.direction
                a.direction = b.direction
                b.direction = directtmp
        self.drawShapes()


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Driver)
    app.run()