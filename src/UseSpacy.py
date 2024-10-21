import spacy

nlp = spacy.load("./trained_model.spacy")

doc = nlp("RT @Kuffiya3: In a shameful act, the European Union (EU) held the Association Council meeting with Apartheid Israel after ten years of suspension, despite calls to cancel it over the Israeli occupation's crimes against Palestinians.")

print(doc.cats)