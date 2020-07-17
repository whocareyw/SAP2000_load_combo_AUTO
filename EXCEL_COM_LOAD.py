import os
import csv

## 用于快速生成sap2000荷载组合

#组合文件地址定义
combolist_dir = r'C:\Users\2020055\Desktop\sap处理\py荷载组合\雪_标准组合216_220_39.csv'

# factor [组合系数,分项系数]
factor_D = [1, 1.0]
# D L T W S 分别为 恒 活 温度 风 雪  需提前在 loadcase 中定义好
D = ['SDL','SELF',factor_D]
factor_L = [0.7,1.0]
L = ['LIVE',factor_L]
factor_T = [0.6,1.0]
T = ['TEMPL','TEMPH',factor_T ]
factor_W = [0.6,1.0]
W = ['WIND00' ,'WIND10' ,'WIND20' ,'WIND30' ,'WIND40' ,'WIND50' ,'WIND60' ,'WIND70' ,'WIND80' ,'WIND90' ,
     'WIND100','WIND110','WIND120','WIND130','WIND140','WIND150','WIND160','WIND170','WIND180','WIND190',
     'WIND200','WIND210','WIND220','WIND230','WIND240','WIND250','WIND260','WIND270','WIND280','WIND290',
     'WIND300','WIND310','WIND320','WIND330','WIND340','WIND350',factor_W]
factor_S = [0.7,1.0]
S = ['SNOW',factor_S]

# example: CASE = [D,L,T,W]   第一个必须为恒载
def Combo_case(CASE): #[[Comboname0,(case0,factor0),...(casen,factorn)],...[Combonamen,(case0,factor0),...(casen,factorn)]]
    COMBO = [] #所有组合
    combo = [] #单个特定组合
    Case_Factor_List = []  #特定case与factor组合  [[case,factor_X],...]
    case_factor_list = []

    num = len(CASE)
    if num <= 0 :
        return print('至少输入一个荷载工况啊喂')

    if num > 0 :
        for i in range(0, len(CASE[0])-1 ) :
            case_factor_list.append([CASE[0][i],CASE[0][-1]])

    if num > 1 :
        for ii in range(0, len(CASE[1])-1 ) :
            if num == 2:
                case_factor_list.append([CASE[1][ii],CASE[1][-1]])
                new = [i for i in case_factor_list]
                Case_Factor_List.append(new)
                del case_factor_list[-1]
            else:
                if ii == 0 :
                    case_factor_list.append([CASE[1][ii],CASE[1][-1]])
                else :
                    del case_factor_list[-1]
                    case_factor_list.append([CASE[1][ii],CASE[1][-1]])

            if num > 2 :
                for iii in range(0, len(CASE[2])-1 ) :
                    if num == 3:
                        case_factor_list.append([CASE[2][iii],CASE[2][-1]])
                        new = [i for i in case_factor_list]
                        Case_Factor_List.append(new)
                        del case_factor_list[-1]
                    else:
                        if iii == 0 :
                            case_factor_list.append([CASE[2][iii],CASE[2][-1]])
                        else :
                            del case_factor_list[-1]
                            case_factor_list.append([CASE[2][iii],CASE[2][-1]])

                    if num > 3 :
                        for iiii in range(0, len(CASE[3])-1 ) :
                            if num == 4:
                                case_factor_list.append([CASE[3][iiii],CASE[3][-1]])
                                new = [i for i in case_factor_list]
                                Case_Factor_List.append(new)
                                #print(case_factor_list)
                                del case_factor_list[-1]
    #以上代码  生成了 Case_Factor_List 即 [[case,factor_X],...]

    for case_factor_list in Case_Factor_List:
        single_case_factor = []  #[(case0,factor0),...(casen,factorn)]
        for num_D in range(0,len(CASE[0])-1):
            factor = round(case_factor_list[0][1][0]*case_factor_list[0][1][1],2)
            single_case_factor.append((case_factor_list[0][0],factor))
            Comboname_D = 'SBZ' +'_'+str(factor)+'D'
            del case_factor_list[0]
        for num_L in range(0, len(case_factor_list)):
            factor = round(case_factor_list[num_L][1][1],2)
            single_case_factor.append((case_factor_list[num_L][0],factor))
            Comboname = Comboname_D +'_'+ str(factor)+case_factor_list[num_L][0]
            REST = [i for i in case_factor_list]
            del REST[num_L]
            for rest_case in REST :
                factor = round(rest_case[1][0]*rest_case[1][1],2)
                single_case_factor.append((rest_case[0],factor))
                Comboname = Comboname +'_'+ str(factor)+rest_case[0]
            combo = [Comboname, single_case_factor]

            COMBO.append(combo)
            single_case_factor = single_case_factor[0:len(CASE[0])-1]
    return COMBO

def printexcel(COMBO):

        for combo in COMBO :
            comboname = combo[0]
            for i in range(0,len(combo[-1])) :
                casename = combo[-1][i][0]
                scalefactor = combo[-1][i][-1]
                if i == 0 :
                    line = [comboname, 'Linear Add' ,'NO' ,casename , None ,scalefactor]
                    writer.writerow(line)
                else :
                    line = [comboname, None , None , casename  , None ,scalefactor]
                    writer.writerow(line)

#print(Combo_case([D,W,T]))

with open(combolist_dir,"w", newline='') as f:
    writer = csv.writer(f)
    printexcel(Combo_case([D,S]))
    printexcel(Combo_case([D,W]))
    printexcel(Combo_case([D,T]))
    printexcel(Combo_case([D,S,W]))
    printexcel(Combo_case([D,T,S]))
    printexcel(Combo_case([D,T,W]))
    printexcel(Combo_case([D,S,W,T]))




















#
