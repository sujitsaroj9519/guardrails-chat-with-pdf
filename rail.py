# Download pdf and load it

import guardrails as gd
from rich import print

content = gd.docs_utils.read_pdf("chase_card_agreement.pdf")

print(f"Chase Credit Card Document:\n\n{content[:275]}\n...")


# Creat rail
rail_str = """
<rail version="0.1">

<output>

    <list name="fees" description="What fees and charges are associated with my account?">
        <object>
            <integer name="index" format="1-indexed" />
            <string name="name" format="lower-case; two-words" on-fail-lower-case="fix" on-fail-two-words="reask" />
            <string name="explanation" format="one-line" />
            <float name="value" format="percentage"/>
        </object>
    </list>
    <object name="interest_rates" required="false" description="What are the interest rates offered by the bank on savings and checking accounts, loans, and credit products?" />
</output>


<instructions>
You are a helpful assistant only capable of communicating with valid JSON, and no other text.

${gr.json_suffix_prompt_examples}
</instructions>


<prompt>
Given the following document, answer the following questions. If the answer doesn't exist in the document, enter 
`null`.

${document}

Extract information from this document and return a JSON that follows the correct schema.

${gr.xml_prefix_prompt}

${output_schema}
</prompt>

</rail>
"""


##Create a guard object

guard = gd.Guard.from_rail_string(rail_str)



##Wrapping LLM APi Call
import openai
# openai.api_key = "YOUR_OPENAI_KEY"

raw_llm_response, validated_response, *rest = guard(
    openai.Completion.create,
    prompt_params={"document": content[:6000]},
    max_tokens=2048,
    temperature=0,
)


print(validated_response)


print(guard.history.last.tree)

