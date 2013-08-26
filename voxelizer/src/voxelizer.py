'''
Created on 2010. 10. 19

@author: jikhanjung
'''


X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2


import sys
def print_log( str ):
  f = open( "log.txt", "a+" )
  f.writelines( str )
  f.close()

import pickle
import os 
import os.path
import re
import math
from numpy import *
NEWLINE = "\n" 
import math
import numpy
#from libpy.model_mddataset import MdDataset

point_of_origin_data = {
"Acanthastrea echinata 48020": "4.1886040e+001 -5.1105404e+001 -2.1638176e+001",
"Acanthastrea echinata 48089": "-2.4704361e+001 -1.9822198e+002 -1.4858128e+001",
"Acanthastrea echinata 89920": "1.9463367e+001 -4.4530457e+001  7.4484024e+000",
"Acropora palmata 1146600": "1.1587353e+001 -1.0722864e+002 -3.3831825e+000",
"Acropora palmata 15503": "6.2832565e+001 -2.3275037e+002 -6.7379883e+001",
"Acropora tenuis 1131458": "1.3760742e+001 -8.7072136e+001 5.1327820e+000",
"Acropora tenuis 82224": "1.5123585e+001 -8.4338371e+001 -2.6678391e+000",
"Acropora_cervicornis": "-7.6392151e+001 -1.3853206e+002 -9.0569839e+000",
"Agaricia humilis 92528": "-8.3911438e+000 -1.8484221e+002 5.4472168e+001",
"Agaricia humilis 92532": "1.5729558e+001 -5.8508251e+001 -2.6091476e+001",
"Agaricid_HJ305": "3.5565567e+001 -5.4414623e+001  1.7695999e+000",
"Alveopora sp 82769": "2.4444443e+001 -6.4616501e+001 -4.0718498e+001",
"Alveopora sp 90628": "2.1092718e+001 -9.9912148e+001 -1.9907269e+001",
"Anacropora forbesi 44780": "2.0515835e+001 -8.7630775e+001 8.4224281e+000",
"Anacropora matthai 93401-1": "1.6833130e+001 -8.6737740e+001 1.1709808e+001",
"Anacropora matthai 93401-2": "1.7194981e+001 -4.4957840e+001 -3.2032013e-002",
"Astreopora myriophthalma 89494": "-3.2652130e+001 -2.1402310e+002 2.7704552e+001",
"Astreopora myriophthalma 89496": "-4.1698380e+001 -2.3043500e+002 3.9028664e+001",
"Barabattoia amoricum 93641": "1.4432365e+001 -7.9879616e+001 -5.5590057e+000",
"Barabattoia amoricum 93642": "7.4345322e+000 -7.9047997e+001 1.0479828e+001",
"Blastomussa merleti 83336": "3.2335815e+001 -7.1763832e+001 -3.0062965e+001",
"Blastomussa wellsi 83338": "3.4893120e+001 -6.2450455e+001 -3.2479156e+001",
"Caulastrea furcata 92348": "5.4538101e+001 -1.0128497e+002 5.9590015e+000",
"Caulastrea furcata 92349": "-8.6143799e+000 -9.0642914e+001 2.4374489e+001",
"Cladocora arbuscula 71916": "8.8528862e+000 -8.9684883e+001 -2.4147858e+001",
"Cladocora arbuscula 84588": "1.1273937e+001 -9.9585876e+001 -1.4301865e+001",
"Colpophylla natans C6 17m": "-9.5661240e+000 -1.5309053e+002  2.5327148e+000",
"Coscinaraea columna 1115402": "1.6373951e+001 -2.5496417e+002 6.0366096e+000",
"Coscinaraea columna 79579": "1.9764660e+001 -5.8207073e+001 -2.0582901e+001",
"Coscinaraea columna 82553": "5.3341060e+000 -1.7037544e+002 -2.3763428e+001",
"Cynarina lacrymalis 72365": "1.7869995e+001 -5.0913277e+001 -5.0329189e+001",
"Cynarina lacrymalis 83345": "9.8591709e+000 -7.8391586e+001 -2.9084274e+001",
"Cyphastrea chalcidicum 1149588": "2.8490486e+000 -1.8688611e+002 2.3519028e+001",
"Cyphastrea chalcidium 48174": "1.8004717e+001 -7.3444855e+001 3.1767838e+001",
"Cyphastrea chalcidium 83258": "1.2466204e+001 -7.3006989e+001 -3.5016556e+000",
"Cyphastrea serialia 38363": "2.0363785e+001 -4.9436172e+001 -1.3582886e+001",
"Cyphastrea suvadivae 83254": "1.3612986e+001 -4.7663261e+001 -4.1755951e+001",
"Dendrogyra cylindrus 1148001": "1.1408076e+001 -8.1860191e+001 -2.0226397e+001",
"Dendrogyra cylindrus 36486": "2.0911366e+001 -8.6825111e+001 -4.1763082e+000",
"Dichocoenia stokesi 74371": "1.2699983e+001 -1.8116566e+002 -1.6850403e+001",
"Dichocoenia stokesi 74382": "2.1161228e+001 -2.1809512e+002 -2.0335571e+001",
"Dichocoenia stokesi 74392": "2.4121616e+001 -6.0497841e+001 -5.0718430e+001",
"Dichocoenia_stellaris": "2.0227249e+001 -4.5003525e+001 -3.2318359e+001",
"Dichocoenia_stokesi_SUI_102813": "-1.9709740e+000 -5.7743019e+001 -2.9882813e+000",
"Diploastrea heliopora 1183350": "1.8841408e+001 -4.7628849e+001 -2.8344513e+001",
"Diploastrea heliopora 91106": "1.8193268e+001 -1.9683183e+002 -5.4307129e+001",
"Diploria Labyrinthiformis 36755": "-3.7486877e+000 -1.1943017e+002  3.5173553e+001",
"Diploria clivosa 1144264": "2.2854584e+001 -1.3488368e+002  2.1634445e+001",
"Diploria clivosa 74112": "1.9602638e+001 -9.5551277e+001  3.4097090e+000",
"Diploria clivosa 74118": "3.5992485e+001 -6.0235046e+001 -8.2010765e+000",
"Diploria labyrinthiformis 7268": "5.7005444e+000 -1.6495638e+002  3.6329224e+001",
"Diploria strigosa 1138925": "1.1417603e+001 -1.4054239e+002  2.5673920e+001",
"Diploria strigosa 47708": "1.2873581e+001 -9.5286621e+001 -7.4808426e+000",
"Diploria strigosa 74948": "3.6430382e+001 -6.3409420e+001  3.1002113e+001",
"Diploria_strigosa_2": "2.4902435e+001 -1.7905882e+002 -6.4023132e+000",
"Echinophyllia aspera 1134505": "-3.3570557e+000 -2.3078906e+002 -4.1303101e+001",
"Echinophyllia aspera 45072-1": "3.1837784e+001 -7.5138229e+001 -3.2767395e+001",
"Echinophyllia aspera 45072-2": "4.1238075e+001 -6.3563129e+001 -5.9489731e+001",
"Echinophyllia aspera 89517": "-1.1991699e+001 -1.0718359e+002 3.0675507e+001",
"Echinophyllia echinoparoides 83483": "8.2847595e+000 -8.0097099e+001 -1.1916122e+001",
"Echinophyllia sp 1134483": "-3.2710228e+001 -1.8702080e+002 -3.3556747e+001",
"Echinopora gemmacea 48055": "1.3831692e+000 -2.5642355e+002 -3.9676628e+000",
"Echinopora gemmacea 48063": "1.2351498e+001 -2.5744919e+002 1.1473576e+001",
"Echinopora gemmacea 83294": "1.4077974e+001 -9.4544258e+001 4.0123215e+000",
"Echinopora gemmacea 93734": "2.7312592e+001 -3.9987274e+001 -5.2801628e+001",
"Echinopora gemmacea acc 273012": "-1.5146484e+000 -1.9215950e+002 1.3975220e+000",
"Euphyllia ancora 92356": "4.4824356e+001 -5.9044716e+001 -3.2151344e+001",
"Euphyllia ancora 93824": "-8.1140533e+001 -2.5561252e+002 -2.6953094e+001",
"Euphyllia ancora 93825": "2.1460403e+001 -1.0016382e+002 -2.3222628e+001",
"Euphyllia glabrescens 47996": "4.9633789e-001 -1.0158939e+002 -2.3470490e+001",
"Euphyllia glabrescens 89509": "1.8936562e+001 -9.4454811e+001 4.1410706e+001",
"Eusmilia fastigiata 36516": "6.0240952e+001 -5.9976543e+001 -4.4798363e+001",
"Eusmilia fastigiata 85198": "5.2397644e+001 -2.4736856e+002 -2.9130535e+001",
"Favia laxa 90605": "3.3509369e+001 -1.6485777e+002 2.3462433e+001",
"Favia laxa 93652": "2.9669250e+001 -7.7349937e+001 -1.0890617e+001",
"Favia leptophylla 83059": "-6.9880981e+000 -4.9621277e+001 -3.7956207e+001",
"Favia pallida 90731-1": "4.3262177e+000 -7.5441063e+001 3.2911377e+001",
"Favia pallida 90731-2": "-1.3673584e+001 -2.0890826e+002 2.9571350e+001",
"Favia speciosa 90727-1": "-2.3140549e+001 -1.9162250e+002 4.5854950e+001",
"Favia speciosa 90727-2": "1.1444283e+000 -1.8994402e+002 7.9219055e+001",
"Favia speciosa 90727-3": "-1.5609531e+000 -8.9069267e+001 1.8448601e+000",
"Favia stelligera 1137027": "-2.2876770e+001 -2.5630823e+002 6.6549530e+000",
"Favia stelligera 1137030": "6.0760193e+000 -1.1278735e+002 -9.2337303e+000",
"Favia stelligera 1137661": "-2.4568558e+000 -2.3010324e+002 -2.0937119e+000",
"Favia_f_pacific_loc3": "9.8761597e+000 -7.2677956e+001 -1.2104469e+001",
"Favites chinensis 90359": "1.4630438e+001 -9.3303207e+001 3.1037903e-001",
"Favites chinensis 91103": "3.0667427e+001 -2.3189154e+002 4.9364624e+001",
"Favites chinensis cf 91321": "7.9271088e+000 -8.7864159e+001 3.1381607e+000",
"Favites halicora 83068": "1.5516289e+001 -8.7938133e+001 -5.1270203e+001",
"Favites halicora 91279": "-3.0172272e+000 -7.9789566e+001 -2.7518353e+001",
"Favosites halicora 79656": "2.3425945e+001 -6.9831833e+001 -5.8547058e+000",
"Fungia scutaria 77899-1": "1.7942818e+001 -7.0385490e+001 -1.6450531e+001",
"Fungia scutaria 77899-2": "2.0917597e+001 -6.6313545e+001 -9.2783508e+000",
"Fungia scutaria 77899-3": "6.6867218e+000 -2.1403528e+002 -7.2232323e+000",
"Fungia_fungites": "1.2497543e+001 -4.7325378e+001 -9.5223083e+000",
"Galaxea fascicularis 90634": "1.4185562e+001 -7.9524246e+001 5.6507940e+000",
"Galaxea fascicularis 90860-1": "-1.8040314e+001 -2.0137941e+002 -1.8016968e+000",
"Galaxea fascicularis 90860-2": "9.3975525e+000 -2.0736113e+002 1.4606171e+000",
"Goniastrea pectinata 1148024": "4.5071121e+001 -6.9657547e+001 -2.5314379e+001",
"Goniastrea pectinata 1148085": "1.7860794e+000 -2.5825085e+002 7.0052719e+000",
"Goniastrea pectinata 21972": "-1.4729614e+000 -2.5501247e+002 -9.6194191e+000",
"Goniopora sp 91102": "4.5418365e+001 -1.8302217e+002 -3.0992615e+001",
"Goniopora sp 91142": "4.1760544e+001 -2.0834410e+002 -5.3941162e+001",
"Helioseris_1": "3.3347527e+001 -7.2414406e+001 -2.5876480e+001",
"Herpolitha limax 45399": "1.7884979e+001 -2.1270047e+002 -3.9622498e+000",
"Herpolitha limax 94709": "1.9907074e+001 -4.8762276e+001 -8.1968384e+000",
"Herpolitha limax noid": "-2.3191528e+000 -2.0159683e+002 1.5747192e+001",
"Hydnophora exesa 1149603": "2.4599428e+001 -6.6927429e+001 -1.9423859e+001",
"Hydnophora exesa 48191": "1.8044592e+001 -6.8968475e+001 6.0074768e+000",
"Hydnophora exesa 90661": "5.1644165e+001 -2.4603055e+002 -7.1717224e+000",
"Hydnophora microconos 45030": "1.8345612e+001 -1.0864119e+002 -7.4034958e+000",
"Hydnophora rigida box50": "1.8056271e+001 -1.1813104e+002 7.7145004e-001",
"Isophyllia sinuosa Loc No6 Tortugas Vaughan 1908": "1.1062950e+001 -5.3409454e+001 1.0591545e+001",
"Isophyllia_sinuosa_USNM_36819": "4.3759323e+001 -6.3828018e+001 -1.6868156e+001",
"Leotpastrea fluians 48490": "2.7683233e+001 -2.8439690e+001 -2.4465820e+001",
"Leptastrea pruinosa 1150570": "2.3661949e+001 -4.8056751e+001 -3.4860291e+001",
"Leptastrea pruinosa 93756": "2.4636719e+001 -6.1241478e+001 -1.8005310e+001",
"Leptoria phrygia 1146677": "2.4910690e+001 -8.1619682e+001 -2.0553741e+000",
"Leptoria phrygia 79225": "4.5407104e+000 -2.0087831e+002 1.3988434e+001",
"Leptoseris mycetoseroides 93438": "1.5349529e+001 -1.9819360e+002 -8.0863647e+000",
"Lobophyllia corymbosa 89902": "-4.7202881e+001 -2.3446577e+002 -1.3925247e+001",
"Lobophyllia corymbosa 91009": "5.2724548e+001 -9.6818611e+001 -3.8837177e+001",
"Lobophyllia corymbosa acc273012": "5.1613098e+001 -2.5224356e+002 -1.8918732e+001",
"Lobophyllia hemprichii 100552": "4.0717800e+001 -3.0983650e+001 -5.7483963e+001",
"Lobophyllia hemprichii 45060": "4.3563110e+001 -1.9901353e+002 3.4954529e+000",
"Lobophyllia hemprichii 92367": "-3.1910461e+001 -1.5275893e+002 3.4181671e+001",
"Lobophyllia pachysepta 45442": "-2.6489594e+001 -1.6260847e+002 2.7194916e+001",
"Lobophyllia pachysepta 91130": "-2.7243881e+000 -1.6813692e+002 -2.0104675e+000",
"M_annularis_2": "4.4226379e+000 -7.8490646e+001  2.1587051e+001",
"M_annularis_Panama_1987": "1.1619675e+001 -9.4615730e+001 -6.3516464e+000",
"Madracis mirabilis 088031": "3.4988842e+000 -2.3611484e+002 -1.6402969e+001",
"Madracis mirabilis 1113051": "3.1795029e+001 -9.9064926e+001 -4.0187740e+001",
"Manicina areolata 40623-1": "1.5940084e+001 -4.7504913e+001 -4.4442383e+001",
"Manicina areolata 40623-2": "1.1158842e+001 -1.6888185e+002 -7.4992371e+000",
"Manicina areolata 77697": "1.9964294e+001 -4.5514549e+001 -4.0517883e+001",
"Manicina_1": "2.2709129e+001 -1.0427603e+002 -2.0027290e+001",
"Manicina_2": "2.3014378e+001 -7.3653236e+001 -2.3563606e+001",
"Meandrina brasiliensis 1150404": "2.6421377e+001 -5.8771660e+001 -9.3230286e+000",
"Meandrina brasiliensis 1150406": "1.9624416e+001 -5.9735226e+001 -1.7269028e+001",
"Meandrina brasiliensis 48128": "3.1089067e+001 -3.8369511e+001 -5.0493439e+001",
"Meandrina meandrites 1150583": "1.1519501e+001 -5.3290524e+001 -1.5880463e+001",
"Meandrina meandrites 74979": "3.3099419e+001 -2.4576222e+002 4.9389954e+000",
"Meandrina meandrites 84905": "4.5522049e+001 -7.8535049e+001 -1.8456238e+001",
"Meandrina": "3.2967628e+001 -7.6831459e+001 -6.9918823e+000",
"Merulina ampliata 90766-1": "1.5955441e+001 -5.8164936e+001 -3.9291412e+001",
"Merulina ampliata 90766-2": "3.1971024e+001 -2.0917340e+002 -4.4731262e+001",
"Merulina ampliata 90766-3": "1.1294609e+001 -1.8731151e+002 -4.2808258e+001",
"Merulina scabricula 90768-1": "-2.7876007e+001 -2.4721069e+002 3.7516998e+001",
"Merulina scabricula 90768-2": "7.1294899e+000 -2.1432539e+002 -1.5992249e+001",
"Merulina scabricula 93775": "1.8233938e+001 -8.6238892e+001 -7.2387257e+000",
"Montastraea annularis 1150979": "5.5981522e+000 -2.6001791e+002 6.6001205e+000",
"Montastraea annularis 36645": "3.3709122e+001 -1.8411142e+002 -4.8063171e+001",
"Montastraea cavernosa 74183": "8.3173370e-001 -2.4469461e+002 5.2273226e+000",
"Montastraea cavernosa 74190": "1.0253460e+001 -2.1746149e+002 -4.0900864e+001",
"Montastraea curta 1153616": "2.4933273e+001 -7.3155807e+001 1.1384323e+001",
"Montastraea curta 45700": "-4.1867981e+000 -2.1089998e+002 2.4227631e+001",
"Montastraea curta 89988": "1.0772141e+001 -7.3279243e+001 1.9529083e+001",
"Montastraea valenciennesi 1153624": "6.8594894e+000 -1.0450546e+002 5.7389832e+000",
"Montastraea valenciennesi 90671": "1.3707466e+001 -2.0891316e+002 4.9866821e+001",
"Mussa angulosa 36786": "-1.2984325e+001 -1.8372644e+002  2.6032272e+001",
"Mussa angulosa 7277": "-9.2221405e+001 -1.6079630e+002  2.5808441e+001",
"Mussa angulosa 7286": "-2.1946884e+001 -7.1655449e+001 -9.7899237e+000",
"Mussa_angulosa_USNM_7297": "-1.8109497e+001 -8.5837814e+001  1.5539841e+001",
"Mussismilia braziliensis 5379": "1.5315058e+001 -2.0302142e+002  1.4823723e+001",
"Mussismilia hartti 10895": "2.1613159e+001 -4.9921936e+001  1.6320313e+001",
"Mussismilia hartti 95414": "-6.6544495e+000 -1.9444620e+002  8.9142487e+001",
"Mussismilia hispida 85176": "1.7119041e+001 -4.8856674e+001  7.6245117e+000",
"Mussismilia hispida 85177": "2.3832664e+001 -4.2208817e+001  1.3207283e+001",
"Mussismilia sp 1164621": "2.1879272e+001 -1.4432071e+002  3.0703476e+001",
"Mussismilia sp 5351": "1.7885658e+001 -1.9447639e+002  2.1082979e+001",
"Mycedium elephantotus 93805-1": "6.2306976e+000 -5.1913921e+001 -3.6148697e+001",
"Mycedium elephantotus 93805-2": "-5.8784119e+001 -1.7201582e+002 3.3739594e+001",
"Mycedium elephantotus no_id": "-4.6697083e+000 -2.1901704e+002 2.2632904e+001",
"Mycetophyllia aliciae 85182": "-3.5823822e+000 -1.1240541e+002  3.4617889e+001",
"Mycetophyllia aliciae 95476": "-3.8822754e+001 -1.7547557e+002  5.3296814e+001",
"Mycetophyllia danaana 85166": "-2.5096512e-001 -1.6071135e+002 -6.7347412e+000",
"Mycetophyllia danaana 95480": "-6.1180115e-001 -1.4220007e+002 -1.2789825e+001",
"Mycetophyllia lamarckiana 74341": "-1.0957336e+001 -1.5084018e+002  8.3386230e+001",
"Mycetophyllia_815": "9.6132393e+000 -2.5543980e+002  3.4797997e+001",
"Mycetophyllia_818": "1.9117966e+000 -2.0723824e+002 -9.4236755e+000",
"Mycetophyllia_859": "1.1580052e+001 -2.6039691e+002  1.3718666e+001",
"Oculina diffusa 36555": "5.2071945e+001 -2.4473189e+002 1.7468632e+001",
"Oculina diffusa 45310": "5.2346680e+001 -9.9377113e+001 -1.6967964e+001",
"Oculina_diffusa_1127": "1.5640965e+001 -9.8015495e+001 -1.0259720e+001",
"Oculina_val_1128": "1.7754761e+001 -9.7256737e+001 -1.5055336e+001",
"Oulastrea crispata 90691-1": "2.6597540e+001 -1.0092024e+002 -1.4185292e+001",
"Oulastrea crispata 90691-2": "3.3627930e+001 -7.8926384e+001 -1.3726924e+001",
"Oulastrea crispata 90691-3": "2.1581654e+001 -7.5886337e+001 -3.0441559e+001",
"Oulophyllia crispa 1150982": "6.1255493e+000 -6.3656029e+001 -7.7460785e+000",
"Oulophyllia crispa 83123": "6.3913116e+000 -7.3167107e+001 -1.0651001e+001",
"Oxypora lacera 83473": "-3.1852966e+001 -1.2251700e+002 7.1327438e+000",
"Oxypora lacera 83474": "2.1185246e+001 -7.4974701e+001 -1.7136261e+001",
"Pachyseris speciosa 90646-1": "4.5027847e+001 -1.8226688e+002 -9.8440247e+000",
"Pachyseris speciosa 90646-2": "-6.4526367e-001 -2.1221446e+002 -8.1849976e+000",
"Pavona cactus 44330": "7.6738708e+001 -7.5850113e+001 1.6334419e+000",
"Pavona cactus 90784": "4.3042671e+001 -5.7972637e+001 -1.1217285e+001",
"Pectinia alcicornis 47131": "-9.1589689e-001 -2.5319484e+002 -9.5144882e+000",
"Pectinia alcicornis 93812": "1.3208673e+001 -1.0688276e+002 -1.1084551e+001",
"Pectinia lactuca 92383": "-2.8432068e+001 -2.4341652e+002 2.6249222e+001",
"Pectinia paeonia 90812": "4.5649551e+001 -2.1820692e+002 5.4229309e+001",
"Pectinia paeonia no_id": "-1.2539459e+001 -8.9777779e+001 -1.0007481e+001",
"Physogyra lichtensteini 93832": "2.3739258e+001 -1.9482594e+002 -7.1449280e+000",
"Platygyra daedalea 1146788": "3.0441986e+001 -6.1930298e+001 -9.2519226e+000",
"Platygyra daedalea 90679": "3.3705460e+001 -5.7485085e+001 5.3852081e+000",
"Platygyra daedalea 90679-2": "8.3482971e+000 -1.3198471e+002 6.1775421e+001",
"Platygyra lamellina 21975": "2.3003647e+001 -7.7221649e+001 2.8706543e+001",
"Platygyra lamellina 93713": "-4.9480667e+000 -1.5322441e+002 5.3260590e+001",
"Plesiastrea versipora 44996": "4.9950333e+001 -8.0114807e+001 -2.4972759e+001",
"Plesiastrea versipora 82795": "3.4829681e+001 -5.6133224e+001 -3.2381912e+001",
"Pocillopora verrucosa 45609": "1.5714256e+001 -9.1073212e+001 6.4760437e+000",
"Porites astreoides 74655": "1.9945076e+001 -1.9012593e+002 -1.2736084e+001",
"Porites astreoides 74658": "1.7453751e+001 -7.4627571e+001 -5.0772598e+001",
"Porites lutea 1175404-1": "2.0429592e+001 -7.6538742e+001 -4.4216011e+001",
"Porites lutea 1175404-2": "2.4269474e+001 -5.5574417e+001 -7.0160049e+001",
"Porites lutea 99437": "2.0347923e+001 -4.9938065e+001 -5.7862854e+001",
"Porites_astreoides_2": "-1.6894623e+001 -5.3236530e+001 -1.3314819e+000",
"Porites_astreoides_SUI_102795": "1.2411621e+001 -6.8821152e+001 -5.5802917e-001",
"Porites_divaricata": "5.5657654e+001 -7.6879829e+001 -1.9648855e+001",
"Porites_porites_1": "-1.8820595e+001 -1.8573315e+002  5.9567856e+001",
"Porites_porites_2": "6.0859451e+000 -1.0545271e+002 -1.5638166e+001",
"Psammocora contigua 80272": "2.7369562e+001 -6.9958015e+001 -2.7527573e+001",
"Scapophyllia cylindrica 83309": "2.4684750e+001 -2.6154822e+002 1.0059151e+001",
"Scapophyllia cylindrica 89934": "4.6285706e+000 -2.6261981e+002 -1.2190409e+001",
"Scolymia sp 83335-1": "1.4465848e+001 -6.5900566e+001 -4.8914368e+001",
"Scolymia sp 83335-2": "1.3755693e+001 -7.7984489e+001 -1.2294250e+001",
"Scolymia sp 83335-3": "1.4123884e+001 -9.3563362e+001 -1.6607597e+001",
"Scolymia vitiensis 83331": "-8.2886963e+000 -7.2180367e+001 -3.8018951e+000",
"Scolymia vitiensis 93788": "4.0478279e+001 -5.2648003e+001 -6.9602020e+001",
"Scolymia_cubensis_YPM_7569": "5.3022705e+001 -5.7309002e+001 -3.7884399e+001",
"Seriatopora hystrix 79201": "2.9838280e+001 -8.0203842e+001 1.0428028e+001",
"Seriatopora hystrix 93376": "3.3682629e+001 -8.4818939e+001 -3.3441002e+001",
"Siderastrea radians 1143820": "-2.6804504e+001 -1.6416243e+002 1.5240204e+001",
"Siderastrea radians 1143827-1": "1.1620155e+001 -8.9526688e+001 -2.6632645e+001",
"Siderastrea radians 1143827-2": "3.4756012e+000 -7.4490746e+001 -2.3190125e+001",
"Siderastrea savignyana 1154339": "-1.6461288e+001 -5.4678650e+001 -2.7886353e+000",
"Siderastrea savignyana 82563": "1.2314621e+001 -7.3041313e+001 -5.4994812e+000",
"Siderastrea siderea 1143794": "2.1085985e+001 -8.4857285e+001 -9.5415115e+000",
"Siderastrea siderea 47606": "2.6521545e+001 -8.5656845e+001 -7.0893817e+000",
"Siderastrea sp 10935": "3.2101601e+001 -6.2135899e+001 -2.2383972e+001",
"Siderastrea sp 47604": "-1.9044922e+001 -1.7673033e+002 1.0736084e+001",
"Siderastrea_1": "1.9051682e+001 -7.9479408e+001 -1.9264252e+001",
"Siderastrea_siderea_1": "1.2498138e+001 -7.4174187e+001 -7.2018280e+000",
"Siderastrea_siderea_2": "2.1728859e+001 -9.0336777e+001 -2.2100109e+001",
"Siderastrea_siderea_3": "4.5291199e+001 -5.8801537e+001  3.5862265e+000",
"Siderastrea_siderea_4": "3.8383484e-001 -5.0934601e+001  3.0430664e+001",
"Solenastrea bournoni 1139380": "-6.7285919e-001 -1.0302217e+002 7.3719673e+000",
"Solenastrea bournoni 86692": "1.1047028e+001 -1.0224758e+002 -6.0874710e+000",
"Stephanocoenia michelini 1154436": "2.5892679e+001 -4.5156940e+001 -8.8888550e+000",
"Stephanocoenia michelini 72791-1": "3.1677753e+001 -7.9893387e+001 3.9516479e+001",
"Stephanocoenia michelini 72791-2": "2.2176563e+001 -5.8604195e+001 1.9271088e+001",
"Stylocoeniella guentheri 100223": "-2.9459381e+000 -5.2035503e+001 5.3506012e+000",
"Stylocoeniella guentheri 79560": "-7.5718079e+000 -1.9838176e+002 1.1164780e+001",
"Stylocoeniella guentheri 80253": "1.8034653e+001 -7.9466309e+001 1.1770628e+001",
"Stylophora pistillata 79250": "-2.4146667e+001 -1.6351065e+002 -4.4254303e+001",
"Stylophora pistillata 90842-1": "-4.5372314e+000 -7.6155151e+001 -2.2483521e+000",
"Stylophora pistillata 90842-2": "2.4668167e+001 -9.4392708e+001 2.3141413e+000",
"Symphyllia agaricia 1134475": "7.0319786e+000 -2.0632904e+002 2.6408173e+001",
"Symphyllia agaricia 90582": "1.3861595e+001 -1.7830992e+002 9.4407578e+000",
"Symphyllia radians 1114429": "1.5812439e+001 -1.9348129e+002 2.5105255e+001",
"Symphyllia radians 90797": "2.1532959e+001 -2.0838188e+002 1.7501404e+001",
"Symphyllia recta 91132-1": "2.5353195e+001 -1.9475439e+002 1.4450684e+000",
"Symphyllia recta 91132-2": "1.6774811e+001 -7.1131241e+001 8.7964172e+000",
"Trachyphyllia geoffroyi 1155044": "2.4948483e+001 -1.0586796e+002 -3.1185516e+001",
"Trachyphyllia geoffroyi 90314": "3.7608795e+000 -9.0496925e+001 2.6813309e+001",
"Turbinaria peltata 83733": "-1.2094727e+001 -6.8782181e+001 -3.7882412e+001",
"Turbinaria peltata noid 2": "-7.1124878e+000 -1.6107693e+002 1.5567963e+001",
"Turbinaria peltata noid": "-8.3706436e+000 -4.5036572e+001 -4.0980637e+001",
}


