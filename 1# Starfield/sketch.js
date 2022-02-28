// List of stars
var stars = [];

// Speed of star
var speed;

function setup() {
  let canvas = createCanvas(900, 900);
  canvas.position(windowWidth/2 - width/2, windowHeight/2 - height/2) // to center the star

  // Creating all the stars
  for (var i = 0; i < 1100; i++) {
    stars[i] = new Star();
  }
}

function draw() {
  speed = map(mouseX, 0, width, 0, 50);
  background(0);
  translate(width / 2, height / 2);
  for (var i = 0; i < stars.length; i++) {
    stars[i].update();
    stars[i].show();
  }
}