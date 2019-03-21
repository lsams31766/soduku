
var TILE_WIDTH = 50;
var WIDTH = 10 * TILE_WIDTH;
var HEIGHT = 10 * TILE_WIDTH;
var GREEN = "#00ff00"
var BLACK = "#000000"
var RED   = "#ff0000"
var YELLOW = "#ffff00"
var STARTX = 10
var STARTY = 10

// button tags 1 to 81 are grid cells
var LAST_GRID_BUTTON_TAG = 80;
// button tags 82 to 90 are cell value selectors
var LAST_CELL_VALUE_BUTTON_TAG = 89;
// button tag 91 is Clear Cell
var CLEAR_CELL_TAG = 90;
// button tag 92 is Clear All Cells
var CLEAR_ALL_CELLS_TAG = 91;
// button tag 93 is Load Game
var LOAD_GAME_TAG = 92;
// button tag 94 is Solve Puzzle
var SOLVE_PUZZLE_TAG = 93;
// solve custom tag
var SOLVE_CUSTOM_TAG = 94;
// buttons 94 tp 98 are difficulty
var FIRST_DIFFICULTY_TAG = 95;
var LAST_DIFFICULTY_TAG = 99;


var selectedCell = -1; // -1 menas none selected
var selectedDifficulty = 0; // easy
var buttons = new Array(); // array of buttons

var canvas = document.getElementById("myCanvas");
var context = canvas.getContext("2d");

class Button {

	constructor (x, y, width, height, color, text, radius) {
		this.text = text;
		this.x = x;
		this.y = y;
		this.width = width;
		this.height = height;
		this.color = color;
		this.radius = radius;
	}

	print () {
		console.log("button tag:" + this.tag + " text:" + this.text);
	}

	draw () {
		//console.log("draw x " + this.x + " y " + this.y)
		context.font = "24px Arial";
		context.fillStyle = this.color;
		if (this.radius == 0) {
			context.fillRect(this.x,this.y,this.width,this.height);
			context.strokeRect(this.x,this.y,this.width,this.height);		
		} else {
			context.roundRect(this.x,this.y,this.width,this.height,this.radius).fill();
			context.roundRect(this.x,this.y,this.width,this.height,this.radius).stroke();			
		}
		// draw number on top
		context.fillStyle = BLACK;
		context.textAlign = "center";
		context.fillText(this.text, this.x + this.width/2, this.y + 32); // x = fontSize, y = fontSize * 1.2
	}

}

function GetButtonHit(x,y) {
	// check if x,y within any button, if so return button index
	//console.log("GetButtonHit " + x + " " + y)
	for (var i=0; i<buttons.length; i++) {
		btn = buttons[i];
		x2 = parseInt(btn.x) + btn.width;
		y2 = parseInt(btn.y) + btn.height;	
		if ((x>=btn.x) && (x<=x2) && (y>=btn.y) && (y<=y2)) 
		{
			//console.log("hit for " + btn.x + " " + x2 + " " + btn.y + " " + y2);
			return i;
		}
	}
	return -1; // not found
}


window.onload = function() {
	console.log("window onload");    
    drawGame();
    canvas.addEventListener('mousedown',ProcessTouchStart,false);

    $(document).keypress(function(event){
        KeyPressed(event.which);
        });
}

function drawGame() {
	drawButtons(STARTX,STARTY);
	drawGrid(STARTX,STARTY);

/*
	// print buttons
	console.log("Buttons are:")
	for (var i=0; i<buttons.length; i++) {
		buttons[i].print();
	}
*/

}

function drawButtons(startX, startY) {
	var x = startX;
	var y = startY;

	// grid buttons
	for (var i=0; i<9; i++) {
		x = startX;
		for (var j=0; j<9; j++) {
			createButton(x,y,TILE_WIDTH,TILE_WIDTH,GREEN,nbrToString(j+1),0);
			x += TILE_WIDTH;
		}
		y += TILE_WIDTH;
	}

	// cell value buttons
	x = startX;
	y += TILE_WIDTH;
	for (var i=1; i<=9; i++)
	{
		createButton(x,y,TILE_WIDTH-4, TILE_WIDTH,YELLOW,nbrToString(i),5);
		x += TILE_WIDTH+10;
		// TODO make them rounded with a border
	}

	// other buttons
	x = startX;
	y += (1.5*TILE_WIDTH);
	createButton(x,y,160, TILE_WIDTH,YELLOW,"CLEAR CELL",5);
	createButton(x+370,y,160, TILE_WIDTH,YELLOW,"CLEAR ALL",5);
	createButton(x,y+1.5*TILE_WIDTH,200, TILE_WIDTH,YELLOW,"LOAD GAME",5);
	createButton(x,y+3*TILE_WIDTH,200, TILE_WIDTH,YELLOW,"SOLVE GAME",5);
	createButton(x+370,y+3*TILE_WIDTH,200,TILE_WIDTH,YELLOW,"SOLVE CUSTOM",5);


	// opitons - round circles wih value 0 to 4
	x = startX + 220;
	y = y+1.5*TILE_WIDTH
	for (var i=0; i<=4; i++) {
        createButton(x,y,TILE_WIDTH, TILE_WIDTH,YELLOW,i,20);
        x += TILE_WIDTH * 1.2;
	}
	// set difficulty 0 on
	btn = buttons[FIRST_DIFFICULTY_TAG]
	btn.color = RED;
	btn.draw();




}

