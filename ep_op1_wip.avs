a01 = LWLibavVideoSource("Z:\dconv2\src\01.avi").Trim(150, 0)
a02 = LWLibavVideoSource("Z:\dconv2\src\02.avi").Trim(142, 0)
a03 = LWLibavVideoSource("Z:\dconv2\src\03.avi").Trim(143, 0)
a04 = LWLibavVideoSource("Z:\dconv2\src\04.avi").Trim(145, 0)
a05 = LWLibavVideoSource("Z:\dconv2\src\05.avi").Trim(150, 0)

avg = Median(a01, a02, a03, a04, a05)

avg
Trim(0, 2757)


# tfmd = avg.TFM(mode=1, PP=0, display=True, ovr="Z:\dconv2\src\OP1_Average_ovr.txt")
# tfmd2 = avg.TFM(mode=1, PP=7, display=True, ovr="Z:\dconv2\src\OP1_Average_ovr.txt")
# StackVertical(StackHorizontal(tfmd, tfmd2), StackHorizontal(avg, avg.DoubleWeave().SelectOdd()))

a = avg.TFM(mode=1, PP=7, ovr="Z:\dconv2\src\OP1_Average_ovr.txt", display=True)
p1 = a.Trim(0, 250).TDecimate(mode=1)
p2 = a.Trim(251, 1145).TDecimate(mode=1)
p3 = a.Trim(1146, 1223).TDecimate(mode=1, cycleR=2, cycle=5).AssumeFPS(24000, 1001)
p4 = a.Trim(1224, 2757).TDecimate(mode=1)
p = p1 + p2 + p3 + p4

p
BilinearResize(640, 480, 10, 0, -4, -0)