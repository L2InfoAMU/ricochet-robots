# test des classes


from robot import *



fd = open('test2.txt','r')
A = Board.load_from_file(fd)
group = Robot_group()
r1 = Robot (group, RColors.RED, (0,0) )
r2 = Robot (group, RColors.GREEN, (4,0) )
r3 = Robot (group, RColors.BLUE, (3,4) )
r4 = Robot (group, RColors.YELLOW, (2,4) )
goal = Goal(RColors.GREEN, (4,2))
game = Game(A,group,goal)
print (game.actions_list() )

state = game.do_action("RS")
state = game.do_actions("RE","GN","RN","BW","BN","YS" )

