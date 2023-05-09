#!/bin/bash

gmt begin istasyonlar

	gmt set FONT_ANNOT 7p
	gmt set GMT_LANGUAGE TR
	gmt set PROJ_ELLIPSOID TOPEX

	gmt coast -R25/45/35/44 -Jm0.8 -Dh -Ggray -Slightblue -Wthinnest -B2.5g2.5 -N1 -Ia/79/148/205
	gmt text gmt_icin_yazilar.txt -R25/45/35/44 -Jm0.8 -F+f6p,Helvetica,0/0/0
	gmt plot gmt_icin_sekiller.txt -R25/45/35/44 -Jm0.8 -St0.15c -Gred 

	echo 25.40 38.55 EGE DENIZI | gmt text -R25/45/35/44 -Jm0.8 -F+a90+f7p,Helvetica-Oblique,255/0/0
	echo 31.40 35.55 AKDENIZ | gmt text -R25/45/35/44 -Jm0.8 -F+f7p,Helvetica-Oblique,255/0/0
	echo 34.00 42.70 KARADENIZ | gmt text -R25/45/35/44 -Jm0.8 -F+f7p,Helvetica-Oblique,255/0/0
	echo 28.15 40.59 MARMARA | gmt text -R25/45/35/44 -Jm0.8 -F+f7p,Helvetica-Oblique,255/0/0

gmt end show