## Dox Rigging Tools written by Andrew Christophersen 2016

import maya.cmds as cmds
import dox.shapes as shapes
import maya.api.OpenMaya as om
from dox.ui import dox_OptionsWindow

class armRigger(dox_OptionsWindow):
    def __init__(self):
        dox_OptionsWindow.__init__(self)
        self.title = 'Dox Arm Rigging Tool'
        self.actionName = 'Create'
    def displayOptions(self):
        cmds.columnLayout()
        cmds.separator(height=5)
        self.objType = cmds.checkBoxGrp(
            label='Arm Sections to Rig: ',
            labelArray3=[
                'Clavicle',
                'Arm',
                'Hand'
            ],
            numberOfCheckBoxes=3
        )
        cmds.separator(height=10)
        self.xformGrp = cmds.frameLayout(
            label='Skinned Bones to Rig',
            collapsable=True,
            w=415
        )
        self.xformCol = cmds.rowColumnLayout(nc=3)
        self.clavicleLabel = cmds.textField(
            annotation='Clavicle Bone',
            text='Clavicle Bone',
            bgc=[0.1,0.06,0.06],
            editable=0,
            w=115
        )
        self.clavicleText = cmds.textField(
            annotation='Clavicle Bone',
            text='None',
            w=250
        )
        self.clavicleButton = cmds.button(
            label='add', w=50,
            c=self.addClavicleCmd
        )
        self.shoulderLabel = cmds.textField(
            annotation='Shoulder Bone',
            text='Shoulder Bone',
            bgc=[0.1,0.06,0.06],
            editable=0,
            w=115
        )
        self.shoulderText = cmds.textField(
            annotation='Shoulder Bone',
            text='None',
            w=250
        )
        self.shoulderButton = cmds.button(
            label='add', w=50,
            c=self.addShoulderCmd
        )
        self.elbowLabel = cmds.textField(
            annotation='Elbow Bone',
            text='Elbow Bone',
            bgc=[0.1,0.06,0.06],
            editable=0,
            w=115
        )
        self.elbowText = cmds.textField(
            annotation='Elbow Bone',
            text='None',
            w=250
        )
        self.elbowButton = cmds.button(
            label='add', w=50,
            c=self.addElbowCmd
        )
        self.wristLabel = cmds.textField(
            annotation='Wrist Bone',
            text='Wrist Bone',
            bgc=[0.1,0.06,0.06],
            editable=0,
            w=115
        )
        self.wristText = cmds.textField(
            annotation='Wrist Bone',
            text='None',
            w=250
        )
        self.clavicleButton = cmds.button(
            label='add', w=50,
            c=self.addWristCmd
        )
        cmds.setParent('..')
        cmds.setParent('..')
        self.attrGrp = cmds.frameLayout(
            label='Rig Attributes',
            collapsable=True,
            w=415
        )
        self.xformCol = cmds.rowColumnLayout(nc=2)
        self.scaleLabel = cmds.textField(
            annotation='The scale of the shape object used to select the rig.',
            text='Control Scale',
            bgc=[0.06,0.06,0.1],
            editable=0,
            w=115
        )
        self.scaleAttr = cmds.floatField(
            v=1, min=0, max=10
        )
        self.poleLabel = cmds.textField(
            annotation='A scalar value to adjust the angle of the pole vector. Smaller numbers push the point out.',
            text='Pole Vector Position',
            bgc=[0.06,0.06,0.1],
            editable=0,
            w=115
        )
        self.poleAttr = cmds.floatField(
            v=1, min=0, max=2
        )
    def addClavicleCmd(self, *args):
        cmds.textField(self.clavicleText, e=1, text=str(cmds.ls(sl=1, type='joint', hd=1))[3:-2] or 'None')
    def addShoulderCmd(self, *args):
        cmds.textField(self.shoulderText, e=1, text=str(cmds.ls(sl=1, type='joint', hd=1))[3:-2] or 'None')
    def addElbowCmd(self, *args):
        cmds.textField(self.elbowText, e=1, text=str(cmds.ls(sl=1, type='joint', hd=1))[3:-2] or 'None')
    def addWristCmd(self, *args):
        cmds.textField(self.wristText, e=1, text=str(cmds.ls(sl=1, type='joint', hd=1))[3:-2] or 'None')
    def applyBtnCmd(self, *args):
        clavIndex = cmds.checkBoxGrp(
            self.objType, q=1,
            v1=1
        )
        armIndex = cmds.checkBoxGrp(
            self.objType, q=1,
            v2=1
        )
        handIndex = cmds.checkBoxGrp(
            self.objType, q=1,
            v3=1
        )
        clavicleBone = cmds.textField(
            self.clavicleText, q=1,
            text=1
        )
        shoulderBone = cmds.textField(
            self.shoulderText, q=1,
            text=1
        )
        elbowBone = cmds.textField(
            self.elbowText, q=1,
            text=1
        )
        wristBone = cmds.textField(
            self.wristText, q=1,
            text=1
        )
        scale = cmds.floatField(
            self.scaleAttr, q=1,
            v=1
        )
        poleVector = cmds.floatField(
            self.poleAttr, q=1,
            v=1
        )
        if clavIndex:
            createClavicleRig(scale, clavicleBone)
        if armIndex:
            createArmRig(scale,poleVector,shoulderBone,elbowBone,wristBone)
        if handIndex:
            createHandRig(scale,wristBone)
        cmds.select(cl=1)

