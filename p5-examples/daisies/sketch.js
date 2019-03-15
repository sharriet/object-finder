/*	Demonstration of p5 sketch which uses object location data obtained
 *  by the object_finder.py script implemented as a rudimentary API.
 *  This particular example plots flowers (my 3 year old liked it when
 *  we used real beans to plant virtual flowers!) but of course the 
 *  plotting functions can be replaced with your own.
 *  See project documentation for help getting the API running.
 *  */

var timer = 0;
var data;
var V;

function preload() {
	/* Preload capture data either from JSON file (quicker for testing) or
	 * by invoking the serve_capture.py script running on the localhost
	 */
	//data = loadJSON('http://localhost:8000/json/test.json');
	data = loadJSON('http://localhost:8000/cgi-bin/call_object_finder.py');
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	noStroke;
	fill(255);
	if (data.locs != null) {
		// map the location data to the canvas
		V = mapCoords(data.locs);
	} else {
		console.log("no data")
	}
}

function draw() {
	background(1,57,94);
	// draw things at the object locations!
	plotStems();
	plotFlowers();
	plotNodes();
	// wait 20 seconds between captures
	if (millis() - timer >= 5000) {
		//data = loadJSON('http://localhost:8000/json/test.json', callback);
		data = loadJSON('http://localhost:8000/json/call_object_finder.py', callback);
		timer = millis();
	}
}

/* ------ Helper functions ------ */

function callback(data) {
	/* Update the Vertices array, V, after JSON is returned
	 */
	if (data.locs != null) {
		V = mapCoords(data.locs);
	}
}

function mapCoords(V) {
	/* Map the coordinates of the nodes to the same location on the p5 
	 * canvas and reverse the order from y,x -> x,y
	 * */
	var V_mapped = V.map(function(e) { 
		  e[0] = Math.round(map(e[0], 0, data.h, 0, height));
		  e[1] = Math.round(map(e[1], 0, data.w, 0, width));
		  return e.reverse();
	});
	return V_mapped;
}

function plotNodes() {
  	/* Plots the nodes of the graph at the x,y coordinates
   	* specified in the list of vertices, V
   	* param V: Array of vertices
   	**/
	for (var i=0; i<V.length; i++) {
		noStroke();
		fill(250, 203, 0);
		ellipse(V[i][0], V[i][1], 20, 20);
	}  
}

function plotStems() {
  	/*	Plots the stems of the daisies
   	*	param V: Array of vertices
   	**/
	for (var i=0; i<V.length; i++) {
		stroke(178, 182, 1);
		line(V[i][0], height, V[i][0], V[i][1]);
	}  
}

function plotFlowers() {
	/* Draw some pretty daisies
 	* */
	strokeWeight(4);
  	stroke(255);
  	fill(200);
  	for (var i=0; i<V.length; i++) {
    	var coords = calcMaurer(V[i]);
    	beginShape();
		for (var j=0; j<coords[0].length; j++) {
			vertex(coords[0][j], coords[1][j]);
		}
		endShape(CLOSE);
  	}  
}

function calcMaurer(c, a=30, k=6, d=0.02) {
	/* Calcs x,y coordinates of a Maurer rose
	 * param c: Arr central coordinate of rose [x,y]
	 * param k: Int determines number of petals 
	 * param a: determines radius of flower
	 * param d: Int determines smoothness of curve
	 * */
	var n = Math.ceil( (2*Math.PI)/d );
	var xvals = new Array(n);
	var yvals = new Array(n);
	var theta = 0;
	for (var i=0;i<n;i++) {
		theta = d*i;
		xvals[i] = a*cos(k*theta)*cos(theta)+c[0];
		yvals[i] = a*cos(k*theta)*sin(theta)+c[1];
	}
	return [xvals, yvals];
}
