# Aeroforest.py NASA Space App Challenge 2024 submussion.

## GA.IA - Storytelling with generative AI based on grounded climate data.

Aeroforest.py team deliverables for NASA International Space Apps Challenge 2024 Hackaton taking place in University of León

A brief showcase of the app:


https://github.com/user-attachments/assets/7c579c7b-1bbf-43ad-bed3-482b28354f6e


Streamlit RAG app with curated content from NASA and GHG Center Data. Documents curated by hand and available on the `base_documents` folder.

## To reproduce

Install required dependencies:

```bash
pip install -r requirements.txt
```

Launch a qdrant instance in docker:

```bash
sh run_qdrant.sh
```

Process documents, generate the embeddings and upload the results to qdrant vector database:

```bash
python generate_embeddings.py ./base_documents/aumento_temperatura aumento_temperatura
python generate_embeddings.py ./base_documents/drought drought
python generate_embeddings.py ./base_documents/rising_sea_level rising_sea_level
python generate_embeddings.py ./base_documents/tropical_storms tropical_storms
python generate_embeddings.py ./base_documents/wildfires wildfires
```

Configure .env to use `OPENAI_API_KEY` and `OPENROUTER_API_KEY`:

```
cp .env.example .env
```

Run app:

```bash
streamlit run landing.py
```
