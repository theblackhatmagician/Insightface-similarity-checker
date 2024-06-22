# Insightface Similarity Checker for Stable Diffusion Web UI

This custom script integrates a face similarity checker into the Stable Diffusion Web UI, enabling users to conveniently check the similarity between a reference image and generated images using the Insightface library.

## Installation and Setup

### Prerequisites
- Ensure you have Stable Diffusion Web UI installed.
- Make sure you have Python and a virtual environment set up for the Stable Diffusion Web UI.

### Steps to Install

1. **Download the Script:**
   - Download or clone the script `Insightface_similarity_checker.py` and place it in the `scripts` directory of your Stable Diffusion Web UI installation.
   - The path should be `stable-diffusion-webui/scripts/Insightface_similarity_checker.py`.

2. **Install Required Packages:**
   - Open a terminal and navigate to the root directory of your Stable Diffusion Web UI installation.
   - Activate the virtual environment:
     - For Windows: `venv\Scripts\activate`
     - For Linux/macOS: `source venv/bin/activate`
   - Install the required packages by running:
     ```bash
     pip install albumentations==1.4.0 onnxruntime==1.15.0 insightface==0.7.3 protobuf==3.20.3
     ```

3. **Start the Web UI:**
   - Start the Stable Diffusion Web UI as you normally would. The Insightface similarity checker will now be available.

## Usage

1. **Enable Insightface Similarity Checker:**
   - Open the Stable Diffusion Web UI.
   - Navigate to the scripts section.
   - Enable the Insightface similarity checker script.

2. **Upload Reference Image:**
   - Upload a reference image which will be used for similarity comparison with the generated images.

3. **Generate Images:**
   - Generate images as usual using the Stable Diffusion Web UI.
   - The similarity score between the reference image and each generated image will be calculated and displayed in the metadata section below each generated image.

4. **Refresh Metadata:**
   - If the similarity score is not displayed after generation, click on the image to view it in full screen and then close the full screen view to refresh the metadata. The score should then appear.

## Additional Information

- The similarity score indicates how closely the generated image matches the reference image based on facial features.
- This script leverages the Insightface library, which provides state-of-the-art face recognition capabilities.

For any issues or further assistance, please refer to the documentation of Insightface and the Stable Diffusion Web UI.

---

Feel free to contribute to the development or suggest improvements by creating issues or pull requests in the repository. Happy generating!
