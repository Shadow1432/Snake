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
#possible modes : Autoplay, Manual and Play
playmode = "manual"
level = 1
show_debug_info = False
update_interval = 1/20


	
def advance() :
	global snake, pills, slen
	snake.insert(0,snake[0] + dir.to_Vec())
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


	
	


wn = pyglet.window.Window(width = GRID.x * GRID_STEP + 1, height = GRID.y * GRID_STEP, resizable = True)
batch = pyglet.graphics.Batch()
fps = pyglet.window.FPSDisplay(wn)
label = pyglet.text.Label(text = "",x = GRID.x * GRID_STEP - 10, y = GRID_STEP, anchor_x = 'right', batch = batch)

time_passed_since_last_step = 0


def update(dt) :
	global time_passed_since_last_step
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
	pill = [pyglet.shapes.Rectangle(g.x * GRID_STEP, g.y * GRID_STEP, GRID_STEP, GRID_STEP, color = (55,255,255), batch = batch) for g in pills]
	l = [pyglet.shapes.Rectangle(g.x * GRID_STEP, g.y * GRID_STEP, GRID_STEP, GRID_STEP, color = (55,55,255), batch = batch) for g in reversed(snake)]
	l[-1].color = (125,44,227)
	fps.draw()
	batch.draw()
	
@wn.event
def on_key_press(symbol, modifiers):
	global dir , playmode, update_interval
	
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
		
		case key.O :
			update_interval = update_interval + 0.01
		case key.P :
			update_interval = update_interval - 0.01
			
		case key.I :
			show_debug_info = True
			
	if playmode == "manual" :
		manual_play()

pyglet.clock.schedule_interval(update, 1/120)

pyglet.app.run()