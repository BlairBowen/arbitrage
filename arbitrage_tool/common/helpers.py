import yaml

def read_yaml(yaml_name):
    # Load YAML configuration
    path = f'/home/bowenbv/Code/arbitrage_tool/arbitrage_tool/config/{yaml_name}.yaml'
    with open(path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config[yaml_name]
