import os
import yaml

config_folder = '../config'
config_name = 'config1.yml'
yaml_save_path = os.path.join(config_folder, config_name)
print(yaml_save_path)
write = True   # otherwise, read yaml


data = dict(
    probability_from = 0.7,
    probability_to = 0.9,
    probability_step = 0.1,
    iteration_from = 5,
    iteration_to = 15,
    iteration_step = 5,
    expand_size_from = 100,
    expand_size_to = 200,
    expand_size_step = 50,
    patch_size_from = 10,
    patch_size_to = 20,
    patch_size_step = 5,
    kernel_size_from = 3,
    kernel_size_to = 9,
    kernel_size_step = 3,
    dice_range_from = 0.8,
    dice_range_to = 0.9,
    mask_num = 5
#     IOU_range_from = 0.8,
#     IOU_range_to = 0.9,
#     HD_range_from = 0.8,
#     HD_range_to = 0.9
)


if write:

    with open(yaml_save_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)
else:
    
    with open(yaml_save_path, 'r') as stream:
        try:
            parsed_yaml = yaml.safe_load (stream)
            print (parsed_yaml)
        except yaml.YAMLError as exc:
            print(exc)