def createClavicleRig(controlScale=1, *args):
    skinBones = args or cmds.ls(sl=True) or []
    color = limbColor(skinBones[0])
    clavicleControl, clavicleParent = createControlJoint(skinBones[0])
    cmds.parent(clavicleControl, cmds.listRelatives(clavicleParent, p=1))
    cmds.delete(clavicleParent)
    clavicleControl[0] = cmds.rename(clavicleControl, str(clavicleControl[0])[:-4]+'ik')
    clavicleEnd = cmds.joint(n=clavicleControl[0]+'_end')
    alignAtoB(clavicleEnd, cmds.listRelatives(skinBones[0], c=1)[0])
    freezeJointRotation(clavicleEnd)
    #Create IK
    clavicleIK = cmds.ikHandle(sj=clavicleControl[0], ee=clavicleEnd, sol='ikSCsolver')
    clavicleIK = cmds.rename(clavicleIK[0], str(clavicleControl[0])[:-3]+'_ikHandle')
    clavicleTrans = cmds.createNode('transform', n=str(clavicleControl[0])[:-3]+'_CTRL')
    alignAtoB(clavicleTrans, clavicleEnd)
    cmds.parent(clavicleTrans, cmds.listRelatives(clavicleControl[0], p=1))
    cmds.makeIdentity(clavicleTrans, apply=1)
    cmds.parent(clavicleIK, clavicleTrans)
    limit = (cmds.xform(clavicleEnd, q=1, t=1))[0]
    if limit < 0:
        limit = limit*-1
    cmds.transformLimits(clavicleTrans, tx=(-limit/2, limit/2), ty=(-limit, limit), tz=(-limit, limit), etx=(1, 1), ety=(1, 1), etz=(1, 1))
    lockChannels(0, 1, 1, 0, clavicleTrans)
    #Control Shape
    clavicleShape = shapes.clavicle(color)
    snapAtoB(clavicleShape, clavicleEnd)
    if (cmds.xform(clavicleShape, q=1, t=1))[0] > 0:
        cmds.xform(clavicleShape, ro=(0,90,0), s=(controlScale, controlScale, controlScale))
    else:
        cmds.xform(clavicleShape, ro=(0,-90,0), s=(controlScale, controlScale, controlScale))
    addControlShape(clavicleShape, clavicleTrans)
    hideChannels(clavicleControl[0], clavicleEnd, clavicleIK)
    cmds.setAttr(clavicleIK+'.visibility', 0)
    zeroRadius(clavicleControl[0], clavicleEnd)
    cmds.select(clavicleTrans)