class MdDatamatrix:
  def __init__(self):
    pass
  def SetMatrix(self,matrix):
    self.matrix = matrix
    self.nVariable, self.nObservation = matrix.shape
  def AddDataset(self,dataset):
    self.dataset = dataset
    self.dimension = dataset.dimension
    self.nObservation = len( dataset.objects )
    self.nVariable = len( dataset.objects[0].landmarks ) * self.dimension
    self.matrix = numpy.zeros( ( self.nVariable, self.nObservation ) )
    i = 0
    #for object in dataset.objects:
    for object in dataset.objects:
      j = 0
      #for lm in object.landmarks:
      
      for lm in object.landmarks:
        #print lm.xcoord, lm.ycoord, lm.zcoord
        self.matrix[j,i] = lm.xcoord
        j += 1
        self.matrix[j,i] = lm.ycoord
        j += 1
        if self.dimension == 3:
          self.matrix[j,i] = lm.zcoord
          j += 1
        if j == self.nVariable:
          break
      i += 1

class MdPrincipalComponent:
  def __init__(self):
    self.dimension = -1
    self.data = MdDatamatrix()
    #self.datamatrix = []
    return
  def AddDataset(self,dataset):
    self.data.AddDataset( dataset )
  def SetMatrix(self, matrix):
    self.data.SetMatrix( matrix )

  def Analyze(self):
    '''analyze'''
    #print "analyze"
    self.raw_eigen_values = []
    self.eigen_value_percentages = []
        
    #for d in self.datamatrix :
      #print d

    sums = []
    avrs = []
    ''' calculate the empirical mean '''
    for i in range ( self.data.nVariable ): 
      sums.append(  0 )
      for j in range ( self.data.nObservation ):
        sums[i] += self.data.matrix[i,j] 
    
    for sum in sums:
      avrs.append( float( sum ) / float( self.data.nObservation ) )
    
    #print "sum:", sums
    #print "avgs:",avrs
    #return
    
    for i in range ( self.data.nVariable ): 
      for j in range ( self.data.nObservation ):
        self.data.matrix[i,j] -= avrs[i] 

    #print self.datamatrix
    
    ''' covariance matrix '''
    self.covariance_matrix = numpy.dot( self.data.matrix, numpy.transpose(self.data.matrix)) / self.data.nObservation

    #print "covariance_matrix", self.covariance_matrix
  
    ''' zz '''
    v, s, w = numpy.linalg.svd( self.covariance_matrix )
    #print "v", v
    #print "w", w
    
    #print "s[",
    self.raw_eigen_values = s
    sum = 0
    for ss in s:
      sum += ss
    for ss in s:
      self.eigen_value_percentages.append( ss/sum )
    cumul = 0
    eigen_values = []
    i = 0
    nSignificantEigenValue = -1
    nEigenValues = -1
    for ss in s:
      cumul += ss
      eigen_values.append( ss )
      #print sum, cumul, ss
      if cumul / sum > 0.95 and nSignificantEigenValue == -1:
        nSignificantEigenValue = i + 1
      if (ss /sum ) < 0.00001 and nEigenValues == -1:
        nEigenValues = i + 1
      i += 1
    
    #print nEigenValues, "eigen values obtained,", nSignificantEigenValue, "significant."
    #print eigen_values
    
    #for i in range( len(s) ):
      #print math.floor( ( s[i] / sum ) * 10000 + 0.5 ) / 100

    #print "s", int( s * 100 )/100
    #print "w", w
    #print v
    
    #print self.data.matrix
    for i in range(nSignificantEigenValue):
      k = v[...,i]
      #print i, k, numpy.transpose(k) 
      det = numpy.dot( k, numpy.transpose( k ))
      #print det
    self.rotated_matrix = numpy.dot( w, self.data.matrix )
    self.rotation_matrix = w
    #print w
    #print self.datamatrix[...,2]
    #print self.rotated_matrix[...,2]
    #print self.rotated_matrix
    self.loading = w
    return
    self.new_dataset = self.data.dataset.copy()
    self.new_dataset.objects = []
    for i in range( self.data.nObservation ):
      #object = MdObject()
      object.objname = self.data.dataset.objects[i].objname
      object.coords = self.rotated_matrix[...,i]
      object.group_list[:] = self.data.dataset.objects[i].group_list[:]
      self.new_dataset.objects.append( object )
      #if( i == 2 ) : print object.coords

