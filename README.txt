8-19-2024 Andre
It incorporates a rewritten agent_core that will call the LLM up to 2 times. It can make a query and then get the information back and print the response.
Tools have been augmented to return a flag that tells the action-perception loop when to quit
if multiple functions are called it only takes one to tell it to continue.

This branch state_query_tool is based on modular_groq_agent branch
Note a bug was found in Tool_Box.add_tool_mandatory_args
When t_description["function"]["description"] is set it was hardwired and as a result it only worked in that branch where there was just one tool

9-6-2024 Andre
In this Branch we are going to try to use Chain of Thought to deal with multiple gestures. this may require dealing with
responses that contain both text and function calls.
