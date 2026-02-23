"""
yaml
"""

import yaml
from .path_tools import get_abs_path


def load_yaml(path: str, encoding: str = 'utf-8'):
    with open(path, 'r', encoding=encoding) as f:
        return yaml.load(f, Loader=yaml.FullLoader)


def load_rag_config(config_path: str=get_abs_path('config/rag.yaml'), encoding: str='utf-8'):
    return load_yaml(config_path, encoding=encoding)

def load_chroma_config(config_path: str=get_abs_path('config/chroma.yaml'), encoding: str='utf-8'):
    return load_yaml(config_path, encoding=encoding)

def load_prompts_config(config_path: str=get_abs_path('config/prompts.yaml'), encoding: str='utf-8'):
    return load_yaml(config_path, encoding=encoding)

def load_agent_config(config_path: str=get_abs_path('config/agent.yaml'), encoding: str='utf-8'):
    return load_yaml(config_path, encoding=encoding)


rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agents_config = load_agent_config()

if __name__ == '__main__':
    print(rag_config['chat_model_name'])