MODELS = {
    "checkpoint": {
        "realism-engine-sdxl": {
            "url": "https://huggingface.co/sid38/base_models/resolve/main/realism-engine.safetensors",
            "filename": "realism-engine-sdxl.safetensors",
            "enabled": True,
            "category": "SDXL"
        },
        "realistic-stock-photo-v2-sdxl": {
            "url": "https://huggingface.co/sid38/base_models/resolve/main/realistic-stock-photo.safetensors",
            "filename": "realistic-stock-photo-v2-sdxl.safetensors",
            "enabled": False,
            "category": "SDXL"
        },
        "realistic-vision-sd15": {
            "url": "https://civitai.com/api/download/models/501240?type=Model&format=SafeTensor&size=full&fp=fp16",
            "filename": "realistic-vision-sd15.safetensors",
            "enabled": True,
            "category": "SD 1.5"
        }
    },
    "unet": {
        "flux-dev-acorn-is-spinning": {
            "url": "https://civitai.com/api/download/models/757421?type=Model&format=SafeTensor&size=pruned&fp=fp8",
            "filename": "flux-dev-acorn-is-spinning.safetensors",
            "enabled": True,
            "category": "FLUX dev"
        }
    },
    "lora": {
        "flux-boring-reality_v2": {
            "url": "https://huggingface.co/sid38/loras/resolve/main/flux_boring_reality_v2.safetensors",
            "filename": "flux-boring-reality_v2.safetensors",
            "enabled": True,
            "category": "FLUX dev"
        }
    },
    "vae": {
        "vae-ft-mse-840000-ema-pruned": {
            "url": "https://huggingface.co/sid38/vae/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors",
            "filename": "vae-ft-mse-840000-ema-pruned.safetensors",
            "enabled": True
        }
    }
}

def get_enabled_models():
    enabled_models = {}
    for category, models in MODELS.items():
        enabled_models[category] = {
            name: model for name, model in models.items() if model['enabled']
        }
    return enabled_models

def toggle_model(category, model_name, enable=True):
    if category in MODELS and model_name in MODELS[category]:
        MODELS[category][model_name]['enabled'] = enable
    else:
        print(f"Model {model_name} not found in category {category}")

# Example usage:
if __name__ == "__main__":
    print("Enabled models:")
    for category, models in get_enabled_models().items():
        print(f"  {category}:")
        for name, model in models.items():
            print(f"    - {name}: {model['url']}")
    
    # Toggle a model off
    toggle_model("checkpoint", "realistic-vision-sd15", False)
    
    print("\nAfter toggling 'realistic-vision-sd15' off:")
    enabled_checkpoints = get_enabled_models()['checkpoint']
    for name, model in enabled_checkpoints.items():
        print(f"  - {name}: {model['url']}")
