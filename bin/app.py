import random
from random import randint
import web
from content import *

# creates a urls variable which has a list of urls in it
urls = (
	'/game', 'GameEngine',
	)


app = web.application(urls, globals())

# sets up the sessions so that the game can keep the state
if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store, initializer={'scene': 'greeting', 'name': 'Buddy', 'error': None})

	web.config._session = session
else:
	session = web.config._session


# creates a render variable which runs the render method from web.template with templates/ and a base layout
render = web.template.render('templates/', base="text")

render_quiz = web.template.render('templates/')

render_error = web.template.render('templates/', base="error")


# creates an Index class with a GET function that...
class GameEngine(object):

	def GET(request):
		session.kill()
		session.scene = 'greeting'

		current_scene = scene_map[session.scene]()
		return current_scene.present(session)


	def POST(self):
		current_scene = scene_map[session.scene]()

		next_scene = current_scene.process(session)
		current_scene = scene_map[session.scene]()

		return current_scene.present(session.scene)


class Scene(object):

	def __init__(self):
		pass

	def userInput(self):
		form = web.input(action=None)
		words = form.action
		lowercase = words.lower()
		keywords = lowercase.split(' ')
		return keywords


	def present(self, session):
		pass

	def process(self, session):
		pass


class Greeting(Scene):
	def present(self, session):
		return render.greeting()

	def process(self, session):
		global name

		form = web.input(action=None)
		name = "%s" % form.action

		session.name = name
		session.scene = 'wakeroom'

		return session


class WakeRoom(Scene):

	def present(self, session):
		return render.wake_room(name = name)

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in theWheelRoom:
				session.scene = 'wheelroom'
				break
			elif i in pixieRoom:	
				session.scene = 'pixie'
				break
			else:
				session.scene = 'wakeroomerror'	
					
		return session


class WakeRoomError(Scene):

	def present(self, sesssion):
		return render.wake_room_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in theWheelRoom:
				session.scene = 'wheelroom'
				break
			elif i in pixieRoom:	
				session.scene = 'pixie'
				break
			else:
				session.scene = 'wakeroomerror'
					
		return session


class WheelRoom(Scene):
	def present(self, session):
		return render.wheel_room()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm or i in spin:
				session.scene = 'postspin'
				break
			elif i in negate:
				session.scene = 'death'
				break
			else:
				session.scene = 'wheelroomerror'
		return session


class WheelRoomError(Scene):
	def present(self, session):
		return render.wheel_room_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm or i in spin:
				session.scene = 'postspin'
				break
			elif i in negate:
				session.scene = 'death'
				break
			else:
				session.scene = 'wheelroomerror'
		return session


class PostSpin(Scene):
	def present(self, session):
		return render.spin_text()
			
	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm or i in ahead:	
				number = random.randint(0, 7)
				if int(number) in range(0, 3):
					session.scene = 'child'
				elif int(number) in range(3, 6):
					session.scene = 'spacetime'
				else:
					session.scene = 'wakeagain'
				break

			elif i in negate or i in stay_here:
				session.scene = 'death'
				break
			else:
				session.scene = 'postspinerror'
		return session

class PostSpinError(Scene):
	def present(self, session):
		return render.spin_text_error()
			
	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm or i in ahead:	
				number = random.randint(0, 7)
				if int(number) in range(0, 3):
					session.scene = 'child'
				elif int(number) in range(3, 6):
					session.scene = 'spacetime'
				else:
					session.scene = 'wakeagain'
				break
			elif i in negate or i in stay_here:
				session.scene = 'death'
				break
			else:
				session.scene = 'postspinerror'
		return session



class Pixie(Scene):
	def present(self, session):
		return render.pixie()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:

			if i in pixieHappy1:
				session.scene = 'pixieawake'
				break
			elif i in pixieCross1:
				session.scene = 'death'
				break
			else:
				session.scene = 'pixieerror'
		return session

class PixieError(Scene):
	def present(self, session):
		return render.pixie_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:

			if i in pixieHappy1:
				session.scene = 'pixieawake'
				break
			elif i in pixieCross1:
				session.scene = 'death'
				break
			else:
				session.scene = 'pixieerror'
		return session



class PixieAwake(Scene):
	def present(self, session):
		return render.pixie_awake()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in pixieHappy2:
				session.scene = 'emptyroom'
				break
			elif i in pixieCross2:
				session.scene = 'pixiebored'
				break
			else:
				session.scene = 'pixieawakeerror'
		return session

