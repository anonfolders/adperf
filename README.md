# ADPerf

This repository contains the implementation for ADPerf: Investigating and Testing Performance in Autonomous Driving Systems

There are two parts, in folder [measure_model](measure_modelopen), we include the QPME model described in section 4, which can be run using [QPME](https://github.com/DescartesResearch/QPME) which can be downloaded [on GitHub](https://github.com/DescartesResearch/QPME). For the input rate can be varied for the desired results

In folder [adperf](adperf), we include the implementation for ADPerf as described in section 5. This can be run as follows.

## Preparations

1. Set up (OpenPCdet)(https://github.com/open-mmlab/OpenPCDet/) and (nuScenes)[https://github.com/open-mmlab/OpenPCDet/] according to [this set up](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/GETTING_STARTED.md). Setup a conda environment since we would need two. Let's call it `openpcdet`
2. Download models PointPillar-MultiHead and PointPillar-MultiHead from the OpenPCDet model zoo.
2. Download [Trajectron++](https://github.com/StanfordASL/Trajectron-plus-plus) and set up according to instructions in a conda environment.

## LiDAR-based 3D Obstacle Detection

1. In the `openpcdet` conda environment
2. Copy and overwrite contents in [adperf/tools](adperf/tools) to `<root>/OpenPCDet/tools/`
3. Navigate to OpenPCDet/tools
4. Run `<root>/OpenPCDet/tools/generate_pcd.ipynb` to generate the perturbation. Set parameters in the 5th and 6th cells target the nuScenes location and specify the test and value.
5. Run `bash <root>/OpenPCDet/tools/run_model_nuscenes.sh`
6. Open `<root>/OpenPCDet/tools/analyze_delays_adperf.ipynb` and `Run all`
7. The location of the raw data is in `<root>/OpenPCDet/tools/adperf_results.txt` and the computed frames dropped is in `<root>/OpenPCDet/tools/frames_dropped.txt`

## Trajectory Prediction

1. Enter the Trajectron++ environment
2. Copy [adperf/experiments/nuScenes](adperf/experiments/nuScenes) to `<root>/Trajectron_plus_plus/experiments/nuScenes/`
3. Copy generated `<root>/OpenPCDet/tools/frames_dropped.txt` and `<root>/OpenPCDet/tools/trajectory_modification.txt` from the previous section to `<root>/Trajectron_plus_plus/experiments/nuScenes/`.
4.  Open `Trajectron_plus_plus/experiments/nuScenes/run_experiment_perturb_adperf.ipynb` and `Run all`. The ADE & FDE is shown at the bottom.