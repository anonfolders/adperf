#! /usr/bin/bash

# backup LIDAR_TOP
orig_backup=../data/nuscenes/v1.0-mini/samples/LIDAR_TOP_ORIG
target=../data/nuscenes/v1.0-mini/samples/LIDAR_TOP
mv $target $orig_backup

# target the generated PCD for testing
data=data/corruptions/pcds/obs_left_1

# choose model
# pointpillar
# model_config=cfgs/nuscenes_models/cbgs_pp_multihead.yaml
# model=../checkpoints/pp_multihead_nds5823_updated.pth

# centerpoint
model_config=cfgs/nuscenes_models/cbgs_dyn_pp_centerpoint.yaml
model=../checkpoints/cbgs_pp_centerpoint_nds6070.pth

# move testing data in place for execution
cp -r $data $target
# execute model
for i in {1..1}
do
    python test_adperf.py --choose_dataset nuscenes --cfg_file $model_config --batch_size 1 --workers 1 --ckpt $model
done
rm -r $target

# restore backup data
mv $orig_backup $target

