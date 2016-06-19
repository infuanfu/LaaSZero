# This Project has been ABANDONED

It will no longer receive updates.

# Infuanfu's Location as a service

## Further Resources

### Docker

The docker image can be downloaded from https://hub.docker.com/r/infuanfu/laaszero/. Or just do a
```
docker pull infuanfu/laaszero
```

## TODO
 * use a VM or docker and always install software packages using apt
   * pyserial
   * python sdl (python3-pygame?)
 * set up py.test

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
