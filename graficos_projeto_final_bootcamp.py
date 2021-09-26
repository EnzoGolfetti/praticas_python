import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler

mpl.rcParams['font.size'] = 12 
mpl.rcParams['font.serif'] = 'Times New Roman'
mpl.rcParams['axes.prop_cycle'] = cycler(color=['#0475BD', '#FF0000', '#FFF200', '#7D3E11'])
plt.style.use('seaborn-talk')
mpl.rcParams['figure.figsize'] = [12,8]