class ThreeDShape:
  def __init__(self):
    scale = 1
    self.orig_verts = {}
    self.verts = {}
    self.faces = {}
    self.verts_in_sphere = {}
    self.dists = {}
    self.centroid_size = -1
    self.point_of_origin = []

    self.is_centered = False
    self.is_aligned = False
    self.is_voxelized = False
    self.outlier_removed = False

    self.name = ""
    self.max_x = 0
    self.max_y = 0
    self.max_z = 0
    self.avg_dist = 0
    self.scale_factor = 1.0
    self.max_D2_dist = -9999
    self.min_D2_dist = 9999

    self.D2_dist_list = []
    self.dist_dist_list = []
    self.dist_dist_list_pct = []
    self.sp_dist = []
    self.sp_dist_pct = []

  def ToTpsString(self):
        tpsstring = "lm=" + str( len( self.verts ) ) + " " + self.filename + "\n"
        tpsstring += " ".join( [ str( x ) for x in self.point_of_origin ] ) + "\n" 
        for k in self.verts.keys():
            tpsstring += " ".join( [ str( x ) for x in self.verts[k] ] ) + "\n"
        return tpsstring
  def SaveAsTps(self,path):
        f = open( path, 'wb' )
        f.write( self.ToTpsString() )
        f.close()
  def SaveAsPickle(self, path):
        output = open( path, 'wb' )
        pickle.dump( self, output )
        output.close()

  def RestoreFromPickle(self, path ):
        pkl_file = open( path, "rb" )
        data = pickle.load( pkl_file )
        print data.name, data.no_of_vertices, "vertices"
        
        self.verts = data.verts
        self.no_of_vertices = data.no_of_vertices
        self.avg_dist = data.avg_dist
        self.max_x = data.max_x
        self.max_y = data.max_y
        self.max_z = data.max_z
        return

  def Simplify(self,n_vert=1000):
    #n_total_vert = self.no_of_vertices
    print "simplify"
    if self.no_of_vertices <= n_vert: return
    print "begins.", len( self.verts.keys() ), "verts,", len( self.faces.keys()), "faces,"#, self.voxels.shape, "voxels."
    new_verts = {}
    idx_list = []
    for i in range( n_vert ):
        idx = int( random.random() * self.no_of_vertices )
        while( idx in idx_list or idx not in self.verts.keys() ):          
            idx = int( random.random() * self.no_of_vertices )
        new_verts[i] = self.verts[idx]
    self.verts = new_verts
    self.orig_verts = {}
    self.faces = {}
    self.dists = {}
    self.verts_in_sphere = {}
    self.no_of_vertices = len( self.verts.keys() )

    self.D2_dist_list = []
    self.dist_dist_list = []
    self.dist_dist_list_pct = []
    self.sp_dist = []
    self.sp_dist_pct = []

    print "simplify done.", len( self.verts.keys() ), "verts,", len( self.faces.keys()), "faces,"#, self.voxels.shape, "voxels."
    
  def OpenObjFile(self, filepath, load_faces = False, use_pickle = True ):
    if os.path.exists( filepath + ".pkl" ) and use_pickle:
        self.name = filepath
        self.RestoreFromPickle()
        return
            
    f = open( filepath, 'r' )
    objdata = f.read()
    f.close()
    self.name = filepath
    
    verts = {}
    faces = {}
    vert_exist = {}
    num_v = 1
    num_f = 1  
    scale = 1

    obj_lines = [ l.strip() for l in objdata.split( NEWLINE ) ]
    for line in obj_lines:
      line = line.strip() 
      fpoint = re.split( '\s+', line )
      if fpoint[0] == 'v':
        x, y, z = float( fpoint[1] ), float( fpoint[2] ), float( fpoint[3] )
        verts[num_v] = [ x/scale, y/scale, z/scale ]
        num_v += 1 
      if fpoint[0] == 'f' and load_faces:
        #print line
        #print fpoint, fpoint[1:]
        f_vert = []
        for point in fpoint[1:]:
          p_split = point.split( "/" )
          if len( p_split ) > 0:
            v_idx = int( p_split[0] )
            f_vert.append( v_idx )
            vert_exist[v_idx] = 1
        faces[num_f] = f_vert
        #print f_vert
        num_f += 1
    real_verts = {}
    for k in vert_exist.keys():
      real_verts[k] = verts[k]

    self.faces = faces
    self.verts = verts #self.orig_verts = verts  
    self.no_of_vertices = len( verts.keys() )
    return

  def remove_outlier(self):
    sum = 0
    dist_avg = 0
    dist_diff = {}
    ids = self.dists.keys()
    num_dist = len(ids)
    for id in ids:
      sum += self.dists[id]
    dist_avg = sum / num_dist
    #max_diff = -9999
    #min diff = 9999
    sum_sq_diff = 0
    for id in ids:
      diff = self.dists[id] - dist_avg
      sum_sq_diff += diff ** 2.0
      dist_diff[id] = diff
    var = sum_sq_diff / num_dist
    std = var ** 0.5
    max_dist = max( self.dists.values() )
    min_dist = min( self.dists.values() )
    #print dist_avg, var, std, max_dist, min_dist
    for id in ids:
      if abs( dist_diff[id] ) > 5 * std:
        del dist_diff[id]
        del self.verts[id]
        del self.dists[id]
    max_dist = max( self.dists.values() )
    min_dist = min( self.dists.values() )
    #print dist_avg, var, std, max_dist, min_dist
    self.outlier_removed = True
    self.is_centered = False

  def center( self ): 
    ( max_x, max_y, max_z ) = ( -9999, -9999, -9999 )
    ( min_x, min_y, min_z ) = ( 9999, 9999, 9999 )
    #print len( verts )
    #return
    
    verts = self.verts
    new_verts = {}
    x_sum, y_sum, z_sum = 0, 0, 0
    for id in verts.keys( ):
      x, y, z = verts[id]
      x_sum += x
      y_sum += y
      z_sum += z
      max_x = max( x, max_x )
      max_y = max( y, max_y )
      max_z = max( z, max_z )
      min_x = min( x, min_x )
      min_y = min( y, min_y )
      min_z = min( z, min_z )
    n_vert = len( verts.keys() )
    x_avg = x_sum / n_vert
    y_avg = y_sum / n_vert
    z_avg = z_sum / n_vert
    max_x -= x_avg
    max_y -= y_avg
    max_z -= z_avg
    min_x -= x_avg
    min_y -= y_avg
    min_z -= z_avg
    
    #print max_x, max_y, max_z, min_x, min_y, min_z\
    for id in verts.keys( ):
      x, y, z = verts[id]
      x -= x_avg
      y -= y_avg
      z -= z_avg
      verts[id] = [ x, y, z ]
    self.point_of_origin[0] -= x_avg
    self.point_of_origin[1] -= y_avg
    self.point_of_origin[2] -= z_avg
      #new_verts.setdefault( ( x - min_x, y - min_y, z - min_z ), set() ).add( id ) #[id] = [ x - min_x, y - min_y, z - min_z ]
    self.max_x = max_x
    self.max_y = max_y
    self.max_z = max_z
    self.min_x = min_x
    self.min_y = min_y
    self.min_z = min_z
    self.verts = verts
    self.is_centered = True
    #return verts, max_x, min_x, max_y, min_y, max_z, min_z

  def get_centroid_size(self, calculate_anyway = False ):
    if not calculate_anyway and self.centroid_size > 0:
      return self.centroid_size
    
    #if not self.is_centered:
    #  self.center()
    sum_of_squares = 0
    min_dist = 9999
    max_dist = -9999
    dists = {}
    sum_dist = 0
    for id in self.verts.keys( ):
      x, y, z = self.verts[id]
      sum_of_squares += x**2 + y**2 + z**2 
      dist = ( x**2 + y**2 + z** 2 ) ** 0.5
      sum_dist += dist
      min_dist = min( min_dist, dist )
      max_dist = max( max_dist, dist )
      dists[id] = dist 
      #if int( id ) < 10:
      #  print "x,y,z", x, y, z
    #print "sum of squares", sum_of_squares, self.no_of_vertices
    sss = sum_of_squares ** 0.5
    #print "sss", sss
    self.centroid_size = ( sss ) 
    self.min_dist = min_dist
    self.max_dist = max_dist 
    self.avg_dist = sum_dist / len( self.verts.keys() )
    self.dists = dists
    return self.centroid_size

  def rotate_on_axis(self,angle,axis):
    if axis == X_AXIS:
        idx1 = 1
        idx2 = 2
    elif axis == Y_AXIS:
        idx1 = 0
        idx2 = 2
    elif axis == Z_AXIS:
        idx1 = 0
        idx2 = 1

    ks = self.verts.keys()
    rotate = numpy.zeros( (3,3) )
    for i in range(3):
        rotate[i,i] = 1
    rotate[idx1,idx1] = rotate[idx2,idx2] = math.cos( angle )
    rotate[idx2,idx1] = math.sin( angle )
    rotate[idx1,idx2] = -1.0 * math.sin( angle )
    #self.rotated_verts = {}
    for k in ks:
        #x, y, z = self.verts[k]
        #print self.verts[k],
        vec = numpy.zeros( ( 3 ) )
        vec[:] = self.verts[k][:]
        rotated_vec = numpy.dot( rotate, vec )
        self.verts[k] = rotated_vec[:]
        #print self.verts[k]
      
    ''' rotate point of origin as well''' 
    vec = numpy.zeros( ( 3 ) )
    vec[:] = self.point_of_origin[:]
    rotated_vec = numpy.dot( rotate, vec )
    self.point_of_origin[:] = rotated_vec[:]
      

  def rotate(self, theta, phi ):
    ks = self.verts.keys()
    rotate_theta = numpy.zeros( (3,3) )
    rotate_phi = numpy.zeros( (3,3) )
    for i in range(3):
      rotate_theta[i,i] = 1
      rotate_phi[i,i] = 1
    rotate_phi[0,0] = rotate_phi[1,1] = math.sin( phi)
    rotate_phi[0,1] = math.cos(phi)
    rotate_phi[1,0] = -1.0 * math.cos(phi)
    rotate_theta[0,0] = rotate_theta[2,2] = math.sin( theta )
    rotate_theta[0,2] = math.cos(theta)
    rotate_theta[2,0] = -1.0 * math.cos(theta)
    #self.rotated_verts = {}
    for k in ks:
      #x, y, z = self.verts[k]
      vec = numpy.zeros( ( 3 ) )
      vec[:] = self.verts[k][:]
      rotated_vec = numpy.dot( rotate_phi, numpy.dot( rotate_theta, vec ) )
      self.verts[k] = rotated_vec[:]
      
    ''' rotate point of origin as well''' 
    vec = numpy.zeros( ( 3 ) )
    vec[:] = self.point_of_origin[:]
    rotated_vec = numpy.dot( rotate_phi, numpy.dot( rotate_theta, vec ) )
    self.point_of_origin[:] = rotated_vec[:]
    #self.verts = self.rotated_verts

  def translate_using_origin(self):
      for k in self.verts.keys():
          x, y, z = self.verts[k] 
          ox, oy, oz = self.point_of_origin
          x -= ox
          y -= oy
          z -= oz
          self.verts[k] = [ x, y, z ]
      self.point_of_origin = [ 0,0,0 ]

  def align_using_point_of_origin(self):
      #for k in self.verts.keys()[0:10]:
      #    print self.verts[k]
          
      #print self.point_of_origin
      x, y, z = self.point_of_origin
      sin_val = y / math.sqrt( x*x + y*y )
      angle = math.degrees( math.asin(sin_val) )
      if x < 0: angle = 180 - angle
      rotate_angle = 90 - angle
      rotate_angle_radian = math.radians( rotate_angle )
      
      self.rotate_on_axis( rotate_angle_radian, Z_AXIS )
      #print self.point_of_origin

      x, y, z = self.point_of_origin
      sin_val = z / math.sqrt( y*y + z*z )
      angle = math.degrees( math.asin(sin_val ))
      if y < 0: angle = 180 - angle
      rotate_angle = ( 90 - angle ) + 180 
      rotate_angle_radian = math.radians( rotate_angle )
      self.rotate_on_axis( rotate_angle_radian, X_AXIS ) 

      #for k in self.verts.keys()[0:10]:
      #    print self.verts[k]
      
      #print self.point_of_origin
      self.is_aligned = True
      return

  def align_on_xy_plane(self):    
    ks = self.verts.keys()
    matrix = numpy.zeros( ( 2, len( ks ) ) )
    i = 0
    for k in ks:
      matrix[0,i] = self.verts[k][0]
      matrix[1,i] = self.verts[k][1]
      i+= 1
  
    pca = MdPrincipalComponent()
    pca.SetMatrix( matrix )
    #print "a"
    pca.Analyze()
    #print pca.rotated_matrix
    #print "rotation:", pca.rotation_matrix
    new_verts = {}
    i = 0
    for k in ks:
      vert = []
      vert[:] = pca.rotated_matrix[:,i]
      vert.append( self.verts[k][2] )
      new_verts[k] = vert
      i+=1
    #print "rotation", pca.rotation_matrix
    self.rotation_matrix = pca.rotation_matrix
    self.is_aligned = True
    self.verts = new_verts
  
  def align(self):
    
    ks = self.verts.keys()
    matrix = numpy.zeros( ( 3, len( ks ) ) )
    i = 0
    for k in ks:
      matrix[:,i] = self.verts[k][:]
      i+= 1
  
    pca = MdPrincipalComponent()
    pca.SetMatrix( matrix )
    #print "a"
    pca.Analyze()
    #print pca.rotated_matrix
    #print "rotation:", pca.rotation_matrix
    new_verts = {}
    i = 0
    for k in ks:
      new_verts[k] = pca.rotated_matrix[:,i]
      i+=1
    #print "rotation", pca.rotation_matrix
    self.rotation_matrix = pca.rotation_matrix
    self.is_aligned = True
    self.verts = new_verts

  def scale(self, factor = -1):
    if factor < 0 : return
    #print "before scale", self.centroid_size
    new_verts = {}
    for id in self.verts.keys( ):
      x, y, z = self.verts[id]
      new_x, new_y, new_z = x * factor, y * factor, z * factor 
      new_verts[id] = [ new_x, new_y, new_z ]
      #self.scaled_verts[id] = [ new_x, new_y, new_z ]
      #if int( id ) < 10:
        #print "old x,y,z", x, x*factor, y, y*factor, z, z*factor
        #print "new x,y,z", new_verts[id]

    ''' scale point of origin '''
    x, y, z = self.point_of_origin
    new_x, new_y, new_z = x * factor, y * factor, z * factor
    self.point_of_origin = [ new_x, new_y, new_z ]  

    
    self.verts = new_verts
    self.get_centroid_size( True )
    #print "after scale", self.centroid_size
    self.max_x *= factor
    self.max_y *= factor
    self.max_z *= factor
    self.min_x *= factor
    self.min_y *= factor
    self.min_z *= factor
    return

  def get_voxels( self, min_x, max_x, min_y, max_y, min_z, max_z ):
    #print "min, max", min_x, max_x, min_y, max_y, min_z, max_z
    dim_x = max_x-min_x+3
    dim_y = max_y-min_y+3
    dim_z = max_z-min_z+3
    data = numpy.zeros((dim_x, dim_y, dim_z))
    
    #print dim_x, dim_y, dim_z
    count = 0
    for id in self.verts.keys():
        x, y, z = [ int( math.floor( co ) ) for co in self.verts[id] ]
        if y-min_y >= dim_y or z-min_z >= dim_z or x-min_x>=dim_x:
            print x, y, z
        if data[x-min_x,y-min_y,z-min_z] == 0:
            data[x-min_x,y-min_y,z-min_z]+= 1
            count += 1
    '''        
    for id in self.faces.keys():
      vs = self.faces[id]
      #print vs
      ( mx_x, mx_y, mx_z ) = ( -9999, -9999, -9999 )
      ( mn_x, mn_y, mn_z ) = ( 9999, 9999, 9999 )
      for v in vs:
        if v in self.verts.keys():
          x, y, z = [ int( math.floor( co ) ) for co in self.verts[v] ]
          #print v, self.verts[v], x, y, z
          #if int(id)<10: print x, y, z
          mx_x = max( mx_x, x )
          mx_y = max( mx_y, y )
          mx_z = max( mx_z, z )
          mn_x = min( mn_x, x )
          mn_y = min( mn_y, y )
          mn_z = min( mn_z, z )
      #if mx_x - mn_x > 1 or mx_y - mn_y > 1 or mx_z - mn_z > 1: print mx_x - mn_x, mx_y - mn_y, mx_z - mn_z  
      #print "x,y,z", mx_x, mx_y, mx_z, mn_x, mn_y, mn_z
      for x in range( mn_x, mx_x + 1):
        for y in range( mn_y, mx_y + 1):
          for z in range( mn_z, mx_z + 1):
            #if x
            #print x-min_x, y-min_y, z-min_z
            if data[x-min_x,y-min_y,z-min_z] == 0:
              data[x-min_x,y-min_y,z-min_z]+= 1
              count += 1
    '''

    self.no_of_filled_voxels = count
    #print "dim", data.shape, "count", count
    self.voxels = data
    self.is_voxelized = True
    return data

  def print_voxels(self):
    z = 0
    (max_x,max_y,max_z)= self.voxels.shape
    if z > 0:
      from_z = z-1
      to_z = z
    else:
      from_z = 0
      to_z = max_z
    retstr = ""
    count = 0
    for z in range( from_z, to_z):
      for y in range( max_y ):
        retstr += "|"
        for x in range( max_x ):
          n = int(self.voxels[x,y,z])
          if n != 0:
            if n > 9 : n = 9
            retstr += str(n)
            count += 1
          else:
            retstr += " "
        retstr += "|\n"
      retstr += str(z)+"------------\n"
    print_log( self.name )
    print_log( retstr )
    print self.name
    print retstr
    return count
    
  def voxel_as_vector(self):
    x, y, z = self.voxels.shape
    vlen = x * y * z
    return self.voxels.reshape( vlen, 1 )

  def calculate_D2(self):
    D2_dist_list = []
    for k1 in self.verts.keys():
      for k2 in self.verts.keys() :
        if k1 != k2:
          x1, y1, z1= self.verts[k1]
          x2, y2, z2= self.verts[k1]
          dist = ((x2-x1)**2.0 + (y2-y1)**2.0 + (z2-z1)**2.0 ) ** 0.5
          D2_dist_list.append( dist )
    max_d = max( D2_dist_list )
    min_d = min( D2_dist_list )
    self.max_D2_dist = max_d
    self.min_D2_dist = min_d
    self.D2_dist_list = D2_dist_list
  def get_D2_distribution(self, max_dist, no_of_bin):
    bin_size = float( max_dist ) / float( no_of_bin )
    bins = numpy.zeros(no_of_bin)
    c = 0
    ks = self.verts.keys()
    
    for i in range( len( ks ) - 1 ):
      #print i
      for j in range( i+1, len(ks)):
          x1, y1, z1= self.verts[ks[i]]
          x2, y2, z2= self.verts[ks[j]]
          dist = ((x2-x1)**2.0 + (y2-y1)**2.0 + (z2-z1)**2.0 ) ** 0.5
          bin_idx = int( math.floor( float( dist ) / float( bin_size ) ) )
      #bin_idx = int( math.floor( bin_idx ) )
          #if c < 10:
          #  print bin_idx, dist
          #  c += 1
          bins[bin_idx] += 1
    self.D2_dist_list = bins
    self.D2_dist_list_pct = bins / len( self.verts.keys() )
    return bins
  def get_dist_distribution(self, max_dist, no_of_bin):
    bin_size = float( max_dist ) / float( no_of_bin )
    bins = numpy.zeros(no_of_bin+1)
    
    for dist in self.dists.values():
          bin_idx = int( math.floor( float( dist ) / float( bin_size ) ) )
      #bin_idx = int( math.floor( bin_idx ) )
          #if c < 10:
          #  print bin_idx, dist
          #  c += 1
          #print dist, bin_size, bin_idx, len( bins )
          bins[bin_idx] += 1
    self.dist_dist_list = bins
    self.dist_dist_list_pct = bins / len( self.verts.keys() )
    return bins

  def calculate_spherical_coordinate(self):
    for id in self.verts.keys():
      x,y,z = self.verts[id]
      r = ( x**2.0 +y**2.0+z**2.0 ) ** 0.5
      theta = math.acos( z / r )
      rho = math.atan2( y, x )
      self.verts_in_sphere[id] = [ r, theta, rho ]
      
  def get_spherical_distribution(self, max_r, r_div, theta_div, phi_div ):
    unit_r = max_r / r_div
    unit_theta = math.pi * 2 / theta_div
    unit_phi = math.pi * 2 / phi_div
    bins = numpy.zeros( ( r_div, theta_div, phi_div ))
    for id in self.verts_in_sphere.keys():
      r, theta, phi = self.verts_in_sphere[id]
      r_idx = int( math.floor( r / unit_r ) )
      theta_idx = int( math.floor( theta / unit_theta ) )
      phi_idx = int( math.floor( phi / unit_phi ) )
      bins[r_idx, theta_idx, phi_idx ] += 1
    self.sp_dist = bins
    self.sp_dist_pct = bins / len( self.verts_in_sphere.keys() )
    return bins

  def compute_distance( self, a_obj, keyword ):
    sum_sq_diff = 0
    if keyword == "SECSHELL":
      r,t,p = self.sp_dist.shape
      for i in range(r):
        for j in range(t):
          for k in range(p):
            diff = self.sp_dist_pct[i,j,k] - a_obj.sp_dist_pct[i,j,k]
            sum_sq_diff += diff ** 2
      euc_dist = ( sum_sq_diff ** 0.5 ) / r*t*p
      return euc_dist
    elif keyword == "D2":
      for i in range( len( self.D2_dist_list )):
        diff = self.D2_dist_list_pct[i] - a_obj.D2_dist_list_pct[i]
        sum_sq_diff += diff**2
      euc_dist = ( sum_sq_diff ** 0.5 ) / len( self.D2_dist_list )
      return euc_dist
    elif keyword == "SHELL":
      for i in range( len( self.dist_dist_list )):
        diff = self.dist_dist_list_pct[i] - a_obj.dist_dist_list_pct[i]
        sum_sq_diff += diff**2
      euc_dist = ( sum_sq_diff ** 0.5 ) / len( self.dist_dist_list )
      return euc_dist
    elif keyword == "VOXEL":
      x,y,z = self.voxels.shape
      for i in range(x):
        for j in range(y):
          for k in range(z):
            diff = self.voxels[i,j,k] - a_obj.voxels[i,j,k]
            sum_sq_diff += diff ** 2
      euc_dist = ( sum_sq_diff ** 0.5 ) / x*y*z
      return euc_dist      

