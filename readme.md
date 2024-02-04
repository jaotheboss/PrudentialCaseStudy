# Prudential Coding Challenge

## Task Overview
To implement a RAG solution for the Prudential product - PRUmax plus. 

First step is to develop the RAG solution and implement a web UI that can be deployed locally and on cloud providers. Next step is to improve on the RAG solution by better aligning the solution with business expectations. Last step if there is time is to develop an intent discovery and clarification module to handle out-of-scope questions; with the goal of improving user experience (UX).

## Project Breakdown
- Since this is just a prototype, we will use simple frameworks to develop the solution. `venv` for the virtual environment, `llama-index` for the RAG framework, and `streamlit` as the web chat interface. 
- The LLM component will be an OpenAI API endpoint. The reason for this is convenience. Since we want to develop the solution and iterate through problems quickly, we use highly compatible and stable tools to start with.
- `llama-index` comes with a slew of tools to configure the each aspect of a RAG system: data loading, indexing, retrieval and querying. The idea is to use the standard configuration first and thereafter perform tweaks to optimize the solution w.r.t the dataset
- `streamlit` will provide a standard chat interface with caching for the data loading and indexing step. This can be performend via llama-index as well. 
- The solution will thereafter be converted into a Docker image and deployed locally and over the cloud. 
  - Only tested on local deployment and Google CloudRun. AWS App Runner is not compatible with streamlit deployment.

