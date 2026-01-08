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

# REINVENT4 Drug Generation Application (Dr. Roy Version)

An advanced drug discovery platform combining REINVENT4's generative AI with QSAR activity prediction and ADMET property optimization.

## 🚀 Features

- **De Novo Drug Design**: Generate novel molecules from scratch using RNN-based SMILES generation
- **Scaffold Hopping**: Replace molecular scaffolds while preserving substituents with position markers
- **Linker Design**: Design optimal linkers between molecular fragments
- **R-Group Replacement**: Systematic R-group exploration and optimization
- **QSAR Activity Prediction**: Gaussian Process Regression for biological activity prediction
- **ADMET-AI Integration**: Multi-endpoint ADMET property prediction using transformer models
- **Multi-Objective Optimization**: Balance drug-likeness, activity, and ADMET properties
- **Curriculum Learning**: Progressive 4-stage training approach

## 📊 Key Capabilities

### Molecular Generation Modes
1. **De Novo Generation**: Create molecules from scratch with desired properties
2. **Scaffold Hopping**: Replace core scaffolds (benzene → pyridine, etc.) with visual position markers
3. **Linker Design**: Connect molecular fragments with optimal linkers
4. **R-Group Replacement**: Systematic exploration of substituents

### Property Prediction & Optimization
- **QED** (Quantitative Estimate of Drug-likeness)
- **SA Score** (Synthetic Accessibility)
- **Target Similarity** (Tanimoto similarity to reference compounds)
- **QSAR Activity**: GPR-based μM activity prediction
- **ADMET Properties**: CYP inhibition, hERG toxicity, solubility, permeability

### Interactive Visualization
- Real-time molecular structure display
- Property distribution plots
- Activity vs. property correlation analysis
- Generation statistics and metrics

## 🎯 Use Cases

- **Drug Discovery**: Generate novel drug candidates with optimal properties
- **Lead Optimization**: Improve existing molecules through systematic modifications
- **Scaffold Exploration**: Find alternative scaffolds with similar activity
- **ADMET Optimization**: Balance activity with safety and pharmacokinetic properties

## 💡 Getting Started

1. Navigate to the desired generation mode in the sidebar
2. Configure generation parameters (number of molecules, sampling strategy)
3. Set optimization criteria (QED, SA Score, target similarity)
4. Enable QSAR/ADMET predictions if needed
5. Click "Generate Molecules" and analyze results

## 📚 Documentation

See `METHODOLOGY.tex` for detailed technical documentation including:
- Mathematical formulations for QSAR GPR models
- ADMET-AI transformer architecture
- Multi-objective reward functions
- Curriculum learning strategy

## 🔬 Technology Stack

- **REINVENT4**: RNN-based molecular generation
- **RDKit**: Molecular structure handling
- **Streamlit**: Interactive web interface
- **PyTorch**: Deep learning framework
- **Gaussian Process Regression**: Activity prediction
- **ADMET-AI**: Transformer-based ADMET prediction

## ⚠️ Important Notes

### Hugging Face Spaces Limitations
- **Large Model Files**: Prior models (>50MB) may need to be downloaded on first run
- **GPU**: Some operations benefit from GPU acceleration (use GPU Space if available)
- **Memory**: Complex generation tasks may require upgraded Space tier
- **Timeout**: Long-running generations may hit time limits on free tier

### Performance Considerations
- Start with smaller batch sizes (10-50 molecules) for faster results
- Use "Fast Sampling" strategy for quick exploration
- Enable QSAR/ADMET only when needed (adds computational overhead)
- Consider upgrading to GPU Space for production use

## 📖 Citation

If you use this application in your research, please cite:
- REINVENT4: Modern AI-driven generative chemistry
- Original repository: [REINVENT4 GitHub](https://github.com/MolecularAI/REINVENT4)

## 🤝 Contributing

This is a specialized deployment for drug discovery research. For issues or feature requests, please contact the repository maintainer.

## 📄 License

Apache License 2.0 - See LICENSE file for details

## 🙏 Acknowledgments

- REINVENT4 development team at Molecular AI
- RDKit community
- ADMET-AI developers
- Streamlit team

---

**Note**: This application is for research purposes only. Generated molecules should be validated through proper experimental procedures before any real-world application.
