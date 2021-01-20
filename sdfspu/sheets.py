import datetime
from time import sleep
import os
import logging

import gspread
import gspread.utils
from oauth2client.service_account import ServiceAccountCredentials
# from googleauth.google.oauth2.service_account import Credentials
from sdfspu.csv_data import DataObject

init_scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]
basedir = os.path.abspath(os.path.dirname(__file__))
if '/home/buddhafield' in basedir:
    init_key = '/home/buddhafield/apicred/key_copy.json'
elif '/home/pi' in basedir:
    init_key = '/home/pi/apicred/key_copy.json'
else:
    init_key = '/Users/samuelfreeman/Dropbox/apicred/Buddhafield-a5c4356bb210.json'


class SheetsConnection:
    def __init__(self, api_key=init_key):
        self.scope = init_scope
        self.key = api_key  # set this before .login()
        self.credentials = None  # will be initialised by login()
        self.c = None  # self.c will be the gspread client - use .login()
        self.status_msg = 'Connection Status: Unknown'
        # spaghetti danger, watch out where status things are set
        self.status_ok = False  # use self.update_ok_status(bool)
        self.when_status_updated = datetime.datetime.now()
        self.login()  # connects self.c etc

    def login(self):
        self.status_msg = 'Connection Status: '
        # to do: try . . .
        # self.credentials = ServiceAccountCredentials.from_json_keyfile_name(
        self.credentials = Credentials.from_json_keyfile_name(
            self.key, self.scope)
        self.c = gspread.authorize(self.credentials)
        self.status_msg += 'OK'
        self.update_ok_status(True)
        # to do: . . . except errors

        return self.status_msg
    # end def login()

    def update_ok_status(self, status_ok_bool):
        self.status_ok = status_ok_bool
        self.when_status_updated = datetime.datetime.now()
        print('SheetsConnection.status_ok:',
              status_ok_bool,
              self.when_status_updated)
    # end def update_ok_status

    def time_since_ok_status_update(self):
        return datetime.datetime.now() - self.when_status_updated

# end class SheetsConnection


class SheetMonkey:
    """
    holds data and interacts with worksheets
    """
    def __init__(self, client):
        self.c = client
        self.data = [DataObject()]  # list of DataObjects (can load csv, etc)
        self.row = 1
        self.col = 1
        self.cp_dict = {}  # used when Monkey captures copy of cell value
        self.shift_is_on = False
        self.sid = None  # spreadsheet document id
        self.wks = None  # gspread.Worksheet()

        self.pyprint = True
        self.pydelay = 0.6

    def pypr(self, what_):
        sleep(self.pydelay)
        if self.pyprint:
            print('SheetMonkey:', what_)

    def set_wks(self, worksheet_name_):
        self.pypr('wks "{}" in Sheets doc "{}"'.format(worksheet_name_,
                                                       self.sid))
        # to do: error catching
        self.wks = self.c.open_by_key(self.sid).worksheet(worksheet_name_)

    # cell interaction
    def m_cell(self)->str:
        """
        get current cell location
        :return: string e.g. 'A1'
        """
        return gspread.utils.rowcol_to_a1(self.row, self.col)

    def move_to(self, cell_name_):
        """
        set cell location
        :param cell_name_: e.g. 'A1'
        :return: None
        """
        self.pypr("moving to cell {}".format(cell_name_))
        self.row, self.col = gspread.utils.a1_to_rowcol(cell_name_)

    # Monkey qwertyesque functions
    def shift(self):
        self.shift_is_on = True

    def shift_off(self):
        self.shift_is_on = False

    def tab(self):
        """
        Monkey presses tab key
        :return: None
        """
        nav = -1 if self.shift_is_on else 1
        self.col_nav(nav)

    def shift_tab(self):
        self.shift()
        self.tab()
        self.shift_off()

    def col_nav(self, nav_):
        if isinstance(nav_, int):
            new = self.col + nav_
            self.col = new if new > 0 else 1
        else:
            pass

    def cr(self):
        """
        Monkey presses carriage-return
        :return: None
        """
        nav = -1 if self.shift_is_on else 1
        self.row_nav(nav)
        # self.col = self.cr_col

    def row_nav(self, nav_):
        if isinstance(nav_, int):
            new = self.row + nav_
            self.row = new if new > 0 else 1
        else:
            pass

    def put(self, what_):
        self.pypr('putting "{}" at cell {}'.format(what_, self.m_cell()))
        try:
            self.wks.update_cell(self.row, self.col, what_)
            return 'updated {}: {}'.format(self.m_cell(), what_)
        except gspread.exceptions.APIError as err:
            self.pypr(err)
            return err

    def read(self):
        """
        Monkey reads value of cell
        :return: cell value
        """
        self.pypr('reading cell {}...'.format(self.m_cell()))
        return self.wks.acell(self.m_cell()).value

    def cp(self, _key):
        """
        Monkey captures copy of cell value
        :param _key: key for self.cp_dict
        :return: None
        """
        self.cp_dict[_key] = self.read()

    def pc(self, _key):
        return self.cp_dict[_key]

    def put_pc(self, _key):
        return self.put(self.pc)

    def confirm_cell_values(self, _dict):
        """
        given a dict of cell_name keys with values, check the worksheet
        :param _dict:
        :return: Bool: True if all cell values on wks match the _dict
        """
        self.pypr("start\tconfirm_cell_values : {} items".format(len(_dict)))
        col_was, row_was = self.col, self.row
        for k, v in _dict.items():
            self.move_to(k)
            r = self.read()
            if r != v:
                self.pypr('end False\tunexpected value at {}: {}'.format(k,r))
                self.col, self.row = col_was, row_was
                return False
        self.col, self.row = col_was, row_was
        self.pypr('end True \tcell values confirmed')
        return True


# end class SheetMonkey


if __name__ == '__main__':
    pass
