# Dictionary of Basic Client Information
import pandas as pd
clients_info = {'arctos':{
    'official_name': "Arctos",
    'id':"6",
    'abbrev':"arc"
    },
    'cat':{
    'official_name':"CAT",
    'id':"8",
    'abbrev':"cat"
    },
    'ncc':{
    'official_name':"NCC",
    'id':"9",
    'abbrev':"ncc"
    },
    'el polmar':{
    'official_name':"El Polmar",
    'id':"10",
    'abbrev':"elpol"
    },
    }

clients_df = pd.DataFrame.from_dict(clients_info).T
# Get client name, given an ID
# ID = '6'
# clientName = clients_dict.index[clients_dict['id']==ID].item()