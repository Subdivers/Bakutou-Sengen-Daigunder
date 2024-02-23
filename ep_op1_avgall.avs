a01 = LWLibavVideoSource("Z:\dconv2\src\01.avi").Trim(150, 0)
a02 = LWLibavVideoSource("Z:\dconv2\src\02.avi").Trim(142, 0)
a03 = LWLibavVideoSource("Z:\dconv2\src\03.avi").Trim(143, 0)
a04 = LWLibavVideoSource("Z:\dconv2\src\04.avi").Trim(145, 0)

a05 = LWLibavVideoSource("Z:\dconv2\src\05.avi").Trim(150, 0)
a06 = LWLibavVideoSource("Z:\dconv2\src\06.avi").Trim(150, 0)
a07 = LWLibavVideoSource("Z:\dconv2\src\07.avi").Trim(150, 0)
a08 = LWLibavVideoSource("Z:\dconv2\src\08.avi").Trim(150, 0)

a09 = LWLibavVideoSource("Z:\dconv2\src\09.avi").Trim(150, 0)
a10 = LWLibavVideoSource("Z:\dconv2\src\10.avi").Trim(150, 0)
a11 = LWLibavVideoSource("Z:\dconv2\src\11.avi").Trim(150, 0)
a12 = LWLibavVideoSource("Z:\dconv2\src\12.avi").Trim(150, 0)

a13 = LWLibavVideoSource("Z:\dconv2\src\13.avi").Trim(150, 0)
a14 = LWLibavVideoSource("Z:\dconv2\src\14.avi").Trim(145, 0)
a15 = LWLibavVideoSource("Z:\dconv2\src\15.avi").Trim(146, 0)
a16 = LWLibavVideoSource("Z:\dconv2\src\16.avi").Trim(1146, 0)

a17 = LWLibavVideoSource("Z:\dconv2\src\17.avi").Trim(150, 0)
a18 = LWLibavVideoSource("Z:\dconv2\src\18.avi").Trim(143, 0)
a19 = LWLibavVideoSource("Z:\dconv2\src\19.avi").Trim(146, 0)
a20 = LWLibavVideoSource("Z:\dconv2\src\20.avi").Trim(149, 0)

a21 = LWLibavVideoSource("Z:\dconv2\src\21.avi").Trim(150, 0)
a22 = LWLibavVideoSource("Z:\dconv2\src\22.avi").Trim(150, 0)
a23 = LWLibavVideoSource("Z:\dconv2\src\23.avi").Trim(150, 0)
a24 = LWLibavVideoSource("Z:\dconv2\src\24.avi").Trim(150, 0)

a25 = LWLibavVideoSource("Z:\dconv2\src\25.avi").Trim(149, 0)
a26 = LWLibavVideoSource("Z:\dconv2\src\26.avi").Trim(145, 0)
a27 = LWLibavVideoSource("Z:\dconv2\src\27.avi").Trim(149, 0)
a28 = LWLibavVideoSource("Z:\dconv2\src\28.avi").Trim(149, 0)

a29 = LWLibavVideoSource("Z:\dconv2\src\29.avi").Trim(150, 0)
a30 = LWLibavVideoSource("Z:\dconv2\src\30.avi").Trim(144, 0)
a31 = LWLibavVideoSource("Z:\dconv2\src\31.avi").Trim(146, 0)
a32 = LWLibavVideoSource("Z:\dconv2\src\32.avi").Trim(146, 0)

a33 = LWLibavVideoSource("Z:\dconv2\src\33.avi").Trim(149, 0)

med1 = Median(a01, a02, a03, a04, a05, a06, a07, a08, a09, a10, a11)
med2 = Median(a12, a13, a14, a15, a16, a17, a18, a19, a20, a21, a22)
med3 = Median(a23, a24, a25, a26, a27, a28, a29, a30, a31, a32, a33)
avg = Average(med1, 1.0/3, med2, 1.0/3, med3, 1.0/3)

a = avg.TFM(mode=1, PP=7, ovr="Z:\dconv2\src\OP1_Average_ovr.txt")
p1 = a.Trim(0, 250).TDecimate(mode=1)
p2 = a.Trim(251, 1145).TDecimate(mode=1)
p3 = a.Trim(1146, 1223).TDecimate(mode=1, cycleR=2, cycle=5).AssumeFPS(24000, 1001)
p4 = a.Trim(1224, 2757).TDecimate(mode=1)
p = p1 + p2 + p3 + p4
p
BilinearResize(640, 480, 10, 0, -4, -0)