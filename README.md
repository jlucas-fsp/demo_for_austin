# Getting Started:

With python 3.11 installed (or greater), in the root of the repo, install the dependencies:

```bash
pip install -r requirements.txt
```

Then, create a .env file in the root of the repository and add your Anthropic API key in like so:

```.env
ANTHROPIC_API_KEY=<key>
```

Then, run the following command in the root of the repository to run the demo user-interface that will an example of an output of LLM grading of open-ended homework question responses:

```bash
streamlit run graph.py
```

A browser window should pop up with the results. These are the results I've generated in my testing, but feel free to prompt engineer as you want and edit the code to better suit your needs. 

If you'd like to test any changes you make, be sure to delete the data/grades.json 

Happy grading!

# Getting around the repo:

In the root of the repo are all the python files. The main workflow is implemented in grade.py, but there are some util functions in utils.py

The prompt, specialized for Anthropic Claude, is in the prompts directory

The example homework question, grading criteria, and example answers are all in the documents directory

The raw data that is output from the graph in grade.py (the value of the `res` variable at the bottom) is stored in the data directory
