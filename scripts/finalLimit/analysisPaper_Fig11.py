# For long paper Figure 10

import pandas as pd
import os
import matplotlib
from numpy             import *
from ou_Axion_limit    import analyse, Glimit
from matplotlib.pyplot import *
from glob              import glob
from scipy.signal      import savgol_filter
from scipy             import interpolate
from scipy.optimize    import curve_fit
import mplhep as hep
hep.style.use(hep.style.ROOT)

INPUT_EXPERIMENT_FLODER = "others_experiment"
INPUT_limit_PATH        = "gayy_unc_updateFF_06July.txt"
OUTPUT_FILE_NAME        = "Figure11.png"


color_map ={
    "ADMX"   :"#7FF547",
    "HAYSTAC":"#FFDC4A",
    "CAPP"   :"#7157E8",
    "UF"     :"#9B6669",
    "RBF"    :"#534D6D",
    "CAST"   :"#9E7068"
}
########################################################################## functions
def ma_to_freq(ma):   # eat ev output GHz
    g = Glimit()
    return ma/( g.h_bar  * 2 * pi) * 1e-9

def freq_to_ma(freq): # eat GHz output ev
    g = Glimit()
    return freq *( g.h_bar  * 2 * pi) * 1e9

########################################################################## Read data
print(f"[*] Reading {INPUT_limit_PATH}\n")
df = pd.read_table(INPUT_limit_PATH,sep="\s+")
df.columns = ["Freq","limit_cen","noise_un","mis_un","QL_un","toal_un","Nan"]
print(df.head())


hein_limit_freq = df["Freq"     ].values * 1e9
center_limits   = df["limit_cen"].values
to_un           = df["toal_un"  ].values

upper__limits   = center_limits + sqrt(  to_un**2  )
lower__limits   = center_limits - sqrt(  to_un**2  )

######################################################################### remove two non-axion range

for i in range(len(hein_limit_freq)):
    if (4.747300e9<=hein_limit_freq[i] and  hein_limit_freq[i]<=4.747380e9):
        center_limits[i]   = None # np.nan
        upper__limits[i]   = None # np.nan
        lower__limits[i]   = None # np.nan
    if (4.710170e9<=hein_limit_freq[i] and  hein_limit_freq[i]<=4.710190e9):
        center_limits[i]   = None # np.nan
        upper__limits[i]   = None # np.nan
        lower__limits[i]   = None # np.nan


##########################################################################  plot
print(f"[*] Creating figures")


matplotlib.rcParams.update({'font.size': 14})

# create plot
fig, ax = subplots(squeeze = True,figsize = (10,8))
g       = Glimit()
fa_x    = linspace(0,8,10000)
ma_x    = freq_to_ma(fa_x)

KSVZ_g_a_gamma = 0.97 * ma_x * g.alpha /(pi * g.big_A * g.big_A)  * 1e9
DFSZ_g_a_gamma = 0.36 * ma_x * g.alpha /(pi * g.big_A * g.big_A)  * 1e9

ax.plot(fa_x , KSVZ_g_a_gamma,"b--",alpha=0.8,label="KSVZ")
ax.plot(fa_x , DFSZ_g_a_gamma,"r--",alpha=0.8,label="DFSZ")

ax.fill_between(fa_x,KSVZ_g_a_gamma*4,DFSZ_g_a_gamma/4,alpha=0.8,color="#C0C0C0",label="model region")

ax.text(4,  4e-15,"KSVZ",fontsize=12,color="blue",rotation=2,ha='center', va='center')
ax.text(4,1.5e-15,"DFSZ",fontsize=12,color="r"   ,rotation=2,ha='center', va='center')
ax.text(7,1.6e-15,"model region",fontsize=18,color="black",rotation=3,ha='center', va='center')


###########################################################################  plot other experiment

WANT = ["HAYSTAC","CAPP","ADMX","RBF","UF","CAST"]

for each_limit_file in glob(f"{INPUT_EXPERIMENT_FLODER}/*.csv"):
    flag = 0
    for want_ in WANT:
        if (want_ in each_limit_file):
            flag = 1
            this_color = color_map[want_]
            break
    
    if (not flag): continue
    if ("Projected" in each_limit_file):continue
    
    # read data
    df = pd.read_csv(each_limit_file,index_col=0)
    
    limit  = array(df["G_ap[GeV^-1]"].values,dtype=float)
    this_x = ma_to_freq(df["m_a [eV]"].values)
    
    if ("RBF" in each_limit_file):
        sort_index = argsort(this_x)
        this_x = this_x[sort_index]

    if ("CAST" in each_limit_file):
        new_x       = linspace(this_x[0],this_x[-1],1000)
        this_interp = interp(new_x , this_x, limit)
        limit       = this_interp 
        this_x      = new_x

    text_x = mean(this_x)
    text_y = min(limit) * 60
    if ("HAYSTAC"  in each_limit_file):
        text_y = text_y/4
        if ("highres" in each_limit_file):
            text_y = text_y/8

        
    if ("ADMX" in each_limit_file  and ("20" in each_limit_file or "SLIC" in each_limit_file)):
        ax.fill_between(this_x, limit,1,alpha=.3,color=this_color)
        continue
    else:
        ax.fill_between(this_x, limit,1,alpha=.3,color=this_color,label=os.path.basename(each_limit_file)[0:-4])