Assumptions:
1. The LLM component is handled via the OpenAI API format. In the event where we want to use an LLM in another format, refer [here](https://docs.llamaindex.ai/en/stable/examples/llm/llama_2_llama_cpp.html)
2. Key stakeholders of this solution are financial advisors that require to search up information when studying. Or people that are already interested in knowing more about the product. If stakeholders extend to general public then more information would need to be added.
3. There are potential malicous users that we have to defend against. 

## Deployment Instructions
The key files that are required for this app are:
1. `data/` - the whole data folder (!Note that you might have to add files into this folder yourself)
2. `app.py` - the app logic
3. `utils.py` - utility logic
4. `requirements.txt` - the list package requirements
5. `Dockerfile` - the instructions for building a Docker image

### Local Deployment
Step 1 - Navigate to the root of your project folder

Step 2 - Run streamlit app. `streamlit run app.py`

### Local Docker Deployment
Step 1 - Navigate to the root of your project folder

Step 2 - Build the Docker image. `docker build -t rag_app .`

Step 3 - Run the Docker image as a container. Pass your OpenAI API Key as the environment variable for the solution to work. `docker run -e OPENAI_API_KEY=<openai-api-key> -p 8080:8080 rag_app`

The solution should be up and running on your localhost on port 8080. To perform a health check, ping `/healthz`. 

### Deploying on GCP CloudRun
Need to show at least 1 deployment on a cloud provider. For this case it'll be GCP CloudRun which allows deployment of single containers.

Step 1 - On your CLI, login to gcloud. `gcloud auth login`; This will prompt you to signin to your google account

Step 2 - Configure the project that you'll be working in on gcloud. `gcloud config set project <project name>`; Set the project you want to deploy the app in

Step 3 - Configure docker and gcloud interaction. `gcloud auth configure-docker asia-southeast1-docker.pkg.dev`; Configure docker to link with GCP. Be sure to enable artifact registry in your GCP project

Step 4 - Build the Docker image via gcloud. `gcloud builds submit . -t asia-southeast1-docker.pkg.dev/<project name>/<repo name>/rag-app:0.1`; This will build and store the Docker image in gcloud's Artifact Registry

Step 5 - Deploy on CloudRun. `gcloud run deploy <app name> --image asia-southeast1-docker.pkg.dev/<project name>/<repo name>/rag-app:0.1 --platform managed --allow-unauthenticated --region asia-southeast1 --update-env-vars=OPENAI_API_KEY=<openai-api-key>`; Be sure to set `--allow-unauthenticated` as this will allow calls via the internet.

One thing to note about GCP CloudRun is that all apps are exposed via port 8080. That's why we declare port 8080 for the streamlit app. On top of that, we have to build the image in GCP itself if not there will be an error.

### Deploying on AWS App Runner [WIP]
`aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com`

`docker tag rag_app <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/rag-app:0.1`

`docker push <account-id>.dkr.ecr.ap-southeast-1.amazonaws.com/rag-app:0.1`

## Example of How to Use
[Watch the video!](https://youtu.be/Q3mtkexvLXA)


## Benchmark Questions:
1. **Do PRUmax-plus cover TPD after 70 years old?**
   - As shown under the notes on page 11, Total and Permanent Disability (TPD) benefit will cease upon attaining age 70.

2. **What is PRUmax plus?**
   - PRUmax plus is a regular premium non-participating endowment plan that offers both savings and protection in one plan.

3. **What are the entry age limits for the Child and Adult plans under PRUmax plus?**
   - Child Plan: 1 to 15 years; Adult Plan: 16 to 50 years.

4. **What premium terms are available under PRUmax plus?**
   - Premium terms available are 10 and 20 years. # solution doesn't seem to understand what premium term means here. 

5. **What coverage terms are offered by PRUmax plus?**
   - Coverage terms offered are 20, 30, 40, and 50 years.

6. **How does PRUmax plus handle non-accidental death or Total and Permanent Disability (TPD) benefits?**
   - It provides the sum assured or surrender value or 125% of total premiums paid, whichever is higher, before age 70.

7. **What are the benefits in case of Accidental Death under PRUmax plus?**
   - After age 70, in the case of accidental death, 200% of the Basic Sum Assured will be payable.

8. **What guaranteed cash payments does PRUmax plus offer?**
   - It offers 4% of Basic Sum Assured every 2 years starting from the end of Policy Year 2 up to maturity.

9.  **How does the Waiver of Premium on Critical Illness work in PRUmax plus?**
    - Upon diagnosis of a Critical Illness, the remaining premiums of the policy will be waived while the policy remains in force until a claim is made.

10. **What is the minimum loan amount available under the policy loan feature?**
    - The minimum loan amount available is RM500.

11. **What options are available for receiving Guaranteed Cash Payments?**
    - Policyholders can choose to receive the Guaranteed Cash Payment or accumulate it with potential interest.

Key things to take note. We should also test for questions beyond the scope of the product as a way to prevent malicous users. We should also test for follow-up questions that by itself doesn't seem to be relevant to the product, but in conversation history context, is relevant.

## Misc

### Deliverables
1. Develop a prototype in the form of a Docker image that is cloud agnostic. (GitHub repository with instructions on how to build Docker image)
2. An instruction readme file to explain how to install and use the prototype. (Instructions on how to use)

### Criteria
1. End-to-end functionality; From code to web ui. As long as we are able to get answers when asking questions.
2. Creativity and originality of solution; Out of the box implementation methods 
3. Quality of code and documentation; Engineering excellence. Simplicity. Well documented solution.
4. Effectiveness of prototype (performance); How well does it handle its task. Which is to answer questions about the product and only the product.
5. Impact - whether the solution aligns with the business objectives; Does it fulfill its intended purpose and is it useful

## To-do:
- [x] Handle out-of-context request. This will prevent customers from taking advantage of the chatbot as a generic LLM. (via prompting) 
- [x] Prompt engineer the bot to have a personality tailored to answering questions specifically for PRUmax Plus (via prompting) 
- [ ] Improve retrieval and synthesising performance (configuring the chunking, indexing and parsing) [pending re-ranking]

Improvements
- [ ] Expand to products beyond PRUmax Plus? Using [this](https://docs.llamaindex.ai/en/stable/examples/agent/react_agent_with_query_engine.html) example, I can develop indexes of each product and enable cross product validation
- [ ] Context validation should be done before querying the chat engine to conserve chat memory buffer. Simple classifier is a possibility
- [ ] Implement a hybrid retriever that includes re-ranking (see utils)

Thoughts:
For intention recognition, if there was as simpler way to recognise intention we could provide a prompt template based on these intentions. We can do this using LangChain multi-chain approach. Or manually implement the logic if we're using a traditional classification model.


How do I tweak the Llama-Index framework to work with the streamlit interface? Especially to handle chain-prompting scenarios like "if similarity scores are all low, craft a follow up question to clarify which references are the most relevant. or if non of them are relevant, perhaps providing more information in the query"
