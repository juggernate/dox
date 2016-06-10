import maya.cmds as cmds
import dox.FBXWrapper as fbxw

def animationExport(joints, fileNames, animationNames, startFrames, endFrames, saveDirectory):
    referencedJoints = []
    for x in range(len(fileNames)):
        targetScene = saveDirectory+fileNames[x]

        if (cmds.file(q=1, sc=1) != targetScene):
            #    Check to see whether the filename matches the current file.
            #    If not, load the named file as a reference.
            referencedFile = cmds.file(lr=targetScene)
            #    Select the referenced joints and meshes
            for j in range(len(joints)):                
                referencedJoints.append(fileNames[x][:-3]+"_"+joints[j])
            cmds.select(referencedJoints)
        else:
            cmds.select(joints)

        # Animation      
        mm.eval("FBXExportBakeComplexAnimation -v true")
        mm.eval("FBXExportBakeComplexStart -v "+str(startFrames[x]))
        mm.eval("FBXExportBakeComplexEnd -v "+str(endFrames[x]))
        mm.eval("FBXExportBakeComplexStep -v 1")
        mm.eval("FBXExportUseSceneName -v false")
        mm.eval("FBXExportQuaternion -v euler")
        mm.eval("FBXExportShapes -v true")
        mm.eval("FBXExportSkins -v true")
        # Constraints
        mm.eval("FBXExportConstraints -v false")
        # Cameras
        mm.eval("FBXExportCameras -v false")
        # Lights
        mm.eval("FBXExportLights -v false")
        # Embed Media
        mm.eval("FBXExportEmbeddedTextures -v false")
        # Connections
        mm.eval("FBXExportInputConnections -v false")
        # Axis Conversion
        mm.eval("FBXExportUpAxis y")
        # Export!
        fbxSaveFile = saveDirectory+animationNames[x]+".fbx"
        mm.eval("FBXExport -f \""+fbxSaveFile+"\" -s")