def createArmRig(controlScale=1, pv=1, *args):
    armBones = args or cmds.ls(sl=True) or []
    #Build RIG, FK and IK bone setups
    controls, parents = createControlJoint(*armBones)
    controlBase = [str(controls[0])[:-5], str(controls[1])[:-5], str(controls[2])[:-5]]
    controlName = str(str(parents[0])[0]+'_arm')
    attrName = controlName.lower()[0]+'Arm'
    color = limbColor(armBones[0])
    root = str(cmds.listRelatives(parents[0], p=1, f=1))
    root = list(root.split('|'))
    root = root[1]
    chest = cmds.listRelatives(parents[0], p=1)
    clavSpace = False
    if str(chest).find('clav') > -1:
        chest = cmds.listRelatives(chest, p=1)
        clavSpace = True
    for control in controls:
        cmds.select(control)
        cmds.joint(n=str(control)[:-4]+'RIG')
        cmds.joint(n=str(control)[:-4]+'ik')
    cmds.joint(n=str(controls[2])[:-4]+'ik_end')
    rig = [controlBase[0]+'_RIG', controlBase[1]+'_RIG', controlBase[2]+'_RIG']
    ik = [controlBase[0]+'_ik', controlBase[1]+'_ik', controlBase[2]+'_ik', controlBase[2]+'_ik_end']
    cmds.parent(rig[2], rig[1])
    cmds.parent(rig[1], rig[0])
    cmds.parent(rig[0], parents[0])
    cmds.parent(ik[2], ik[1])
    cmds.parent(ik[1], ik[0])
    cmds.parent(ik[0], parents[0])
    cmds.joint(ik[3], e=1, r=1, p=(10,0,0))
    newJointConnection(rig[0], armBones[0])
    newJointConnection(rig[1], armBones[1])
    newJointConnection(rig[2], armBones[2])
    #Add Control Shapes for FK Rig
    upArmLen = cmds.xform(parents[1], q=1, t=1)[0]
    loArmLen = cmds.xform(parents[2], q=1, t=1)[0]
    control0Shape = shapes.cube(color)
    cmds.parent(control0Shape, controls[0])
    cmds.xform(control0Shape, t=(upArmLen/2,0,0), ro=(0,0,0), s=(upArmLen, controlScale*(upArmLen*0.4), controlScale*(upArmLen*0.4)))
    addControlShape(control0Shape, controls[0])
    control1Shape = shapes.cube(color)
    cmds.parent(control1Shape, controls[1])
    cmds.xform(control1Shape, t=(loArmLen/2,0,0), ro=(0,0,0), s=(loArmLen, controlScale*(loArmLen*0.3), controlScale*(loArmLen*0.3)))
    addControlShape(control1Shape, controls[1])
    control2Shape = shapes.cube(color)
    cmds.parent(control2Shape, controls[2])
    cmds.xform(control2Shape, t=((loArmLen/2)*0.25,0,0), ro=(0,0,0), s=(loArmLen*0.25, controlScale*(loArmLen*0.15), controlScale*(loArmLen*0.25)))
    addControlShape(control2Shape, controls[2])
    #Add Space Switcher
    createSpaceSwitch(1, 1, 1, 0, controls[0], ik[0], rig[0])
    createSpaceSwitch(1, 1, 1, 0, controls[1], ik[1], rig[1])
    createSpaceSwitch(1, 1, 1, 0, controls[2], ik[2], rig[2])
    #Build IK Controls
    armIk = cmds.ikHandle(sj=ik[0], ee=ik[2], sol='ikRPsolver')
    armIk = cmds.rename(armIk[0], controlName+'_ikHandle')
    wristIk = cmds.ikHandle(sj=ik[2], ee=ik[3], sol='ikSCsolver')
    wristIk = cmds.rename(wristIk[0], controlName[0]+'_wrist_ikHandle')
    armIkTrans = cmds.createNode('transform', n=controlName+'_CTRL')
    alignAtoB(armIkTrans, controls[2])
    cmds.parent(armIkTrans, root)
    cmds.makeIdentity(armIkTrans, apply=1)
    cmds.parent(armIk, armIkTrans)
    cmds.parent(wristIk, armIkTrans)
    poleVector = createPoleVector(pv, *ik)
    cmds.parent(poleVector, chest)
    poleVectorShape = shapes.sphere(color)
    snapAtoB(poleVectorShape, poleVector)
    cmds.xform(poleVectorShape, s=(controlScale, controlScale, controlScale))
    addControlShape(poleVectorShape, poleVector)
    cmds.poleVectorConstraint(poleVector, armIk)
    cmds.addAttr(armIkTrans, ln='twist', at='float', k=1)
    cmds.connectAttr(armIkTrans+'.twist', armIk+'.twist')
    lockChannels(0, 1, 1, 0, poleVector)
    armIkShape = shapes.cube(color)
    snapAtoB(armIkShape, armIkTrans)
    cmds.xform(armIkShape, s=(controlScale*10, controlScale*10, controlScale*10))
    addControlShape(armIkShape, armIkTrans)
    cmds.xform(armIkTrans, p=1, roo='xzy' )
    #Shoulder Space Switcher
    if clavSpace == True:
        createSpaceSwitch(0, 1, 0, 0, chest[0], cmds.listRelatives(parents[0], p=1)[0], parents[0])
    #Setup IKFK Attributes
    cmds.addAttr(root, ln=attrName+'IK_FK', at='float', k=1, min=0, max=1)
    cmds.addAttr(root, ln=attrName+'Template', at='float', k=1, min=0, max=1)
    cmds.addAttr(root, ln=attrName+'Visibility', at='float', k=1, min=0, max=1)
    #Hook up IK FK
    cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[0]+'.spaceBlend')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[1]+'.spaceBlend')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[2]+'.spaceBlend')
    #Hook up Template
    templateSwitch = cmds.createNode('multiplyDivide', n=controlName+'_templateSwitch')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', templateSwitch+'.input1X')
    cmds.connectAttr(root+'.'+attrName+'Template', templateSwitch+'.input2X')
    cmds.connectAttr(templateSwitch+'.outputX', parents[0]+'.template')
    templateReverse = cmds.createNode('reverse', n=controlName+'_tempateReverse')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', templateReverse+'.inputX')
    cmds.connectAttr(templateReverse+'.outputX', templateSwitch+'.input1Y')
    cmds.connectAttr(root+'.'+attrName+'Template', templateSwitch+'.input2Y')
    cmds.connectAttr(templateSwitch+'.outputY', armIkTrans+'.template')
    cmds.connectAttr(templateSwitch+'.outputY', poleVector+'.template')
    #Hook up Visibility
    visIkCondition = cmds.createNode('condition', n=controlName+'_visibilityIkCondition')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', visIkCondition+'.firstTerm')
    cmds.setAttr(visIkCondition+'.secondTerm', 0.5)
    cmds.setAttr(visIkCondition+'.operation', 3)
    cmds.setAttr(visIkCondition+'.colorIfTrueR', 1)
    cmds.connectAttr(root+'.'+attrName+'Visibility', visIkCondition+'.colorIfFalseR')
    cmds.connectAttr(visIkCondition+'.outColorR', armIkTrans+'.visibility')
    cmds.connectAttr(visIkCondition+'.outColorR', poleVector+'.visibility')
    visFkCondition = cmds.createNode('condition', n=controlName+'_visibilityFkCondition')
    cmds.connectAttr(root+'.'+attrName+'IK_FK', visFkCondition+'.firstTerm')
    cmds.setAttr(visFkCondition+'.secondTerm', 0.5)
    cmds.setAttr(visFkCondition+'.operation', 5)
    cmds.setAttr(visFkCondition+'.colorIfTrueR', 1)
    cmds.connectAttr(root+'.'+attrName+'Visibility', visFkCondition+'.colorIfFalseR')
    cmds.connectAttr(visFkCondition+'.outColorR', parents[0]+'.visibility')
    #Create Strechy IK
    distance = cmds.createNode('distanceBetween', n=controlName+'_distance')
    stretchStart = cmds.createNode('transform', n=controlName+'_stretchStart')
    stretchEnd = cmds.createNode('transform', n=controlName+'_stretchEnd')
    cmds.pointConstraint(parents[0], stretchStart)
    cmds.pointConstraint(armIkTrans, stretchEnd)
    cmds.connectAttr(stretchStart+'.translate', distance+'.point1')
    cmds.connectAttr(stretchEnd+'.translate', distance+'.point2')
    armLen = (cmds.xform(ik[1], q=1, t=1)[0])+(cmds.xform(ik[2], q=1, t=1)[0])
    distanceMult = cmds.createNode('multiplyDivide', n=controlName+'_distanceMult')
    cmds.setAttr(distanceMult+'.input1X', armLen)
    cmds.connectAttr(root+'.scaleY', distanceMult+'.input2X')
    distanceDivide = cmds.createNode('multiplyDivide', n=controlName+'_distanceDivide')
    cmds.setAttr(distanceDivide+'.operation', 2)
    cmds.connectAttr(distance+'.distance', distanceDivide+'.input1X')
    cmds.connectAttr(distanceMult+'.outputX', distanceDivide+'.input2X')
    stretchCondition = cmds.createNode('condition', n=controlName+'_stretchCondition')
    cmds.setAttr(stretchCondition+'.operation', 2)
    cmds.connectAttr(distance+'.distance', stretchCondition+'.firstTerm')
    cmds.connectAttr(distanceMult+'.outputX', stretchCondition+'.secondTerm')
    cmds.connectAttr(distanceDivide+'.outputX', stretchCondition+'.colorIfTrueR')
    cmds.addAttr(armIkTrans, ln='stretch', at='float', k=1, min=0, max=1)
    stretchBlender = cmds.createNode('blendColors', n=controlName+'_stretchBlender')
    cmds.connectAttr(armIkTrans+'.stretch', stretchBlender+'.blender')
    cmds.connectAttr(stretchCondition+'.outColorR', stretchBlender+'.color1R')
    cmds.connectAttr(stretchBlender+'.outputR', ik[0]+'.scaleX')
    cmds.connectAttr(stretchBlender+'.outputR', ik[1]+'.scaleX')
    cmds.setAttr(stretchBlender+'.color2R', 1)
    #Lock and Hide
    lockChannels(1, 1, 1, 0, *rig)
    hideChannels(*ik)
    hideChannels(armIk, wristIk)
    cmds.setAttr(ik[0]+'.visibility', 0)
    cmds.setAttr(armIk+'.visibility', 0)
    cmds.setAttr(wristIk+'.visibility', 0)
    lockChannels(1, 1, 1, 1, *parents)
    lockChannels(0, 0, 0, 1, armIkTrans, poleVector)
    zeroRadius(*parents)

def createFootLocators():
    locatorsNames = ['ankle', 'heel', 'toe', 'ball', 'toeWiggle']
    locators = []
    for loc in locatorsNames:
        locators.append((cmds.spaceLocator(n=loc+'_loc', p=(0, 0, locatorsNames.index(loc)*10)))[0])
    return locators

