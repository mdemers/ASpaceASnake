import os, json, re, csv, glob

# assumes we are iterating over a full download of resources... which I just happen to have right now.

def get_restrictions(writer):
    files = glob.glob("*.json")
    for jsonFile in files:
          res_num = jsonFile.rstrip('.json')
          resource = json.load(open(jsonFile))
          title = resource['display_string']
          ancestor = 'collection'
          publish = resource['publish']
          try:
              restrictions = resource['restrictions_apply']
          except:
              restrictions = "Not found"
          for note in resource['notes']:
            if 'type' in note and note['type'] == 'accessrestrict':
              try:
                end_date = note['rights_restriction']['end']
              except:
                end_date = "NONE"
              for sub in note['subnotes']:
                  writer.writerow({'AO_ID' : res_num, 'Title' : title, 'Published?' : publish, 'Restricted?' : restrictions, 'Note_ID' : note['persistent_id'], 'Note_Type' : note['type'], 'End' : end_date, 'Note_Content': sub['content'] })

def write_notes_csv(csvName):
    fieldnames = ['AO_ID', 'Title', 'Published?', 'Restricted?', 'Note_ID', 'Note_Type', 'End', 'Note_Content']
    with open(csvName, 'w', newline='') as outputFile:
        writer = csv.DictWriter(outputFile, fieldnames=fieldnames)
        writer.writeheader()
        get_restrictions(writer)

write_notes_csv('../object_accessrestrict_notes.csv')
