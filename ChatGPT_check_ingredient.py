from openai import OpenAI
import openai


def ChatGPT_check_ingredient(prompt):
    openai.api_key = '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'

    client = OpenAI(
        api_key = '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',
    )

    prompt = str(prompt)
    stream = client.chat.completions.create(
        model='gpt-4',
          messages=[
            {
              'role': 'system',
              'content': "I will give you a list of sublists except for the first element of the list. I want you to immediately break this down into two parts, one with the allergy which is the first element of the list I provided you, this will be a list of allergies that is the ingredient someone is allergic to, call this ALLERGYNAME. For the second part, go to the second list of the list I provided, call this list the INGREDIENT LIST. Note that even if one of the sublists has multiple elements in them, still consider the whole sublist as one index. For example, if I gave you the list of [ ['nuts', ‘seafood’], [['chestnut', 'broccoli'], ['oil'], ['tuna'], ['fish'], ['peanut butter', 'beef'] , ['beans'], ['oil'], ['oil'], ['oil']]]. 'nuts' and ‘seafood’ are the ALLERGYNAME, ['chestnut', 'broccoli'] is considered as one subset, they have the index of 0. ['peanut butter', 'beef'] is the 4th sublist, therefore it will have an index of 3. The INGREDIENT LIST, contains a set of ingredients in the value of strings. I want you to output the index of all of the lists that have ingredients that are harmful to eat for someone who is allergic to the ALLERGYNAME. For example, someone won’t be able to eat ‘chestnut’, ‘tuna’, ‘fish’, and ‘peanut butter’ because they are harmful to people who are allergic to ‘seafood’ and ‘nuts’, therefore outputing: [0, 2, 3, 4] — a list of the indexes of the sublists that contains dangerous ingredients. For example, the output “0” indicates the sublist of ['chestnut', 'broccoli'] and the output “4” indicates the sublist of ['peanut butter', 'beef']. In the process of making the decision, try to dive into the causes of the allergies to assist you in making your decision, look for common foods that cause allergic reactions for the given allergy. Your output MUST BE ONLY ONE LIST, NO EXPLANATION NEEDED. If any general terms like 'animal products' are used, you are to ensure that everything that came from an animal, is also filtered out. These examples include: eggs, seafood, or any animal-derived products like cheese."
            },
            {
              'role': 'user',
              'content': prompt
            }
          ],
          stream = True,
          temperature=0.8,
          max_tokens=64,
          top_p=1
    )
    output = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            output += (chunk.choices[0].delta.content)
    return(output)