def createLegRig(controlScale=1, pv=1, **kwargs):
    legBones = kwargs['legBones']
    legLoc = kwargs['legLoc']
    #Build RIG, FK and IK bone setups
    controls, parents = createControlJoint(*legBones)
    controlBase = [str(controls[0])[:-5], str(controls[1])[:-5], str(controls[2])[:-5]]
    controlName = str(str(parents[0])[0]+'_leg')
    attrName = controlName.lower()[0]+'Leg'
    color = limbColor(legBones[0])
    prefix = limbPrefix(legBones[0])
    root = str(cmds.listRelatives(parents[0], p=1, f=1))
    root = list(root.split('|'))
    root = root[1]
    pelvis = cmds.listRelatives(parents[0], p=1)
    rig = []
    ik = []
    n = 0
    legControlScaleY = [20, 15, 8, 8]
    legControlScaleZ = [20, 15, 13, 13]
    for control in controls[:4]:
        cmds.select(control)
        rig.append(cmds.joint(n=str(control)[:-4]+'RIG'))
        ik.append(cmds.joint(n=str(control)[:-4]+'ik'))
        newJointConnection(rig[n], legBones[n])
        if n == 0:
            cmds.parent(rig[n], parents[0])
            cmds.parent(ik[n], parents[0])
        else:
            cmds.parent(rig[n], rig[n-1])
            cmds.parent(ik[n], ik[n-1])
        if n == 3:
            ik.append(cmds.joint(n=str(controls[3])[:-4]+'ik_end'))
            cmds.joint(str(controls[n])[:-4]+'ik_end', e=1, r=1, p=(10,0,0))
            length = legControlScaleY[n]
        else:
            length = cmds.xform(parents[n+1], q=1, t=1)[0]
        createSpaceSwitch(1, 1, 1, 0, controls[n], ik[n], rig[n])
        shape = shapes.cube(color)
        cmds.parent(shape, controls[n])
        cmds.xform(shape, t=(length/2,0,0), ro=(0,0,0), s=(length, controlScale*(legControlScaleY[n]), controlScale*(legControlScaleZ[n])))
        addControlShape(shape, controls[n])
        n += 1
    #Build IK Controls
    legIk = cmds.ikHandle(sj=ik[0], ee=ik[2], sol='ikRPsolver', n=controlName[0]+'_ankle_ikHandle')
    ballIk = cmds.ikHandle(sj=ik[2], ee=ik[3], sol='ikSCsolver', n=controlName[0]+'_ball_ikHandle')
    toeIk = cmds.ikHandle(sj=ik[3], ee=ik[4], sol='ikSCsolver', n=controlName[0]+'_toe_ikHandle')
    revIkTrans = []
    n = 0
    for loc in legLoc:
        revIkTrans.append(cmds.createNode('transform', n=prefix+list(loc.split('_'))[0]))
        alignAtoB(revIkTrans[n], loc)
        if n == 0:
            cmds.parent(revIkTrans[n], root)
        elif n == 4:
            cmds.parent(revIkTrans[n], revIkTrans[n-2])
        else:
            cmds.parent(revIkTrans[n], revIkTrans[n-1])
        cmds.makeIdentity(revIkTrans[n], apply=1)
        n += 1
    legIkTrans = cmds.rename(revIkTrans[0], prefix+'Foot_CTRL')
    cmds.parent(legIk[0], revIkTrans[3])
    cmds.parent(ballIk[0], revIkTrans[3])
    cmds.parent(toeIk[0], revIkTrans[4])
    poleVector = createPoleVector(pv, *ik[:3])
    cmds.parent(poleVector, root)
    poleVectorShape = shapes.sphere(color)
    snapAtoB(poleVectorShape, poleVector)
    cmds.xform(poleVectorShape, s=(controlScale, controlScale, controlScale))
    addControlShape(poleVectorShape, poleVector)
    cmds.poleVectorConstraint(poleVector, legIk[0])
    cmds.addAttr(legIkTrans, ln='twist', at='float', k=1)
    cmds.connectAttr(legIkTrans+'.twist', legIk[0]+'.twist')
    lockChannels(0, 1, 1, 0, poleVector)
    legIkShape = shapes.cube(color)
    snapAtoB(legIkShape, legIkTrans)
    cmds.xform(legIkShape, s=(controlScale*10, controlScale*10, controlScale*10))
    addControlShape(legIkShape, legIkTrans)
    cmds.xform(legIkTrans, p=1, roo='xzy' )
    #Setup IK Roll Attributes
    #ikAttrNames = [toeLift, ballRoll, ballSwivel, toeWiggle, heelLift]
    #for name in ikAttrNames:
    #    cmds.addAttr(legIkTrans, ln=name, at='float', k=1)
    #    cmds.connectAttr(legIkTrans+'.'+name, revIkTrans[])
    #Setup IKFK Attributes
    #cmds.addAttr(root, ln=attrName+'IK_FK', at='float', k=1, min=0, max=1)
    #cmds.addAttr(root, ln=attrName+'Template', at='float', k=1, min=0, max=1)
    #cmds.addAttr(root, ln=attrName+'Visibility', at='float', k=1, min=0, max=1)
    #Hook up IK FK
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[0]+'.spaceBlend')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[1]+'.spaceBlend')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', rig[2]+'.spaceBlend')
    ##Hook up Template
    #templateSwitch = cmds.createNode('multiplyDivide', n=controlName+'_templateSwitch')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', templateSwitch+'.input1X')
    #cmds.connectAttr(root+'.'+attrName+'Template', templateSwitch+'.input2X')
    #cmds.connectAttr(templateSwitch+'.outputX', parents[0]+'.template')
    #templateReverse = cmds.createNode('reverse', n=controlName+'_tempateReverse')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', templateReverse+'.inputX')
    #cmds.connectAttr(templateReverse+'.outputX', templateSwitch+'.input1Y')
    #cmds.connectAttr(root+'.'+attrName+'Template', templateSwitch+'.input2Y')
    #cmds.connectAttr(templateSwitch+'.outputY', legIkTrans+'.template')
    #cmds.connectAttr(templateSwitch+'.outputY', poleVector+'.template')
    ##Hook up Visibility
    #visIkCondition = cmds.createNode('condition', n=controlName+'_visibilityIkCondition')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', visIkCondition+'.firstTerm')
    #cmds.setAttr(visIkCondition+'.secondTerm', 0.5)
    #cmds.setAttr(visIkCondition+'.operation', 3)
    #cmds.setAttr(visIkCondition+'.colorIfTrueR', 1)
    #cmds.connectAttr(root+'.'+attrName+'Visibility', visIkCondition+'.colorIfFalseR')
    #cmds.connectAttr(visIkCondition+'.outColorR', legIkTrans+'.visibility')
    #cmds.connectAttr(visIkCondition+'.outColorR', poleVector+'.visibility')
    #visFkCondition = cmds.createNode('condition', n=controlName+'_visibilityFkCondition')
    #cmds.connectAttr(root+'.'+attrName+'IK_FK', visFkCondition+'.firstTerm')
    #cmds.setAttr(visFkCondition+'.secondTerm', 0.5)
    #cmds.setAttr(visFkCondition+'.operation', 5)
    #cmds.setAttr(visFkCondition+'.colorIfTrueR', 1)
    #cmds.connectAttr(root+'.'+attrName+'Visibility', visFkCondition+'.colorIfFalseR')
    #cmds.connectAttr(visFkCondition+'.outColorR', parents[0]+'.visibility')
    ##Create Strechy IK
    #distance = cmds.createNode('distanceBetween', n=controlName+'_distance')
    #stretchStart = cmds.createNode('transform', n=controlName+'_stretchStart')
    #stretchEnd = cmds.createNode('transform', n=controlName+'_stretchEnd')
    #cmds.pointConstraint(parents[0], stretchStart)
    #cmds.pointConstraint(legIkTrans, stretchEnd)
    #cmds.connectAttr(stretchStart+'.translate', distance+'.point1')
    #cmds.connectAttr(stretchEnd+'.translate', distance+'.point2')
    #armLen = (cmds.xform(ik[1], q=1, t=1)[0])+(cmds.xform(ik[2], q=1, t=1)[0])
    #distanceMult = cmds.createNode('multiplyDivide', n=controlName+'_distanceMult')
    #cmds.setAttr(distanceMult+'.input1X', armLen)
    #cmds.connectAttr(root+'.scaleY', distanceMult+'.input2X')
    #distanceDivide = cmds.createNode('multiplyDivide', n=controlName+'_distanceDivide')
    #cmds.setAttr(distanceDivide+'.operation', 2)
    #cmds.connectAttr(distance+'.distance', distanceDivide+'.input1X')
    #cmds.connectAttr(distanceMult+'.outputX', distanceDivide+'.input2X')
    #stretchCondition = cmds.createNode('condition', n=controlName+'_stretchCondition')
    #cmds.setAttr(stretchCondition+'.operation', 2)
    #cmds.connectAttr(distance+'.distance', stretchCondition+'.firstTerm')
    #cmds.connectAttr(distanceMult+'.outputX', stretchCondition+'.secondTerm')
    #cmds.connectAttr(distanceDivide+'.outputX', stretchCondition+'.colorIfTrueR')
    #cmds.addAttr(legIkTrans, ln='stretch', at='float', k=1, min=0, max=1)
    #stretchBlender = cmds.createNode('blendColors', n=controlName+'_stretchBlender')
    #cmds.connectAttr(legIkTrans+'.stretch', stretchBlender+'.blender')
    #cmds.connectAttr(stretchCondition+'.outColorR', stretchBlender+'.color1R')
    #cmds.connectAttr(stretchBlender+'.outputR', ik[0]+'.scaleX')
    #cmds.connectAttr(stretchBlender+'.outputR', ik[1]+'.scaleX')
    #cmds.setAttr(stretchBlender+'.color2R', 1)
    ##Lock and Hide
    #lockChannels(1, 1, 1, 0, *rig)
    #hideChannels(*ik)
    #hideChannels(legIk, ballIk)
    #cmds.setAttr(ik[0]+'.visibility', 0)
    #cmds.setAttr(legIk+'.visibility', 0)
    #cmds.setAttr(ballIk+'.visibility', 0)
    #lockChannels(1, 1, 1, 1, *parents)
    #lockChannels(0, 0, 0, 1, legIkTrans, poleVector)
    #zeroRadius(*parents)

