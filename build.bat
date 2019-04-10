cp template.sav SYSTEMFLAW.0.sav
rm payload.bin
armips payload.s
py -2 inject.py
pause