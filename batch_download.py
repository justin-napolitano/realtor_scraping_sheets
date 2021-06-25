from pprint import pprint

def batch_download(sheet_properties: dict):
    
    #pprint(dictionary)

    for spreadsheet_key, spreadsheet_properties in sheet_properties.items():
        
        #pprint(spreadsheet_value)
        #spreasheet_list = []
        #spreadsheet_id = spreadsheet['spreadsheetID']
        #request = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, ranges=A0:, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        
        #print(end_column)
        for data_sheet in spreadsheet_value['sheets']:
                pprint(data_sheet)