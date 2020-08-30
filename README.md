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
**Beware:** This is currently mostly a writeup on how I want it to work, not a reflection on how it works at the moment.

### Turntable
You have a houdini file containing a turntable setup where you load a geometry file from an external path and render a sequence to disk. Now you have multiple assets that you want to create turntables of. With pydini this could be done like this:

```python
""" create_asset_turntables.py
This is your python file from which you process the blueprint. 
You pass the necessary variables to the blueprint via python dict. 
"""

from pydini.process import process

# all my assets
assets = [
    "/path/to/assets/robot.abc",
    "/path/to/assets/dinosaur.abc",
    "/path/to/assets/spaceship.abc"
]

# iterate over all my assets and run turntable process
for asset in assets:
    env = {
        "asset": asset
    }
    
    process("/path/to/turntable.bp", env)

```

***/path/to/turntable.bp***
```bash
# turntable.bp
# load base setup
houdini load /path/to/turntable.hip

# use python file to set framerange
# this instruction will be cached and only cooked once
# each call to turntable.bp will then refer to the cached file instead
python load /path/to/turntablesetup.py setFrameRange 1001 1002

# use python file to set path attribute for asset geometry
# use ${asset} to load the asset variable from env
python load /path/to/turntablesetup.py setAssetPath ${asset}

# save turntable
houdini save /path/to/assets/${asset}_turntable.hip
```

***/path/to/turntablesetup.py***
```python
""" turntablesetup.py
This file contains the methods that should be triggered via blueprint instructions.
"""
import hou

def setFrameRange(start, stop):
    """ Set Frame Range of turntable.
    
    Args:
        int start
        int stop
    """
    
    hou.playbar.setFrameRange(start, stop)

def setAssetPath(asset):
    """ Set path to asset of turntable.
    
    Args:
        string asset
    """
    
    hou.node("/obj/turntable").parm("assetpath").set(asset)
```

### Lighting
You now realize, that you want to present your assets in a different lighting, we can chain new instructions to the initial ***turntable.bp*** to achieve this.

***/path/to/turntable_with_different_lighting.bp***
```bash
# turntable_with_different_lighting.bp
# this file will load the previous turntable.bp as a dependency and build up on that
blueprint load /path/to/turntable.bp

# use python file to change lighting
python load /path/to/turntablesetup.py setAlternativeLighting

# save turntable with alternative lighting
houdini save /path/to/assets/${asset}_turntable_alternative_lighting.hip
```

We modify our turntablesetup.py accordingly.

***/path/to/turntablesetup.py***
```python
""" turntablesetup.py
This file contains the methods that should be triggered via blueprint instructions.
"""
import hou

def setFrameRange(start, stop):
    # [...]

def setAssetPath(asset):
    # [...]
    
def setAlternativeLighting():
    hou.node("/obj/turntable").parm("lighting").set(1)
```

Last but not least we change our ***create_asset_turntables.py*** to point to ***turntable_with_different_lighting.bp***. This will now continue with the cached results from ***turntable.bp*** and build on top of that the new instructions from the blueprint. 

```python
""" create_asset_turntables.py
This is your python file from which you process the blueprint. 
You pass the necessary variables to the blueprint via python dict. 
"""

from pydini.process import process

# all my assets
assets = [
    "/path/to/assets/robot.abc",
    "/path/to/assets/dinosaur.abc",
    "/path/to/assets/spaceship.abc"
]

# iterate over all my assets and run turntable process
for asset in assets:
    env = {
        "asset": asset
    }
    
    process("/path/to/turntable_with_different_lighting.bp", env)

```