// support for rounded rectangle
CanvasRenderingContext2D.prototype.roundRect = function (x, y, w, h, r) {
  if (w < 2 * r) r = w / 2;
  if (h < 2 * r) r = h / 2;
  this.beginPath();
  this.moveTo(x+r, y);
  this.arcTo(x+w, y,   x+w, y+h, r);
  this.arcTo(x+w, y+h, x,   y+h, r);
  this.arcTo(x,   y+h, x,   y,   r);
  this.arcTo(x,   y,   x+w, y,   r);
  this.closePath();
  return this;
}

function createButton(x,y,width,height,color,text,radius) {
	// console.log("cb x " + x + " y " + y);

	btn = new Button(x,y,width,height,color,text,radius);
	btn.draw();
	buttons.push(btn);
}

function drawGrid(startX, startY) {
  // draw grid on top
    context.fillStyle = BLACK;
    x = TILE_WIDTH + startX - 2;
    for (var i=0; i<8; i++)
    {
    	if ( (i == 2) || (i == 5) )
    	{
			context.fillRect(x-2,startY,10,9*TILE_WIDTH) ;
    	}
    	else
    	{
			context.fillRect(x,startY,2,9*TILE_WIDTH);
    	}
		x += TILE_WIDTH;	    	
    }

    y = TILE_WIDTH + startY;
    for (var i=0; i<8; i++)
    {
    	if ( (i == 2) || (i == 5) )
    	{
			context.fillRect(startX,y-6,9*TILE_WIDTH,10);
    	}
    	else
    	{
			context.fillRect(startX,y,9*TILE_WIDTH,2);
    	}
		y += TILE_WIDTH;	    	
    }
    
}

 function getMousePos(evt) {
    var rect = canvas.getBoundingClientRect();
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
    };
  }


// touchstart handler
function ProcessTouchStart(e) {
  // Use the event's data to call out to the appropriate gesture handlers
  var mousePos = getMousePos(e);
  //console.log("Touch Start (" + mousePos.x + "," + mousePos.y + ")");
  b = GetButtonHit(mousePos.x, mousePos.y);
  //console.log("b = " + b);
  if (b < 0) {
  	return;
  }
  if (b <= LAST_GRID_BUTTON_TAG) {
  	CellButtonClicked(b);
  } else if (b <= LAST_CELL_VALUE_BUTTON_TAG) {
  	CellValueButtonClicked(b);
  } else if (b == CLEAR_CELL_TAG) {
  	ClearCellButtonClicked();
  } else if (b == CLEAR_ALL_CELLS_TAG) {
  	ClearAllCellsButtonClicked();
  } else if (b == LOAD_GAME_TAG) {
  	LoadGameClicked();
  } else if (b == SOLVE_PUZZLE_TAG) {
  	SolvePuzzleClicked();
  } else if (b == SOLVE_CUSTOM_TAG) {
    SolveCustomClicked();
  } else if (b <= LAST_DIFFICULTY_TAG) {
    SelectDifficulty(b);
  } else {
  	console.log("Unhandled button tag (sender.tag) pressed");
  }
}

function CellButtonClicked(b) {
	// console.log("cell " + b+ " clicked");
	btn = buttons[b];
	btn.color = RED;
	btn.draw();
	if (selectedCell >= 0) {
		btn = buttons[selectedCell];
		btn.color = GREEN;
		btn.draw();
	}
	selectedCell = b;
	drawGrid(STARTX,STARTY);
}

function CellValueButtonClicked(b) {
	// console.log("cell value " + b + " clicked");
	if (selectedCell >= 0) {
		var cellValue = parseInt(b) - LAST_GRID_BUTTON_TAG;
		btn = buttons[selectedCell];
		btn.text = cellValue;
		btn.color = GREEN;
		btn.draw();
		drawGrid(STARTX,STARTY);
		selectedCell = -1; // nothing selected
	}
}

