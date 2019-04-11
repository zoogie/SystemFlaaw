WHAT:
This is a savegame exploit for the System Flaw cartridge game on the Nintendo DSi (NOT the DSiWare game, System Flaw: Recruit).
This game is available for the US and EU and is the first DSi exclusive cartridge title to be exploited (to my knowledge).
It uses a null terminated high-score name string that is not size checked to overwrite the stack with data. See inject.py for more info.

WHY:
Just for fun. Because I could.
The exploit has little practical purpose due to carts not having NAND or SD access, and the fact this game's save is only 512 bytes.
60% of the space is available for a payload, but that's still not a lot.
Q: Why isn't the hax title very creative?
A: Because the game's name is already a perfect exploit name :p

HOW:
Install - Just take the SYSTEMFLAW.0.SAV file and use TWLSaveTool on the 3DS to write it to your cart. The included save works for both US and EU.
You might also use a DS savegame manager, but I don't know much about those, or if they even work with DSi exclusive games.
Exploit trigger - Click past the splash screens then select: Survival -> HARD -> Start, and the exploit will run.
This also works fine on the no$gba emulator. I tested with the latest emu version and the NAND booting option set up.

Notes: This is a very minor project to take a break from larger and more difficult projects. Thus, I will not accept pull requests and issues. The repo will likely be archived soon. Feel free to fork and play around with it though. You need armips, windows, and python2 to compile.

Greetz:
CTURT for the color pattern asm code.
Martin Korth for no$gba
rebane2001 for testing the EU version