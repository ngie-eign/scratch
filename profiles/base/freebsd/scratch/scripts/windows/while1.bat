REM This script is the equivalent of a while 1 loop for all command arguments
REM passed. Only works in win2k+.
REM
REM usage: while1.bat argv[1:]

@ECHO OFF
shift
:loop
%*
goto loop
