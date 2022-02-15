import yaml, json, os, shutil

def main():
    update_front_end()

def update_front_end():
    # The Build
    copy_folders_to_front_end("./build/contracts", "./front_end/src/brownie-build")

    # The Contracts
    copy_folders_to_front_end("./contracts", "./front_end/src/contracts")

    # The ERC20
    copy_files_to_front_end(
        "./build/contracts/dependencies/OpenZeppelin/openzeppelin-contracts@4.5.0/ERC20.json",
        "./front_end/src/brownie-build/ERC20.json",
    )
    # The Map
    copy_files_to_front_end(
        "./build/deployments/map.json",
        "./front_end/src/brownie-build/map.json",
    )

    # The Config, converted from YAML to JSON
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open(
            "./front_end/src/brownie-config.json", "w"
        ) as brownie_config_json:
            json.dump(config_dict, brownie_config_json)

def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

def copy_files_to_front_end(src, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copyfile(src, dest)
