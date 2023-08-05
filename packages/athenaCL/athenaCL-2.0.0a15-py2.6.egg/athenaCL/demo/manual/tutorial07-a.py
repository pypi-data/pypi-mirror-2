from athenaCL.libATH import athenaObj
ath = athenaObj.Interpreter()
ath.cmd('emo mp')
ath.cmd('tmo lg')

ath.cmd('tin a1 36')
ath.cmd('tie r l,((4,3,1),(4,3,0),(4,2,1)),rc')

ath.cmd('tin b1 37')
ath.cmd('tie r l,((4,6,1),(4,1,1),(4,3,1)),rc')

ath.cmd('tin c1 53')
ath.cmd('tie r l,((4,1,1),(4,1,1),(4,6,0)),rw')

ath.cmd('tee a bg,rc,(.5,.7,.75,.8,1)')
ath.cmd('tee b ws,t,4,0,122,118')

ath.cmd('eln')
ath.cmd('elh')