##### Eiko
#    if ("highres" in each_limit_file):
#        each_text = ax.text(text_x*1.01,text_y,
#                            os.path.basename(each_limit_file)[0:-4].replace("_"," ").replace(" highres","\nhighres")
#                            ,fontsize=11,color="black",rotation=0,ha='center', va='center')
#    elif (not ("highres" in each_limit_file) and "HAYSTAC_2020" in each_limit_file):
#        each_text = ax.text(text_x*0.98,text_y,
#                            os.path.basename(each_limit_file)[0:-4].replace("_"," ")
#                            ,fontsize=11,color="black",rotation=0,ha='center', va='center')
    # elif ("UF" in each_limit_file or "RBF" in each_limit_file):
    #     # each_text = ax.text(text_x*1.01,text_y,os.path.basename(each_limit_file)[0:-4].replace("_"," "),fontsize=12,color="black",rotation=0,ha='center', va='center')
    #     pass
    # else:
    #     each_text = ax.text(text_x*1.01,text_y,os.path.basename(each_limit_file)[0:-4].replace("_"," "),fontsize=12,color="black",rotation=0,ha='center', va='center')



###########################################################################  plot TASEH

limits    =  center_limits
our_limit = ax.fill_between(1e-9 * hein_limit_freq[800:-800], limits[800:-800],1,alpha=1,color="r",label="TASEH CD102")
#ax.text(median(1e-9 * hein_limit_freq)*0.988,min(limits)/1.23,"TASEH CD102",fontsize=12,color="r",rotation=0,ha='center', va='center')


ax.text(7.2,1.1e-11,"ADMX sidecar",fontsize=13,color="black",rotation=0,ha='center', va='center')
ax.text(5.5,1.1e-11  ,"ADMX sidecar",fontsize=13,color="black",rotation=0,ha='center', va='center')
ax.text(4.1,1.1e-11,"ADMX sidecar",fontsize=13,color="black",rotation=0,ha='center', va='center')

ax.text(1.3 ,1e-14    ,"CAPP",size=13)
ax.text(2.35,2e-14    ,"CAPP",size=13)
ax.text(3.1 ,4e-14    ,"CAPP",size=13)
ax.text(4.6 ,1.1e-14  ,"CAPP",size=13)
ax.text(4.85 ,8e-14  ,"TASEH",size=13,color="red")
ax.text(4.85 ,4e-14  ,"CD102",size=13,color="red")
#ax.text(0.7 ,9e-13  ,"ADMX",size=13,ha='center', va='center')
ax.text(0.5 ,8.87e-13  ,"ADMX",size=13)
ax.text(2   ,8.87e-13 ,"RBF" ,size=13)
ax.text(1.3 ,8.87e-13 ,"UF"  ,size=13)
ax.text(3.7 ,2e-13 ,"HAYSTAC"  ,size=13)
ax.text(5.4 ,2e-13 ,"HAYSTAC"  ,size=13)
ax.text(1.8   ,1.5e-10  ,"CAST",size=13)
# ax.text(5.06,9e-14,"ADMX",size=12)

# ax.text(4.57,1e-14,"CAPP",size=12)

xlabel("Frequency [GHz]",size=20,labelpad=15)
ylabel(r"$|g_{a \gamma \gamma}|\ \ [GeV^{-1}]$",size=15)
yscale("log")
grid(True, which='minor')


ax.xaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_minor_locator(MultipleLocator(0.2))
ax.tick_params(which='both', width=2,top=None)
xlim(0,8)
ylim(1.6e-17,6.5e-10)

###########################################################################  right axis
new_axis = twinx()
new_axis.plot(fa_x , KSVZ_g_a_gamma,"b--",alpha=0,label="KSVZ")
new_axis.plot(fa_x , DFSZ_g_a_gamma,"r--",alpha=0,label="DFSZ")
new_axis.fill_between(fa_x,KSVZ_g_a_gamma*4,DFSZ_g_a_gamma/4,alpha=0,color="#423D56",label="model region")
new_axis.tick_params(which='both', width=2)
new_axis.set_ylim(ax.get_ylim())
new_axis.set_yscale("log")
new_axis.set_ylabel(ax.get_ylabel(),size=15)
new_axis.grid(True, which='minor')


###########################################################################  upper axis
new_axisx = twiny()
new_axisx.set_xlabel(r"$m_a\ [{\mu}eV]$",size=20,labelpad=15)
new_axisx.plot(ma_x*1e6 , KSVZ_g_a_gamma,"b--",alpha=0,label="KSVZ")
new_axisx.set_xlim(freq_to_ma(0)*1e6,freq_to_ma(8)*1e6)
# new_axisx.xaxis.set_major_locator(MultipleLocator(2))
new_axisx.xaxis.set_minor_locator(MultipleLocator(1))
new_axisx.tick_params(which='both', width=2)
new_axisx.set_yscale("log")
tight_layout()

savefig(OUTPUT_FILE_NAME,dpi=300)
print(f"[*] Saved in {OUTPUT_FILE_NAME}")

show()
