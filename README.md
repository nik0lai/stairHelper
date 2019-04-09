# staircaseHelper

This is a helper class to implement and track a staircase procedure. In a Python environment like Spyder you can quickly check if the script is working by `execfile('path_to_script/staircaseHelper.py')`. This should output a randomly simulated staircase threshold, an array with the simulated answers and dv evolution, and a plot.

## Modules

The script is tested on Ubuntu 16.04 and Windows 7 with the following modules (version)

- Python (2.7.15 | packaged by conda-forge)
- NumPy (1.15.4)
- Matplotlib (2.2.3)

## Basic use

```python
# Import class
from staircaseHelper import staircaseHelper
# Create (initialize) staircase
some_staircase = staircaseHelper(dv0 = 10, conv_p = .75, reversals = 20, stepsize = 3)
# Update staircase (boolean indicating if correct or incorrect answer)
some_staircase.new_trial(True)
# Get the updated dv value
some_staircase.dv
# ... after the number of reversals is reached
some_staircase.get_treshold()
```

## Known issues

- The method ```plot_staircase()```, either if the plot is saved or displayed, will switch the focus to the iPhyton console, or to whatever console is being used. If a full-screen experiment with Psychopy is being run the mouse will become visible and the focus will switch from the experiment window to the console or terminal.