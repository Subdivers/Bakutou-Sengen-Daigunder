src = LWLibavVideoSource("Z:\dconv2\src\OP1.avi")
# tfmd = avg.TFM(mode=1, PP=0, display=True, ovr="Z:\dconv2\src\OP1_Average_ovr.txt")
# tfmd2 = avg.TFM(mode=1, PP=7, display=True, ovr="Z:\dconv2\src\OP1_Average_ovr.txt")
# StackVertical(StackHorizontal(tfmd, tfmd2), StackHorizontal(avg, avg.DoubleWeave().SelectOdd()))

a = src.TFM(mode=1, PP=1, ovr="Z:\dconv2\src\OP1_Clean_ovr.txt")#, display=True)
p1 = a.Trim(0, 250).TDecimate(mode=1)
p2 = a.Trim(251, 1145).TDecimate(mode=1)
p3 = a.Trim(1146, 1223).TDecimate(mode=1, cycleR=2, cycle=5).AssumeFPS(24000, 1001)
p4 = a.Trim(1224, 2757).TDecimate(mode=1)
p = p1 + p2 + p3 + p4 
p
BilinearResize(640, 480, 10, 0, -4, -0)

a