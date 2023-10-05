"""
This script intends to generate sample
Use-Cases from the QA generated through
Semantic feature selection.
@TODO
Use BERT/Transformers to do intent modelling
"""
import os

from bert import Ner
import pandas as pd
import random
import spacy

# output = model.predict("The Adicolor Classics 3-Stripes Windbreaker is the best jacket for crisp winter mornings and long commutes in the city.")
# print(output)


class UseCaseTemplates:

    def __init__(self, named_entity):
        self.named_entity = named_entity
        self.templates = [
            (f"Recommend products similar to  {self.named_entity}", "K_Means"),
            (f"Forecast the sales of the product {self.named_entity} for next quarter", "LSTM"),
            (f"Generate catalogue of similar type of products {self.named_entity}", "DBSCAN"),
            (f"Project the price of product {self.named_entity} for next quarter", "ARIMA"),
            (f"Predict the popularity of the product {self.named_entity} for next quarter", "XgBoost"),
            (f"Do Market Basket Analysis for the product {self.named_entity}", "AssociativeLearning")
        ]


class Use_Case_Generator:

    def __init__(self, dataframe: pd.DataFrame, model):
        self.qa_df = dataframe
        self.model = model
        self.answer_priority_1_list = []
        self.answer_priority_2_list = []
        self.answer_priority_3_list = []
        self.nlp = spacy.load("en_core_web_lg")

    def parse_answer_from_df(self):
        for each in self.qa_df:
            if str(each) == 'QA_1':
                self.answer_priority_1_list = list(map(lambda x: eval(x)[1]['answer'], list(self.qa_df[each])))
            elif str(each) == 'QA_2':
                self.answer_priority_2_list = list(map(lambda x: eval(x)[1]['answer'], list(self.qa_df[each])))
            elif str(each) == 'QA_3':
                self.answer_priority_3_list = list(map(lambda x: eval(x)[1]['answer'], list(self.qa_df[each])))

    def get_noun_entities(self):
        def pos_token_analyzer(sentence):
            doc = self.nlp(sentence)
            token_container = []
            for token in doc:
                if token.pos_ in ('ADJ', 'NOUN') and not token.is_stop and token.dep_ not in ("pobj", "attr", "amod", "acomp"):
                    # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                    #       token.shape_, token.is_alpha, token.is_stop)
                    token_container.append(token.text)
                print(' '.join(token_container))
            return ' '.join(token_container)
        generate_pos_words = [list(map(lambda x: pos_token_analyzer(x), each_priority))
                              for each_priority in [self.answer_priority_1_list, self.answer_priority_2_list, self.answer_priority_3_list]]
        map_index = list(map(lambda x: dict(enumerate(x)), generate_pos_words))
        print(map_index)
        generate_pos_index_filter = [{k: v for k, v in each_priority.items() if len(v.split()) > 1}
                                     for each_priority in map_index]

        print(generate_pos_index_filter)
        print([self.answer_priority_1_list, self.answer_priority_2_list, self.answer_priority_3_list])
        return generate_pos_index_filter

    def generate_predictive_model_use_case(self, pos_words_list):
        random.seed()
        final_set_words = set()
        priority_count = 0
        print("Generating NER entity for each priority Answers\n")
        for each_priority in [self.answer_priority_1_list, self.answer_priority_2_list, self.answer_priority_3_list]:
            gen_ner_component = list(map(lambda x: self.model.predict(x), each_priority))
            print(gen_ner_component)

            filter_entity_tags = [list(filter(lambda x: '-' in x['tag'] and float(x['confidence']) > 0.80, each_answer))
                                  for each_answer in gen_ner_component]
            # print(filter_entity_tags)
            get_entity_words = [list(map(lambda x: x['word'] if 'word' in x else [], each_ner))
                                for each_ner in filter_entity_tags]
            # print(get_entity_words)

            form_entity_dict = dict(enumerate(list(map(lambda x: ' '.join(x), get_entity_words))))
            print(form_entity_dict)

            for ner, pos in zip(form_entity_dict, pos_words_list[priority_count]):
                full_entity = form_entity_dict[ner] + " " + pos_words_list[priority_count][pos]
                print(full_entity)
                final_set_words.add(full_entity.replace("home", "").replace("day", "").replace("temperature", "").strip())
        return final_set_words

    def create_use_cases(self, entity_list):
        use_case_list = []
        for each_entity in entity_list:
            use_case_template = UseCaseTemplates(each_entity)
            use_case_list.extend(use_case_template.templates)
        return use_case_list


if __name__ == '__main__':
    print("\n")
    print("Initializing Code to Generate NER\n")
    print("[*]\n")
    print("Initializing NER class Initialization\n")
    print("[*]\n")
    model = Ner("out_large/")
    print("Reading Question Answer generated per Topic\n")
    print("[*]\n")
    qa_df = pd.read_csv("QA_Per_Topic.csv")
    print("\n")
    print(qa_df.head())
    print("\n")
    output = model.predict(
        "The Adicolor Classics 3-Stripes Windbreaker is the best jacket for crisp winter mornings and long commutes in the city."
    )
    print(output)
    use_case_gen_obj = Use_Case_Generator(dataframe=qa_df, model=model)
    use_case_gen_obj.parse_answer_from_df()
    get_pos_words_list = use_case_gen_obj.get_noun_entities()
    final_entity_set = use_case_gen_obj.generate_predictive_model_use_case(get_pos_words_list)
    get_use_cases = use_case_gen_obj.create_use_cases(final_entity_set)
    print(list(get_use_cases))
    use_case_df = pd.DataFrame(get_use_cases, columns=['Use_Cases', 'ML_Algo'])
    use_case_df.to_csv("Final_Use_Case_List_With_Algo_Label.csv")



