#!/usr/bin/python

# Pweave, Literate programming tool for Python 
# ============================================
# 
# :Author: Matti Pastell <matti.pastell@helsinki.fi
# :Website: http://mpastell.com
# Version: 0.12

import sys
import StringIO
import re
from optparse import OptionParser
import os

if len(sys.argv)==1:
    print "This is Pweave, enter Pweave -h for help"
    sys.exit()

# Command line options

parser = OptionParser(usage="%prog [options] sourcefile", version="%prog 0.12")
parser.add_option("-f", "--format", dest="format", default='sphinx',
                  help="The ouput format: 'sphinx' (default), 'rst' or 'tex'")
parser.add_option("-m", "--matplotlib", dest="mplotlib", default='true',
                  help="Do you want to use matplotlib true (default) or false")
parser.add_option("-g", "--figure-format", dest="figfmt",
                  help="Figure format for matplolib graphics: Defaults to 'png' for rst and Sphinx html documents and 'pdf' for tex")
parser.add_option("-d", "--figure-directory", dest="figdir", default = 'images/',
                  help="Directory path for matplolib graphics: Default 'images/'")
(options, args) = parser.parse_args()
format = options.format
infile = args[0]


# Is matplotlib used? 

if options.mplotlib.lower() == 'true':
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

# Format specific options for tex or rst

if format == 'tex':
    codestart = '\\begin{verbatim}' 
    codeend = '\end{verbatim}\n'
    outputstart = '\\begin{verbatim}' 
    outputend = '\end{verbatim}\n' 
    codeindent = ''
    figfmt = '.pdf'
    ext = 'tex'
if format == 'rst':
    codestart = '::\n' 
    codeend = '\n'
    outputstart = '::\n' 
    outputend = '\n' 
    codeindent = '  '
    figfmt = '.png'
    ext = 'rst'
if format == 'sphinx':
    codestart = '::\n' 
    codeend = '\n'
    outputstart = '::\n' 
    outputend = '\n' 
    codeindent = '  '
    figfmt = '.png'
    sphinxtexfigfmt = '.pdf'
    ext = 'rst'

# Override the default fig format with command line option

if options.figfmt > 0:
    figfmt = '.' + options.figfmt

# Open the file to be processed and get the output file name

codefile = open(infile, 'r')
outfile = infile.split('.')[0] + '.' + ext
pyfile = infile.split('.')[0] + '.' + 'py'
sys.stdout = open(outfile, 'w')
lines = codefile.readlines()

# Initialize some variables

state = 'text'
block = ''
nfig = 1
allcode = ''
imgdir = options.figdir

# Create figure directory if it doesn't exist
if os.path.isdir(imgdir) == False:
    os.mkdir(imgdir)


# A function for parsing options

def options(optionstring):
    echo = True
    results = 'verbatim'
    fig = False
    evaluate = True
    width = '15 cm'
    caption = False
    term = False
    optionstring = re.sub(',', ';', optionstring)
    exec(optionstring)
    return(echo, results, evaluate, fig, width, caption, term)

# Process the whole text file with a loop

for line in lines:
# If start of code block, set state as block and get the options
    code = re.search('^<<(.|)+>>=$', line.strip())
    if code > 0:
        state = 'code'
        optionstring = line[2:len(line.strip())-3]
        line = ''

# The codeblock has ended, less process it
    if line.startswith('@'):
        #Get options 
        echo, results, evaluate, fig, width, caption, term = options(optionstring)

        #Output in doctests mode
        #print dtmode
        if term:
            print
            if format=="tex": print codestart  
            #Write output to a StringIO object
            #loop trough the code lines
            for x in block.splitlines():
                print '>>> ' + x
                tmp = StringIO.StringIO()
                sys.stdout = tmp
                try:
                    print(eval(x))
                except:
                    exec(x)
                result = tmp.getvalue()                
                tmp.close()
                sys.stdout = open(outfile, 'a')
                if len(result) > 0:
                    print result ,                                   
            result = ''        
            print codeend

        #include source?
        if echo==True and term==False:
            #Split the code block and output Rst block
            print codestart
            #For sphinx or rst2htmlhighlight
            #print '.. code-block:: python', '\n'
            inblock = block.splitlines()
            for x in inblock:
                print codeindent + x
            print codeend
        #Evaluate the code?
        if evaluate==True and term==False:
            if fig:
                #A placeholder for figure options
                #import matplotlib
                #matplotlib.rcParams['figure.figsize'] = (6, 4.5)
                pass
        #Write output to a StringIO object
            tmp = StringIO.StringIO()
            sys.stdout = tmp
            exec(block)
            sys.stdout = open(outfile, 'a')
            result = tmp.getvalue().splitlines()
            tmp.close()
            
        #If we get results they are printed    
        if len(result) > 0:
            if results == "verbatim":
                print outputstart
                indent = codeindent
            if results == "rst" or results == "tex":
                indent = ''
            for x in result:
                print indent + x
            print
            if results == "verbatim":
                print outputend
            result = ''
        #Save and include a figure?
        if fig:
            figname = imgdir + 'Fig' +str(nfig) + figfmt
            plt.savefig(figname, dpi = 200)
            #savefig(figname)
            if format == 'sphinx':
                figname2 = imgdir + 'Fig' +str(nfig) +  sphinxtexfigfmt
                plt.savefig(figname2)
            plt.clf()
            if format == 'rst':
                if caption > 0:
                    #If the image has a caption, use Figure directive
                    print '.. figure:: ' + figname
                    print '   :width: ' + width + '\n'
                    print '   ' + caption + '\n'   
                else:
                    print '.. image:: ' + figname
                    print '   :width: ' + width + '\n'
            if format == 'sphinx':
                if caption > 0:
                    print '.. figure:: ' + imgdir + 'Fig' + str(nfig)  + '.*'
                    print '   :width: ' + width + '\n'
                    print '   ' + caption + '\n'   
                else:
                    print '.. image:: ' + imgdir + 'Fig' + str(nfig)  + '.*'
                    print '   :width: ' + width + '\n'
            if format == 'tex':
                if caption > 0:
                    print r'\begin{figure}'
                    print '\includegraphics{'+ figname + '}'
                    print '\caption{' + caption + '}'
                    print '\end{figure}'                 
                else:
                    print '\includegraphics{'+ figname + '}\n'

            nfig = nfig +1
        allcode = allcode + block
        block = ''
        state = 'text'
        line = ''

# If processing a code block, store the block for processing

    if state == 'code':
        block = block + line
# If processing text, print it as it is 

    if state == 'text':
        print line, 

# Done processing the file, save extracted code and tell the user what has happened
extfile = open(pyfile ,'w')
extfile.write(allcode)
extfile.close()

codefile.close()
sys.stdout = sys.__stdout__
print 'Output written to', outfile
print 'Code extracted to', pyfile
