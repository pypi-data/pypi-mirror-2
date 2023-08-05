## Script (Python) "createAutoImagesJSCode_py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=objList,here,debug=None
##title=
"""
# version : 0.2
# author  : T.Hinze (HiDeVis)
# datum   : 19.02.2007
#
# parameter
#   objList             - list with image references or None
#   here                - reference to the current ATMP
#
# return value
#   dict                - the jsCode and the reference to the 1st image
#    jsCode               Javascript code with references to all founded images
#    firstImage           reference to the 1st image in the (randomized) list
#
###########################################################
# Documentation
# -------------
#
# This script generates JS-code to preload the images references by
# the objList. The result in Javascript is an array with image objects
# that can be used with DTML-methods.
# Additionaly the small logic for automatic delayed picture change is
# also included in the return string.
#
###########################################################
"""

#---------
# imports
#---------
from random import shuffle

#------
# init
#------
jsOut = ''
imgList = objList
if here.getUseImageZoom():
    useZoom = 1
else:
    useZoom = 0

if not imgList:
    return {'jsCode': '', 'firstImage': None}

autoChangeDelay = here.getAutoChangeDelay()
useRandom = here.getAutoChangeRandom()

# randomize image list
if useRandom:
    # randomize list
    shuffle(imgList)

# create the JS code sequence
if imgList:
    jsOut += '\nvar allImages = new Array();\n'
    jsOut += '\nvar allImageTitle = new Array();\n'
    idx = 0
    for img in objList:
        jsOut += 'allImages[' + str(idx) + '] = new Image();\n'
        jsOut += 'allImages[' + str(idx) + '].src = "' + img.absolute_url() + \
                 '/image_mini";\n'
        jsOut += 'allImageTitle[' + str(idx) + '] = "' + img.Title() + \
                 ' | ' + img.Description() + '";\n'
        idx += 1

    jsOut += """
            /* the function to change the image source named
               'autoChangeSideImage()' is defined in the skin-javascript file.
            */
            var autoChangeDelay = """ + str(autoChangeDelay) + """;
            initAutoChange();
            var imgNum = 0;
            var useZoom = """ + str(useZoom) + """;

            """
#--------
# return
#--------
return {'jsCode': jsOut, 'firstImage': imgList[0]}
