---
name: IRYM_0.0
description: >
  LLM + 2D image generation system using Django, FastAPI (on Colab), and Ngrok.
  Connects a language model to generate prompts and a 2D image generation model to visualize them.
version: 0.0.1
license: MIT
authors:
  - name: Your Name
    email: your.email@example.com
dependencies_file: environment.yml
frameworks:
  - Django
  - FastAPI
  - Conda
  - Google Colab
  - Ngrok
setup:
  - step: Create conda environment
    command: conda env create -f environment.yml
  - step: Activate environment
    command: conda activate irym_env
  - step: Run Django server
    command: python manage.py runserver
  - step: Configure Ngrok
    description: >
      Add your Ngrok public URL to the .env file in Django
      using the variable name "ng_key"
    env_variable: ng_key
colab_notebook: utils/fast_api_colab_side.ipynb
tags:
  - LLM
  - AI image generation
  - Django
  - FastAPI
  - Ngrok
---
