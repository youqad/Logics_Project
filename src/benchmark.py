import os
from subprocess import check_output, call
import re
from timeit import timeit
from matplotlib import pyplot as plt
 
def benchmark(path='./Examples/Simple/'):
    N = 1
    OCamL, Python, Cython = [], [], []
    color_OCamL, color_Python, color_Cython = 'orange', 'b', 'g'
    
    compt = 0
    namefiles = []
    default_time = timeit("call(['sleep', '0'])", setup="from subprocess import call", number=N)
    for root, dirs, files in os.walk(path):
        for file in files:
            namefile = os.path.join(root, file)
            namefiles.append(file)
            print(namefile)
            OCamL_avgtime = (timeit("call(['OCamL/DPLL', '"+namefile+"'])", setup="from subprocess import call", number=N)-default_time)/N
            Python_avgtime = (timeit("call(['python', 'Python/DPLL.py', '"+namefile+"'])", setup="from subprocess import call", number=N)-timeit("call(['sleep', '0'])", setup="from subprocess import call", number=N) - default_time)/N
            Cython_avgtime = (timeit("call(['Cython/DPLL_compiled', '"+namefile+"'])", setup="from subprocess import call", number=N)-timeit("call(['sleep', '0'])", setup="from subprocess import call", number=N) - default_time)/N
            OCamL.append(OCamL_avgtime)
            Python.append(Python_avgtime)
            Cython.append(Cython_avgtime)
            compt+=1
    
    common_params = dict(range=(1, compt))
    
    a, b, c = OCamL, Cython, Python
    step = 5
    x = list(range(0,step*compt, step))
    w = 1       # the width of the bars
    dw = 0.2  # space between bars

    
    ax = plt.subplot(311)
    rects1 = ax.bar([i-w-dw for i in x], a,width=w,color=color_OCamL,align='center')
    rects2 = ax.bar(x, b,width=w,color=color_Cython,align='center')
    rects3 = ax.bar([i+w+dw for i in x], c,width=w,color=color_Python,align='center')
    
    ax.legend( (rects1[0], rects2[0],rects3[0]), ('OCamL', 'Cython', 'Python'), loc='upper left')
    ax.set_ylabel("Execution time")
    ax.set_xticks(x)
    ax.set_xticklabels([(s[:10] + '..') if len(s) >10 else s for s in namefiles], size = 'small', rotation=45)
    
    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.03*h, "{0:.2f}".format(h),
                    ha='center', va='bottom', size = 'xx-small', rotation=45)

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    ax2 = plt.subplot(313)
    ax2.plot(x,a, label="OCamL", drawstyle='steps',color=color_OCamL, linewidth = 1.5)   
    ax2.plot(x,b, label="Cython", drawstyle='steps',color=color_Cython, linewidth = 1.5)   
    ax2.plot(x,c, label="Python", drawstyle='steps',color=color_Python, linewidth = 1.5)   
    
    ax2.set_ylabel("Execution time")
    ax2.set_xticks(x)
    ax2.set_xticklabels([(s[:10] + '..') if len(s) >10 else s for s in namefiles])
    ax2.legend(loc='upper left', frameon=False) 
    

    ax3 = plt.subplot(312)
    width = step - 1       # the width of the bars
    
    ax3.bar(x,a, width, color=color_OCamL, label="OCamL")
    ax3.bar(x, b, width, color=color_Cython, bottom=a, label="Cython")
    ax3.bar(x, c, width, color=color_Python, bottom=b, label="Python")
    
    ax3.set_ylabel("Relative execution time")
    ax3.set_xlabel('Tested files')
    
    ax3.set_xticks([i + width/2. for i in x])
    ax3.set_xticklabels([(s[:10] + '..') if len(s) >10 else s for s in namefiles], rotation=45)
    ax3.legend(loc='upper left')

    plt.tight_layout()
    plt.savefig('benchmarks.png')
    plt.show()

                
if __name__ == '__main__':
    benchmark()