nums = [ 1, 5, 6, 23, 31, 110, 126, 263, 323, 325 ]
obj_list = []
fs = []
vxs = []
sizes = []
rotated_vs = []
fit_max = 7.0

def convert_obj_into_pickle( nvert = 5000 ):
    files = os.listdir( "D:/voxelizer_data/Coral_OBJ/")
    for fn in files:
        fn = fn.lower()

    ''' nvert pickle processing '''
    for fn in files: #nums:
    #fname = "Crystal_" + str( n ) + ".obj"
        fname = "D:/voxelizer_data/Coral_OBJ/" + fn
        ( name, ext ) = os.path.splitext( fn )
        if ext != ".obj":
            continue
        obj = ThreeDShape()
        print "loading", fname + "...", 
        obj.OpenObjFile( fname )
        
        print obj.no_of_vertices, "vertices", 
        obj.Simplify( nvert )
        print "simplified to", obj.no_of_vertices, "vertices"
        pkl1_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_original/" + name + ".pkl"
        if not os.path.exists( pkl1_fname ):
            obj.SaveAsPickle( pkl1_fname )


def load_files( nvert = 5000 ):
    max_abs_x = -9999
    max_abs_y = -9999
    max_abs_z = -9999
    max_dist = -9999
    real_max = -9999
    files = os.listdir( "D:/voxelizer_data/Coral_OBJ/")
    print files
    #for fn in files:
        #fn = fn.lower()

    ''' restore pickle and normalize '''
    for fn in files:
        ( name, ext ) = os.path.splitext( fn )
        if ext != ".obj": continue
        pkl_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_original/" + name + ".pkl"
        obj = ThreeDShape()
        obj.RestoreFromPickle( pkl_fname )
        obj.filename = name
        #print name, point_of_origin_data[name]
        
        point_of_origin = point_of_origin_data[name]
        #print point_of_origin
        pt = point_of_origin.split( )
        #print pt
        obj.point_of_origin = [ float(x) for x in pt ]
        #print obj.point_of_origin
        
        if obj.is_centered == False:
            #print "origin before center", obj.point_of_origin
            obj.center()
            #print "origin after center", obj.point_of_origin
        csize = obj.get_centroid_size( True )
        #print "before remove outlier", object.max_dist, object.min_dist, object.avg_dist
        if obj.outlier_removed == False:
            obj.remove_outlier()
            obj.center()
        if obj.is_aligned == False:
            #obj.align()
            #print"before align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            obj.align_using_point_of_origin()
            #print"after origin align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            obj.align_on_xy_plane()
            #print"after xy align"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #print "origin after align", obj.point_of_origin
            obj.translate_using_origin()
            #print"after translate"
            #for k in obj.verts.keys()[0:9]:
            #  print obj.verts[k]
            #print "origin after translate", obj.point_of_origin
        csize = obj.get_centroid_size( True )
        #print "after remove outlier", object.max_dist, object.min_dist, object.avg_dist
        #print object.avg_dist
        #print_log( fname + "\n")
        #print_log( "\n".join( [ fname, str(object.no_of_vertices), str(object.get_centroid_size()) ] ) )
        obj.scale( (1.0/obj.avg_dist) )
        obj.get_centroid_size(True)

        #print "after scale", object.max_dist, object.min_dist, object.avg_dist
        max_abs_x = max( abs( obj.max_x ) , abs( obj.min_x ), max_abs_x )
        max_abs_y = max( abs( obj.max_y ) , abs( obj.min_y ), max_abs_y )
        max_abs_z = max( abs( obj.max_z ) , abs( obj.min_z ), max_abs_z )
        max_dist = max( obj.max_dist, max_dist )
        real_max = max( max_abs_x, max_abs_y, max_abs_z, real_max )

        obj_list.append( obj )
    
    #rotated_vs.append( rotated_v )
    #fs.append( f )

    factor = fit_max / max_dist
