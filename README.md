# ADPerf

This repository contains the implementation for ADPerf: Investigating and Testing Performance in Autonomous Driving Systems

There are two parts, in folder [measure_model](measure_model), we include the QPME model described in section 4, which can be run using [QPME](https://github.com/DescartesResearch/QPME) which can be downloaded [on GitHub](https://github.com/DescartesResearch/QPME). The input rate can be varied for the desired results.

In folder [adperf](adperf), we include the implementation for ADPerf as described in section 5. This can be run as follows.

## Preparations

1. First, confirm that you have an NVIDA GPU with compatible driver and CUDA. We conduct our study on an Ubuntu 22.04 system equipped with an AMD Ryzen 16-core CPU, 256 GiB of memory, and an NVIDIA GeForce RTX 3090. 
    ```
    nvidia-smi
    ```
    which outputs
    ```
    +---------------------------------------------------------------------------------------+
    | NVIDIA-SMI 535.183.01             Driver Version: 535.183.01   CUDA Version: 12.2     |
    |-----------------------------------------+----------------------+----------------------+
    | GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
    |                                         |                      |               MIG M. |
    |=========================================+======================+======================|
    |   0  NVIDIA GeForce RTX 3090        Off | 00000000:01:00.0 Off |                  N/A |
    | 30%   29C    P8              26W / 350W |     10MiB / 24576MiB |      0%      Default |
    |                                         |                      |                  N/A |
    +-----------------------------------------+----------------------+----------------------+
    ```
    and
    ```
    nvcc --version
    ```
    which outputs
    ```
    nvcc: NVIDIA (R) Cuda compiler driver
    Copyright (c) 2005-2022 NVIDIA Corporation
    Built on Tue_Mar__8_18:18:20_PST_2022
    Cuda compilation tools, release 11.6, V11.6.124
    Build cuda_11.6.r11.6/compiler.31057947_0
    ```
    In this case, it shows that I have `Driver Version: 535.183.01` and `Build cuda_11.6`. The provided commands are specific to cuda 11.6. If you have a different version installed, please confirm the the libraries are compatible.

2. Set up in a new conda environment as follows:  
    1. Create a new conda environment called `adperf` using python 3.7.
        ```
        conda create -n adperf python=3.7
        conda activate adperf
        ```
    2. Install the appropriate [PyTorch](https://pytorch.org/) version. In our case, we used
        ```
        pip install torch==1.13.1+cu116 torchvision==0.14.1+cu116 torchaudio==0.13.1 --extra-index-url https://download.pytorch.org/whl/cu116
        ```
    3. Install the appropriate [spvconv](https://github.com/traveller59/spconv) version. We used
        ```
        pip install spconv-cu116
        ```

3. Navigate to the [OpenPCDet](adperf/OpenPCDet) folder.
    ```
    cd OpenPCDet
    ```

5. Install requirements and build OpenPCDet
    ```
    pip install -r requirements.txt
    pip install -e .
    ```

6. Install an appropriate version of [`torch_scatter`](https://pypi.org/project/torch-scatter/), e.g.,
    ```
    pip install torch-scatter -f https://data.pyg.org/whl/torch-1.13.1+cu116.html
    ```

6. Download NuScenes-mini from [NuScenes 3D object detection dataset](https://www.nuscenes.org/download) (needs to register an account) according to [nuScenes set up](https://github.com/open-mmlab/OpenPCDet/blob/master/docs/GETTING_STARTED.md).
    1. Organize the files as follows:
        ```
        OpenPCDet
        ├── data
        │   ├── nuscenes
        │   │   │── v1.0-mini
        │   │   │   │── maps
        │   │   │   │── samples
        │   │   │   │── sweeps
        │   │   │   │── v1.0-mini  
        ├── pcdet
        ├── tools
        ```
    2. Setup install the nuScenes-panoptic expandsion, download the dataset from [https://www.nuscenes.org/download](https://www.nuscenes.org/download) (same place as the full data). Unpack the compressed files into same location. The folder at this point should look like this:
        ```
        OpenPCDet
        ├── data
        │   ├── nuscenes
        │   │   │── v1.0-mini
        │   │   │   │── lidarseg <- Contains the .bin files
        │   │   │   │── maps
        │   │   │   │── panoptic <- Contains the *_panoptic.npz files
        │   │   │   │── samples
        │   │   │   │── sweeps
        │   │   │   │── v1.0-mini
        │   │   │   │   │── Usual files (e.g. attribute.json, 
        |   |   |   |   |                calibrated_sensor.json etc.)
        │   │   │   │   │── lidarseg.json
        │   │   │   │   │── panoptic.json
        │   │   │   │   │── category.json  <- note that the original
        |   |   |   |   |                     category.json is overwritten. 
        |   |   |   |   |                     (original < lidarseg < panoptic)
        ├── pcdet
        ├── tools
        ```
    2. Install the `nuscenes-devkit` version 1.1.8:
        ```
        pip install nuscenes-devkit==1.1.8
        ```
    3. Generate the data infos
        ```
        # for lidar-only setting
        python -m pcdet.datasets.nuscenes.nuscenes_dataset --func create_nuscenes_infos \
        --cfg_file tools/cfgs/dataset_configs/nuscenes_dataset.yaml \
        --version v1.0-mini
        ```


7. Download models PointPillar-MultiHead and PointPillar-MultiHead from the OpenPCDet model zoo and put them in [`adperf/OpenPCDet/checkpoints`](adperf/OpenPCDet/checkpoints) (needs to be created). (Note: these are official links provided on the [OpenPCDet repository](https://github.com/open-mmlab/OpenPCDet/). Please feel free to download from there.)

    |              model                                                                         |                                              download                                              | 
    |----------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------:|
    | [PointPillar-MultiHead](adperf/tools/cfgs/nuscenes_models/cbgs_pp_multihead.yaml)                         |  [model-23M](https://drive.google.com/file/d/1p-501mTWsq0G9RzroTWSXreIMyTUUpBM/view?usp=sharing)   | 
    | [CenterPoint-PointPillar](adperf/tools/cfgs/nuscenes_models/cbgs_dyn_pp_centerpoint.yaml)                 |  [model-23M](https://drive.google.com/file/d/1UvGm6mROMyJzeSRu7OD1leU_YWoAZG7v/view?usp=sharing)   |

2. Download [Trajectron++](https://github.com/StanfordASL/Trajectron-plus-plus) and set up according to instructions in a conda environment.

## LiDAR-based 3D Obstacle Detection

[`adperf/OpenPCDet/`](adperf/OpenPCDet/) should look similar to this at this point
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
1. Navigate to [`adperf/OpenPCDet/tools`](adperf/OpenPCDet/tools)
3. Run [`generate_pcd.ipynb`](adperf/OpenPCDet/tools/generate_pcd.ipynb) to generate the perturbation. Set parameters in the 5th (to point to the correct input) and 6th (experiment values) cells target the nuScenes location and specify the test and value. The available values are listed in comments.
4. Next, run [`run_model_nuscenes.sh`](adperf/OpenPCDet/tools/run_model_nuscenes.sh) to execute the models on the testing data.
    1. For the target data, set `data` (line 9). The default/example is set to `noise_left_1`.
    2. For the chosen model, uncomment line 13-14 (for PointPillar) or 17-18 (for CenterPoint). The default is CenterPoint.
5. Once done, open [`analyze_delays_adperf.ipynb`](adperf/OpenPCDet/tools/analyze_delays_adperf.ipynb) and `Run all` to analyze the latency and compute the latency
    1. The location of the raw data is in [`adperf/OpenPCDet/tools/adperf_results.txt`](adperf/OpenPCDet/tools/adperf_results.txt) 
    2. And the computed frames dropped is in [`frames_dropped.txt`](adperf/trajectron_input/frames_dropped.txt)


## Trajectory Prediction

1. Clone (Trajectron++)[https://github.com/StanfordASL/Trajectron-plus-plus].
```
git clone --recurse-submodules https://github.com/StanfordASL/Trajectron-plus-plus
```

2. Set up, and enter the Trajectron++ environment per (instructions)[https://github.com/StanfordASL/Trajectron-plus-plus]
```
conda create --name trajectron++ python=3.6 -y
conda activate trajectron++
cd Trajectron_plus_plus
pip install -r requirements.txt

```

3. Copy the nuscenes-mini data as above and place them in the experiments/nuScenes directory. Then, download the map expansion pack (v1.1) and copy the contents of the extracted maps folder into the experiments/nuScenes/v1.0-mini/maps folder.
```
Trajectron_plus_plus
├── experiments
│   ├── nuScenes
│   │   │── v1.0-mini
│   │   │   │── maps
│   │   │   │   │── ... (4 map png files)
│   │   │   │   │── boston-seaport.json
│   │   │   │   │── singapore-hollandvillage.json
│   │   │   │   │── singapore-onenorth.json
│   │   │   │   │── singapore-queenstown.json
│   │   │   │── samples
│   │   │   │── sweeps
│   │   │   │── v1.0-mini  
...
```

4. Process them into a data format the model can work with
```
cd experiments/nuScenes

# For the mini nuScenes dataset, use the following
mkdir ../processed
python process_data.py --data=./v1.0-mini --version="v1.0-mini" --output_path=../processed
```

5. Set `data_path = Path('../../trajectron_input')` (line 6 in [experiment_helper.py](adperf/experiments/nuScenes/experiment_helper.py)) to the absolute path of [trajectron_input/](adperf/trajectron_input/)
6. Copy the contents of [adperf/experiments/nuScenes](adperf/experiments/nuScenes) to `Trajectron_plus_plus/experiments/nuScenes/`
7.  Open `Trajectron_plus_plus/experiments/nuScenes/run_experiment_perturb_adperf.ipynb` and `Run all`. The ADE & FDE is shown at the bottom. In case of no deviation, it can shows as 0 or nan.