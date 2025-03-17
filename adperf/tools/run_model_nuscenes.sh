#! /usr/bin/bash

data=data/corruptions/pcds/obs_left_1
orig_backup=../data/nuscenes/v1.0-mini/samples/LIDAR_TOP_ORIG

# pointpillar
# model_config=cfgs/nuscenes_models/cbgs_pp_multihead.yaml
# model=../checkpoints/pp_multihead_nds5823_updated.pth

# centerpoint
model_config=cfgs/nuscenes_models/cbgs_dyn_pp_centerpoint.yaml
model=../checkpoints/cbgs_pp_centerpoint_nds6070.pth

target=../data/nuscenes/v1.0-mini/samples/LIDAR_TOP

# backup LIDAR_TOP
mv $target $orig_backup

cp -r $data $target

for i in {1..1}
do
    python test_adperf.py --choose_dataset nuscenes --cfg_file $model_config --batch_size 1 --workers 1 --ckpt $model
done
rm -r $target
