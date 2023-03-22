import random 
import pyglet
from pyglet.window import key 
from enum import Enum , auto
from dataclasses import dataclass

@dataclass
class Vec:
	x : int
	y : int
#	def __init__(self, x, y) :
#		self.x = x
#		self.y = y
		
	def __add__(self, v) :
		return Vec(self.x + v.x , self.y + v.y)

	def __sub__(self, v) :
		return Vec(self.x -v.x , self.y - v.y)
	
	def __eq__(self, v) :
		return self.x == v.x and self.y == v.y
	
	def distance(self, v, d) :
		if d == Dir.U :
			return (v - self).y 
		elif d == Dir.D :
			return self.y +1
		elif d == Dir.R :
			return (v - self).x 
		elif d == Dir.L :
			return self.x +1
		
	def move1(self,d) :
		return self + d.to_Vec()

class Dir(Enum) :
	U = auto()
	D = auto()
	L = auto()
	R = auto()
	
	def left(self) :
		if self == Dir.U :
			return Dir.L
		elif self == Dir.D :
			return Dir.R
		elif self == Dir.L :
			return Dir.D
		elif self == Dir.R :
			return Dir.U
		
	def right(self) :
		if self == Dir.U :
			return Dir.R
		elif self == Dir.D :
			return Dir.L
		elif self == Dir.L :
			return Dir.U
		elif self == Dir.R :
			return Dir.D
		

		
	def to_Vec(self) :
		if self == Dir.U :
			return Vec(0, 1)
		elif self == Dir.D :
			return Vec(0,-1)
		elif self == Dir.L :
			return Vec(-1, 0)
		elif self == Dir.R :
			return Vec(1, 0)

	
def make_pills(n, max) :
	return [Vec(random.randint(0,max.x-1), random.randint(0,max.y-1)) for n in range(n)]

def intersects(pos,positions) :
	for p in positions :
		if pos == p :
			return True
	return False

def is_on_tail(s) :
	head = s[0]
	tail = s[1:]
	return intersects(head, tail)

def is_at_edge(h,d,g) :
	dist = h.distance(g, d)
	return dist == 1

#=====================


GRID_STEP = 10
GRID = Vec(80,50)

snake = [Vec(5,0)]
dir = Dir.U
pills = make_pills(1, GRID)
slen = 5
#possible modes : Autoplay, Manual, Play, title screen, startgame and endgame
playmode = "manual"
level = 1
show_debug_info = False
update_interval = 1/20


	
def advance() :
	global snake, pills, slen
	snake.insert(0,snake[0].move1(dir))
	
	#snake.insert(0,snake[0] + dir.to_Vec())
	snake = snake[:slen]
	if intersects(snake[0], pills) :
		pills.remove(snake[0])
		slen = slen + 1

def restart_game():
	global snake,dir,pills,slen,playmode,level,update_interval
	snake = [Vec(5,0)]
	dir = Dir.U
	pills = make_pills(1, GRID)
	slen = 5
	playmode = "manual"
	level = 1
	update_interval = 1/20
	for _ in range(1, slen) :
		advance()
	print(pills)
	

def game_over() :
	global game, playmode
	playmode = "manual"
	game = False

def pills_eaten() :
	return len(pills) == 0
	

def advance_level() :
	global level, pills
	level = level + 1
	pills = make_pills(level, GRID)
	
restart_game()	
#=====================
def auto_play(dt) :
	global dir, slen
	dir = random.choices([dir, dir.left(), dir.right()], weights=[20,1,1])[0]
	while is_at_edge(snake[0],dir, GRID) :
		dir = dir.right()
	if random.randint(0,100) > 80 :
		slen = slen + 1
	advance() 

def manual_play() :
	if is_at_edge(snake[0],dir, GRID) :	
		return
	elif pills_eaten() :
		advance_level()
	else :
		advance()

def play(dt) :
	if is_at_edge(snake[0],dir, GRID) :
		game_over() 
	elif is_on_tail(snake) :
		game_over()
	elif pills_eaten() :
		advance_level()
	else :
		advance()


