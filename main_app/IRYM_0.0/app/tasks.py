from celery import shared_task
from models.img_model.img_llm import img_generator
from models.text_llm.text_llm_responder import responder
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
@shared_task
def generate_description_task(user_prompt: str) -> str:
    description = responder.generate_response(user_prompt)
    return description

@shared_task
def generate_image_task(description: str, image_path: str = "output.png") -> str:
    img_generator.generate(description, output_path=image_path)
    return image_path


"""
message_structure = {
    "type": "", # type of the scene nature, city, animal, etc...
    "shape": "", #shape of the scene circle, square, etc...
    "objects": [
            {
                "type": "",
                "colors": [],
                "
            }
        ], # objects on the seans
    "colors":[], # color of the objects
    "background":[], # background color of the screen
    "mode": [], # light, night, dark ,day , etc...
}
"""

SceneTypes = Literal["nature", "city", "animal", "animation"]
Shapes = Literal["circle", "square", "triangle", "rectangle"]
ObjectTypes = Literal[
    "human", "man", "woman", "person", "tree", "car", "building", "bridge",
    "mountain", "bird", "fish", "flower", "sun", "moon",
]
Modes = Literal["light", "dark", "day", "night"]

# identfy the object in the scene
class ObjectInScene(BaseModel):
    object_type: ObjectTypes = Field(..., description="Type of the object in the scene")
    colors: List[str] = Field(..., min_items=1, description="List of colors in the object")

# identfy the scene
class Scene(BaseModel):
    scene_type: SceneTypes = Field(..., description="General type of the scene")
    shape: Shapes = Field(..., description="Geometric shape of the scene")
    objects: List[ObjectInScene] = Field(..., min_items=1,max_items=10, description="Objects in the scene")
    colors: List[str] = Field(..., min_items=1, max_items=10,description="Main object colors in the scene")
    background: List[str] = Field(..., min_items=1, max_items=10, description="Background colors of the scene")
    mode: Modes = Field(..., description="Lighting or mood mode like night or day")



def build_prompt(user_prompt: str):
    return [
        {
            "role": "system",
            "content": "\n".join([
                "You are an expert NLP data parser.",
                "Your task is to extract structured information from the input text.",
                "You must return the extracted data as a valid JSON object based on the Pydantic model provided.",
                "Do not add any explanation, introduction, or summary — just return the raw JSON."
            ])
        },
        {
            "role": "user",
            "content": "\n".join([
                "Prompt:",
                user_prompt.strip(),
                "\nPydantic schema (use this as a reference for keys and types):",
                json.dumps(Scene.model_json_schema(), indent=2, ensure_ascii=False)
            ])
        }
    ]

# def prompt_to_image(prompt):
#     recommendations = []
#     extraction_message = build_prompt(prompt)
#     print("Prompt received:", extraction_message)
#     initial_response = recommender(extraction_message)
#     if initial_response:
#         recommendations.append(initial_response)
#     percentages = [0.2, 0.3, 0.4, 0.5, 0.6]
#     for i, p in enumerate(percentages):
#         if i < len(recommendations):
#             rec = recommendations[i]
#             if isinstance(rec, str) and rec:
#                 cutoff = max(1, int(p * len(rec)))
#                 new_prompt = rec[:cutoff].strip()
#                 prompt_message = build_prompt(new_prompt)
#                 response = recommender(prompt_message)
#                 if response and response not in recommendations and len(response) > 15:
#                     recommendations.append(response)
#     print("Recommendations:", recommendations[0])
#     return JsonResponse({"response": recommendations[0]})