#print real_max, factor, max_dist

    print "scaling..."
    for obj in obj_list:
  #print "before", obj.get_centroid_size(), 
  #print obj.min_dist, obj.max_dist
        obj.scale( factor ) 
        obj.scale_factor = factor
        #obj.calculate_D2()
        #print obj.name
        #print "after", obj.get_centroid_size(),
        #print obj.min_dist, obj.max_dist
    print "scaling done!"
    max_x = math.ceil( max( [ obj.max_x for obj in obj_list ]) )
    min_x = math.floor( min( [ obj.min_x for obj in obj_list ]) )
    max_y = math.ceil( max( [ obj.max_y for obj in obj_list ]) )
    min_y = math.floor( min( [ obj.min_y for obj in obj_list ]) )
    max_z = math.ceil( max( [ obj.max_z for obj in obj_list ]) )
    min_z = math.floor( min( [ obj.min_z for obj in obj_list ]) )
    print max_x, min_x, max_y, min_y, max_z, min_z

    for obj in obj_list:
        if obj.is_voxelized == False:
            #print "make voxels"
            obj.get_voxels( min_x, max_x, min_y, max_y, min_z, max_z )
            #obj.print_voxels()
  
    for obj in obj_list:
        pkl_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_processed/" + obj.filename + ".pkl"
        if not os.path.exists( pkl_fname ):
            obj.SaveAsPickle( pkl_fname )

    tps_fname = "D:/voxelizer_data/Coral_" + str( nvert ) + "_tps/" + "coral_" + str(nvert) + ".tps"
    tps_string = ""
    for obj in obj_list:
        tps_string += obj.ToTpsString()
    f = open( tps_fname, "wb" )
    f.write( tps_string )
    f.close()

