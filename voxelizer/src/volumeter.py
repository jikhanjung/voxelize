'''
Created on 2012. 11. 20.

@author: jikhanjung
'''

from ThreeDShape import ThreeDShape
from datetime import datetime
import math
import os
import wx

''' read file '''
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

def traverse( a_voxel, a_x, a_y, a_z, bgcolor, point_list ):
    width = len( a_voxel )
    height = len( a_voxel[0] )
    
    dir_list = [ [ 1, 0 ], [0, 1], [-1, 0], [0, -1] ]
    if a_x >= width-1 or a_x < 0: 
        return -1
    if a_y >= height-1 or a_y < 0: 
        return -1
    been_there = -1

    color = a_voxel[a_x][a_y][a_z]
    print a_x, a_y, color
    a_voxel[a_x][a_y][a_z] = been_there
    
    if color == bgcolor:
        point_list.append( [ a_x, a_y ] )
        curr_x = a_x
        curr_y = a_y
        for l_dir in dir_list:
            print a_x, a_y, l_dir
            a_x = curr_x + l_dir[0]
            a_y = curr_y + l_dir[1]
            val = traverse( a_voxel, a_x, a_y, a_z, bgcolor, point_list )
        #voxel[curr_x][curr_y][z] = been_there

def get_outer_area( a_voxel, l_z ):
    l_x = 0
    l_y = 0
    
    width = len( a_voxel )
    height = len( a_voxel[0] )
    dir_list = [ [ 1, 0 ], [0, 1], [-1, 0], [0, -1] ]
    
    bgcolor = a_voxel[l_x][l_y][l_z]

    point_list = []
    to_traverse_list = []
    been_there = [[0 for l_a in range(height)] for l_b in range(width) ]

    to_traverse_list.append( [l_x,l_y] )
    been_there[l_x][l_y] = 1
    while  len( to_traverse_list ) > 0 :
        curr_x, curr_y = to_traverse_list.pop(0)
        color = a_voxel[curr_x][curr_y][l_z]
        #print curr_x, curr_y, color
        if color == bgcolor:
            point_list.append( [curr_x,curr_y] )
            for l_dir in dir_list:
                next_x = curr_x + l_dir[0]
                next_y = curr_y + l_dir[1]
                #print next_x, next_y,
                if next_x <= width - 1 and next_x >= 0 and next_y >= 0 and next_y <= height-1 and been_there[next_x][next_y]==0:
                    to_traverse_list.append( [next_x, next_y] )
                    been_there[next_x][next_y] = 1
                    #print "added",
                #print ""
    #print "black count", black_count, "total area", width * height, "outer area", len( point_list )   
    #point_list.sort()
    #print point_list 
    area = width * height - len( point_list )
    return area, point_list

def get_area( p1, p2, p3 ):
    l_x1, l_y1, l_z1 = p1
    l_x2, l_y2, l_z2 = p2
    l_x3, l_y3, l_z3 = p3
    l_v1 = [ l_x3-l_x1, l_y3-l_y1, l_z3-l_z1 ]
    l_v2 = [ l_x2-l_x1, l_y2-l_y1, l_z2-l_z1 ]
    vabs = [ l_v1[1] * l_v2[2] - l_v1[2] * l_v2[1], l_v1[2] * l_v2[0] - l_v1[0] * l_v2[2], l_v1[0] * l_v2[1] - l_v1[1] * l_v2[0] ] 
    area = 0.5 * math.sqrt( vabs[0] ** 2 + vabs[1] ** 2 + vabs[2]** 2 ) 
    return area

def add_vertice( a_x, a_y, a_z, vertices, vert_list ):
    if vertices[a_x][a_y][a_z] == 0:
        vertices[a_x][a_y][a_z] = len( vert_list ) + 1
        vert_list.append( [a_x,a_y,a_z] )
    return vertices[a_x][a_y][a_z]

