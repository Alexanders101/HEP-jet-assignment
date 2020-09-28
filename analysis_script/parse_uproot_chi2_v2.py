import uproot
import pandas as pd 
import numpy as np 
from particle_properties_uproot import particle_properties  #import particle properties helper function from particle_properties.py
from jet_properties_uproot import jet_properties  #import jet properties helper function from jet_properties.py
import h5py, os, sys

#Define variable for input/output files

def main(DATA, OUTPUT_FILE):
    SUM_1 = 0
    SUM_2 = 0

    particle = particle_properties(DATA)
    jet = jet_properties(DATA)

    Length = len(particle.event)
    test_length = 100

    PID_W_plus = 24 
    PID_W_minus = -24
    PID_DOWN = 1
    PID_DOWN_VAR = -1
    PID_UP = 2
    PID_UP_BAR = -2
    PID_STRANGE = 3
    PID_STRANGE_BAR = -3
    PID_CHARM = 4
    PID_CHARM_BAR = -4
    PID_BOTTOM = 5
    PID_BOTTOM_BAR = -5
    PID_TOP = 6
    PID_TOP_BAR = -6

    top_idx = np.zeros(len(particle.event))
    top_daughter_idx_1 = np.zeros(len(particle.event))
    top_daughter_pid_1 = np.zeros(len(particle.event))
    top_daughter_idx_2 = np.zeros(len(particle.event))
    top_daughter_pid_2 = np.zeros(len(particle.event))

    top_bar_idx = np.zeros(len(particle.event))
    top_bar_daughter_idx_1 = np.zeros(len(particle.event))
    top_bar_daughter_pid_1 = np.zeros(len(particle.event))
    top_bar_daughter_idx_2 = np.zeros(len(particle.event))
    top_bar_daughter_pid_2 = np.zeros(len(particle.event))

    parton_array = np.zeros([ len(particle.event) , 6, 7])

    #Generate maker for each stage(event selection and jet selection.)
    marker_event = []
    marker_jet = []
    marker_bjet = []

    for i in range(len(particle.event)):
    #for i in range(test_length):
        marker_event.append(0)
        marker_jet.append(np.zeros([len(jet.pt[i])]))
        marker_bjet.append(np.zeros([len(jet.pt[i])]))


    marker_event = np.asanyarray(marker_event, dtype=object)
    marker_jet = np.asanyarray(marker_jet, dtype=object)
    marker_bjet = np.asanyarray(marker_bjet, dtype=object)

    #Mark which jet in each event pass the selection.
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Start jet selection.")
    # print("+------------------------------------------------------------------------------------------------------+")
    for i in range(len(particle.event)):
    #for i in range(test_length):
        for j in range(len(jet.pt[i])):
            if jet.btag[i][j] == 1 and jet.pt[i][j] > 25 and np.abs(jet.eta[i][j]) < 2.5:
                marker_bjet[i][j] = 1 
            else: pass 
        
            if jet.pt[i][j] > 25 and np.abs(jet.eta[i][j]) <= 2.5:
                marker_jet[i][j] = 1
            else: pass 

    for i in range(len(particle.event)):
    #for i in range(test_length):
        if np.sum(marker_jet[i] == 1) >= 6 and np.sum(marker_bjet[i] == 1) >= 2 :
            marker_event[i] = 1 
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Jet selection doen. {0} events has been selected.".format(np.sum(marker_event == 1)))
    # print("+------------------------------------------------------------------------------------------------------+")
    SUM_1 += np.sum(marker_event == 1)
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Recording the kinematics variables of jets in the selected event.")
    # print("+------------------------------------------------------------------------------------------------------+")
    #Record the kinematical variables of jet in the selected event.
    jet_pt = []
    jet_eta = []
    jet_phi = []
    jet_mass = []
    jet_btag = []

    for i in range(len(jet.event)):
    #for i in range(test_length):
        if marker_event[i] == 1:
            jet_pt_tmp = []
            jet_eta_tmp = []
            jet_phi_tmp = []
            jet_mass_tmp = []
            jet_btag_tmp = []
            for j in range(len(jet.pt[i])):
                jet_pt_tmp.append(jet.pt[i][j])
                jet_eta_tmp.append(jet.eta[i][j])
                jet_phi_tmp.append(jet.phi[i][j])
                jet_mass_tmp.append(jet.mass[i][j])
                jet_btag_tmp.append(jet.btag[i][j])
                    
            jet_pt.append(jet_pt_tmp)
            jet_eta.append(jet_eta_tmp)
            jet_phi.append(jet_phi_tmp)
            jet_mass.append(jet_mass_tmp)
            jet_btag.append(jet_btag_tmp)
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Finished to record the kinematics variables of jets in the selected event.")
    # print("+------------------------------------------------------------------------------------------------------+")

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Starting parton tracing and looking for its daughter.")
    # print("+------------------------------------------------------------------------------------------------------+")
    #Particle tracing and daughter finding section
    def shift_particle_tracing(dataset, PID_d, idx):
        if (dataset.iloc[idx,6] == PID_d):
            return dataset.iloc[idx,4]

    def particle_tracing(dataset, PID, STATUS):

        for i in range(len(dataset)):
            if(dataset.iloc[i,1] == STATUS and dataset.iloc[i,6] == PID ): 
                daughter_index = int(dataset.iloc[i,0])
        if( dataset.iloc[daughter_index,6] == PID ):
            shifted_particle_index = dataset.iloc[daughter_index, 4]


        while dataset.iloc[shifted_particle_index,6] == PID:
                init_shifted_particle_index = shifted_particle_index
                shifted_particle_index = shift_particle_tracing(dataset, PID, init_shifted_particle_index)       

        dauthter_idx_1 = dataset.iloc[init_shifted_particle_index, 4]
        daughter_pid_1 = dataset.iloc[dauthter_idx_1, 6]

        dauthter_idx_2 = dataset.iloc[init_shifted_particle_index, 5]
        daughter_pid_2 = dataset.iloc[dauthter_idx_2, 6]

        return init_shifted_particle_index, dauthter_idx_1, daughter_pid_1, dauthter_idx_2, daughter_pid_2

    for i in range(len(particle.event)):
    #for i in range(test_length):
        if marker_event[i] == 1:
            #print("+------------------------------------------------------------------------------------------------------+")
            #print("Start parsing event : {0}\nStart to trace top quark and find its daughters.".format(i))
            top_idx[i], top_daughter_idx_1[i], top_daughter_pid_1[i], top_daughter_idx_2[i], top_daughter_pid_2[i] = particle_tracing(particle.dataframelize(i), PID_TOP, 22)
            #print("+------------------------------------------------------~-----------------------------------------------+")
            #print("Start to find top_bar quark and its daughters.")
            top_bar_idx[i], top_bar_daughter_idx_1[i], top_bar_daughter_pid_1[i], top_bar_daughter_idx_2[i], top_bar_daughter_pid_2[i] = particle_tracing(particle.dataframelize(i), PID_TOP_BAR, 22)
            #print("+------------------------------------------------------------------------------------------------------+")

    #tracing the daughters
    #Input two daughter of top/top_bar and find their daughter
    def quark_finder(dataset, mother_idx_1, mother_idx_2):
        
        #Specific two daughter of top
        def W_b_specifier(dataset, input_1_idx, input_2_idx):
            if dataset.iloc[int(input_1_idx),6] == PID_W_plus or dataset.iloc[int(input_1_idx),6] == PID_W_minus :
                return int(input_1_idx), int(dataset.iloc[int(input_1_idx),6]), int(input_2_idx)
            elif dataset.iloc[int(input_1_idx),6] == PID_BOTTOM or dataset.iloc[int(input_1_idx),6] == PID_BOTTOM_BAR :
                return  int(input_2_idx), int(dataset.iloc[int(input_1_idx),6]), int(input_1_idx)
            else :
                pass
                #print("Please check your data.")
        
        W_boson_idx, mother_pid, b_quark_idx = W_b_specifier(dataset, mother_idx_1, mother_idx_2)
        
        #Find the two daughters of boson
        
        daughter_1_idx = dataset.iloc[W_boson_idx, 4]
        daughter_1_pid = dataset.iloc[daughter_1_idx, 6]
        daughter_2_idx = dataset.iloc[W_boson_idx, 5]
        daughter_2_pid = dataset.iloc[daughter_2_idx, 6]

        
        if daughter_1_pid == mother_pid or daughter_2_pid == mother_pid:

            init_idx = W_boson_idx
            daughter_pid = daughter_1_pid
            if daughter_2_pid == mother_pid:
                daughter_pid = daughter_2_pid
            while daughter_pid == mother_pid :
                daughter_1_idx = dataset.iloc[int(init_idx), 4]
                daughter_2_idx = dataset.iloc[int(init_idx), 5]

                daughter_1_pid = dataset.iloc[int(daughter_1_idx), 6]
                daughter_2_pid = dataset.iloc[int(daughter_2_idx), 6]

                daughter_pid = daughter_1_pid
                init_idx = daughter_1_idx
                if daughter_2_pid == mother_pid:
                    daughter_pid = daughter_2_pid
                    init_idx = daughter_2_idx
        
        #print("Found daughter 1 index: {0}, PID: {1}.\nFound daughter 2 index: {2}, PID: {3}".format(daughter_1_idx, daughter_1_pid, daughter_2_idx, daughter_2_pid))
        return  b_quark_idx, daughter_1_idx, daughter_2_idx

    for i in range(len(particle.event)):
    #for i in range(test_length):
        if marker_event[i] == 1 :
            #print("+------------------------------------------------------------------------------------------------------+")
            #print("Start parsing event : {0}\nStart to find top quark's daughters.".format(i))
            parton_array[i][0][0], parton_array[i][1][0], parton_array[i][2][0] = quark_finder(particle.dataframelize(i), top_daughter_idx_1[i], top_daughter_idx_2[i])
            #print("+------------------------------------------------------~-----------------------------------------------+")
            #print("Start to find top_bar quark's daughters.")
            parton_array[i][3][0], parton_array[i][4][0], parton_array[i][5][0], = quark_finder(particle.dataframelize(i), top_bar_daughter_idx_1[i], top_bar_daughter_idx_2[i])
            #print("+------------------------------------------------------------------------------------------------------+")
        elif marker_event[i] == 0 :
            parton_array[i] = 'Nan'
        else: pass
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Parton tracing section complete. The daughter of W+/W- and bbbar has been found.")
    # print("+------------------------------------------------------------------------------------------------------+")

    # Barcode system
    # t t~ W+ W- b b~ 
    # 0 0  0  0  0 0

    # i.e.
    # col 3 = 100010 
    # col 5 = 101000
    # col 6 = 101000
    # col 8 = 010100
    # col 10= 010001
    # col 11= 010001

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Recording the kinematics variables of partons in the selected event.")
    # print("+------------------------------------------------------------------------------------------------------+")
    parton_pdgid = []
    parton_barcode = []
    parton_pt = []
    parton_eta = []
    parton_phi = []
    parton_mass = []

    barcode = np.array([34, 40, 40, 17, 20, 20])
    for i in range(len(particle.event)):
    #for i in range(test_length):
        if marker_event[i] == 1:
            _parton_pdgid = []
            _parton_barcode = []
            _parton_pt = []
            _parton_eta = []
            _parton_phi = []
            _parton_mass = []
            for j in range(0,6):
                dataset = particle.dataframelize(i)

                _parton_pdgid.append(dataset.iloc[int(parton_array[i][j][0]), 6])
                _parton_barcode.append(barcode[j])
                _parton_pt.append(dataset.iloc[int(parton_array[i][j][0]), 7])
                _parton_eta.append(dataset.iloc[int(parton_array[i][j][0]), 8])
                _parton_phi.append(dataset.iloc[int(parton_array[i][j][0]), 9])
                _parton_mass.append(dataset.iloc[int(parton_array[i][j][0]), 10])


            parton_pdgid.append(_parton_pdgid)
            parton_barcode.append(_parton_barcode)
            parton_pt.append(_parton_pt)
            parton_eta.append(_parton_eta)
            parton_phi.append(_parton_phi)
            parton_mass.append(_parton_mass)
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Finished to record the kinematics variables of partons in the selected event.")
    # print("+------------------------------------------------------------------------------------------------------+")

    #Define Chi square minimizer
    def chi_square_minimizer( jet_pt_chi2, jet_eta_chi2, jet_phi_chi2, jet_btag_chi2, jet_mass_chi2):
    
        num_of_btag = np.sum(np.array(jet_btag_chi2) ==1)

        class jet_cand_properties():
            def __init__(self, idx):
                self.idx = idx
                self.pt = jet_pt_chi2[self.idx]
                self.eta = jet_eta_chi2[self.idx]
                self.phi = jet_phi_chi2[self.idx]
                self.mass = jet_mass_chi2[self.idx]
                self.px = self.pt*np.cos(self.phi)
                self.py = self.pt*np.sin(self.phi)
                self.pz = self.pt*np.sinh(self.eta)
                self.e = np.sqrt( (self.px**2 + self.py**2 + self.pz**2) + self.mass**2 )

        def cal_W_inv(jet1, jet2):
            part_1 = (jet1.e + jet2.e)**2
            part_2 = (jet1.px + jet2.px)**2
            part_3 = (jet1.py + jet2.py)**2
            part_4 = (jet1.pz + jet2.pz)**2
            return np.sqrt( part_1 - part_2 - part_3 - part_4 )

        def cal_top_inv(jet1, jet2, jet3):
            part_1 = (jet1.e + jet2.e + jet3.e)**2
            part_2 = (jet1.px + jet2.px + jet3.px)**2
            part_3 = (jet1.py + jet2.py + jet3.py)**2
            part_4 = (jet1.pz + jet2.pz + jet3.pz)**2
            return np.sqrt( part_1 - part_2 - part_3 - part_4 )

        _bjet_list = []
        
        
        bjet = []
        _jet_list = []

        min_chi2 = -1
        m_W = 80.9
        sigma_W = 17.77
        sigma_t = 27.49

        jet_idx_list = np.array(['Nan', 'Nan', 'Nan', 'Nan', 'Nan', 'Nan'])
        
        _jet_index = []
        for i in range(len(jet_pt_chi2)):
            _jet_index.append(i)

        for i in range(len(jet_btag_chi2)):
            if jet_btag_chi2[i] == 1:
                _bjet_list.append(i)
            else :
                _jet_list.append(i)
                
        _bjet = itertools.combinations(_bjet_list, 2)
        
        for a in _bjet:
            bjet.append(a)

        bjet = np.array(bjet, dtype='object')

        #print(_bjet_list)
        #print(bjet)
        jet_index_candidate = []

        for i in range(len(bjet)):
            #print(bjet[i])

            jet = []
            
            tmp_jet_index = _bjet_list.copy()
            for c in range(len(bjet[i])): 
                
                _tmp = bjet[i][c]
                tmp_jet_index.remove(_tmp)
            
            tmp_jet_list = _jet_list.copy()

            for d in tmp_jet_index:
                tmp_jet_list.append(d)
            
            _jet = itertools.permutations(tmp_jet_list, 4)

            for b in _jet:
                jet.append(b)

            jet = np.array(jet, dtype='object')
            #print( jet)
            
            for j in range(len(jet)):
            
                _jet_index_candidate = []
                _jet_index_candidate.append(bjet[i][0])
                _jet_index_candidate.append(bjet[i][1])
                _jet_index_candidate.append(jet[j][0])
                _jet_index_candidate.append(jet[j][1])
                _jet_index_candidate.append(jet[j][2])
                _jet_index_candidate.append(jet[j][3])
                jet_index_candidate.append(_jet_index_candidate)
        #print(jet_index_candidate)   

        for i in range(len(jet_index_candidate)):

            b_1_idx = jet_index_candidate[i][0]
            b_2_idx = jet_index_candidate[i][1]

            j_1_idx = jet_index_candidate[i][2]
            j_2_idx = jet_index_candidate[i][3]
            j_3_idx = jet_index_candidate[i][4]
            j_4_idx = jet_index_candidate[i][5]

            bjet_1 = jet_cand_properties(b_1_idx)
            bjet_2 = jet_cand_properties(b_2_idx)

            jet_1 = jet_cand_properties(j_1_idx)
            jet_2 = jet_cand_properties(j_2_idx)
            jet_3 = jet_cand_properties(j_3_idx)
            jet_4 = jet_cand_properties(j_4_idx)
            
            W_1_inv = cal_W_inv(jet_1, jet_2)
            W_2_inv = cal_W_inv(jet_3, jet_4)
            top_1_inv = cal_top_inv(bjet_1, jet_1, jet_2)
            top_2_inv = cal_top_inv(bjet_2, jet_3, jet_4)

            chi2_part_1 = (top_1_inv - top_2_inv)**2
            chi2_part_2 = (W_1_inv - m_W)**2
            chi2_part_3 = (W_2_inv - m_W)**2
            
            chi2_tmp = chi2_part_1/(2*(sigma_t**2)) + chi2_part_2/sigma_W**2 + chi2_part_3/sigma_W**2
            #print(chi2_tmp, b_1_idx, j_1_idx, j_2_idx, b_2_idx, j_3_idx, j_4_idx)
            if (min_chi2 < 0 or chi2_tmp < min_chi2 ):
                min_chi2 = chi2_tmp
                jet_1_best_idx = j_1_idx
                jet_2_best_idx = j_2_idx
                jet_3_best_idx = j_3_idx
                jet_4_best_idx = j_4_idx
                b_1_best_idx = b_1_idx
                b_2_best_idx = b_2_idx
                jet_idx_list = np.array([b_1_best_idx, jet_1_best_idx, jet_2_best_idx, b_2_best_idx, jet_3_best_idx, jet_4_best_idx])
            else: 
                pass
            
        return min_chi2, jet_idx_list

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Starting chi square matching.")
    # print("+------------------------------------------------------------------------------------------------------+")
    parton_jet_index = np.zeros([len(parton_pdgid), 6])
    jet_parton_index = []

    for i in range(len(parton_pdgid)):
    #for i in range(test_length):
        tmp = np.zeros([len(jet_pt[i])])
        tmp[:] = 9999999
        jet_parton_index.append(tmp)

    for i in range(len(jet_pt)):
    #for i in range(test_length):
        #print("Event: {0}".format(i))
        _tmp_jet_parton_idx = []
        chi2, jet_idx_list_= chi_square_minimizer(jet_pt[i], jet_eta[i], jet_phi[i], jet_btag[i], jet_mass[i])
        if _chi2_value == -1 :
            print("+++++++++++++++++++++++++++++++++++++")
            print('An error occur!')
            print("Ebvent number: {0}, chi2 vslue: {1}, candidate: {2}".format(i, _chi2_value, _tmp_parton_jet_idx))
            print("+++++++++++++++++++++++++++++++++++++")
        if _chi2_value != -1 :
            print(_chi2_value, _tmp_parton_jet_idx, jet_btag[i])

            for j in range(len(_tmp_parton_jet_idx)):
                parton_jet_index[i][j] = _tmp_p｀arton_jet_idx[j]
            
            for k in range(len(_tmp_parton_jet_idx)):
                for l in range(len(_tmp_parton_jet_idx)):
                    if _tmp_parton_jet_idx[l] == int(k):
                        jet_parton_index[i][k] = int(l)
                    else :
                        pass
        else: pass 

    for i in range(len(jet_pt)):
    #for i in range(test_length):
        for k in range(len(jet_parton_index[i])):
            if jet_parton_index[i][k] == 9999999:
                jet_parton_index[i][k] = 'Nan'
            else : 
                pass
    #print(jet_parton_index[i])
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("chi square matching finished.")
    # print("+------------------------------------------------------------------------------------------------------+")  

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Recording barcode information.")
    # print("+------------------------------------------------------------------------------------------------------+")

    jet_barcode = []
    for i in range(len(parton_pdgid)):
    #for i in range(test_length):
        jet_barcode.append(np.zeros([len(jet_pt[i])]))

    jet_barcode = np.array(jet_barcode, dtype=object)

    for i in range(len(parton_pdgid)):
    #for i in range(test_length):
        for j in range(len(jet_parton_index[i])):
            if jet_parton_index[i][j] == 0:
                jet_barcode[i][j] = barcode[0]
            elif jet_parton_index[i][j] == 1: 
                jet_barcode[i][j] = barcode[1]
            elif jet_parton_index[i][j] == 2: 
                jet_barcode[i][j] = barcode[2]
            elif jet_parton_index[i][j] == 3: 
                jet_barcode[i][j] = barcode[3]
            elif jet_parton_index[i][j] == 4: 
                jet_barcode[i][j] = barcode[4]
            elif jet_parton_index[i][j] == 5: 
                jet_barcode[i][j] = barcode[5]
            else :
                jet_barcode[i][j] = 'Nan'

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Barcode information has beed record.")
    # print("+------------------------------------------------------------------------------------------------------+")

    N_match_top_in_event = np.zeros([len(jet_pt)])
    for i in range(len(jet_parton_index)):
    #for i in range(test_length):
        for j in range(len(jet_parton_index[i])):
            if np.sum(jet_parton_index[i] <= 2) == 3 and np.sum(jet_parton_index[i] > 2) != 3 and np.sum(jet_parton_index[i] <= 5) != 6:
                N_match_top_in_event[i] = 1
            elif np.sum(jet_parton_index[i] <= 2) != 3 and np.sum(jet_parton_index[i] > 2) == 3 and np.sum(jet_parton_index[i] <= 5) != 6:
                N_match_top_in_event[i] = 1
            else : 
                pass 
    
            if np.sum(jet_parton_index[i] <= 5) == 6:
                N_match_top_in_event[i] = 2
            #print(i, N_match_top_in_event[i])
    #print(len(N_match_top_in_event))
    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Jet-parton matching section complete.\n Found {0} events with 1 ttbat candidate exist.\n Found {1} events with 2 ttbar candidate exist.".format( np.sum(N_match_top_in_event == 1), np.sum(N_match_top_in_event == 2)  ))
    # print("+------------------------------------------------------------------------------------------------------+")
    #Save selected events

    lene = len(parton_pdgid)

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Writing event record to the hdf5 file.")
    # print("+------------------------------------------------------------------------------------------------------+")

    # #Save the event which pass the selection

    with h5py.File(OUTPUT_FILE,'w') as f:
        dt = h5py.vlen_dtype(np.dtype('float16'))

        hdf5_jet_parton_index = f.create_dataset('jet_parton_index', (lene, ), dtype=dt)
        hdf5_jet_barcode = f.create_dataset('jet_barcode', (lene, ), dtype=dt)
        hdf5_jet_pt = f.create_dataset('jet_pt', (lene, ), dtype=dt)
        hdf5_jet_eta = f.create_dataset('jet_eta', (lene, ), dtype=dt)
        hdf5_jet_phi = f.create_dataset('jet_phi', (lene, ), dtype=dt)
        hdf5_jet_mass = f.create_dataset('jet_mass', (lene, ), dtype=dt)
        hdf5_jet_btag = f.create_dataset('jet_btag', (lene, ), dtype=dt)

        for i in range(lene):
            hdf5_jet_parton_index[i] = jet_parton_index[i]
            hdf5_jet_barcode[i] = jet_barcode[i]
            hdf5_jet_pt[i] = jet_pt[i]
            hdf5_jet_eta[i] = jet_eta[i]
            hdf5_jet_phi[i] = jet_phi[i]
            hdf5_jet_mass[i] = jet_mass[i]
            hdf5_jet_btag[i] = jet_btag[i]

        hdf5_parton_jet_index = f.create_dataset('parton_jet_index', (lene, ), dtype=dt)
        hdf5_parton_pdgid = f.create_dataset('parton_pdgid', (lene, ), dtype=dt)
        hdf5_parton_barcode = f.create_dataset('parton_barcode', (lene, ), dtype=dt)
        hdf5_parton_pt = f.create_dataset('parton_pt', (lene, ), dtype=dt)
        hdf5_parton_eta = f.create_dataset('parton_eta', (lene, ), dtype=dt)
        hdf5_parton_phi = f.create_dataset('parton_phi', (lene, ), dtype=dt)
        hdf5_parton_mass = f.create_dataset('parton_mass', (lene, ), dtype=dt)
        hdf5_N_match_top_in_event = f.create_dataset('N_match_top_in_event', data = N_match_top_in_event)

        for i in range(lene):
            hdf5_parton_jet_index[i] = parton_jet_index[i]
            hdf5_parton_pdgid[i] = parton_pdgid[i]
            hdf5_parton_barcode[i] = parton_barcode[i]
            hdf5_parton_pt[i] = parton_pt[i]
            hdf5_parton_eta[i] = parton_eta[i]
            hdf5_parton_phi[i] = parton_phi[i]
            hdf5_parton_mass[i] = parton_mass[i]

    # print("+------------------------------------------------------------------------------------------------------+")
    # print("Event record has been send to {0}.".format(OUTPUT_FILE))
    # print("+------------------------------------------------------------------------------------------------------+")
    SUM_2 += len(N_match_top_in_event)
    return SUM_1, SUM_2, jet_parton_index, parton_jet_index

sum_C1 = 0
sum_C2 = 0
jet_paton_index_chi2 = []
parton_jet_index_chi2 = []
jet_paton_index_del = []
parton_jet_index_del = []


#INPUT_PREFIX = './data/1M_events/'
#OUTPUT_PREFIX = './output/output_'
#FILE = ""
#seq = (INPUT_PREFIX, "run_0", str(i), "/tag_1_delphes_events.root") 
#seq_1 = (OUTPUT_PREFIX,str(i), "_chi2.h5") 
#INPUT_FILE = FILE.join(seq)
#OUTPUT_FILE = FILE.join(seq_1)

INPUT_FILE = sys.argv[1]
OUTPUT_FILE = sys.argv[2]

data  = uproot.open(INPUT_FILE)['Delphes']

main(data, OUTPUT_FILE)
        


