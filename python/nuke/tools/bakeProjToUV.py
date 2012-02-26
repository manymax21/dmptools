import nuke
import nukescripts

def deselectAll():
    for n in nuke.allNodes():
        n['selected'].setValue(False)

def selectReplace(node):
    for n in nuke.allNodes():
        n['selected'].setValue(False)
    node['selected'].setValue(True)

def selectAdd(node):
    node['selected'].setValue(True)

def bakeIt(node, filePath, fileSize,  fileType, outcolorspace, framerange, connectToObj, alpha, antialiasing, samples, shutter):
    
    if fileSize == '1K':
        
        formatN = ("bakeUV_1K")
        form = ("1024 1024 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])
    
    if fileSize == '2K':
        
        formatN = ("bakeUV_2K")
        form = ("2048 2048 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])

    if fileSize == '4K':
        
        formatN = ("bakeUV_4K")
        form = ("4096 4096 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])
    
    if fileSize == '8K':
        
        formatN = ("bakeUV_8K")
        form = ("8192 8192 1 %s" % (formatN))
        nuke.addFormat(form)
        formatDict = {}
        for item in nuke.formats():
            formatDict[item.name()]=item
        nuke.Root()['format'].setValue(formatDict[formatN])	
    
    selectReplace(node)
    
    scanlineR = nuke.createNode('ScanlineRender', inpanel = False)
    scanlineR['name'].setValue("Scanline_"+node.name()+"_bake")
    scanlineR['projection_mode'].setValue('uv')
    
    scanlineR['antialiasing'].setValue(antialiasing)
    scanlineR['samples'].setValue(samples)
    scanlineR['shutter'].setValue(shutter)
    
    deselectAll()
    
    reformatBake = nuke.createNode('Reformat', inpanel = False)
    reformatBake['name'].setValue("reformat_"+node.name()+"_bake")
    reformatBake['format'].setValue("bakeUV_"+fileSize)
    
    deselectAll()
    
    scanlineR.setInput(0, reformatBake)
    selectReplace(scanlineR)
    
    mpcCol = nuke.createNode('MPC_ColIO_!MPC_COLIO_VERSION!', inpanel = False)
    mpcCol['inspace'].setValue('Linear')
    mpcCol['output_space'].setValue(outcolorspace)
    
    writeNode = nuke.createNode('Write', inpanel = False)
    try:
        writeNode['views'].setValue('left')
    except:
        pass
        
    writeNode['file_type'].setValue(fileType)
    writeNode['name'].setValue("write_"+node.name()+"_bake")
    writeNode['raw'].setValue(True)

    try:
        startF = int(framerange.split("-")[0])
        endF = int(framerange.split("-")[1])
        if startF == endF:
            writeNode['file'].setValue(filePath+node.name()+"_COL."+fileType)
        else:
            writeNode['file'].setValue(filePath+node.name()+"_COL.%04d."+fileType)
        
    except:
        startF = int(framerange)
        endF = int(framerange)
        writeNode['file'].setValue(filePath+node.name()+"_COL."+fileType)
        
    if alpha == 1:	
        writeNode['channels'].setValue('rgba')
    
    nuke.execute(writeNode, startF, endF)
    
    deselectAll()
    selectAdd(scanlineR)
    selectAdd(reformatBake)
    selectAdd(mpcCol)
    selectAdd(writeNode)
    nukescripts.node_delete()
    deselectAll()
    
    deselectAll()
    readUV = nuke.createNode('Read', inpanel = False)
    readUV['name'].setValue("Read_"+node.name()+"_baked")
    readUV['file'].setValue(filePath+node.name()+"_COL."+fileType)
    readUV['raw'].setValue(True)
    
    lastNode = nuke.createNode('MPC_ColIO_'+MPC_colio, inpanel = False)
    lastNode['inspace'].setValue('Linear')
    lastNode['output_space'].setValue(outcolorspace)
    
    if alpha:
        lastNode = nuke.createNode('Premult', inpanel = False)
    
    if connectToObj:    
        node.setInput(0, lastNode)
    
def bakeItUI():

    sel = nuke.selectedNodes()

    if sel:	
        availableColorspace = 'Linear Log sRGB Screen'
        fileTypes = 'tif exr jpg'
        fileSizes = '1K 2K 4K 8K'
        antialiasingMenu = 'none low medium high'
        
        panel = nuke.Panel("Bake Proj To UV")
        panel.setWidth(400)
        panel.addFilenameSearch("Path of UV output files: ","")
        panel.addEnumerationPulldown("Size: ", fileSizes)
        panel.addEnumerationPulldown("File type: ", fileTypes)
        panel.addBooleanCheckBox("alpha channel", 0)
        panel.addEnumerationPulldown("output colorspace: ", availableColorspace)
        panel.addSingleLineInput("Frame Range: ", str(int(nuke.root()['first_frame'].getValue()))+"-"+str(int(nuke.root()['last_frame'].getValue())))
        panel.addEnumerationPulldown("Antialiasing: ", antialiasingMenu)
        panel.addSingleLineInput("S-R Samples", '1')
        panel.addSingleLineInput("S-R Shutter", '0')
        panel.addBooleanCheckBox("Connect to object ?", 0)
        
        retVar = panel.show()
        if retVar == 1:
            for node in sel:
                
                filePath = panel.value("Path of UV output files: ")
                fileSize = panel.value("Size: ")
                fileType = panel.value("File type: ")
                outcolorspace = panel.value("output colorspace: ")
                framerange = panel.value("Frame Range: ")
                connectToObj = panel.value("Connect to object ?")
                alpha = int(panel.value("alpha channel"))
                antialiasing = panel.value("Antialiasing: ")
                samples = int(panel.value("S-R Samples"))
                shutter = int(panel.value("S-R Shutter"))
                
                bakeIt(node, filePath, fileSize,  fileType, outcolorspace, framerange, connectToObj, alpha, antialiasing, samples, shutter)
    else:
        nuke.message('Please select one or multiple 3d objects.')