def createHandRig(controlScale=1, *args):
    wrist = args or cmds.ls(sl=True) or []
    fingers, digitNames = selectFingers(wrist[0])
    fingerControls = []
    fingerParents = []
    for finger in fingers:
        controls, parents = createControlJoint(*finger)
        fingerControls.append(controls)
        fingerParents.append(parents)
    root = str(cmds.listRelatives(wrist, p=1, f=1))
    root = list(root.split('|'))[1]
    wristFollow = cmds.createNode('transform', n=wrist[0]+'_follow')
    snapAtoB(wristFollow, wrist)
    cmds.makeIdentity(wristFollow, apply=1)
    n = 0
    while len(fingerControls) > n:
        fingerSetup(controlScale, wristFollow, fingerParents[n], fingerControls[n])
        n += 1

def selectFingers(*args):
    bones = cmds.ls(args, dag=1, ap=1) or cmds.ls(dag=1, ap=1, sl=1 )
    digitNames = []
    #Sort Digit Names
    for bone in bones:
        digitNames.append(bone.split("_")[1])
    digitNames = list(set(digitNames))
    digitNames.remove(bones[0].split("_")[1])
    fingers = []
    for digit in digitNames:
        fingers.append(filter(lambda x: x.find(digit) > -1 and x.find('end') == -1, bones))
    return fingers, digitNames

def metacarpalSetup(*args):
    fingerControls = args[0]
    fingerParents = args[1]
    fingerControl = args[2]
    fingerControls[0] = cmds.rename(fingerControls[0], str(fingerControls[0])[:-4]+'ik')
    ikEnd = cmds.rename(createParent(fingerParents[1]), fingerControls[0]+'_end')
    #Create IK
    fingerIk = cmds.ikHandle(sj=fingerControls[0], ee=ikEnd, sol='ikSCsolver', n=str(fingerControls[0])[:-4]+'ikHandle')
    cmds.parent(fingerIk[0], fingerControl)
    knuckleParent = createSpaceSwitch(0, 1, 0, 1, fingerParents[0], fingerParents[1])
    lockChannels(1, 1, 1, 0, fingerIk[0], ikEnd, knuckleParent)
    zeroRadius(ikEnd, knuckleParent)
    cmds.setAttr(fingerIk[0]+'.visibility', 0)