class PixieAwakeError(Scene):
	def present(self, session):
		return render.pixie_awake_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in pixieHappy2:
				session.scene = 'emptyroom'
				break
			elif i in pixieCross2:
				session.scene = 'pixiebored'
				break
			else:
				session.scene = 'pixieawakeerror'
		return session

class PixieBored(Scene):
	def present(self, session):
		return render.pixie_bored()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in pixieHappy1:
				session.scene = 'pixieawake'
				break
			elif i in pixieCross1:
				session.scene = 'death'
				break
			else:
				session.scene = 'pixieerror'

		return session


class EmptyRoom(Scene):
	def present(self, session):
		return render.empty_room()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if "1" in key_words:
				session.scene = 'wakeagain'
				break
			elif "2" in key_words:
			 	session.scene = 'ocean'
			 	break
			elif "3" in key_words:
			 	session.scene = 'godot'
			 	break
			else:
			 	session.scene = 'emptyroomerror'
		return session

class EmptyRoomError(Scene):
	def present(self, session):
		return render.empty_room_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if "1" in key_words:
				session.scene = 'wakeagain'
				break
			elif "2" in key_words:
			 	session.scene = 'ocean'
			 	break
			elif "3" in key_words:
			 	session.scene = 'godot'
			 	break
			else:
			 	session.scene = 'emptyroomerror'
		return session

class WakeAgain(Scene):

	def present(self, session):
		return render.wake_again()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:

			if i in theWheelRoom:
				session.scene = 'wheelroom'
				break
			elif i in pixieRoom:	
				session.scene = 'pixie'
				break
			else:
				session.scene = 'wakeroomerror'
	
		return session

class Ocean(Scene):
	def present(self, session):
		return render.ocean()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					session.scene = 'tortoise'
				elif which_q == 1:
					session.scene = 'overshoot'
				else:
					session.scene = 'greenpeace'
				break
			elif i in negate:
				session.scene = 'decline'
				break
			else:
				session.scene = 'oceanerror'
		return session

class OceanError(Scene):
	def present(self, session):
		return render.ocean_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					session.scene = 'tortoise'
				elif which_q == 1:
					session.scene = 'overshoot'
				else:
					session.scene = 'greenpeace'
				break
			elif i in negate:
				session.scene = 'decline'
				break
			else:
				session.scene = 'oceanerror'
		return session


class Tortoise(Scene):
	def present(self, session):
		return render_quiz.tortoise()

	def process(self, session):
		pass

class Overshoot(Scene):
	def present(self, session):
		return render_quiz.overshoot()

	def process(self, session):
		pass

class Greenpeace(Scene):
	def present(self, session):
		return render_quiz.greenpeace()

	def process(self, session):
		pass


class Godot(Scene):
	def present(self, session):
		return render.godot()

	def process(self, session):
		pass

class GodotError(Scene):
	def present(self, session):
		return render.godot_error()

	def process(self, session):
		pass

class Child(Scene):
	def present(self, session):
		return render.child(name = name)

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in child_bottle:
				session.scene = 'bottle'
				break
			elif i in child_key:
				session.scene = 'key'
				break
			else:
				session.scene = 'childerror'

		return session

class ChildError(Scene):
	def present(self, session):
		return render.child_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in child_bottle:
				session.scene = 'bottle'
				break
			elif i in child_key:
				session.scene = 'key'
				break
			else:
				session.scene = 'childerror'

		return session

class Bottle(Scene):
	def present(self, session):
		return render.bottle()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i == 'east':
				session.scene = 'wizard'
				break
			elif i == 'west':
				session.scene = 'ninja'
				break
			else:
				session.scene = 'bottleerror'
		return session

class BottleError(Scene):
	def present(self, session):
		return render.bottle_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if 'east' in i:
				session.scene = 'wizard'
				break
			elif 'west' in i:
				session.scene = 'ninja'
				break
			else:
				session.scene = 'bottleerror'
		return session


class Key(Scene):
	def present(self, session):
		return render.key()

	def process(self, session):
		pass

class Wizard(Scene):
	def present(self, session):
		return render.wizard()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm:
				session.scene = 'riddle'
				break
			elif i in negate:
				session.scene = 'death'
				break
			else:
				session.scene = 'wizarderror'
		return session


