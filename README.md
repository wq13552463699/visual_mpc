# How to start visual-MPC on Sawyer
start kinect-bridge node:
```cd visual_mpc/python_visual_mpc/sawyer/visual_mpc_rospkg/launch/bridgeonly.launch```

and run
```./startkinect.sh```

To launch visual MPC run:

```roslaunch visual_mpc_rospkg visual_mpc_singletask.launch robot:=<robot_name> exp:=<name_of_folder_inside:visual_mpc/experiments/cem_exp/benchmarks_sawyer>```

The parameter exp specifies which configuration file inside ```:visual_mpc/experiments/cem_exp/benchmarks_sawyer```  to use.

# Information for Simulation Setup:

In order to run rendering remotely on a different machine it is necessary to give remote users access to the x server:
Log into graphical session on remote computer and give access by typing:
xhost +

Also set the DISPLAY variable
export DISPLAY=:0

### To generate training data:
Go in the root directory of the repo and run:

```python python/lsdc/parallel_data_collection.py  <name_of_datafolder>```

Note: <name_of_datafolder> is the folder-name inside lsdc/pushing_data
Each of the folders in pushing_data must have a "/train" and "/test" subdirectory.
The hyperparams.py file to specifies how the data-collection is done.


### To run a benchmark on the pushing task go in the lsdc base directory and run:
```python python/lsdc/utility/benchmarks.py <benchmark_folder_name>```



