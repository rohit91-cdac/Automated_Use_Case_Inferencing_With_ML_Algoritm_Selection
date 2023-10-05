import spacy

nlp = spacy.load("en_core_web_lg")
doc = nlp("With the same streamlined design that's been effortlessly cool for decades you'll look fresh with every step.")

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

for token in doc:
    if token.pos_ in ('ADJ', 'NOUN') and not token.is_stop and token.dep_ not in ("pobj", "attr", "amod"):
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)