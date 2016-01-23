# Infuanfu's Location as a service

blurb

## TODO
 * use venv on dev, but system packages on prod
   * pyserial
   * python sdl (python3-pygame?)

# Protocols

## AT
    define AT protocol here

## VBA

    msg := VISLIST | ERRORMSG, '\n'
    VISLIST := 'vis|', ITEMCOUNT, '|', [INFO[{'\t', INFO}]]
    ITEMCOUNT := ℕ0
    INFO := BTID, '/-', SIGNALSTRENGTH
    BTID := HEX, ':', HEX, ':', HEX
    HEX := [0-9a-fA-F]+
    SIGNALSTRENGTH := ℕ0
    ERRORMSG := 'err|', ERRORCODE, '|', [ERRORTEXT], '\n'
    ERRORCODE := ℕ0
    ERRORTEXT := string

## ACDC

    msg := PLAYCMD|STOPCMD, '\n'
    PLAYCMD := 'play|', BTID
    STOPCMD := 'stop|'
    BTID := HEX, ':', HEX, ':', HEX


## PCM

    define PCM protocol here
