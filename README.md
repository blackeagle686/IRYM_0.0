# IRYM_0.0
# LLM + 2D Image Generation Project

project:
  name: IRYM_0.0
  description: >
    A project that connects a Language Model (LLM) to a 2D image generation system.
    The backend is powered by Django and FastAPI, with image generation served via Google Colab and Ngrok.

setup:
  conda_environment:
    description: >
      To ensure a clean and consistent environment, use conda to create the environment from the provided YAML file.
    steps:
      - Create the environment:
          command: conda env create -f environment.yml
      - Activate the environment:
          command: conda activate irym_env

usage:
  step_1:
    description: >
      Set up the FastAPI backend on Google Colab and expose it via Ngrok.
    instructions:
      - Create accounts on:
          - https://ngrok.com/
          - https://colab.research.google.com/
      - Open the notebook located at: `utils/fast_api_colab_side.ipynb`
      - Insert your Ngrok private auth token inside the notebook.
      - Run the notebook (make sure you're using a GPU runtime).
      - The code will generate a public Ngrok URL.
      - Copy the public URL and place it in your Django project's `.env` file like this:
          format: ng_key="your_public_ngrok_url"

  step_2:
    description: >
      Install project dependencies and run the Django server.
    instructions:
      - Make sure you've created and activated the conda environment as described above.
      - Run the Django app using the following command:
          command: python manage.py runserver

notes:
  - Ensure the `.env` file exists in the Django app root directory.
  - Replace "your_public_ngrok_url" with the actual URL provided by Ngrok after running the Colab notebook.
  - Do not share your private Ngrok key publicly.
