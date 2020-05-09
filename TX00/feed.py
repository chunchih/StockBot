import sys
sys.path.append('strategy')
from strategy.ntype import nType
from strategy.curve import curve
# from strategy.three_in_row import three_in_row
# from strategy.doubPeriod import doubPeriod
import time
from talib import STOCH, MINUS_DI, PLUS_DI

# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# auth_json_path = 'credentials.json'
# gss_scopes = ['https://spreadsheets.google.com/feeds']
#連線
# credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path,gss_scopes)
# gss_client = gspread.authorize(credentials)
#開啟 Google Sheet 資料表
### https://docs.google.com/spreadsheets/d/1ei5HP4JELwenE5ZhOHpegQZ-WeG6Hld-1J65FM82RFI/edit#gid=0
# spreadsheet_key = '1ei5HP4JELwenE5ZhOHpegQZ-WeG6Hld-1J65FM82RFI' 
# sheet = gss_client.open_by_key(spreadsheet_key).sheet1

def put_in_stat(cur_stat, new_stats, stock_name):
    global sheet
    for stat in new_stats:
        if stat not in cur_stat:
            # if len(cur_stat) == 0:
            #     for i in range(1,51,1):
            #         sheet.delete_row(1)
            f = open(stock_name+'-report.txt', 'a')
            f.write(stat+'\n')
            f.close()
            #send_line(stat)
            # sheet.insert_row([stat], len(cur_stat)+1)
            cur_stat.append(stat)
    return cur_stat
    
def feed_stream(infos, pre_stat, stock_name, K=None):
    if 'ntype' in infos:
        K, _ = STOCH(infos['ntype']['price'][:,1], infos['ntype']['price'][:,2], infos['ntype']['price'][:,3])
        DI_MINUS = MINUS_DI(infos['ntype']['price'][:,1], infos['ntype']['price'][:,2], infos['ntype']['price'][:,3])
        DI_PLUS = PLUS_DI(infos['ntype']['price'][:,1], infos['ntype']['price'][:,2], infos['ntype']['price'][:,3])

        ntype_statUp, ntype_statDown = nType(**infos['ntype'])
        # if (K[-1] < 0.1) and (DI_PLUS[-1] >= DI_MINUS[-1]):
        pre_stat = put_in_stat(pre_stat, ntype_statUp, stock_name)    
        # if (K[-1] > 0.9) and (DI_PLUS[-1] <= DI_MINUS[-1]):
        pre_stat = put_in_stat(pre_stat, ntype_statDown, stock_name)
    # if 'thrInRow' in infos:
    #     thr_statUp, thr_statDown = three_in_row(**infos['thrInRow'])
    #     pre_stat = put_in_stat(pre_stat, thr_statUp, stock_name)
    #     pre_stat = put_in_stat(pre_stat, thr_statDown, stock_name)  

    if 'curve' in infos:
        for c in infos['curve']:
            curve_info = curve(**c)
            pre_stat = put_in_stat(pre_stat, curve_info, stock_name)

    return pre_stat
    
