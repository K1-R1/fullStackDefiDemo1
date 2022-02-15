import yaml, json, os, shutil

def main():
    update_front_end()

def update_front_end():
    # Sending the front end; build folder
    copy_folders_to_front_end("./build", "./front_end/src/brownie-build")

    # Sending the front end; brownie config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print('Front end updated ...\n')

def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
