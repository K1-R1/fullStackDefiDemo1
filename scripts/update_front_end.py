import yaml, json

def main():
    update_front_end()

def update_front_end():
    # Sending the front end; brownie config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)
    print('Front end updated ...\n')
    