def fingerSetup(controlScale=1, *args):
    wristFollow = args[0]
    fingerControls = args[2]
    fingerParents = args[1]
    print fingerControls
    color = limbColor(wristFollow)
    if len(fingerParents) == 4 or str(fingerParents[0]).find('thumb') > -1:
        knuckle = fingerControls[1]
    else:
        knuckle = fingerControls[0]
    if color == 6:
        dirMod = [1,-1]
    else:
        dirMod = [0,1]
    fingerControl = cmds.createNode('transform', n=str(fingerParents[0])[:-5]+'CTRL')
    snapAtoB(fingerControl, knuckle)
    cmds.parent(fingerControl, wristFollow)
    createSpaceSwitch(1, 1, 0, 1, fingerParents[0], fingerControl)
    #Add Attributes
    cmds.addAttr(fingerControl, ln='base', at='float', k=1)
    cmds.addAttr(fingerControl, ln='mid', at='float', k=1)
    cmds.addAttr(fingerControl, ln='tip', at='float', k=1)
    cmds.addAttr(fingerControl, ln='spread', at='float', k=1)
    cmds.addAttr(fingerControl, ln='twist', at='float', k=1)
    #Connect Attributes
    n = 0
    if str(fingerParents[0]).find('thumb') > -1:
        cmds.connectAttr(fingerControl+'.spread', fingerParents[0+n]+'.rotateY')
    else:
        spreadMult = cmds.createNode('multiplyDivide', n=str(fingerParents[0])[:-5]+'spreadMult')
        cmds.connectAttr(fingerControl+'.spread', spreadMult+'.input1X')
        cmds.connectAttr(fingerControl+'.spread', spreadMult+'.input1Y')
        cmds.setAttr(spreadMult+'.input2X', 0.25)
        if str(fingerParents[0]).find('middle') > -1:
            cmds.setAttr(spreadMult+'.input2X', 0.1)
            cmds.setAttr(spreadMult+'.input2Y', 0.5)
        if str(fingerParents[0]).find('ring') > -1:
            cmds.setAttr(spreadMult+'.input2X', -0.1)
            cmds.setAttr(spreadMult+'.input2Y', -0.5)
        if str(fingerParents[0]).find('pinky') > -1:
            cmds.setAttr(spreadMult+'.input2X', -0.25)
            cmds.setAttr(spreadMult+'.input2Y', -1.0)
        if len(fingerParents) == 4:
            cmds.connectAttr(spreadMult+'.outputX', fingerParents[0]+'.rotateY')
            cmds.connectAttr(spreadMult+'.outputY', fingerParents[1]+'.rotateY')
            n = 1
        else:
            cmds.connectAttr(spreadMult+'.outputY', fingerParents[0]+'.rotateY')
    cmds.connectAttr(fingerControl+'.base', fingerParents[0+n]+'.rotateZ')
    cmds.connectAttr(fingerControl+'.mid', fingerParents[1+n]+'.rotateZ')
    cmds.connectAttr(fingerControl+'.tip', fingerParents[2+n]+'.rotateZ')
    cmds.connectAttr(fingerControl+'.twist', fingerParents[0+n]+'.rotateX')
    #Add Control Shape
    fingerControlShape = shapes.heart(color)
    fingerControlShape = cmds.rename(fingerControlShape, str(fingerParents[0])[:-6]+'shape')
    cmds.parent(fingerControlShape, knuckle)
    cmds.xform(fingerControlShape, ro=(180*dirMod[0],-90,0), t=(0,1*controlScale*dirMod[1],0), s=(controlScale, controlScale, controlScale))
    addControlShape(fingerControlShape, fingerControl)
    #Metacarpal
    if len(fingerControls) == 4 or str(fingerParents[0]).find('thumb') > -1:
        metacarpalSetup(fingerControls, fingerParents, fingerControl)
        lockChannels(0, 1, 1, 0, fingerControl)
    else:
        lockChannels(1, 1, 1, 0, fingerControl)
    #Lock Bones
    lockChannels(1, 1, 1, 0, *fingerParents)
    zeroRadius(*fingerParents)

def freezeJointRotation(*args):
    joints = args or cmds.ls(sl=True) or []
    for joint in joints:
        parent = cmds.listRelatives(joint, p=1)
        parentTrans = cmds.createNode('transform')
        if parent:
            alignAtoB(parentTrans, parent)
        trans = cmds.createNode('transform')
        cmds.parent(trans, parentTrans)
        alignAtoB(trans, joint)
        rotValues = cmds.xform(trans, q=1, ro=1)
        cmds.delete(parentTrans)
        cmds.setAttr(joint+'.jointOrientX', rotValues[0])
        cmds.setAttr(joint+'.jointOrientY', rotValues[1])
        cmds.setAttr(joint+'.jointOrientZ', rotValues[2])
        cmds.setAttr(joint+'.rotate', 0, 0, 0)
    cmds.select(joints)

def createSpaceSwitch(point = 1, orient = 1, scale = 1, parent = 1, *spaceBones):
    spaceBones = spaceBones or cmds.ls(sl=True) or []
    object = spaceBones[len(spaceBones)-1]
    spaces = spaceBones[:-1]
    if parent == 1:
        spaceBlendObj = createParent(object)
        spaceBlendObj = spaceBlendObj[0]
    else:
        spaceBlendObj = object
    #Setup _ori_ offsets
    oris = []
    for space in spaces:
        oriName = str(space+'_ori_'+spaceBlendObj)
        oriName = oriName.replace('CTRL', 'control')
        if cmds.objExists(oriName):
            oris.append(oriName)
        else:
            ori = cmds.createNode('transform', n=oriName)
            alignAtoB(ori, object)
            cmds.parent(ori, space)
            lockChannels(1, 1, 1, 0, ori)
            oris.append(ori)
    #Setup Constraints
    if point == 1:
        posCon = cmds.pointConstraint(oris, spaceBlendObj)
    if orient == 1:
        oriCon = cmds.orientConstraint(oris, spaceBlendObj)
    if scale == 1:
        weightedX = cmds.createNode('blendWeighted')
        weightedY = cmds.createNode('blendWeighted')
        weightedZ = cmds.createNode('blendWeighted')
        n = 0
        while n < len(oris):
            cmds.connectAttr(spaces[n]+'.scaleX', weightedX+'.input['+str(n)+']')
            cmds.connectAttr(spaces[n]+'.scaleY', weightedY+'.input['+str(n)+']')
            cmds.connectAttr(spaces[n]+'.scaleZ', weightedZ+'.input['+str(n)+']')
            n += 1
        cmds.connectAttr(weightedX+'.output', spaceBlendObj+'.scaleX')
        cmds.connectAttr(weightedY+'.output', spaceBlendObj+'.scaleY')
        cmds.connectAttr(weightedZ+'.output', spaceBlendObj+'.scaleZ')
    #Setup Blending
    if len(oris) > 1:
        if not cmds.attributeQuery('spaceBlend', node=str(spaceBlendObj), ex=1):
            cmds.addAttr(spaceBlendObj, ln='spaceBlend', at='double', min=0)
        cmds.addAttr(spaceBlendObj+'.spaceBlend', e=1, max=(len(oris)-1))
        cmds.setAttr(spaceBlendObj+'.spaceBlend', e=1, k=1)
        if point == 1:
            n = 0
            while n < len(oris):
                t = 0
                while t < len(oris):
                    cmds.setDrivenKeyframe(
                        posCon[0]+'.'+oris[t]+'W'+str(t),
                        cd=spaceBlendObj+'.spaceBlend',
                        ott='linear',
                        itt='linear',
                        dv=n,
                        v=0
                    )
                    t += 1
                cmds.setDrivenKeyframe(
                    posCon[0]+'.'+oris[n]+'W'+str(n),
                    cd=spaceBlendObj+'.spaceBlend',
                    ott='linear',
                    itt='linear',
                    dv=n,
                    v=1
                )
                n += 1
        if orient == 1:
            n = 0
            while n < len(oris):
                t = 0
                while t < len(oris):
                    cmds.setDrivenKeyframe(
                        oriCon[0]+'.'+oris[t]+'W'+str(t),
                        cd=spaceBlendObj+'.spaceBlend',
                        ott='linear',
                        itt='linear',
                        dv=n,
                        v=0
                    )
                    t += 1
                cmds.setDrivenKeyframe(
                    oriCon[0]+'.'+oris[n]+'W'+str(n),
                    cd=spaceBlendObj+'.spaceBlend',
                    ott='linear',
                    itt='linear',
                    dv=n,
                    v=1
                )
                n += 1
        if scale == 1:
            n = 0
            while n < len(oris):
                t = 0
                while t < len(oris):
                    cmds.setDrivenKeyframe(
                        weightedX+'.weight['+str(t)+']',
                        cd=spaceBlendObj+'.spaceBlend',
                        ott='linear',
                        itt='linear',
                        dv=n,
                        v=0
                    )
                    cmds.setDrivenKeyframe(
                        weightedY+'.weight['+str(t)+']',
                        cd=spaceBlendObj+'.spaceBlend',
                        ott='linear',
                        itt='linear',
                        dv=n,
                        v=0
                    )
                    cmds.setDrivenKeyframe(
                        weightedZ+'.weight['+str(t)+']',
                        cd=spaceBlendObj+'.spaceBlend',
                        ott='linear',
                        itt='linear',
                        dv=n,
                        v=0
                    )
                    t += 1
                cmds.setDrivenKeyframe(
                    weightedX+'.weight['+str(n)+']',
                    cd=spaceBlendObj+'.spaceBlend',
                    ott='linear',
                    itt='linear',
                    dv=n,
                    v=1
                )
                cmds.setDrivenKeyframe(
                    weightedY+'.weight['+str(n)+']',
                    cd=spaceBlendObj+'.spaceBlend',
                    ott='linear',
                    itt='linear',
                    dv=n,
                    v=1
                )
                cmds.setDrivenKeyframe(
                    weightedZ+'.weight['+str(n)+']',
                    cd=spaceBlendObj+'.spaceBlend',
                    ott='linear',
                    itt='linear',
                    dv=n,
                    v=1
                )
                n += 1
        cmds.select(spaceBlendObj)
    return spaceBlendObj