#convert_obj_into_pickle()
#sys.exit()
load_files()
#sys.exit()
#sys.exit()
#max_coord = max( [ math.fabs(x) for x in [ max_x, min_x, max_y, min_y, max_z, min_z ] ])
#print "max min x, y, z", max_x, min_x, max_y, min_y, max_z, min_z
#print "int max min x, y, z", math.ceil(max_x), math.floor(min_x)

#shape = [ max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1 ]
#shape_matrix = numpy.zeros( ( shape[0]*shape[1]*shape[2], len( nums ) ) )

'''
if False:
  descriptor_list = [ "SECSHELL", "VOXEL" ]
  no_of_object = len( object_list ) 
  
  import random
  
  random.seed()  
  
  descriptor = "VOXEL"
  
  theta_div = 6
  phi_div = 6
  r_div = 10
  
  for l in range(no_of_object-1):
    for k in range(l+1,no_of_object):
      obj1 = object_list[l]
      obj2 = object_list[k]
      print "obj1", obj1.name, 
      print "obj2", obj2.name
      distance_list = []
      count_ge = 0
      count_lt = 0
      for kk in obj1.verts.keys():
        obj1.verts[kk] = obj1.scaled_verts[kk]
      for kk in obj2.verts.keys():
        obj2.verts[kk] = obj2.scaled_verts[kk]
      if descriptor == "VOXEL":
        obj1.get_voxels( -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max ) 
        obj2.get_voxels( -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max ) 
      elif descriptor == "SECSHELL":
        obj1.calculate_spherical_coordinate()
        obj1.get_spherical_distribution( fit_max + 1, r_div, theta_div, phi_div)
        obj2.calculate_spherical_coordinate()
        obj2.get_spherical_distribution( fit_max + 1, r_div, theta_div, phi_div)
      
      #obj2.get_voxels( min_x, max_x, min_y, max_y, min_z, max_z )
      aligned_distance = obj1.compute_distance( obj2, descriptor )
      print "aligned_distance", aligned_distance
      
      for i in range( 100 ):
        phi = random.random() * 2 * math.pi
        theta = random.random() * math.pi
        obj2.rotate( theta, phi )
        if descriptor == "VOXEL":
          obj2.get_voxels( -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max, -1.0 * fit_max, fit_max ) 
        elif descriptor == "SECSHELL":
          obj2.calculate_spherical_coordinate()
          obj2.get_spherical_distribution( fit_max + 1, r_div, theta_div, phi_div)
        #obj.calculate_spherical_coordinate()
        #sp_dist = obj.get_spherical_distribution( fit_max + 1, r_div, theta_div, phi_div)
        
        dist = obj1.compute_distance( obj2, descriptor )
        #print phi, theta, "distance:", dist
        #print dist
        distance_list.append( dist )
        if dist < aligned_distance:
          count_lt += 1
        else:
          count_ge += 1
      print l+1, "vs.", k+1, "lt", count_lt, "ge", count_ge
      print "\t".join( [ str(x) for x in distance_list ] )
  
  print "alignment check done"
'''