class WizardError(Scene):
	def present(self, session):
		return render.wizard_errror()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in affirm:
				session.scene = 'riddle'
				break
			elif i in negate:
				session.scene = 'death'
				break
			else:
				session.scene = 'wizarderror'
		return session

class Riddle(Scene):

	def present(self, session):
		return render.riddle()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i == 'purple':
				session.scene = 'win'
				break
			elif i == 'red':
				session.scene = 'death'
				break
			else:
				session.scene = 'riddleerror'
		return session

class RiddleError(Scene):

	def present(self, session):
		return render.riddle_error(name = name)

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i == 'purple':
				session.scene = 'win'
				break
			elif i == 'red':
				session.scene = 'death'
				break
			else:
				session.scene = 'riddleerror'
		return session


class Ninja(Scene):
	def present(self, session):
		return render.ninja()

	def process(self, session):
		pass

class NinjaError(Scene):
	def present(self, session):
		return render.ninja_error()

	def process(self, session):
		pass


class SpaceTime(Scene):
	def present(self, session):
		return render.space_time()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in time_machine:
				session.scene = 'historian'
			elif i in teleportation:
				session.scene = 'wakeagain'
			else:
				session.scene = 'spacetimeerror'
			return session

class SpaceTimeError(Scene):
	def present(self, session):
		return render.space_time_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:
			if i in time_machine:
				session.scene = 'historian'
			elif i in teleportation:
				session.scene = 'wakeagain'
			else:
				session.scene = 'spacetimeerror'
			return session



class Historian(Scene):
	def present(self, session):
		return render.historian()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:

			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					session.scene = 'war'
				elif which_q == 1:
					session.scene = 'acidification'
				else:
					session.scene = 'poverty'

			elif i in negate:
				session.scene = 'decline'
			else:
				session.scene = 'historianerror'
			return session

class HistorianError(Scene):
	def present(self, session):
		return render.historian_error()

	def process(self, session):
		key_words = Scene.userInput(self)
		for i in key_words:

			if i in affirm:
				which_q = random.randint(0,3)

				if which_q == 0:
					session.scene = 'war'
				elif which_q == 1:
					session.scene = 'acidification'
				else:
					session.scene = 'poverty'

			elif i in negate:
				session.scene = 'decline'
			
			else:
				session.scene = 'historianerror'
			return session



class War(Scene):
	def present(self, session):
		return render_quiz.war()

	def process(sels, session):
		pass

class Acidification(Scene):
	def present(self, session):
		return render_quiz.acidification()

	def process(self, session):
		pass

class Poverty(Scene):
	def present(self, session):
		return render_quiz.poverty()

	def process(self, session):
		pass


class Decline(Scene):
	def present(self, session):
		pass

	def process(self, session):
		pass

class Death(Scene):
	def present(self, session):
		return render.death(name = name)
		
	def process(self, session):
		pass

scene_map = {
	'greeting': Greeting,
	'wakeroom': WakeRoom,
	'wakeroomerror': WakeRoomError,
	'wheelroom': WheelRoom,
	'wheelroomerror': WheelRoomError,
	'postspin': PostSpin,
	'postspinerror': PostSpinError,
	'pixie': Pixie,
	'pixieerror': PixieError,
	'pixieawake': PixieAwake,
	'pixieawakeerror': PixieAwakeError,
	'pixiebored': PixieBored,
	'emptyroom': EmptyRoom,
	'emptyroomerror': EmptyRoomError,
	'wakeagain': WakeAgain,
	'ocean': Ocean,
	'oceanerror': OceanError,
	'tortoise':Tortoise,
	'overshoot': Overshoot,
	'greenpeace': Greenpeace,
	'godot': Godot,
	'godoterror': GodotError,
	'child': Child,
	'childerror': ChildError,
	'bottle': Bottle,
	'bottleerror': BottleError,
	'key': Key,
	'wizard': Wizard,
	'wizarderror': WizardError,
	'riddle': Riddle,
	'riddleerror': RiddleError,
	'ninja': Ninja,
	'ninjaerror': NinjaError,
	'spacetime': SpaceTime,
	'spacetimeerror': SpaceTimeError,
	'historian': Historian,
	'historianerror': HistorianError,
	'war': War,
	'acidification': Acidification,
	'poverty': Poverty,
	'decline': Decline,
	'death': Death,
	'win': Win

}


if __name__ == "__main__":
	app.run()