def make_startscreen(b) :
	bg = pyglet.graphics.Group(order = 0)
	fg = pyglet.graphics.Group(order = 1)
	buttons = pyglet.graphics.Group(order = 2)
	letters = pyglet.graphics.Group(order = 3)
	return	[ pyglet.text.Label(text= "P",x = wn.width/2.46 ,y =  wn.height/2.55, width=20, height=20, color=(255,255,255,255),batch = b, group = letters)
			, pyglet.shapes.Rectangle(0,0, wn.width, wn.height, color = (255,255,255), batch = b, group = bg )
			, pyglet.text.Label(text = "S N A K E",font_size = 36,x = wn.width/2, y = wn.height/2, anchor_x = 'center',anchor_y = 'bottom',color = (0,0,0,255), batch = b, group = fg)
			, pyglet.text.Label(text = "P L A Y",x = wn.width/2, y = wn.height/2.55, anchor_x = 'center',color = (0,0,0,255), batch = b, group = fg)
			, pyglet.text.Label(text = "O P T I O N S",x = wn.width/2, y = wn.height/2.95, anchor_x = 'center',color = (0,0,0,255), batch = b, group = fg)
			, pyglet.shapes.Rectangle(x = wn.width/2.5 ,y =  wn.height/2.6, width=20, height=20, color=(0,0,0),batch = b, group = buttons)
			, pyglet.shapes.Rectangle(x = wn.width/2.5 ,y =  wn.height/3, width=20, height=20, color=(0,0,0),batch = b, group = buttons)
			, pyglet.text.Label(text= "O",x = wn.width/2.47 ,y =  wn.height/2.94, width=20, height=20, color=(255,255,255,255),batch = b, group = letters)
			]

	
#	square3 = pyglet.shapes.Rectangle(x = wn.width/2.5 ,y =  wn.height/3.6, width=20, height=20, color=(0,0,0),batch = batch, group = buttons)
#	pyglet.text.Label(text = "Q U I T",x = wn.width/2, y = wn.height/3.5, anchor_x = 'center',color = (0,0,0,255), batch = b, group = fg)
#	letter3 = pyglet.text.Label(text= "Q",x = wn.width/2.47 ,y =  wn.height/3.5, width=20, height=20, color=(255,255,255,255),batch = batch, group = letters)


wn = pyglet.window.Window(width = GRID.x * GRID_STEP + 1, height = GRID.y * GRID_STEP, resizable = True)


batch = pyglet.graphics.Batch()

playmode = "titlescreen"
startscreen = None
label = pyglet.text.Label()
if playmode == "titlescreen" :
	startscreen = make_startscreen(batch) 

elif playmode == "startgame" :
	batch = pyglet.graphics.Batch()

else :

	label = pyglet.text.Label(text = "",x = GRID.x * GRID_STEP - 10, y = GRID_STEP, anchor_x = 'right', batch = batch)

fps = pyglet.window.FPSDisplay(wn)

time_passed_since_last_step = 0


def update(dt) :
	global time_passed_since_last_step
	if playmode == "titlescreen" :
		pass
	else :
		if playmode == "autoplay" :
			auto_play(dt)
		elif playmode == "play" :
			time_passed_since_last_step = dt + time_passed_since_last_step
			if time_passed_since_last_step > update_interval :
				time_passed_since_last_step = 0
				play(dt)
				
		label.text = "{speed} {x}, {y} : {d}, {l} : lvl {lvl} | {mode}".format(speed = update_interval, x = snake[0].x, y = snake[0].y, d = snake[0].distance(GRID, dir), l = slen,lvl = level, mode = playmode)
	
@wn.event
def on_draw() :
	wn.clear()
	if playmode == "titlescreen" :
		pass
	else :
		pill = [pyglet.shapes.Rectangle(g.x * GRID_STEP, g.y * GRID_STEP, GRID_STEP, GRID_STEP, color = (55,255,255), batch = batch) for g in pills]
		l = [pyglet.shapes.Rectangle(g.x * GRID_STEP, g.y * GRID_STEP, GRID_STEP, GRID_STEP, color = (55,55,255), batch = batch) for g in reversed(snake)]
		l[-1].color = (125,44,227)
		fps.draw()
	
	batch.draw()
	
@wn.event
def on_key_press(symbol, modifiers):
	global dir , playmode, update_interval, startscreen, batch
	
	match symbol : 
		case key.A :
			dir = Dir.L 
		case key.S :
			dir = Dir.D
		case key.W :
			dir = Dir.U
		case key.D :
			dir = Dir.R
		case key.B :
			playmode = "autoplay"
		
		case key.R :
			restart_game()
			return
		
		case key.N :
			playmode = "play"
		case key.M :
			playmode = "manual"
		
		case key.U :
			update_interval = update_interval + 0.01
		case key.Z :
			update_interval = update_interval - 0.01
			
		case key.I :
			show_debug_info = True
			
		case key.Q :
			playmode = "titlescreen"
			startscreen = make_startscreen(batch)
			
	if playmode == "titlescreen" :
		match symbol :
			case key.P :

		 
				playmode = "play"
				del startscreen
		 
		
				batch = pyglet.graphics.Batch()
				print("switching to play mode")
			
			case key.O :
				playmode = "options"
				

			
	if playmode == "manual" :
		manual_play()

pyglet.clock.schedule_interval(update, 1/120)

pyglet.app.run()