if True:
  descriptor_list = [ "VOXEL" ] #"SHELL", "SECSHELL" , "D2" ]
  no_of_object = len( obj_list ) 
  
  for descriptor in descriptor_list:
    first = True
    print "getting", descriptor, "distribution"
    i = 0 
    for obj in obj_list:
      print obj.name + "\t" + descriptor + "\t",
      if descriptor == "SECSHELL":
        theta_div = 6
        phi_div = 6
        r_div = 10
        obj.calculate_spherical_coordinate()
        sp_dist = obj.get_spherical_distribution( fit_max + 1, r_div, theta_div, phi_div)
        sp_vec = sp_dist.reshape( ( ( r_div )  * theta_div * phi_div ) )
        print "\t", "\t".join( [ str( x ) for x in sp_vec[:] ] )
        if first:
          first = False
          shape_matrix = numpy.zeros( ( len( sp_vec ), no_of_object ) )
        shape_matrix[:,i] = sp_vec[:]
        shape_matrix[:,i] /= obj.no_of_vertices
      elif descriptor == "SHELL":
        no_of_shells = 50
        dist_dist = obj.get_dist_distribution( fit_max, no_of_shells )
        print "\t" + "\t".join( [ str( d ) for d in dist_dist ] )
        if first:
          first = False
          shape_matrix = numpy.zeros( (no_of_shells+1,no_of_object))
        print shape_matrix.shape
        print len( dist_dist )
        shape_matrix[:,i] = dist_dist[:]
        shape_matrix[:,i] /= obj.no_of_vertices
      elif descriptor == "D2":
        d2_dist = obj.get_D2_distribution( fit_max * 2 + 1, 100 )
        print "\t".join( [ str( d ) for d in d2_dist ] )
        #print max_x, min_x, max_y, min_y, max_z, min_z, len( v.keys() ), count
        if first:
          first = False
          shape_matrix = numpy.zeros( (len(d2_dist),no_of_object))
        shape_matrix[:,i] = d2_dist[:]
        shape_matrix[:,i] /= ( obj.no_of_vertices ** 2 )
      elif descriptor == "VOXEL":
        
        #vx = obj.get_voxels( min_x, max_x, min_y, max_y, min_z, max_z )
        #object.print_voxels()
        v = obj.voxel_as_vector()
        print "\t".join( [ str( d ) for d in v[:,0]] )
        if i == 0:
          x,y = v.shape
          print "n voxel", x, "=",
          #print max_x - min_x, max_y - min_y, max_z - min_z
          shape_matrix = numpy.zeros( (x,no_of_object))
        #print v.shape
        #print shape_matrix.shape
        shape_matrix[:,i] = v[:,0]
      i += 1
  
    for i in range( no_of_object ):
      print obj_list[i].name + "\t" + descriptor + "\t" + "\t".join( [ str( s ) for s in shape_matrix[:,i]] )
  
        
    print descriptor, "distance matrix"
    dist_matrix = numpy.zeros( ( no_of_object, no_of_object ) )
    for i in range( no_of_object ):
      for j in range( len( obj_list ) ):
        o1 = obj_list[i]
        o2 = obj_list[j]
        val = o1.compute_distance( o2, descriptor )
        dist_matrix[i,j] = val
    
    for i in range( no_of_object ):
      print obj_list[i].name + "\t" + "\t".join( [ str( x ) for x in dist_matrix[:,i] ] )
  
    pca = MdPrincipalComponent()
    pca.SetMatrix( shape_matrix )
    #print "a"
    pca.Analyze()
    print descriptor, "PCA result"
    print "\t".join( [ str(pct) for pct in pca.eigen_value_percentages[0:10] ] )
    #print pca.eigen_value_percentages[0:10]
    #for 
    for i in range(no_of_object):
      print "\t".join( [ str( val ) for val in pca.rotated_matrix[0:10,i] ])
  


#i = 0
#for vx in vxs:
  #new_vx = vx.reshape( ( x*y*z, 1 ) ) 
 # print new_vx.shape
#  shape_matrix[:,i] = new_vx[:,0] 
#  i+= 1


