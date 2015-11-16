__author__ = 'Idan'
import numpy as np
import config.configuration as cfg


class ship:

    minimal_hours_of_dock = cfg.SHIP_MINIMAL_DOCKING_TIME_IN_HOURS

    clas = None
    mmsi = None
    size = None
    width = None
    dist_2_bow= None
    dist_2_stern= None
    dist_2_port= None
    dist_2_starboard = None
    history = []
    df = None

    is_consistant = None
    is_well_measured = None

    top_speed = None
    min_speed = None
    avg_speed = None
    med_tx_freq_inminute = None
    stop_time = []
    stops = []
    time_borders = []
    th = None
    docks = None
    minimal_doc_time_idxs_list = []

    def __init__(self, df, verbose = True  ):
        '''
        :param df: the ais record of the ship
        :return: a ship class initialized with mmsi,
        '''
        self.df = df.loc[:, ['Time', 'Latitude', 'Longitude', 'Speed', 'Heading']]
        self.mmsi = np.array( df['MMSI']) [0]
        self.clas = np.array(df['Class'])[0]
        self.size = np.array(df['Size'])[0]
        self.dist_2_bow = np.array(df['DistanceToBow'])[0]
        self.dist_2_stern = np.array( df['DistanceToStern'])[0]
        self.dist_2_port = np.array(df['DistanceToPort'])[0]
        self.dist_2_starboard = np.array(df['DistanceToStarboard'])[0]
        self.validate_df(df, verbose)
        self.process_data()
        self.is_well_measured = self.self_size_test(verbose)

    def process_data(self):
        '''
        speed data,
        stop time : all time where ship speed is 0,
        stops: distinct lang,long and heading data
        '''
        self.top_speed = np.max(self.df['Speed'])
        self.min_speed = np.min(self.df['Speed'])
        self.avg_speed = np.nanmean(self.df['Speed'])
        med_time = np.median(np.diff(self.df['Time']))
        self.med_tx_freq_inminute = med_time / np.timedelta64(1,'m') #med_time.astype('timedelta64[m]')
        stop_time = self.df['Time'][self.df['Speed'] == 0]
        self.stops = self.df[self.df['Time'].isin(stop_time)].loc[:,['Time', 'Latitude', 'Longitude', 'Heading']]
        self.th = np.timedelta64(self.minimal_hours_of_dock,'h')


    def index_time_to_groups(self,mask):
        '''
        returns the indexes of an element distance is greater then th
        # res = []
        # i=1
        # while i < len(arr):
        #     arr[i] - arr[i-1] > th
        #     res.append(i-1)
        # return res
        # starts = [np.diff(arr) > th]
        # stops = [np.diff(arr) < th]
        #
        # for i in range(1,arr):
        #     arr[i]
        # for i, a in enumerate(arr):
        #     acc += a
        #
        on raise ( specifiying the lest side index! )
        #
        '''
        '''
        from a boolian array
        returning a list of tuples specify a start  and a begining of a stop
        these indexs tuples can be translated to time and then to time diffrence
        '''

        res = []
        is_docked = 0
        start_idx, stop_idx = None, None
        for i,is_stopped in enumerate(mask):
            if is_stopped and not is_docked: # raise
                start_idx = i
            if not is_stopped and is_docked:
                stop_idx = i
                res.append((start_idx,stop_idx))
            is_docked = is_stopped
        if is_docked:
            res.append((start_idx, i))
        return res


    def get_time_jumps(self,arr,th):
        '''
        retrive indexes of time jumps
        :param arr:
        :param th:
        :return:
        '''
        '''
        :param arr:
        :param th:
        :return:
        '''
        mask = np.diff(np.array(arr)) > th
        res = []
        for i,ma in enumerate(mask):
            if ma:
                res.append(i)
        return res

    def retrieve_docking_list(self, list_of_tuples, time_array, th):
        '''
        :param list_of_tuples: pairs of start and stop indexes where speed is 0
        :param time_array: the times of each transmission
        :param th: the time diffrence (timediff object) that is considered minimal docking time
        :return:
        a list of tuples of the docking times
        '''
        res=[]
        for pair in list_of_tuples:
            if time_array[ pair[1]] - time_array[ pair[0]] > th:
                res.append(pair)
        return res

    def get_docking_locations(self):
        '''
        :return: res: [the time, location and angle of the apropriate docs
        ['Time', 'Latitude', 'Longitude', 'Heading']
        and
        minimal_doc_time_idxs_list: indexes of rows that represent and filtered location
        stops_indexs:  idexes of starts and stop indexes of time
        '''
        res = []
        stops_indexs = self.index_time_to_groups(np.array(self.df['Speed']) == 0)
        self.minimal_doc_time_idxs_list = self.retrieve_docking_list(stops_indexs, np.array(self.df['Time']), self.th)
        for tup in self.minimal_doc_time_idxs_list:
            res.append(np.array(self.df.loc[:, cfg.DOCK_FIELDS])[tup[0]])
        self.docks = res
        return res, self.minimal_doc_time_idxs_list, stops_indexs


    def validate_df(self, df, verbose, break_if_bad = False):
        self.is_consistant = self.test_consistancy(df, cfg.AIS_CONSTITANCY_TEST , verbose)

    def self_size_test(self,verbose):
        if self.size != self.dist_2_bow + self.dist_2_stern:
            if verbose: print 'Failed test - ship size: reported size is not complient with dist to bow and sern'
            return False
        if self.dist_2_starboard + self.dist_2_port > self.dist_2_bow + self.dist_2_stern:
            if verbose: print 'Failed test - ship size: reported size is not complient with dist to bow and sern'
            return False
        return True

    def test_consistancy(self, df, cols,verbose, rahel_bitha = False):
        inc_cols=[]
        for col in cols:
            if len(df[col].unique()) > 1:
                inc_cols.append(col)
                if verbose and rahel_bitha: print 'Failed test \n -inconsistancy with '+str(col) + ':\nMMSI: '+str(np.array( df['MMSI']) [0])+' count:' + str(df[col].unique())
        if inc_cols:
            if verbose: print 'Failed test -inconsistancy with MMSI: '+str(np.array( df['MMSI']) [0])+' columns::' + str(inc_cols)
            return False
        return True


    def is_any_bigger(self,size):
        if size >= self.size: return True
        if size >= self.dist_2_bow + self.dist_2_stern: return True
        if size >= self.dist_2_port + self.dist_2_starboard: return True
        return False

