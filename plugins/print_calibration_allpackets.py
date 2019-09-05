
def search(data, name):
    if not data:
        return None
    if type(data) is list:
        if type(data[0]) is dict:
            return [element for element in data if element['name'] == name]
        elif type(data[0]) is tuple: 
            return [element for element in data if element[0] == name]
    return None
def get_raw(data, name):
        if type(data[0]) is dict:
            return [int(item['raw'][0]) for item in data if item['name']==name]
        elif type(data[0]) is tuple: 
            return [int(item[1][0]) for item in data if item[0]==name]




def get_calibration_spectra(packet):
    param=packet['parameters']
    search_res=get_nodes(param, 'NIX00159')
    if not search_res:
        return []
    num_struct=int(search_res[0]['raw'][0])
    #number of structure
    cal=search_res[0]['children']
    detectors=get_raw(cal, 'NIXD0155')
    pixels=get_raw(cal, 'NIXD0156')
    spectra=[[int(it['raw'][0]) for it in  item['children']] for item in cal if item['name']=='NIX00146']
    counts=[]
    for e in spectra:
        counts.append(sum(e))
    result=[]
    for i in range(num_struct):
        result.append({'detector':detectors[i],
            'pixel':pixels[i],
            'counts':counts[i],
            'spec':spectra[i]})
    return result

SPID=54124

class Plugin:
    def __init__(self,  packets=[], current_row=0):
        self.packets=packets
        self.current_row=current_row
    def run(self):
        timestamp=[]
        spectra=[]
        print('searching for calibration packets')
        for packet in self.packets:

            spid=0
            try:
                spid=int(packet['header']['SPID'])
            except ValueError:
                #TC 
                continue
            if spid != SPID:
                continue
            spec=get_calibration_spectra(packet)
            spectra.extend(spec)

        tot_num_spec = 0
        for i,spec in enumerate(spectra):
            if spec['counts']>0:
                print('Detector %d Pixel %d, counts: %d '%(spec['detector'], spec['pixel'], spec['counts']))
                tot_num_spec += 1
        print('Total number of non-empty spectra:%d'%tot_num_spec)





        







            
