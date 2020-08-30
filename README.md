# pydini
Programatically create complex houdini setups via simple blueprints.

## What, Why and How?
Create, manage and automate your houdini base setups with maximum flexibility. Houdini can be used as a central hub in any CG or Game Pipeline. It's powerful python API enables the creation of powerful data driven tools and automation of tedious and repetitive tasks. By using pydini you can break those tasks into small fragments called ***blueprints*** which can then be composed to create complex setups.

## Features
* **Automate houdini file setup** - With pydini you can create complex initial setups with ease
* **Chain blueprints** - Split your setup into multiple composable and chainable fragments
* **Performance** - Hash based saving of each instruction optimizes cooking time, detect changes in dependencies and recook only if needed
* **Python** - Use python to describe your setup steps

## Example Usecase
You have a houdini file containing a turntable setup where you load a geometry file from an external path and render a sequence to disk. Now you have multiple assets that you want to create turntables of. With pydini this could be done like this:

create_asset_turntables.py
```python
from pydini.process import process

assets = [
    "/path/to/assets/robot.abc",
    "/path/to/assets/dinosaur.abc",
    "/path/to/assets/spaceship.abc"
]
for asset in assets:
    env = {
        "asset": asset
    }
    
    process("/path/to/turntable.bp", env)

```

**turntable.bp**
```bash
# load base setup
houdini load /path/to/turntable.hip

# use python file to set framerange
python load /path/to/turntablesetup.py setFrameRange 1001 1002

# use python file to set path attribute for asset geometry
# use --cache false to disable caching of instruction
# use ${asset} to load the asset variable from env
python --cache false load /path/to/turntablesetup.py setAssetPath ${asset}

# save turntable
houdini save /path/to/assets/${asset}_turntable.hip
```

**turntablesetup.py**
```python
import hou

def setFrameRange(start, stop):
    hou.playbar.setFrameRange(start, stop)

def setAssetPath(asset):
    hou.node("/obj/turntable").parm("assetpath").set(asset)
```