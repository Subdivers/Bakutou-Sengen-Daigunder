LWLibavVideoSource("Z:\dconv2\src\OP2.avi")
t = TFM(mode=1, PP=7, ovr="Z:\dconv2\src\OP2_Clean_ovr.txt", display=true)
t

p00 = Trim(0, 250).TDecimate(mode=1, cycleR=1, cycle=5)
p01 = Trim(251, 400)
p02 = Trim(401, 1145).TDecimate(mode=1, cycleR=1, cycle=5)
p03 = Trim(1146, 1223).TDecimate(mode=1, cycleR=4, cycle=10)
p04 = Trim(1224, 1365).TDecimate(mode=1, cycleR=1, cycle=5)
p05 = Trim(1366, 1458)
p06 = Trim(1459, 1485).yadifmod2(mode=1).TDecimate(mode=1, cycleR=1, cycle=3)
p07 = Trim(1486, 1501)
p08 = Trim(1502, 1578).TDecimate(mode=1, cycleR=1, cycle=5)
p09 = Trim(1579, 1673).yadifmod2(mode=1).TDecimate(mode=1, cycleR=1, cycle=5)
p10 = Trim(1674, 2251).TDecimate(mode=1, cycleR=1, cycle=5)
p11 = Trim(2252, 2308)
p12 = Trim(2309, 2397).TDecimate(mode=1, cycleR=1, cycle=15)
p13 = Trim(2399, 0).TDecimate(mode=1, cycleR=1, cycle=5)
p = p00.AssumeFPS(30) + p01.AssumeFPS(30) + p02.AssumeFPS(30) + p03.AssumeFPS(30) + p04.AssumeFPS(30) + p05.AssumeFPS(30) + p06.AssumeFPS(30) + p07.AssumeFPS(30) + p08.AssumeFPS(30) + p09.AssumeFPS(30) + p10.AssumeFPS(30) + p11.AssumeFPS(30) + p12.AssumeFPS(30) + p13.AssumeFPS(30)
p
t
