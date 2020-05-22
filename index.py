#! /usr/bin/env python3

import cutie  # for providing options on the command line
import sys  # for getting arguments and ending the program early
import os  # read existing cwl files
import cwlgen  # easily build new workflow
import yaml  # read existing cwl files
import inquirer  # ask questions on the command line


def main():
    workflowName = sys.argv[1]
    listOfNames = sys.argv[2:]

    questions = [
        inquirer.Text('label', message="Please provide some information about the workflow you are creating")
    ]
    answers = inquirer.prompt(questions)

    # Initialize the tool we want to build
    cwl_tool = cwlgen.Workflow(workflow_id=os.path.splitext(workflowName)[0],
                               label=answers['label'],
                               cwl_version='v1.1')

    # Parse CLT tools which were provided on the command line to get a list of inputs and outputs
    CLT_Inputs = {}
    CLT_Outputs = {}
    for i in listOfNames:
        with open(os.path.abspath(i), 'r') as cwl_file:
            cwl_dict = yaml.safe_load(cwl_file)
            try:
                if not isinstance(cwl_dict.get('inputs'), dict) or not isinstance(cwl_dict.get('outputs'), dict):
                    print("Your CWL files are not all of the same format. Please use ToolJig to make sure they all"
                          " have the same format.")
                    sys.exit()
                else:
                    CLT_Inputs[i] = cwl_dict['inputs']
                    CLT_Outputs[i] = cwl_dict['outputs']
            except AttributeError:
                pass

    # Declare first step
    step = cwlgen.workflow.WorkflowStep(step_id=os.path.splitext(listOfNames[0])[0],
                                        run=listOfNames[0])

    # Parse the inputs of the first file to save as Workflow inputs
    workflowInputs = []
    for item in CLT_Inputs[listOfNames[0]]:
        input_Info = cwlgen.workflow.InputParameter(param_id=item,
                                                    label=CLT_Inputs[listOfNames[0]][item].get('label'),
                                                    doc=CLT_Inputs[listOfNames[0]][item].get('doc'),
                                                    param_type=CLT_Inputs[listOfNames[0]][item].get('type'))
        cwl_tool.inputs.append(input_Info)
        idToShow = {'ID': item, 'Label': CLT_Inputs[listOfNames[0]][item].get('label'),
                    'Type': CLT_Inputs[listOfNames[0]][item].get('type')}
        workflowInputs.append(idToShow)
        step_inputs = cwlgen.WorkflowStepInput(input_id=item,
                                               source=item)
        step.inputs.append(step_inputs)

    # Get outputs of first step and append it to the whole workflow
    for y in CLT_Outputs[listOfNames[0]]:
        step_outputs = cwlgen.WorkflowStepOutput(output_id=y)
        step.out.append(step_outputs)
    cwl_tool.steps.append(step)

    # LARGE LOOP: Make the steps and designate how inputs and outputs fit together -------------------------------------
    for i in range(0, len(listOfNames)):
        # Get outputs from "i" step that are of the type Directory or File
        prevStepOutputs = CLT_Outputs[listOfNames[i]]
        importantOutputs = []
        for j in prevStepOutputs:
            idToAdd = {'id': j}
            idToAdd.update(prevStepOutputs[j])
            importantOutputs.append(idToAdd)

        # Get inputs from the "i+1" step that are of type Directory or File
        nextInputs = []
        importantInputs = []
        try:
            nextInputs = CLT_Inputs[listOfNames[i + 1]]
            step = cwlgen.workflow.WorkflowStep(step_id=os.path.splitext(listOfNames[i + 1])[0],
                                                run=listOfNames[i + 1])
        except:
            for x in importantOutputs:
                output = cwlgen.workflow.WorkflowOutputParameter(param_id=x.get('id'),
                                                                 doc=x.get('doc'),
                                                                 param_type=x.get('doc'),
                                                                 output_source=os.path.splitext(listOfNames[i])[0])
                cwl_tool.outputs.append(output)

        for k in nextInputs:
            if nextInputs[k]['type'] == 'File' or nextInputs[k]['type'] == 'Directory':
                idToAdd = {'id': k}
                idToAdd.update(nextInputs[k])
                importantInputs.append(idToAdd)

        # Logic for matching inputs and outputs
        if len(importantInputs) == len(importantOutputs) and len(importantInputs) == 1:
            step_inputs = cwlgen.WorkflowStepInput(input_id=importantOutputs[0].get('id'),
                                                   source=listOfNames[i] + "/" + importantOutputs[0].get('id'))
            step.inputs.append(step_inputs)
        elif len(importantInputs) != len(importantOutputs) or len(importantInputs) != 1 or len(importantOutputs) != 1:
            for m in importantInputs:
                # Declare variables ----------------------------------------------
                first_index = 0
                externalInputToName = 'It is an external input that has yet to be referenced'
                previousOutput = 'It is the output of the workflow, but not the most recently previous step'

                # Provide options ----------------------------------------------
                print("Input ", importantInputs.index(m) + 1, "/", len(importantInputs), "of Command Line File ",
                      i + 1, "/", len(listOfNames))
                print("Your inputs and outputs don't match. Please specify where this input should be retrieved from:",
                      m)
                print("")
                options = ['It is the output of the previous step:']
                for t in importantOutputs:
                    options.append(t)
                    first_index = first_index + 1
                if cwl_tool.inputs:
                    options.append('It is an external input that already exists:')
                    for y in workflowInputs:
                        options.append(y)
                    captions = [0, first_index + 1, first_index + len(cwl_tool.inputs) + 2]
                else:
                    captions = [0, first_index + 1]  # This gets the first line and "other"
                options.append('Other')
                options.append(externalInputToName)
                options.append(previousOutput)
                selection = options[cutie.select(options, caption_indices=captions)]

                # Logic for selection ----------------------------------------------
                if selection == externalInputToName:
                    questions = [
                        inquirer.Text('newID', message="What is the ID of the new input?"),
                        inquirer.Text('newLabel', message="What is the label of the new input?")
                    ]
                    answers = inquirer.prompt(questions)
                    # add it as a master input
                    input_Info = cwlgen.workflow.InputParameter(param_id=answers.get('newID'),
                                                                label=answers.get('newLabel'),
                                                                param_type=m.get('type'))
                    cwl_tool.inputs.append(input_Info)
                    idToShow = {'ID': answers.get('newID'), 'Label': answers.get('newLabel'), 'Type': m.get('type')}
                    workflowInputs.append(idToShow)
                    # add it as a step input
                    step_inputs = cwlgen.WorkflowStepInput(input_id=answers.get('newID'), source=answers.get('newID'))
                elif selection == previousOutput:
                    print("\nPlease select which previous output corresponds to your input:")
                    listOfAllOutputs = []
                    for o in range(0, i + 1):
                        for output in CLT_Outputs.get(listOfNames[o]):
                            toAdd = {'ID': output, 'From step': listOfNames[o]}
                            toAdd.update(CLT_Outputs.get(listOfNames[o])[output])
                            listOfAllOutputs.append(toAdd)
                    selection = listOfAllOutputs[cutie.select(listOfAllOutputs)]
                    step_inputs = cwlgen.WorkflowStepInput(input_id=selection['ID'], source=selection['From step'] +
                                                                                            "/" + selection['ID'])
                elif selection in workflowInputs:
                    print(selection)
                    step_inputs = cwlgen.WorkflowStepInput(input_id=selection.get('ID'), source=selection.get('ID'))
                else:
                    step_inputs = cwlgen.WorkflowStepInput(input_id=m.get('id'),
                                                           source=listOfNames[i] + "/" + selection.get('id'))
                step.inputs.append(step_inputs)

        try:
            for y in CLT_Outputs[listOfNames[i + 1]]:
                step_outputs = cwlgen.WorkflowStepOutput(output_id=y)
                step.out.append(step_outputs)
        except:
            pass
        cwl_tool.steps.append(step)
        cwl_tool.export()

    cwl_tool.export(workflowName)
    #TODO The one logic I didn't work into this command line tool is that sometimes there is a step output that is also 
    # considered a "final state" output, but that isn't reflected in the output section of the workflow yet


if __name__ == '__main__':
    main()
