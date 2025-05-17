# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 10:22:56 2024

@author: Administrator
"""

import os
import re
import argparse

def computeexception(txtpath, idset):
    with open(txtpath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    retrynum = (int)((len(lines) - 2) / 8)
    Tnum = 0
    for i in range(retrynum):
        _id = lines[i * 8 + 5].replace('"', '').replace('id:', '').replace(',', '').strip()
        if i < retrynum - 1 and _id == lines[(i + 1) * 8 + 5]:
            continue
            
        info = lines[i * 8 + 3].replace('"', '').replace('error_info:', '').replace(',', '').strip()
        if ('no such column' in info or 'ambiguous column name' in info or 'no such table' in info) and _id in idset:
            Tnum += 1
    return (Tnum, retrynum)

def compute(txtpath, geoset):
    idset = set()
    enum = 0
    xnum = 0
    rnum = 0
    with open(txtpath, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        m = re.match( r'(?P<id>[a-z]+\d{2}).+\'res\':\s(?P<res>\d),\s\'info\': \'(?P<info>.*)\'', line, re.M|re.I)
        assert(m)
        _id = m.group('id')
        res = m.group('res')
        info = m.group('info')
        if res == '0':
            enum += 1
            if len(info) > 0:
                xnum += 1
            if _id in geoset:
                rnum += 1
        else:
            idset.add(_id)
    #
    return (enum, xnum, rnum, idset)



if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--sdbpath", type=str, default="./sdbdatasets/")
    # parser.add_argument("--resultspath", type=str, default="./experiments/results/")
    # args = parser.parse_args()
    
    # sdbpath = args.sdbpath
    # resultspath = args.resultspath
    sdbs = ['dataset1', 'dataset2']
    dbs = ['ada', 'edu', 'tourism', 'traffic']
    
    sdbpath = './sdbdatasets/'
    resultspath = './experiments/results/'
    logf = open(f'{resultspath}/statistics.txt', 'w', encoding = 'utf-8')
    #
    rangeset = set()
    for sdb in sdbs:
        for db in dbs:
            gsset = set()
            gset = set()
            sset = set()
            geoset = set()
            _dir = f'{sdbpath}{sdb}/{db}/'
            dirs = os.listdir(_dir)
            for _d in dirs:
                if f'QA-{db}' in _d:
                    txtpath = f'{_dir}{_d}'
                    with open(txtpath, 'r', encoding = 'utf-8') as f:
                        lines = f.readlines()
                        assert((len(lines) + 1) % 11 == 0)
                        num = (len(lines) + 1) / 11
                        num = int(num)
                        for i in range(num):
                            label = lines[i * 11 + 0].strip()
                            _id = lines[i * 11 + 9].replace('id:', '').strip()
                            #
                            if 'G' in label and 'S' in label:
                                gsset.add(f'{_id}')
                            elif 'G' in label:
                                gset.add(f'{_id}')
                            elif 'S' in label:
                                sset.add(f'{_id}')
                            if 'Region' in label:
                                geoset.add(f'{_id}')
                                rangeset.add(f'{_id}')
            #
            if db == 'tourism':
                logf.write('sdb:{0} \tDB:{1} \t\tG:{2} \tS:{3} \tGS:{4} \tRegion:{5}\n'.format(sdb, db, len(gset), len(sset), len(gsset), len(geoset)))
            else:
                logf.write('sdb:{0} \tDB:{1} \t\t\tG:{2} \tS:{3} \tGS:{4} \tRegion:{5}\n'.format(sdb, db, len(gset), len(sset), len(gsset), len(geoset)))
    models = ['dail_sql', 'sspa', 'sspa_tips', 'sspa_geo', 'sspa_sdbms']
    nums = [0, 1, 3, 5]
    
    for model in models:
        for sdb in sdbs:
            for num in nums:
                txtpath = f'{resultspath}{model}/{sdb}_ada_edu_shot_{num}/evaluations.txt'
                rae = compute(txtpath, rangeset)
                txtpath = f'{resultspath}{model}/{sdb}_tourism_traffic_shot_{num}/evaluations.txt'
                rtt = compute(txtpath, rangeset)
                enum = rae[0] + rtt[0]
                xnum = rae[1] + rtt[1]
                rnum = rae[2] + rtt[2]
                
                logf.write('model:{0}\tsdb:{1}\t\tshot:{2}\tex:{3:.2f}\twrong:{4}/200\texception:{5}'.format(model, sdb, num, (1 - enum / 200) * 100, enum, xnum))
                logf.write('\tRegion:{0}'.format(34 - rnum))
                
                idset = rae[3].union(rtt[3])
                #
                if model in ['sspa', 'sspa_geo', 'sspa_sdbms']:
                    txtpath = f'{resultspath}{model}/{sdb}_ada_edu_shot_{num}/repetitions.json'
                    rae = computeexception(txtpath, idset)
                    txtpath = f'{resultspath}{model}/{sdb}_tourism_traffic_shot_{num}/repetitions.json'
                    rtt = computeexception(txtpath, idset)
                    Tnum = rae[0] + rtt[0]
                    Trynum = rae[1] + rtt[1]
                    logf.write('\t\tschema-tips:{0}\trepetition:{1}'.format(Tnum, Trynum))
                #
                logf.write('\n')
                logf.flush()
    logf.close()
    print('Finished~')