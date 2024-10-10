8-19-2024 Andre
It incorporates a rewritten agent_core that will call the LLM up to 2 times. It can make a query and then get the
information back and print the response.
Tools have been augmented to return a flag that tells the action-perception loop when to quit
if multiple functions are called it only takes one to tell it to continue.

This branch state_query_tool is based on modular_groq_agent branch
Note a bug was found in Tool_Box.add_tool_mandatory_args
When t_description["function"]["description"] is set it was hardwired and as a result it only worked in that
branch where there was just one tool

9-6-2024 Andre
In this Branch we are going to try to use Chain of Thought to deal with multiple gestures. this may require dealing with
responses that contain both text and function calls.

9-27-2024 Andre
The tool-calling LLaMA variant will only generate either text or tool calls, but not both in the same response.
Therefore, it does not seem possible to achieve true chain-of-thought reasoning without making multiple calls with
different prompts. One possible approach is to ask it to generate a plan in prose, and then call it again with a
different prompt, instructing it to translate the plan into a set of function calls.

After much trial and error, I’ve found that it is not possible to make this work correctly by prompt engineering alone.
There are always cases where it tries to call an action function before gathering enough information. I have yet to find a way to communicate to it that it should wait for a second invocation of the LLM. Specifically, when a command involves querying the color of one button and then setting the color of one or more other buttons, it sometimes tries to set the color immediately instead of just making the queries.

If I emphasize too much that it should avoid this behavior, it stops making function calls altogether.

Running the Program
Currently, there are a few files worth running. If you run main.py, it will bring up the GUI.
You can hold down F4 to speak, and when you are done, release F4. Once the speech recognition result appears, press F5
to make the system run the command. Pressing F1 will delete the last utterance from the action window.

Known Issues and Limitations
The system is still very basic and needs significant upgrades. Firstly, the speech recognition button (F4)
needs to be held down for an excessive amount of time before you can start speaking, and it must remain held until
recognition is complete. This delay is caused by the way Python handles pseudo-multithreading. A system is called to
gather audio into buffers, and periodically, Python passes these buffers to the code that sends them to the server.
The F4 button controls this process, but since we want to minimize how often this process happens, you must hold it down
for an extended period. Ideally, we would capture a timestamp when F4 is pressed and use that to send only portions of the
first and last buffers to the speech recognizer.

Ideally, pressing F1 should delete the last part of the transcribed text. Users can also type in this window, so F1 should
affect typed text as well, perhaps deleting the last character or word. Once all the text is deleted, pressing F1 should
cause the application to undo the last action. This will require implementing an undo stack. Having undo functionality is
critical for any serious application, especially those that rely on perceptual input such as speech recognition, natural
language, and gesture interpretation.

It would also be ideal for users to press F4 and F5 simultaneously if issuing a short command they wish to execute
immediately.

The file called one_step_tests is designed for testing prompts that require multiple steps. It allows you to experiment
with different prompts and user commands, but it does not make a second call. There are capabilities to verify whether the
correct function calls are made and ensure that incorrect ones are not, but it does not actually execute any function
calls.

The file called agent_8_15_modular_1 contains the actual agent that the GUI uses. However, if you run this file directly,
it will invoke some offline tests. Note that one prompt is used for both these offline tests and the GUI, while a different
instruction section of the prompt is used by one_step_tests. The offline tests invoked by agent_8_15_modular_1 will run
all the functions, and when run in offline mode, it will make a follow-up call to the LLM, just as it would when running
the full GUI.

Some potential experiments that could be run include:

Giving the LLM a tool to output text as a debugging step:
This would allow the LLM to express its intermediate thoughts using chain-of-thought reasoning through a tool call.

Providing a tool for requesting an additional invocation of the LLM: This would allow the LLM to request another instance
when more information is needed.

Explaining how to pipe information from one tool to another: There may be a way to implement a cue or stack system,
but one would need to explain this in the prompt for the LLM to understand.

Having the LLM generate Python code: This could enable the LLM to write programs that connect information acquisition
tools with tools for using that information.

Making multiple LLM calls in parallel with different instructions: One set of calls could handle simple questions,
another could handle simple actions, and a third could focus on gathering the information necessary for
two-step interactions.

Adding more examples to address failures: Each time the system encounters a shortfall, more examples could be added.
To make this scalable, it would be worth exploring if RAG (retrieval-augmented generation) could bring up relevant
examples for different commands.

Testing generalization: It would be interesting to see if the current prompt works when adding tools for changing the size
of buttons or labeling them. Additionally, what further instructions, if any, would be necessary?

Exploring text manipulation: Another experiment could involve seeing if the system can handle more complex examples where
the LLM performs text manipulation.

10-9-2024 Andre
open AI brance
This branch lets you run the one_step_tests using an Open Ai model it may have broken all the other runtimes though.