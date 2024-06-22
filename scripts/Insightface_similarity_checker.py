import torch
import insightface
from typing import Any
import numpy as np
import os

Frame = np.ndarray[Any, Any]

FACE_ANALYSER = None
providers = ['CPUExecutionProvider']

import modules.scripts as scripts
import gradio as gr

from modules.processing import process_images
from modules import images

def get_face_analyser() -> Any:
    global FACE_ANALYSER

    if FACE_ANALYSER is None:
        FACE_ANALYSER = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
        FACE_ANALYSER.prepare(ctx_id=0)

    return FACE_ANALYSER

def get_many_faces(frame: Frame):
    try:
        return get_face_analyser().get(frame)
    except ValueError:
        return None

def get_one_face(frame: Frame, position: int = 0):
    many_faces = get_many_faces(frame)
    if many_faces:
        try:
            return many_faces[position]
        except IndexError:
            return many_faces[-1]
    return None

def process_image_embedding(source_frame, target_frame):
    source_face = get_one_face(source_frame)
    
    reference_face_position = 0
    reference_face = get_one_face(target_frame, reference_face_position)
    if reference_face and source_face:
        source_image_embedding = source_face.embedding
        target_image_embedding = reference_face.embedding
        
        cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        output = cos(torch.tensor(source_image_embedding).unsqueeze(0), torch.tensor(target_image_embedding).unsqueeze(0))

        x =output[0] # input value in range [-1, 1]
        x_min = -1  # minimum of original range
        x_max = 1  # maximum of original range
        y_min = 0  # minimum of target range
        y_max = 1  # maximum of target range

        scaled_x = ((x - x_min) / (x_max - x_min)) * (y_max - y_min) + y_min

        return scaled_x.numpy()
    else:
        print("couldn't detect faces")
        return 0

def start(source_frame,target_frame):
    source_frame = np.array(source_frame)
    target_frame = np.array(target_frame)

    face_embedding=process_image_embedding(source_frame, target_frame)
    return face_embedding


class SimilarityChecker(scripts.Script):

    def title(self):
        return "Insightface Similarity Checker"

    def ui(self, is_img2img):
        enable = gr.Checkbox(label='Enable', value=False, elem_id=self.elem_id("enable"))
        img = gr.Image(type="numpy", elem_id=self.elem_id("img"))
        with gr.Row():
            save_filtered = gr.Checkbox(label='Save filtered images', value=False, elem_id=self.elem_id("save_filtered"))
            thresh = gr.Slider(label="Score threshold", minimum=0, maximum=1, value=0.95, step=0.01, elem_id=self.elem_id("thresh"))
        filter_output_path = gr.Textbox(label="path",info="folder path to save the filtered images",lines=1,value="roop_filtered")
        return [img,enable,save_filtered,thresh,filter_output_path]
    
    def run(self, p, img, enable, save_filtered, thresh=0.95, filter_output_path="images_filtered"):
        if img is not None and enable:
            self.source = img
            proc = process_images(p)
            for i in range(proc.index_of_first_image,len(proc.images)):
                result = start(
                    self.source,
                    proc.images[i],
                )
                proc.infotexts[i] += f"\n\nSimilarity: {result}"
                if result >= thresh and save_filtered:
                    os.makedirs(filter_output_path, exist_ok=True)
                    images.save_image(proc.images[i], filter_output_path, "Filtered", suffix=f"score_{result}")
            return proc
        else:
            print(f"Please provide a source face")
        