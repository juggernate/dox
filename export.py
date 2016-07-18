import maya.cmds as cmds
import dox.FBXWrapper as fbxw
import os

def animationExport():
    startFrame = cmds.playbackOptions(q=1, minTime=True)
    endFrame = cmds.playbackOptions(q=1, maxTime=True)
    savePath = findPath()
    select()

    fbxw.FBXResetExport()
    fbxw.FBXExportBakeComplexAnimation(v = 1)
    fbxw.FBXExportBakeComplexStart(v = startFrame)
    fbxw.FBXExportBakeComplexEnd(v = endFrame)
    fbxw.FBXExportBakeComplexStep(v = 1)
    fbxw.FBXExportUseSceneName(v = 0)
    fbxw.FBXExportQuaternion(v = 'euler')
    fbxw.FBXExportShapes(v = 1)
    fbxw.FBXExportSkins(v = 1)
    fbxw.FBXExportConstraints(v = 0)
    fbxw.FBXExportCameras(v = 0)
    fbxw.FBXExportLights(v = 0)
    fbxw.FBXExportEmbeddedTextures(v = 0)
    fbxw.FBXExportInputConnections(v = 0)
    fbxw.FBXExportUpAxis('y')

    fbxw.FBXExport(f = savePath, s = 1)

def meshExport():
    savePath = findPath()
    select(Mesh = True)
    fbxw.FBXResetExport()
    fbxw.FBXExportUseSceneName(v = 0)
    fbxw.FBXExportShapes(v = 1)
    fbxw.FBXExportSkins(v = 1)
    fbxw.FBXExportInstances(v = 0)
    fbxw.FBXExportTangents(v = 1)
    fbxw.FBXExportSmoothMesh(v = 1)
    fbxw.FBXExportSmoothingGroups(v = 1)

    fbxw.FBXExportConstraints(v = 0)
    fbxw.FBXExportCameras(v = 0)
    fbxw.FBXExportLights(v = 0)
    fbxw.FBXExportEmbeddedTextures(v = 0)
    fbxw.FBXExportInputConnections(v = 0)
    fbxw.FBXExportUpAxis('y')

    fbxw.FBXExport(f = savePath, s = 1)

def findPath():
    artPath = cmds.file(q=1, sn=1)
    savePath = artPath.replace('art/characters', 'main/UnityProject/Assets/Uber/Characters')
    savePath = savePath.replace('_rig', '_mesh')
    savePath = savePath.replace('.ma', '.fbx')
    savePath = savePath.replace('.mb', '.fbx')
    if not cmds.file(savePath, q=1, w=1):
        os.chmod(savePath, 0755)
    return savePath

def select(Mesh = False):
    cmds.select('Pelvis')
    cmds.select(hi=1)
    cmds.select('*Constraint*', d=1)
    if Mesh:
        meshes = []
        joints = cmds.ls(sl=1)
        clusters = list(set(cmds.listConnections(joints,type='skinCluster')))
        for cluster in clusters:
            shape = cmds.skinCluster(cluster, q=1, geometry=1)
            meshes.append(cmds.listRelatives(shape, parent=1)[0])
        cmds.select(meshes, add=1)