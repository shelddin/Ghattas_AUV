#this is just passing through for now mode specific configurations will be added in the future


mode_configs={
'full': {'colors' : ['red','green','black','yellow','orange'] },
'path': {'colors' : ['orange']},
'gate': {'colors' : ['red','black']}
}


def mode_selector(mode):
    return mode_configs.get(mode, 'invalid mode selected')