def createParent(*childeren):
    childeren = childeren or cmds.ls(sl=True) or []
    newParents = []
    if childeren:
        n = 0
        for child in childeren:
            currentParent = cmds.listRelatives(child, p=1, f=1)
            cmds.select(cl=1)
            if cmds.nodeType(currentParent) == 'joint':
                newParents.append(cmds.joint(n=child+'_par'))
            else:
                newParents.append(cmds.createNode('transform', n=child+'_par'))
            newName = str(newParents[n]).replace('CTRL', 'control')
            newParents[n] = cmds.rename(newParents[n], newName)
            alignAtoB(newParents[n], child)
            if currentParent:
                cmds.parent(newParents[n], currentParent)
            cmds.parent(child, newParents[n])
            n += 1
        return newParents

def createControlJoint(*args):
    args = args or cmds.ls(sl=True) or []
    ctrlBones = []
    ctrlParents = []
    for bone in args:
        cmds.select(cl=1)
        unlockChannels(bone)
        ctrlBone = cmds.joint(n=bone+'_CTRL')
        ctrlBones.append(ctrlBone)
        alignAtoB(ctrlBone, bone)
        #look for rig parent
        boneParent = cmds.listRelatives(bone, p=1)
        while boneParent:
            if cmds.objExists(boneParent[0]+'_RIG') and cmds.nodeType(boneParent[0]+'_RIG') == 'joint':
                cmds.parent(ctrlBone, boneParent[0]+'_RIG')
                break
            elif cmds.objExists(boneParent[0]+'_CTRL') and cmds.nodeType(boneParent[0]+'_CTRL') == 'joint':
                cmds.parent(ctrlBone, boneParent[0]+'_CTRL')
                break
            elif cmds.objExists(boneParent[0]+'_ik') and cmds.nodeType(boneParent[0]+'_ik') == 'joint':
                cmds.parent(ctrlBone, boneParent[0]+'_ik')
                break
            elif cmds.objExists(boneParent[0]+'_ik_end') and cmds.nodeType(boneParent[0]+'_ik_end') == 'joint':
                cmds.parent(ctrlBone, boneParent[0]+'_ik_end')
                break
            else:
                boneParent = cmds.listRelatives(boneParent[0], p=1)
        #check for offset
        trans = cmds.xform(ctrlBone, q=1, os=1, t=1)
        rot = cmds.xform(ctrlBone, q=1, os=1, ro=1)
        if (abs(trans[0])+abs(trans[1])+abs(trans[2])+abs(rot[0])+abs(rot[1])+abs(rot[2]) > 0.0001):
            ctrlBoneGrp = cmds.joint(n=bone+'_grp')
            ctrlParents.append(ctrlBoneGrp)
            alignAtoB(ctrlBoneGrp, ctrlBone)
            cmds.parent(ctrlBoneGrp, w=1)
            ctrlParent = cmds.listRelatives(ctrlBone, p=1)
            if ctrlParent:
                cmds.parent(ctrlBoneGrp, ctrlParent[0])
            cmds.parent(ctrlBone, ctrlBoneGrp, a=1)
            zeroJointRotation(ctrlBone)
        createJointConnection(ctrlBone, bone)
    return ctrlBones, ctrlParents

def createJointConnection(*args):
    joints = args or cmds.ls(sl=1)
    cmds.pointConstraint(joints[0], joints[1])
    cmds.orientConstraint(joints[0], joints[1])
    cmds.connectAttr(joints[0]+'.scaleX', joints[1]+'.scaleX')
    cmds.connectAttr(joints[0]+'.scaleY', joints[1]+'.scaleY')
    cmds.connectAttr(joints[0]+'.scaleZ', joints[1]+'.scaleZ')
    lockChannels(1, 1, 1, 0, joints[1])
    if not cmds.attributeQuery('controlJoint', node=joints[1], ex=1):
        cmds.addAttr(joints[1], ln='controlJoint', dt='string')
    if not cmds.attributeQuery('isHookedUp', node=joints[1], ex=1):
        cmds.addAttr(joints[1], ln='isHookedUp', at='bool')
    incoming = cmds.listConnections(joints[1]+'.controlJoint', s=1, d=0, scn=1, p=1)
    if incoming:
        cmds.disconnectAttr(str(incoming[0]), joints[1]+'.controlJoint')
    cmds.connectAttr(joints[0]+'.message', joints[1]+'.controlJoint')
    cmds.setAttr(joints[1]+'.isHookedUp', l=0)
    cmds.setAttr(joints[1]+'.isHookedUp', 1)
    cmds.setAttr(joints[1]+'.isHookedUp', l=1)

