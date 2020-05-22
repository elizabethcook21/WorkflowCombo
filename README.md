# Summary
WorkflowCombo is a python command line tool that helps users build a CWL workflow from many CWL command line tools. It is a companion tool to [ToolJig](https://github.com/srp33/ToolJig). The purpose of this command line tool is not to create a perfect workflow that will handle a variety of cirumstances and cases. This is a simple tool that will give you foundation to build upon. Once you've generated a workflow with this tool, you will almost certainly have to open the file and make edits in order for it to run how you would like it to.

# What are CWL Workflows?
[CWL](https://www.commonwl.org/) stands for Common Workflow Language and is a standard defined by a group of bioinformaticians to make the creation and sharing of command line tools and workflows interoperable and standard across the world. When a tool is written in CWL, it can be run by anyone else around the world who knows and uses CWL. CWL is provided in many computer softwares and bioinformatics tools. 
"A workflow describes a set of steps and the dependencies between those steps. When a step produces output that will be consumed by a second step, the first step is a dependency of the second step." [(Source)](https://python-cwlgen.readthedocs.io/en/latest/workflowclasses.html) A wonderful resource to learn more about CWL workflows is [here](https://www.commonwl.org/v1.0/Workflow.html) and to see many visual examples of workflows, refer to [this website](https://view.commonwl.org/workflows).

In summary, there are four main sections of a CWL workflow: metadata, inputs, outputs, and steps. 
1. Metadata: This section describes the general information of a workflow. This metadata of this app defines the class of CWL file (which is "Workflow"), the CWLVersion (which is v1.1), and an "id" for the workflow which is the name provided.
2. Inputs: The inputs of the workflow are the information that a user has prior to running any steps of the workflow, but information that the workflow needs to have in order to run. Some examples of workflow inputs would be raw genomic data, reference files, URL's of files to download from the web, among others.
3. Outputs: The outputs of the workflow are the big picture outputs of what the workflow is trying to accomplish. After running through a series of steps, the workflow will produce certain outputs that are meaningful to researchers. These outputs are defined in this section.
4. Steps: This is the essence of and defining characteristic of workflows. The steps define the many Command Line Tools that the workflow will use to parse the inputs and generate outputs. Each step is connected through their inputs and outputs. It is very common that the output of a certain step will be the input of the next step. 


# Using WorkflowCombo
To begin using WorkflowCombo, there are a few steps to be taken. Firsly, this command line tool has a few dependencies in order to run smoothy. They are 
* cutie  (for providing options on the command line)
* sys  (for getting arguments and ending the program early)
* os  (read existing cwl files)
* cwlgen  (easily build new workflow)
* yaml  (read existing cwl files)
* inquirer  (ask questions on the command line)

You may have to install these packages using `<pip install *package name*>` (to run this, you will have to install pip) before you can use WorkflowCombo. Additionally, if you don't have python installed on your computer, you will need to install that as well. For help in installing pip or python packages, refer to [this](https://packaging.python.org/tutorials/installing-packages/) website. To download python3, follow the directions on the downloads page of the [Python website](https://www.python.org/downloads/).

Once the packages are installed, you can run Workflow Combo by following these steps:
1. **Prepare your files:** Starting by using `<cd>` to enter the location on your computer (refer to [this website](https://www.digitalcitizen.life/command-prompt-how-use-basic-commands) for a refresher on how to use the command line) where you would like to run WorkflowCombo (this is generally where you've downloaded index.py). All your command line tools that you would like to be included in the Workflow should be in the same folder as index.py. Before you run the tool, you will need to look at your Command Line Tools and determine which order they will run in your workflow. Once you have decided the order in which they will run, rename them so they line up in this order. For example, if your first file were named "process_somatic_data.cwl" and your second tool was "compare_to_reference.cwl", you would rename the two files to "01_process_somatic_data.cwl" and "02_compare_to_reference.cwl"
2. **Run the Command Line Tool:** To run the command line tool, enter the following command in the command line: `python3 index.py Name_Of_Your_Workflow.cwl *.cwl`. The first command, "python3" tells the command line to run index.py with python3. The name you provide for your workflow will be used as the workflow ID and the name of the created file. "\*.cwl" will grab all of the command line tools that you've already numnbered. Make sure there are no other cwl files in the location that you are running index.py other than the ones you've numbered. 
3. **Follow the Prompts:** Once you've hit enter, you'll see a number of prompts that come up to help you build your tool. The first prompt will ask you for a label for your Workflow (which is just a brief description of the Workflow you're making). The subsequent prompts will be about the steps of your workflow. Read them carefully so you can match the different sections of the app with the correct parts. 
4. **Double-check the Workflow you Created** Once you've finished following all the prompts of the command line tool, your workflow will have been created!! The file will have been created in the same folder with the rest of your cwl files and index.py. Open up the file and make sure it looks good. If you try running the workflow and it doesn't work, you can tweak the file until it works. Every workflow is different and will require different tweaks.

*Authors: Elizabeth C. Anderson and Dr. Stephen Piccolo (BYU)*
*May 2020*
