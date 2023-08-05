# Polyphonic Sample Grains from a Multiple Audio Files: LineGroove

from athenaCL.libATH import athenaObj
ath = athenaObj.Interpreter()
 
cmd = [
'emo cn',
'apr off',
'tmo TimeFill',
# instrument 32 is a fixed playback rate sample player
'tin a 32',

# set a file path to an directory, a file extension, and a selection method
'tie x6 ds,/Volumes/xdisc/_sync/_x/src/martingale/martingale/audio,.aif,rp',

# set a event time between 60 and 120 ms
'tie r cs,(ru,.030,.090)',

# smooth envelope shapes
'tie x0 c,.01',
'tie x1 c,.5',

# start position within audio file in seconds
'tie x5 ru,0,10',

# set random panning
'tie n ru,0,1',

# control a variety of amplitudes
'tie a ru,.1,.2',

# set number of events
'tie s3 1000',

# start position within texture normalized within unit interval
'tie d0 rb,.3,.3,0,1',
        
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





