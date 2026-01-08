# Hugging Face Spaces Deployment Guide

## Overview

This guide helps you deploy the REINVENT4 Drug Generation Application on Hugging Face Spaces.

## Prerequisites

1. A Hugging Face account (create at https://huggingface.co/)
2. This repository code
3. Understanding of the application's resource requirements

## Deployment Steps

### 1. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in the details:
   - **Space name**: `reinvent4-drug-generation` (or your preferred name)
   - **License**: Apache 2.0
   - **SDK**: Streamlit
   - **Hardware**: 
     - Free tier (CPU-basic): OK for demos and small batches
     - CPU-upgrade: Better for moderate use
     - **GPU (Recommended)**: Best for production use with QSAR/ADMET

### 2. Configure the Space

Copy the README metadata to your Space's README.md header:

```yaml
---
title: REINVENT4 Drug Generation Application
emoji: 💊
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.28.0"
app_file: streamlit_app/app.py
pinned: false
license: apache-2.0
python_version: "3.10"
---
```

### 3. Upload Files

#### Option A: Using Git (Recommended)

```bash
# Clone your Hugging Face Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Add this repository as a remote and pull
git remote add source https://github.com/bhatnira/DrRoy-version-REINVENT4-Docker-Gen-Application.git
git pull source main --allow-unrelated-histories

# Push to Hugging Face
git push origin main
```

#### Option B: Using the Web Interface

1. Upload all files directly through the Hugging Face web interface
2. Make sure to include:
   - `streamlit_app/` directory (entire folder)
   - `requirements.txt`
   - `packages.txt`
   - `.streamlit/config.toml`
   - `README_HUGGINGFACE.md` (as README.md)
   - Other necessary files (configs, reinvent, reinvent_plugins, etc.)

### 4. Essential Files for Deployment

```
YOUR_SPACE/
├── README.md (copy from README_HUGGINGFACE.md with metadata header)
├── requirements.txt
├── packages.txt
├── .streamlit/
│   └── config.toml
├── streamlit_app/
│   ├── app.py (main application)
│   └── ... (other app files)
├── reinvent/
│   └── ... (REINVENT4 core modules)
├── reinvent_plugins/
│   └── components/ (QSAR/ADMET components)
├── configs/
│   └── ... (configuration files)
└── data/
    └── ... (any required data files)
```

### 5. Handle Large Files

The prior model files (*.prior) are large (>50MB). Options:

#### Option A: Exclude Prior Files (Recommended for Spaces)
Add to `.gitignore`:
```
priors/*.prior
priors/*.ckpt
```

Then modify the app to download on first run or work without them.

#### Option B: Use Git LFS
```bash
git lfs install
git lfs track "priors/*.prior"
git add .gitattributes
git add priors/*.prior
git commit -m "Add large prior files with LFS"
git push origin main
```

### 6. Optimize for Hugging Face Spaces

#### Update requirements.txt

Ensure lightweight versions:
```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.21.0
plotly>=5.15.0
rdkit>=2021.0
torch>=2.0.0  # Will use CPU version on CPU spaces
scikit-learn>=1.0.0
# Keep only essential dependencies
```

#### Create a startup script (optional)

Create `setup.sh`:
```bash
#!/bin/bash
echo "Setting up REINVENT4 Drug Generation Application..."
mkdir -p data logs outputs priors
echo "Setup complete!"
```

Make it executable:
```bash
chmod +x setup.sh
```

### 7. Test Your Deployment

1. Wait for the Space to build (check the "Building" indicator)
2. Once ready, the app will be available at: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
3. Test basic functionality:
   - Navigate through different generation modes
   - Generate a small batch (10 molecules)
   - Verify visualizations work
   - Check QSAR/ADMET predictions (if enabled)

## Performance Optimization for Spaces

### Memory Management

1. **Reduce batch sizes**: Default to 10-20 molecules instead of 100
2. **Lazy loading**: Load models only when needed
3. **Clear cache**: Use `st.cache_resource` appropriately

Update in `streamlit_app/app.py`:
```python
# Optimize for Hugging Face Spaces
if os.getenv('SPACE_ID'):  # Hugging Face Space environment
    DEFAULT_BATCH_SIZE = 10
    MAX_BATCH_SIZE = 50
else:
    DEFAULT_BATCH_SIZE = 50
    MAX_BATCH_SIZE = 200
```

### Speed Optimizations

1. **Disable heavy computations** on free tier
2. **Use cached results** when possible
3. **Async operations** for long-running tasks

## Common Issues and Solutions

### Issue 1: Out of Memory Error

**Solution**: 
- Reduce batch size
- Upgrade to CPU-upgrade or GPU tier
- Disable ADMET-AI on CPU tier

### Issue 2: Timeout on Generation

**Solution**:
- Use faster sampling strategy
- Reduce number of molecules
- Consider GPU Space for complex tasks

### Issue 3: Missing Dependencies

**Solution**:
- Check `requirements.txt` has all needed packages
- Add system packages to `packages.txt`
- Check build logs for specific errors

### Issue 4: Prior Model Files Missing

**Solution**:
- App should handle gracefully without priors
- Add download logic for essential models
- Or use smaller pre-trained models

## Cost Considerations

### Free Tier (CPU-basic)
- **Cost**: Free
- **Limitations**: 2 vCPU, 16GB RAM
- **Best for**: Demos, small batches (10-20 molecules)
- **Drawbacks**: Slower, may timeout on large tasks

### CPU-upgrade
- **Cost**: ~$0.03/hour
- **Specs**: 8 vCPU, 32GB RAM
- **Best for**: Regular use, moderate batches (50-100 molecules)

### GPU Tier
- **Cost**: ~$0.60/hour (T4) to ~$3.00/hour (A100)
- **Specs**: GPU + more CPU/RAM
- **Best for**: Production use, large batches, ADMET-AI predictions
- **Recommended**: T4 or A10G for good balance

## Advanced Configuration

### Environment Variables

Set in Space settings:
```bash
SPACE_ID=your-space-id
HF_TOKEN=your-hugging-face-token  # If accessing gated models
TORCH_HOME=/tmp/torch  # Cache directory
```

### Custom Domain (Pro Users)

Hugging Face Pro users can set a custom domain in Space settings.

## Monitoring and Maintenance

1. **Check logs**: Monitor Space logs for errors
2. **User feedback**: Enable discussion tab for feedback
3. **Update regularly**: Pull latest fixes from GitHub
4. **Resource usage**: Monitor memory/CPU usage in Space metrics

## Security Considerations

1. **No sensitive data**: Don't commit API keys or secrets
2. **User limits**: Consider rate limiting for public Spaces
3. **Input validation**: Ensure all user inputs are validated
4. **Output sanitization**: Clean generated SMILES before display

## Support and Resources

- **Hugging Face Docs**: https://huggingface.co/docs/hub/spaces
- **Streamlit Docs**: https://docs.streamlit.io/
- **REINVENT4 Issues**: https://github.com/bhatnira/DrRoy-version-REINVENT4-Docker-Gen-Application/issues

## Example Deployment Commands

### Full Deployment Script

```bash
#!/bin/bash

# Create a new Space repository
# (Do this through HF web interface first)

# Clone your Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/reinvent4-drug-gen
cd reinvent4-drug-gen

# Copy necessary files from your local repo
cp -r /path/to/REINVENT4GUI-APP-Docker/streamlit_app .
cp -r /path/to/REINVENT4GUI-APP-Docker/reinvent .
cp -r /path/to/REINVENT4GUI-APP-Docker/reinvent_plugins .
cp -r /path/to/REINVENT4GUI-APP-Docker/configs .
cp -r /path/to/REINVENT4GUI-APP-Docker/.streamlit .
cp /path/to/REINVENT4GUI-APP-Docker/requirements.txt .
cp /path/to/REINVENT4GUI-APP-Docker/packages.txt .
cp /path/to/REINVENT4GUI-APP-Docker/README_HUGGINGFACE.md README.md

# Commit and push
git add .
git commit -m "Initial deployment of REINVENT4 Drug Generation Application"
git push origin main

echo "Deployment initiated! Check your Space at:"
echo "https://huggingface.co/spaces/YOUR_USERNAME/reinvent4-drug-gen"
```

## Conclusion

Your REINVENT4 Drug Generation Application should now be running on Hugging Face Spaces! Share the link with your team or make it public for the community.

For production deployments, consider:
- GPU Space for better performance
- Private Space for sensitive work
- Regular updates and monitoring
- User authentication if needed

Happy drug discovery! 💊🔬