def connectJoints(*args):
    joints = args or cmds.ls(sl=1)
    for joint in joints:
        if cmds.attributeQuery('controlJoint', node=joint, ex=1) and cmds.attributeQuery('isHookedUp', node=joint, ex=1) and cmds.getAttr(joint+'.isHookedUp') == 0:
            incoming = cmds.listConnections(joint+'.controlJoint', s=1, d=0, scn=1)
            createJointConnection(incoming[0], joint)

def disconnectJoints(*args):
    joints = args or cmds.ls(sl=1)
    for joint in joints:
        if cmds.attributeQuery('isHookedUp', node=joint, ex=1):
            cmds.setAttr(joint+'.isHookedUp', l=0)
            cmds.setAttr(joint+'.isHookedUp', 0)
            cmds.setAttr(joint+'.isHookedUp', l=1)
            unlockChannels(joint)
            cmds.delete(cmds.listRelatives(joint, type='pointConstraint'))
            cmds.delete(cmds.listRelatives(joint, type='orientConstraint'))
            inputX = cmds.listConnections(joint+'.scaleX', s=1, d=0, scn=1, p=1)
            inputY = cmds.listConnections(joint+'.scaleY', s=1, d=0, scn=1, p=1)
            inputZ = cmds.listConnections(joint+'.scaleZ', s=1, d=0, scn=1, p=1)
            cmds.disconnectAttr(inputX[0], joint+'.scaleX')
            cmds.disconnectAttr(inputY[0], joint+'.scaleY')
            cmds.disconnectAttr(inputZ[0], joint+'.scaleZ')

def newJointConnection(*args):
    joints = args or cmds.ls(sl=1)
    if cmds.getAttr(joints[1]+'.isHookedUp') == 1:
        disconnectJoints(joints[1])
    incoming = cmds.listConnections(joints[1]+'.controlJoint', s=1, d=0, scn=1, p=1)
    cmds.disconnectAttr(str(incoming[0]), joints[1]+'.controlJoint')
    cmds.connectAttr(joints[0]+'.message', joints[1]+'.controlJoint')
    connectJoints(joints[1])

def zeroJointRotation(*args):
    args = args or cmds.ls(sl=1)
    channels = ["rotateX", "rotateY", "rotateZ", "jointOrientX", "jointOrientY", "jointOrientZ"]
    for node in args:
        for channel in channels:
            cmds.setAttr(node+'.'+channel, 0)

def unlockChannels(*args):
    args = args or cmds.ls(sl=1)
    channels = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]
    for node in args:
        for channel in channels:
            cmds.setAttr(node+'.'+channel, k=1, l=0)

def lockChannels(p=1, r=1, s=1, v=1, *args):
    args = args or cmds.ls(sl=1)
    channels = []
    if p == 1:
        channels.append("translateX")
        channels.append("translateY")
        channels.append("translateZ")
    if r == 1:
        channels.append("rotateX")
        channels.append("rotateY")
        channels.append("rotateZ")
    if s == 1:
        channels.append("scaleX")
        channels.append("scaleY")
        channels.append("scaleZ")
    if v == 1:
        channels.append("visibility")
    for node in args:
        for channel in channels:
            cmds.setAttr(node+'.'+channel, k=0, l=1)

def hideChannels(*args):
    args = args or cmds.ls(sl=1)
    channels = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ", "scaleX", "scaleY", "scaleZ"]
    for node in args:
        for channel in channels:
            cmds.setAttr(node+'.'+channel, k=0)

def zeroRadius(*args):
    bones = args or cmds.ls(sl=1)
    for node in bones:
        cmds.setAttr(node+'.radius', 0)

def alignAtoB(*args):
    snap = args or cmds.ls(sl=1)
    cmds.delete(cmds.pointConstraint(snap[1], snap[0]))
    cmds.delete(cmds.orientConstraint(snap[1], snap[0]))

def snapAtoB(*args):
    snap = args or cmds.ls(sl=1)
    cmds.delete(cmds.pointConstraint(snap[1], snap[0]))

def limbColor(*args):
    bones = args or cmds.ls(sl=1)
    if cmds.xform(bones[0], q=1, t=1, ws=1)[0] > 0:
        color = 3
    else:
        color = 6
    return color

def limbPrefix(*args):
    bones = args or cmds.ls(sl=1)
    if cmds.xform(bones[0], q=1, t=1, ws=1)[0] > 0:
        prefix = 'L_'
    else:
        prefix = 'R_'
    return prefix

def addControlShape(*args):
    items = args or cmds.ls(sl=1)
    shape = cmds.listRelatives(items[0], shapes=1)
    cmds.parent(shape, items[1], shape=1, absolute=1)
    shapeParent = cmds.listRelatives(shape, parent=1)
    cmds.makeIdentity(shapeParent, apply=True)
    cmds.parent(shape, items[1], shape=1, relative=1)
    cmds.delete(items[0])
    cmds.delete(shapeParent)

def findSkinnedBones(*skinMesh):
    skinMesh = skinMesh or cmds.ls(sl=True) or []
    skinBones = cmds.skinCluster(skinMesh, q=1, influence=1)
    cmds.select(skinBones)
    return(skinBones)

def createPoleVector(pv=1, *args):
    bones = args or cmds.ls(sl=True) or []
    boneA = om.MVector(cmds.xform(bones[0], q=1, t=1, ws=1))
    boneB = om.MVector(cmds.xform(bones[1], q=1, t=1, ws=1))
    boneC = om.MVector(cmds.xform(bones[2], q=1, t=1, ws=1))
    armCenter = (boneC-boneA)*0.5
    poleVectorPos = ((boneA+(armCenter*(pv*0.95)))-boneB)
    poleVectorPos = poleVectorPos.normal()*(armCenter.length()*-2)+boneB
    poleVector = cmds.createNode('transform', n=str(bones[0])[0]+'_pv')
    cmds.xform(poleVector, t=poleVectorPos)
    cmds.makeIdentity(poleVector, apply=1)
    return poleVector
