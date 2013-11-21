// Learning Processing
// Daniel Shiffman
// http://www.learningprocessing.com

// Example 16-6: Drawing a grid of squares

// Size of each cell in the grid, ratio of window size to video size
int videoScale = 20;

// Number of columns and rows in our system
int cols = 30;
int rows = 30;


public class Point {
    public int x;
    public int y;
    public int certainty;
}

// The upper-right-hand corner of each grid square
Point[][] grid = new Point[cols][rows];


void setup() {
  size(rows*videoScale,cols*videoScale);
  
  //Begin loop for columns
  for (int i = 0; i < cols; i++) {
    //Begin loop for rows
    for (int j = 0; j < rows; j++) {
      //save coordinates
      grid[i][j] = new Point();
      grid[i][j].x = i*videoScale;
      grid[i][j].y = j*videoScale;
      grid[i][j].certainty = 0;
      
      // Draw grid to the screen
      fill(255);
      stroke(0);
      // For every column and row, a rectangle is drawn at an (x,y) location scaled and sized by videoScale.
      rect(grid[i][j].x,grid[i][j].y,videoScale,videoScale); 
    }
  }
}

void draw() {

}

void serialEvent(Serial port) {
  String sample = port.readStringUntil('\n');
  sample = trim(sample);
  //figure out how to decide which square to colour
}

//just here to test certainty colourings
void keyPressed() {
  if (keyCode == UP) {  //increase value of square
    addLine(5,5,true);
  }
  if (keyCode == DOWN) {  //decrease certainty of square
    addLine(5,5,false);
  }
}

//adds a line to the specified square of the specified colour
void addLine(int i, int j, boolean add) {
  if(add && grid[i][j].certainty < 3) { 
    grid[i][j].certainty += 1; 
  } else if(add == false && grid[i][j].certainty > 0) { 
    grid[i][j].certainty -= 1;
  }
  Point square = grid[i][j];
  
  //reset square
  stroke(0);
  fill(255);
  rect(square.x,square.y,
        videoScale,videoScale);
  //draw appropriately sized square
  stroke(0);
  fill(colour(square.certainty));
  rect(square.x,square.y,
        videoScale,videoScale);
}

//computes the correct colour to draw rectangle for given certainty
int colour(int certainty) {
  if (certainty < 0 || certainty > 3) { //validation
    return 55;  //hopefully distinguishable from other colours
  } else {
    return 255 - (certainty*85);
  }
}
