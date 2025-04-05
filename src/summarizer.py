# Code to Summarize the Document
import tensorflow as tf

from transformers import pipeline
from dataclasses import dataclass
from src.utils import *


@dataclass
class Model_config:
    model_task: str = "summarization"
    model_repo_id: str = "google/pegasus-large"

class summarizer:
    def __init__(self):
        self.configs = Model_config()

    def initialize_model(self):
        try:
            summarizer = pipeline(self.configs.model_task, model = self.configs.model_repo_id)
            return summarizer
        except Exception as e:
            print("Error Occured While inititlizing the model")
            print(e)
    
    def summarize_the_data(self, extracted_chunks):
        # Take the Extracted text and Summarize the data
        try:
            summaries = []
            print("Initializing the model")
            model = self.initialize_model()
            print("Model initialization completed")
            chunks_counter = 1
            for chunk in extracted_chunks:
                print(chunks_counter)
                summary = model(chunk, max_length=100, min_length=50, do_sample=False)[0]['summary_text']
                chunks_counter += 1
                summaries.append(summary)

            # Concatenate the summaries into a single string
            summary = ' '.join(summaries)
            return summary
            # print(summary)
        except Exception as e:
            print("Error Occured while summarizing the data")
            print(e)



# if __name__ == "__main__":
#     # print(tf.__version__)
#     summarizer = summarizer()
#     # Extract PDF
#     document = extract_pdf("E:\\Python\\AI_Projects\\Documment_summarization_q_a\\artifacts\\data\\attention.pdf")
#     # Clean document
#     cleaned_document = clean_text(document)
#     # Create Chunks
#     chunks = chunks_of_text(cleaned_document)

#     # summarize the document
#     summarizer.summarize_the_data(chunks)