# Docker Images for Kohya_ss and ComfyUI

Utility to create Docker images for Kohya_ss and ComfyUI with GPU and CPU support.

## Configuration

### Model Configuration
Configure models for ComfyUI in `src/config/models_config.yaml`:

```yaml
unet:  # model type
  model_name.safetensors:
    url: "download_url"
    enabled: true  # set to true to download
```

### Environment Variables
Required tokens should be set as environment variables. See `.env.example` for required variables.

## Features

### ComfyUI Image
- **Pre-installed Nodes:**
  - Impact Pack & Subpack
  - Inspire Pack
  - Essentials
  - Use Everywhere
  - RGThree Comfy
  - PuLID
  - Masquerade Nodes
  - Face Parsing
  - Fluxtapoz
  - Detail Daemon
  - KJNodes
  - Segment Anything

- **Automatic Model Download:** Container downloads models based on `models_config.yaml` at deployment

### Kohya Image
Automatically downloads from HuggingFace:
- unet flux1-dev
- text encoders: t5xxl_fp16, clip_l
- vae ae

## Build Commands

### ComfyUI
```bash
# CPU
docker build -t comfy-image-cpu -f Docker/Comfyui/Dockerfile.cpu .

# GPU
docker buildx build --platform linux/amd64 -t comfyui-image:xx --load -f Docker/Comfyui/Dockerfile .
```

### Kohya
```bash
# CPU
docker build -t kohya-image-cpu -f Docker/kohya/Dockerfile.cpu .

# GPU
docker buildx build --platform linux/amd64 -t kohya-image:xx --load -f docker/kohya/Dockerfile .
```

## Deployment Example

ComfyUI CPU container:
```bash
docker run -p 8188:8188 -p 8080:8080 --env-file .env -d comfy-image-cpu
```