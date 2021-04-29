import markovify

# Get raw text as string.
with open("app_module/text_databases/monster_gen/monsters.txt", encoding='utf-8') as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

# Print three randomly-generated sentences of no more than 280 characters
for i in range(15):
    print(text_model.make_sentence(init_state=tuple(["___BEGIN__"] + ["It"])))
    # print(text_model.make_sentence())