function KeyPressed(k) {
    // key used to quickly enter cell values
    if (selectedCell >= 0) {
        if ((k>=48) && (k<=57)) {
            value = parseInt(k) - 48;
            btn = buttons[selectedCell];
		    btn.text = value;
		    btn.color = GREEN;
		    btn.draw();
		    drawGrid(STARTX,STARTY);
		    selectedCell = -1; // nothing selected
        }
    }
}

function ClearCellButtonClicked() {
	// console.log("clear cell button clicked");
	if (selectedCell >= 0) {
		btn = buttons[selectedCell];
		btn.text = " ";
		btn.color = GREEN;
		btn.draw();
		drawGrid(STARTX,STARTY);
		selectedCell = -1; // nothing selected
	}
}

function ClearAllCellsButtonClicked() {
	// console.log("clear all cells button clicked");
	for (var i=0; i<=LAST_GRID_BUTTON_TAG; i++) {
		btn = buttons[i];
		btn.text = " ";
		btn.color = GREEN;
		btn.draw();
	}
	drawGrid(STARTX,STARTY);
	selectedCell = -1; // nothing selected
}

function LoadRowToGrid(row, rowValue) {
    first = parseInt(row) * 9;
    cPos = 0;
    for (b=first; b<first+9; b++) {
        btn = buttons[b];
        cellValue = rowValue.charAt(cPos++);
        if (cellValue == "-") {
            btn.text = " ";
        } else {
            btn.text = cellValue;
        }
        btn.draw();
    }
    drawGrid(STARTX, STARTY);
}

function LoadGridWithRows(rows) {
    rowValues = rows['ROWS'];
    console.log("we got " + rowValues.length + " rows");
    for (i=0; i<rowValues.length; i++) {
        console.log("row " + i + " is " + rowValues[i]);
        LoadRowToGrid(i,rowValues[i]);
    }
    //foreach(row in rows['ROWS'])
    //    console.log('Load ' + row)
}

function LoadGameClicked() {
	console.log("load game clicked");
	// test with ajax call - load difficulty 1 puzzzle
	var data = {
	    LOAD: selectedDifficulty,
	    OTHER_KEY: "-"
	};
	var dataToSend = JSON.stringify(data);

	$.ajax(
	{
	    url: '/test',
	    type: 'POST',
	    data: dataToSend,

	    success: function(jsonResponse)
	    {
	        var objresponse = JSON.parse(jsonResponse);
	        console.log("ROWS " + objresponse['ROWS']);
	        LoadGridWithRows(objresponse)
	    },
	    error: function()
	    {
	        console.log("ERROR to laod api")
	    }
	});

}

function SelectDifficulty(b) {
    difficulty = b - FIRST_DIFFICULTY_TAG;
    if (selectedDifficulty != difficulty) {
        oldButton =  buttons[selectedDifficulty + FIRST_DIFFICULTY_TAG];
        oldButton.color = YELLOW;
        oldButton.draw();
        selectedDifficulty = difficulty;
        newButton = buttons[selectedDifficulty + FIRST_DIFFICULTY_TAG];
        newButton.color = RED;
        newButton.draw();
        drawGrid(STARTX, STARTY);
    }
}

function SolvePuzzleClicked() {
	console.log("solve puzzle clicked");

	// test with ajax call - load difficulty 1 puzzzle
	var data = {
	    SOLVE: "0",
	    OTHER_KEY: "-"
	};
	var dataToSend = JSON.stringify(data);

	$.ajax(
	{
	    url: '/test',
	    type: 'POST',
	    data: dataToSend,

	    success: function(jsonResponse)
	    {
	        var objresponse = JSON.parse(jsonResponse);
	        console.log("ROWS " + objresponse['ROWS']);
	        LoadGridWithRows(objresponse)
	    },
	    error: function()
	    {
	        console.log("ERROR to laod api")
	    }
	});
}

function SolveCustomClicked() {
    var lines = new Array();
    // load cell values to array
    for (i=0; i<9; i++) {
        line = "";
        for (j=0; j<9; j++) {
            b = buttons[i*9 + j];
            if ((b.text == " ") || (b.text == "")) {
                line += "-";
            } else {
                line += b.text;
            }
        }
        lines.push(line);
    }
    // send array to server
    var data = {
	    CUSTOM: lines,
	    OTHER_KEY: "-"
	};
	var dataToSend = JSON.stringify(data);
    $.ajax(
	{
	    url: '/test',
	    type: 'POST',
	    data: dataToSend,

	    success: function(jsonResponse)
	    {
	        var objresponse = JSON.parse(jsonResponse);
	        console.log("ROWS " + objresponse['ROWS']);
	        LoadGridWithRows(objresponse)
	    },
	    error: function()
	    {
	        console.log("ERROR to laod api")
	    }
	});

}

// Utilities
function nbrToString(nbr) {
	var t = "";
	return t + (nbr).toString();
}
