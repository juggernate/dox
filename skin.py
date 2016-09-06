import maya.cmds as cmds

import apiExtensions
from maya.OpenMayaAnim import MFnSkinCluster
from maya.OpenMaya import MIntArray, MDagPathArray

def setSkinWeights( skinCluster, vertJointWeightData ):
    '''
    vertJointWeightData is a list of 2-tuples containing the vertex component name, and a list of 2-tuples
    containing the joint name and weight.  ie it looks like this:
    [ ('someMesh.vtx[0]', [('joint1', 0.25), 'joint2', 0.75)]),
      ('someMesh.vtx[1]', [('joint1', 0.2), 'joint2', 0.7, 'joint3', 0.1)]),
      ... ]
    '''

    #convert the vertex component names into vertex indices
    idxJointWeight = []
    for vert, jointsAndWeights in vertJointWeightData:
        idx = int( vert[ vert.rindex( '[' )+1:-1 ] )
        idxJointWeight.append( (idx, jointsAndWeights) )

    #get an MObject for the skin cluster node
    skinCluster = apiExtensions.asMObject( skinCluster )
    skinFn = MFnSkinCluster( skinCluster )

    #construct a dict mapping joint names to joint indices
    jApiIndices = {}
    _tmp = MDagPathArray()
    skinFn.influenceObjects( _tmp )
    for n in range( _tmp.length() ):
        jApiIndices[ str( _tmp[n].node() ) ] = skinFn.indexForInfluenceObject( _tmp[n] )

    weightListP = skinFn.findPlug( "weightList" )
    weightListObj = weightListP.attribute()
    weightsP = skinFn.findPlug( "weights" )

    tmpIntArray = MIntArray()
    baseFmtStr = str( skinCluster ) +'.weightList[%d]'  #pre build this string: fewer string ops == faster-ness!

    for vertIdx, jointsAndWeights in idxJointWeight:

        #we need to use the api to query the physical indices used
        weightsP.selectAncestorLogicalIndex( vertIdx, weightListObj )
        weightsP.getExistingArrayAttributeIndices( tmpIntArray )

        weightFmtStr = baseFmtStr % vertIdx +'.weights[%d]'

        #clear out any existing skin data - and awesomely we cannot do this with the api - so we need to use a weird ass mel command
        for n in range( tmpIntArray.length() ):
            removeMultiInstance( weightFmtStr % tmpIntArray[n] )

        #at this point using the api or mel to set the data is a moot point...  we have the strings already so just use mel
        for joint, weight in jointsAndWeights:
            if weight:
                infIdx = jApiIndices[ joint ]
                setAttr( weightFmtStr % infIdx, weight )