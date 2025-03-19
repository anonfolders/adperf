# ADPerf

This repository contains the implementation for ADPerf: Investigating and Testing Performance in Autonomous Driving Systems

There are two parts, in folder [measure_model](measure_modelopen), we include the QPME model described in section 4, which can be run using [QPME](https://github.com/DescartesResearch/QPME) which can be downloaded [on GitHub](https://github.com/DescartesResearch/QPME). For the input rate can be varied for the desired results

In folder [adperf](adperf), we include the implementation for ADPerf as described in section 5. This can be run as follows.

## Preparations

1. Download [OpenPCdet](https://github.com/open-mmlab/OpenPCDet/) to `<root>`. Set up according to instructions in a conda environment. Let's call it `openpcdet`.
2. Download NuScenes-mini from [NuScenes 3D object detection dataset](https://www.nuscenes.org/download) (needs to register an account) according to [nuScenes set up](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/GETTING_STARTED.md).
2. Download models PointPillar-MultiHead and PointPillar-MultiHead from the OpenPCDet model zoo and put them in `checkpoints`

|                                                                                                    |                                              download                                              | 
|----------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------:|
| [PointPillar-MultiHead](adperf/tools/cfgs/nuscenes_models/cbgs_pp_multihead.yaml)                         |  [model-23M](https://drive.google.com/file/d/1p-501mTWsq0G9RzroTWSXreIMyTUUpBM/view?usp=sharing)   | 
| [CenterPoint-PointPillar](adperf/tools/cfgs/nuscenes_models/cbgs_dyn_pp_centerpoint.yaml)                 |  [model-23M](https://drive.google.com/file/d/1UvGm6mROMyJzeSRu7OD1leU_YWoAZG7v/view?usp=sharing)   |

2. Download [Trajectron++](https://github.com/StanfordASL/Trajectron-plus-plus) and set up according to instructions in a conda environment.

## LiDAR-based 3D Obstacle Detection

1. In the `openpcdet` conda environment
2. Copy and overwrite contents in [adperf/tools](adperf/tools) to `<root>/OpenPCDet/tools/`
3. Navigate to `OpenPCDet/tools`, which should look similar to this at this point
```
OpenPCDet
├── checkpoints
│   ├── cbgs_pp_centerpoint_nds6070.pth
│   ├── pp_multihead_nds5823_updated.pth
├── data
│   ├── nuscenes
│   │   │── v1.0-mini
│   │   │   │── samples
│   │   │   │── sweeps
│   │   │   │── maps
│   │   │   │── v1.0-mini  
├── pcdet
├── tools
│   ├── adperf_utils
│   ├── cfgs
│   ├── eval_utils
│   ├── analyze_delays_adperf.ipynb
│   ├── generate_pcd.ipynb
│   ├── run_model_nuscenes.sh
│   ├── test_adperf.py
...
```
4. Run `<root>/OpenPCDet/tools/generate_pcd.ipynb` to generate the perturbation. Set parameters in the 5th (to point to the correct input) and 6th (experiment values) cells target the nuScenes location and specify the test and value. The available values are listed in comment.
5. Run `bash <root>/OpenPCDet/tools/run_model_nuscenes.sh` to execute the models on the testing data.
    1. For the target data, set `data` (line 9). The default/example is set to `obs_left_1`.
    2. For the chosen model, uncomment line 13-14 (for PointPillar) or 17-18 (for CenterPoint). The default is CenterPoint.
6. Open `<root>/OpenPCDet/tools/analyze_delays_adperf.ipynb` and `Run all`
    1. The location of the raw data is in `<root>/OpenPCDet/tools/adperf_results.txt` 
    2. and the computed frames dropped is in `<root>/OpenPCDet/tools/frames_dropped.txt`


## Trajectory Prediction

1. Enter the Trajectron++ environment
2. Copy [adperf/experiments/nuScenes](adperf/experiments/nuScenes) to `<root>/Trajectron_plus_plus/experiments/nuScenes/`
3. Copy generated `<root>/OpenPCDet/tools/frames_dropped.txt` and `<root>/OpenPCDet/tools/trajectory_modification.txt` from the previous section to `<root>/Trajectron_plus_plus/experiments/nuScenes/`.
4.  Open `Trajectron_plus_plus/experiments/nuScenes/run_experiment_perturb_adperf.ipynb` and `Run all`. The ADE & FDE is shown at the bottom.