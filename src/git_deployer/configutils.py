import yaml

def load_config(config_path = 'deploy_config.yml') -> dict:
    with open(config_path) as fp:
        config = yaml.safe_load(fp)
    return config