print "preparing shape matrix..."
if False:
  for i in range( len( obj_list ) ):
    obj = obj_list[i]
    print obj.name
    obj.OpenObjFile( obj.name, True, False )
    obj.center()
    csize = obj.get_centroid_size( True )
    print "centroid size 1", csize
    #print "before remove outlier", object.max_dist, object.min_dist, object.avg_dist
    obj.remove_outlier()
    obj.center()
    obj.align()
    obj.scale( (1.0/obj.avg_dist) )
    csize = obj.get_centroid_size( True )
    print "centroid size 2", csize
    obj.scale( obj.scale_factor ) 
    csize = obj.get_centroid_size( True )
    print "centroid size 3", csize
    #print "min max", min_x, max_x, min_y, max_y, min_z, max_z 
    #vx = obj.get_voxels( min_x, max_x, min_y, max_y, min_z, max_z )
    print "voxel processing done"
    obj.Simplify()
    print "simplified!"
    obj.SaveAsPickle()
    print "save as pickle"
    #print vx.shape
    #vxs.append( vx ) 
    #fname = "Crystal_" + str( nums[i] ) + ".obj"
    #print_log( fname )
    obj.print_voxels()
    v = obj.voxel_as_vector()
    if i == 0:
      x,y = v.shape
      shape_matrix4 = numpy.zeros( (x,len(obj_list)))
    #print v.shape
    #print shape_matrix.shape
    shape_matrix4[:,i] = v[:,0]

print "voxel distance matrix"
no_of_object = len( obj_list ) 
dist_matrix4 = numpy.zeros( ( no_of_object, no_of_object ) )
for i in range( no_of_object ):
  for j in range( len( obj_list ) ):
    o1 = obj_list[i]
    o2 = obj_list[j]
    val = o1.compute_distance( o2, "VOXEL" )
    dist_matrix4[i,j] = val

for i in range( no_of_object ):
  print obj_list[i].name + "\t" + "\t".join( [ str( x ) for x in dist_matrix4[:,i] ] )


pca = MdPrincipalComponent()
pca.SetMatrix( dist_matrix4 )
#print "a"
pca.Analyze()
print "\t".join( [ str(pct) for pct in pca.eigen_value_percentages[0:10] ] )
#print pca.eigen_value_percentages[0:10]
#for 
for i in range(10):
  print "\t".join( [ str( val ) for val in pca.rotated_matrix[0:10,i] ])




















''' this does not work 


max_pc1 = max( [ val for val in pca.rotated_matrix[0,:]])
min_pc1 = min( [ val for val in pca.rotated_matrix[0,:]])
max_pc2 = max( [ val for val in pca.rotated_matrix[1,:]])
min_pc2 = min( [ val for val in pca.rotated_matrix[1,:]])
for i in range(10):
  shape_explorer[:,i] = pca.rotated_matrix[:,i]
  shape_explorer[0,i] = max_pc1  
#print pca.rotated_matrix

unrotate = numpy.linalg.inv( pca.rotation_matrix )

h_shapes = numpy.dot( unrotate, shape_explorer )

for i in range(10):
  resulting_shape[:,0] = h_shapes[:,i]
  s = resulting_shape.reshape( object_list[0].voxels.shape )
  print_voxel_data( s )

def opendata( filepath ):
    f = open( filepath, 'r' )
    objdata = f.read()
    f.close()

    point = {}
    tps_lines = [ l.strip() for l in objdata.split( NEWLINE ) ]
    verts = {}
    faces = {}
    vert_exist = {}
    num_v = 1
    num_f = 1  
    scale = 8
    for line in tps_lines:
      line = line.strip() 
      fpoint = re.split( '\s+', line )
      if fpoint[0] == 'v':
        x, y, z = float( fpoint[1] ), float( fpoint[2] ), float( fpoint[3] )
        verts[num_v] = [ x/scale, y/scale, z/scale ]
        num_v += 1 
      if fpoint[0] == 'f':
        f_vert = []
        for point in fpoint[1:3]:
          p_split = point.split( "/" )
          if len( p_split ) > 0:
            v_idx = int( p_split[0] )
            f_vert.append( v_idx )
            vert_exist[v_idx] = 1
        #v1, v2, v3 = int( fpoint[1] ), int( fpoint[2] ), int( fpoint[3] )
        faces[num_f] = f_vert
        num_f += 1
    real_verts = {}
    for k in vert_exist.keys():
      real_verts[k] = verts[k]

      
    return real_verts, faces


def translate_to_zeroes( verts ): 
  ( max_x, max_y, max_z ) = ( -9999, -9999, -9999 )
  ( min_x, min_y, min_z ) = ( 9999, 9999, 9999 )
  #print len( verts )
  #return
  new_verts = {}
  x_sum, y_sum, z_sum = 0, 0, 0
  for id in verts.keys( ):
    x, y, z = verts[id]
    x_sum += x
    y_sum += y
    z_sum += z
    max_x = max( x, max_x )
    max_y = max( y, max_y )
    max_z = max( z, max_z )
    min_x = min( x, min_x )
    min_y = min( y, min_y )
    min_z = min( z, min_z )
  n_vert = len( verts.keys() )
  x_avg = x_sum / n_vert
  y_avg = y_sum / n_vert
  z_avg = z_sum / n_vert
  max_x -= x_avg
  max_y -= y_avg
  max_z -= z_avg
  min_x -= x_avg
  min_y -= y_avg
  min_z -= z_avg
  
  #print max_x, max_y, max_z, min_x, min_y, min_z
  for id in verts.keys( ):
    x, y, z = verts[id]
    verts[id] = [ x - x_avg, y - y_avg, z - z_avg ]
    #new_verts.setdefault( ( x - min_x, y - min_y, z - min_z ), set() ).add( id ) #[id] = [ x - min_x, y - min_y, z - min_z ]
  return verts, max_x, min_x, max_y, min_y, max_z, min_z
  
import numpy 

def voxelize2(verts, faces, max_x, max_y, max_z ):
  data = numpy.zeros((int(max_x*2+1), int(max_y*2+1), int(max_z*2+1)))
  for id in faces.keys():
    vs = faces[id]
    ( mx_x, mx_y, mx_z ) = ( -9999, -9999, -9999 )
    ( mn_x, mn_y, mn_z ) = ( 9999, 9999, 9999 )
    for v in vs:
      x, y, z = [ int( co ) for co in verts[v] ]
      mx_x = max( mx_x, x )
      mx_y = max( mx_y, y )
      mx_z = max( mx_z, z )
      mn_x = min( mn_x, x )
      mn_y = min( mn_y, y )
      mn_z = min( mn_z, z )
    #if mx_x - mn_x > 1 or mx_y - mn_y > 1 or mx_z - mn_z > 1: print mx_x - mn_x, mx_y - mn_y, mx_z - mn_z  
    for x in range( mn_x, mx_x +1 ):
      for y in range( mn_y, mx_y +1):
        for z in range( mn_z, mx_z +1):
          data[x+max_x,y+max_y,z+max_z] = 1
  #print "dim", data.shape
    
  return data
  for id in verts.keys( ):
    logstr += "\t".join( [ str( co ) for co in verts[id] ] ) + "\n"
    x, y, z = int( verts[id][0] ), int( verts[id][1] ), int( verts[id][2] )
    if data[x,y,z] < 9:
      data[x,y,z] = 1
  #f = open( "log.txt", "w+")
  #f.writelines( logstr )
  #f.close()
  return data
    
def voxelize(verts, faces):
  logstr = ""
  new_verts, max_x, max_y, max_z = translate_to_zeroes( verts )
  data = numpy.zeros((int(max_x+1), int(max_y+1), int(max_z+1)))
  for id in verts.keys( ):
    logstr += "\t".join( [ str( co ) for co in verts[id] ] ) + "\n"
    x, y, z = int( verts[id][0] ), int( verts[id][1] ), int( verts[id][2] )
    if data[x,y,z] < 9:
      data[x,y,z] += 1
  #f = open( "log.txt", "w+")
  #f.writelines( logstr )
  #f.close()
  return data
def get_next_pixel( x, y , dir, connectivity = 4 ):
  dir %= connectivity
  if connectivity == 4:
    if( dir == 0 ):
      x+=1
    elif dir== 1:
      y -= 1
    elif dir==2:
      x+=1
    elif dir==3:
      y+=1
  if connectivity == 8:
    if dir<4 and dir >0:
      y-= 1
    if dir > 4:
      y+=1
    if dir< 2 or dir> 6:
      x+=1
    if dir>2 and dir < 6:
      x-=1
  return x,y

def trace_border_from( voxel_data, x, y, z ):
  #print "trace_border_from", x, y, z
  border = []
  border.append( [ x, y ] )
  connectivity = 8
  curr = 0
  prev = -1
  dir = 3
  found = True
  while( found ):
    if connectivity == 8:
      if( int ( dir / 2 ) == ( dir / 2 ) ) : 
        dir += 7
      else:
        dir += 6
    else:
      dir = +3
    dir = dir % connectivity
    if len( border ) > 2 and border[curr] == border[1] and border[curr-1] == border[0]: break
    x, y = border[curr]
    print x, y, z, curr
    found = False
    for i in range(connectivity):
      new_x, new_y = get_next_pixel( x, y, i+dir, connectivity)
      print new_x, new_y, voxel_data[new_x, new_y, z]
      if int(voxel_data[new_x,new_y,z])!=0:
        found = True
        border.append( [new_x, new_y] )
        curr += 1
        break
  for b in border:
    if voxel_data[b[0],b[1],z] > 0:
      voxel_data[b[0],b[1],z] *= -1
      
  return voxel_data
def find_border( voxel_data ) :
  (max_x,max_y,max_z)= voxel_data.shape
  for z in range( min(max_z,5) ):
    for y in range( max_y ):
      for x in range( max_x ):
        #print "find border ", x,y,z
        if voxel_data[x,y,z] > 0:
          voxel_data[x,y,z] *= -1
          voxel_data = trace_border_from( voxel_data, x, y, z )
  return voxel_data

  return
def fill_external_space( voxel_data, z = -1 ):  
  if z > 0:
    from_z = z-1
    to_z = z
  else:
    from_z = 0
    to_z = max_z
  begin_x, begin_y = 0, 0
  #for z in range( from_z, to_z ):
    
    
  retstr = ""
'''
