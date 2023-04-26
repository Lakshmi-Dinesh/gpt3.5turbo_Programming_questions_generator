# Programming Questions Generator - Using a Large Language machine learning model:
A Python 3 based application that generates specified number of programming questions from a programming language(Python/Java) and a topic from the list of topics displayed.
This application internally uses GPT 3.5 turbo engine which is one of the advanced OpenAI's machine learning Language models.

File to execute/run : program_generator_controller.py

To execute this project on your machine,
  - Create a ChatGPT account
  - Go to https://platform.openai.com/account/api-keys and generate the OpenAI secret API key for your account
  - Set the above API key in your device Environment variables under the name OPENAI_API_KEY  
  - Install the python openai and tkinter library packages if you do not have them installed already
    Find more step by step information about the API key generation from https://platform.openai.com/

Other generic libraries used:
  - subprocess
  - traceback
  - os
  - json
  - textwrap
  - time and datetime

Note:
  - This application uses a version of the GPT 3.5 Turbo engine. Your account may be charged depending on token usage.
    There is a free 5$ initial credit available after using which you will be charged.
    Read more about this from https://platform.openai.com/
  - The programs and log files will be generated within the out folder of the project
  - If you do not have notepad installed on your device, the output files would need to be opened manually from its path 
    through your local file explorer using a different .txt reader application.

What to expect - A typical use case:
  - Upon executing the program_generator_controller.py, a GUI window launches where the user has the option to select a specified number of 
    programming questions, a programming language(Python/Java) and a topic from the list of topics displayed.
  - User name and topic selection are mandatory inputs expected from the user.
  - Click the Generate questions button. The questions will be generated and stored in a text(.txt) file.
  - The path to the file created will be displayed to the user. 
  - Browse button will take the user to the folder where the file is generated.
  - Select file and click open to view the contents in notepad(launched by the program)
For troubleshooting and debug purposes, a log file is also generated in the location ./out/logs

Outlook:

For now, the project uses system, user and assistant messages in the initialization phase to set a context. The intent 
of this project is to highlight and showcase the possibilities of using an LLM in education enrichment.
The ML model can be trained using expert vetted, good quality training data to obtain specific, high quality results.
Fine tuning is also a future addition that is expected in the GPT model used here which can improve the outcome further.

