# Polyphonic Sample Grains from a Single Audio File: LineGroove

from athenaCL.libATH import athenaObj
 
cmd = [

'emo cn',
'tmo LineGroove',
# instrument 32 is a fixed playback rate sample player
'tin a 32',
#set a file path to an audio file
'tie x6 cf,/Volumes/xdisc/_sync/_x/src/martingale/martingale/audio/32673.aif',
# set a event time between 60 and 120 ms
'tie r cs,(ru,.060,.120)',
#smooth envelope shapes
'tie x0 c,.01',
'tie x1 c,.5',
# start position within audio file in seconds
'tie x5 ru,0,10',
# set random panning
'tie n ru,0,1',
# create a few more instances
'ticp a b c d e f',       
]


def main(cmdList=[], fp=None, hear=True, render=True):
    ath = athenaObj.Interpreter()

    for line in cmdList:
        ath.cmd(line)

    if fp == None:
        ath.cmd('eln') 
    else:
        ath.cmd('eln %s' % fp)

    if render:
        ath.cmd('elr') 

    if hear:
        ath.cmd('elh') 


if __name__ == '__main__':
    main(cmd)






