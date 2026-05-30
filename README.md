# numclick

A fun idle game for NumWorks

## Features

- Basic clicker mechanic
- Cool circle that shrinks when you click
- Shop items that help you earn more points

## Getting Started

### Executing

#### From the NumWorks website
1. Go to https://my.numworks.com/python/skue/numclick
2. Click on "Send to my calculator"
> Your calculator must be connected, and you must use a Chromium-based browser
3. Done !

#### From Github
1. Download the script from [releases](https://github.com/skueee/numclick/releases/new) (stable) or from the [repo files](https://github.com/skueee/numclick/blob/main/numclick.py) (unstable)
2. Go to https://my.numworks.com/python/
3. Click on My scripts, then New Script
4. Open the script you just downloaded with a text editor and copy everything
5. Paste the code in the NumWorks editor
6. Add a name
7. Click on "Send to my calculator"
> Your calculator must be connected, and you must use a Chromium-based browser.
8. Done !

### Using
#### Bindings :
- OK to click
- UP and DOWN to navigate the shop
- EXE to buy

### Developing

1. Copy the repo :
```
git clone https://github.com/skueee/numclick
```
2. Open the numclick.py script with any editor you want. I personally use VSCode.
> If you want an emulator, you can use [this extension](https://open-vsx.org/vscode/item?itemName=k-kuroguro.numworks-simulator) with VSCode, or the [online emulator](https://www.numworks.com/simulator/). Note that it can be a bit laggy.
3. When you're done, just run the script on your calculator (see Executing section)

* If you want to contribute, you can check [the contributing guide](https://github.com/skueee/numclick/blob/main/CONTRIBUTING.md)

## Common issues

- **Shop items give points too slowly in emulator**
  
  This happens because ticks run slower on emulators than physical calculators. Reduce the tick threshold in the main loop if it feels too slow.

## Support
Feel free to open an [issue](https://github.com/skueee/numclick/issues) if you encounter any problem, or to open a [pull request](https://github.com/skueee/numclick/pulls) if you know how to fix it (check [the contributing guide](https://github.com/skueee/numclick/blob/main/CONTRIBUTING.md))