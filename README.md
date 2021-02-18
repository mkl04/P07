# P07

Question Answering application (chatbot) for Peru's News using Transformers.

### Objective
The purpose of this project was to create a chatbot that could answer some doubts or questions about the Peru's News on 2021.

### Dataset
In order to get the information of the last two weeks of news, I did a Web Scrapping on Gestión's webpage, a very popular and serious newspaper from Perú.
For this, BeatifulSoup was used. About pre-processing, just stopwords was deleted.

### Solution
The template was gotten from [IBM's Web App](https://github.com/IBM/MAX-Question-Answering-Web-App). Due to I need to select the new with the required information, I apply the very known algorithm on IR (Information Retrieval): [BM25](https://en.wikipedia.org/wiki/Okapi_BM25).
For Question Answering, I used a pre-trained Transformers model for spanish vocabulary that is available on [Hugging Face's page](https://huggingface.co/models).

### Results
As can be seen, the chatbot also shows the precision of the inference. Obviously, this application doesn't always shows the right answer, but maybe with fine-tuning, it will.

![Alt text](imgs/results.PNG?raw=true "Demo")