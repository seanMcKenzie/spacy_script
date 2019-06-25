import spacy
import pandas as pd
import Name

data = pd.read_csv('trusts.csv')

trusts = data.loc[:, ['ID', 'Name', 'Address']]

nlp = spacy.load("en_core_web_sm")

first_names = []

middle_names = []

last_names = []

lead_addresses = []

app_ids = []

org_names = []

original_names = []


def get_name(text):
    text = text.lower()
    text = text.replace('the', '')
    text = text.replace('irrevocable', '')
    text = text.replace('revocable', '')
    text = text.replace('trust', '')
    text = text.replace('joint', '')
    text = text.replace('living', '')
    text = text.replace('family', '')
    text = text.replace('amended', '')
    text = text.replace('holdings', '')
    text = text.replace('testamentary', '')
    text = text.replace('descendents', '')
    text = text.replace('descendants', '')
    text = text.replace('exemption', '')
    text = text.replace('exempt', '')
    text = text.replace('residuary', '')
    text = text.replace('estate', '')
    text = text.replace('mineral', '')
    text = text.replace('royalty', '')
    text = text.replace('interest', '')
    text = text.replace('real', '')
    text = text.replace('working', '')

    return text


def replace_ampersand(text):
    if text.find('&') != -1:
        text = text.replace('&', 'and')
    return text


def get_substring_of_trust_title(text):
    if text.lower().find('trustee') != -1:
        trustee_index = text.lower().find('trustee')
        if not text.lower().endswith('trustee'):
            space_index = text.rfind(' ', 0, trustee_index)
            text = text[:space_index]
        else:
            comma_index = text.find(',')
            text = text[comma_index + 1:trustee_index]
    return text


print('******************** PROCESSING ***************************')
for index, row in trusts.iterrows():
    original_name = row['Name']
    #if name == 'Bank of America, N.A (James Harry Johnson Trust "B" for the benefit of James Corey Toombs c/o Bank of America, N.A.)':
        #print('******************** DEBUG ***************************')
    app_id = row['ID']
    address = row['Address']
    open_paren_index = original_name.find('(')
    if open_paren_index != -1 and original_name[0:open_paren_index].lower().find('trustee') == -1:
        name = original_name[:open_paren_index]
        # extracted_names.append(name_sub_a)
    else:
        name = replace_ampersand(original_name)
        name = get_substring_of_trust_title(original_name)
    doc = nlp(name)
    for ent in doc.ents:
        if ent.label_ == 'PERSON' and ent.text.lower().find('successor') == -1:
            if ent.text.lower().endswith('trust'):
                stripped_name = get_name(ent.text)

                name_obj = Name.Name(stripped_name, True)

                last_names.append(name_obj.last_name)
                first_names.append(name_obj.first_name)
                middle_names.append(name_obj.middle_name)
                app_ids.append(app_id)
                lead_addresses.append(address)
                original_names.append(original_name)
                org_names.append('')
            # names = names + stripped_name + ' - '
            else:
                # names = names + ent.text + ' - '
                name_obj = Name.Name(ent.text, True)

                last_names.append(name_obj.last_name)
                first_names.append(name_obj.first_name)
                middle_names.append(name_obj.middle_name)
                app_ids.append(app_id)
                lead_addresses.append(address)
                original_names.append(original_name)
                org_names.append('')
        if ent.label_ == 'ORG' and ent.text.lower().find('successor') == -1:
            if ent.text.lower().endswith('trust'):
                stripped_name = get_name(ent.text)
                # names = names + stripped_name + ' - '
                app_ids.append(app_id)
                lead_addresses.append(address)
                org_names.append(stripped_name)
                original_names.append(original_name)
                last_names.append('')
                first_names.append('')
                middle_names.append('')
            else:
                # names = names + ent.text + ' - '
                app_ids.append(app_id)
                lead_addresses.append(address)
                original_names.append(original_name)
                org_names.append(ent.text)
                last_names.append('')
                first_names.append('')
                middle_names.append('')
        # extracted_names.append(names)

raw_data = {'app_id': app_ids,
            'address': lead_addresses,
            'original_name': original_names,
            'last_name': last_names,
            'first_name': first_names,
            'middle_name': middle_names,
            'org_name': org_names}

df = pd.DataFrame(raw_data, columns=['app_id', 'address', 'original_name', 'last_name', 'first_name', 'middle_name', 'org_name'])
df.to_csv('extracted_names_test.csv')
#data['Extracted Names'] = extracted_names
#data.to_csv('extracted_names.csv')
