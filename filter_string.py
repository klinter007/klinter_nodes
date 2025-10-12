"""Node for filtering strings based on a wordlist in ComfyUI."""

from comfy_api.latest import io

class FilterString(io.ComfyNode):
    """Node for checking if a given string appears in a list of strings and returning a filter word if true."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the filtering node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="filter",
            display_name="Filter String - klinter",
            category="klinter",
            description="Check if a string exists in a wordlist and return either the safeword or original string",
            inputs=[
                io.String.Input("in_question", default="", multiline=False, force_input=True),
                io.String.Input("wordlist", default="", multiline=True, force_input=True),
                io.String.Input("safeword", default="", multiline=True, force_input=True),
            ],
            outputs=[
                io.String.Output()
            ]
        )

    @classmethod
    def execute(cls, in_question: str, wordlist: str, safeword: str) -> io.NodeOutput:
        """Check if a string exists in a wordlist and return either the safeword or original string.
        
        Args:
            in_question: The string to search for
            wordlist: Space-separated list of words to search in
            safeword: Word to return if in_question is found in wordlist
            
        Returns:
            io.NodeOutput: Either safeword or in_question depending on if in_question is in wordlist
        """
        try:
            # Convert the wordlist string into a list of words
            words = wordlist.split()
            
            # Check if in_question is in the list of words
            result = safeword if in_question in words else in_question
            return io.NodeOutput(result)
        except Exception as e:
            print(f"Error in filter_string: {str(e)}")
            return io.NodeOutput(in_question)

# Register the node
NODE_CLASS_MAPPINGS = {
    "filter": FilterString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "filter": "Filter String - klinter"
}

# Export the class
__all__ = ['FilterString']