def check_adjacent_voxels( x, y, z, max_x, max_y, max_z, voxel, vertices, vert_list, face_list ):
    '''
    adjacent_delta = [ [ 1, 0, 0 ], [ -1, 0, 0 ], [ 0, -1, 0 ], [0, 1, 0], [0, 0, 1], [0, 0, -1] ]
    face_normal_direction = [ [ [0,0], [1,0], [1,1], [0,1] ], [ [0,0], [0,1], [1,1], [1,0] ] ]
    
    for adjidx in range( len( adjacent_delta ) ):
        at_the_edge = False
        dx, dy, dz = adjacent_delta[adjidx]
        if x+dx < 0 or x+dx >= max_x: at_the_edge = True
        if y+dy < 0 or y+dy >= max_y: at_the_edge = True
        if z+dz < 0 or z+dz >= max_z: at_the_edge = True
        #if not at_the_edge:
        #    if voxel[]
        if at_the_edge or voxel[x+dx][y+dy][z+dz] == 0:
            new_face = []
            normal_direction = face_normal_direction[adjidx%2]
            for i, j in normal_direction:
                add_vertice( x+dx, y+i, z+j, new_face, vertices, vert_list )
            face_list.append( new_face )
    return
    '''
    count = 0
    adj_x = x+1
    if adj_x == len( voxel ) or voxel[adj_x][y][z] == 0:
        new_face = []
        for i, j in [ [0,0], [1,0], [1,1], [0,1] ]:
            new_face.append( add_vertice( x+1, y+i, z+j, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1
    adj_x = x-1
    if adj_x < 0 or voxel[adj_x][y][z] == 0:
        new_face = []
        for i, j in [ [0,0], [0,1], [1,1], [1,0] ]:
            new_face.append( add_vertice( x, y+i, z+j, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1

    adj_y = y+1
    if adj_y == len( voxel[0] ) or voxel[x][adj_y][z] == 0:
        new_face = []
        for i, j in [ [0,0], [0,1], [1,1], [1,0] ]:
            new_face.append( add_vertice( x+i, y+1, z+j, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1

    adj_y = y-1
    if adj_y < 0 or voxel[x][adj_y][z] == 0:
        new_face = []
        for i, j in [ [0,0], [1,0], [1,1], [0,1] ]:
            new_face.append( add_vertice( x+i, y, z+j, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1

    adj_z = z+1
    if adj_z == len( voxel[0][0] ) or voxel[x][y][adj_z] == 0:
        new_face = []
        for i, j in [ [0,0], [1,0], [1,1], [0,1] ]:
            new_face.append( add_vertice( x+i, y+j, z+1, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1

    adj_z = z-1
    if adj_z < 0 or voxel[x][y][adj_z] == 0:
        new_face = []
        for i, j in [ [0,0], [0,1], [1,1], [1,0] ]:
            new_face.append( add_vertice( x+i, y+j, z, vertices, vert_list ) )
        face_list.append( new_face )
        count += 1

    return count


def voxel_to_obj( a_voxel, level = -1 ):
    vertices = [[[0 for z in range(len(a_voxel[0][0])+1)] for y in range(len(a_voxel[0])+1)] for x in range( len(a_voxel)+1) ]

    ''' make obj file ''' 
    l_tstart = datetime.now()
    vert_list = []
    face_list = []
    max_x = len( a_voxel )
    max_y = len( a_voxel[0] ) 
    max_z = len( a_voxel[0][0] )
    for x in range( max_x ):
        for y in range( max_y ):
            for z in range( max_z ):
                if a_voxel[x][y][z] == 1:
                    ret_val = check_adjacent_voxels( x, y, z, max_x, max_y, max_z, a_voxel, vertices, vert_list, face_list )
                    if False:
                        print ret_val
                        
                '''            
                if a_voxel[x][y][z] == 1:
                    v1 = [x-1.0, y-1.0, z-1.0]
                    v2 = [x, y-1.0, z-1.0]
                    v3 = [x-1.0,y,z-1.0]
                    v4 = [x,y,z-1.0]
                    v5 = [x-1.0, y-1.0,z]
                    v6 = [x,y-1.0,z]
                    v7 = [x-1.0,y,z]
                    v8 = [x,y,z]
                    idx = len( vert_list )
                    vert_list.append( v1 )
                    vert_list.append( v2 )
                    vert_list.append( v3 )
                    vert_list.append( v4 )
                    vert_list.append( v5 )
                    vert_list.append( v6 )
                    vert_list.append( v7 )
                    vert_list.append( v8 )
                    face_list.append( [ idx+1, idx+3, idx+4, idx+2 ] )
                    face_list.append( [ idx+1, idx+2, idx+6, idx+5 ] )
                    face_list.append( [ idx+1, idx+5, idx+7, idx+3 ] )
                    face_list.append( [ idx+2, idx+4, idx+8, idx+6 ] )
                    face_list.append( [ idx+5, idx+6, idx+8, idx+7 ] )
                    face_list.append( [ idx+3, idx+7, idx+8, idx+4 ] )
                '''
    objstr = ""
    for v in vert_list:
        objstr += "v " + str(v[0]) + " " + str( v[1] ) + " " + str( v[2] ) +"\n"
    objstr += "g all\n"
    for f in face_list:
        objstr += "f " + str(f[0]) + " " + str( f[1] ) + " " + str( f[2] ) + " " + str( f[3] ) + "\n"
    filename = "e:/voxelized_obj/" + name + "_voxel" 
    if level >= 0: 
        filename += "_%02d" %tuple([level]) 
    filename += ".obj"
    fh = file( filename, 'w' )
    
    fh.write( objstr )
    fh.close()
    
        
    l_tend = datetime.now()

    l_et = l_tstart - l_tend
    if False:
        print l_et



files = os.listdir( "D:/voxelizer_data/Coral_OBJ/")
for fn in files:
    fn = fn.lower()

for fn in files: #nums:
#fname = "Crystal_" + str( n ) + ".obj"
    fname = "D:/voxelizer_data/Coral_OBJ/" + fn
    ( name, ext ) = os.path.splitext( fn )
    if ext != ".obj":
        continue
    obj = ThreeDShape()
    point_of_origin = point_of_origin_data[name]
    pt = point_of_origin.split( )
    #print pt
    obj.point_of_origin = [ float(x) for x in pt ]
    print "loading", fname + "..." 
    obj.OpenObjFile( fname )
    #print obj.no_of_vertices, "vertices", 
    obj.center()
    obj.get_centroid_size()
    obj.remove_outlier()
    obj.center()
    count = 0
    total_area = 0
    for k in obj.faces.keys():
        v1, v2, v3 = obj.faces[k]
        x1, y1, z1 = obj.verts[v1]
        x2, y2, z2 = obj.verts[v2]
        x3, y3, z3 = obj.verts[v3]
        #print "[", x1, y1, z1, "]",
        #print "[", x2, y2, z2, "]",
        #print "[", x3, y3, z3, "]",
        count += 1
        #area = get_area( obj.verts[v1], obj.verts[v2], obj.verts[v3] )
        #total_area += area
        #print "area:", area
    #print obj.max_x, obj.min_x, obj.max_y, obj.min_y, obj.max_z, obj.min_z
    int_min_x = int( math.floor( obj.min_x ) )
    int_min_y = int( math.floor( obj.min_y ) )
    int_min_z = int( math.floor( obj.min_z ) )
    init_x = int( math.ceil( obj.max_x ) - int_min_x )
    init_y = int( math.ceil( obj.max_y ) - int_min_y )
    init_z = int( math.ceil( obj.max_z ) - int_min_z ) 
    #print init_x, init_y, init_z

    factor = 1 
    for i in range(1):
        volume_z = [0 for z in range(int(init_z*factor)+2)]
        void_area_z = [0 for z in range(int(init_z*factor)+2)]
        voxel = [[[0 for z in range(int(init_z*factor)+2)] for y in range(int(init_y*factor)+2)] for x in range( int(init_x *factor)+2 ) ]
        new_voxel = [[[1 for z in range(len(voxel[0][0]))] for y in range(len(voxel[0]))] for x in range( len(voxel) ) ]
        for k in obj.verts.keys():
            x, y, z = obj.verts[k]
            x_idx = int( math.floor( ( x - int_min_x ) * factor ) )
            y_idx = int( math.floor( ( y - int_min_y ) * factor ) )
            z_idx = int( math.floor( ( z - int_min_z ) * factor ) )
            voxel[x_idx+1][y_idx+1][z_idx+1] = 1
            
        '''' make image stack '''        
        tstart = datetime.now()
        for z in range( len( voxel[0][0] )):
            volume_z[z], void_area_z[z] = get_outer_area( voxel[:],z ) 
            for x, y in void_area_z[z]:
                new_voxel[x][y][z] = 0

            l_img = wx.EmptyImage( len( voxel), len( voxel[0]) )
            for x in range( len( voxel ) ):
                for y in range( len( voxel[0] )):
                    if new_voxel[x][y][z] == 1:
                        l_img.SetRGB( x, y, 255, 255, 255 )
            filename = name + "-" + "%02d" %tuple([i]) + "_" + "%03d"%tuple([z])
            #print filename, 
            l_img.SaveFile( "e:/stack/" + filename + ".png", wx.BITMAP_TYPE_PNG )
        tend = datetime.now()
        voxel_to_obj( new_voxel )

        #print tend - tstart
        factor += 1.0  
    print name, "\t" + str( sum( volume_z ) ) + "\t" + str( total_area )
    #print "total_area", total_area
    