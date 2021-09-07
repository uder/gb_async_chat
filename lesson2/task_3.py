import yaml


data = {
    'first': ['element_1', 'element_2', 'element_3'],
    'second': 256,
    'third': {
        'nested_first': '1 ∀',
        'nested_second': '2 ∄',
        'nested_third': '3 ∞',
    },
}

def main():
    with open ('file.yaml', 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

if __name__ == "__main__":
    main()