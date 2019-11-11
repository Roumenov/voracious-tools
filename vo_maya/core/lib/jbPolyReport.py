# Poly Report, by Joshua Buck, (c)2019, all rights reserved

"""
import jbPolyReport
jbPolyReport.jbPolyReportGo()
"""

import maya.cmds as cmds

defColor = 0.3, 0.3, 0.3
passColor = (0.17, 1.0, 0.17)
warningColor = (1.0, 1.0, 0.17)
errorColor = (1.0, 0.17, 0.17)

def jbPolyReportGo():
    jbPolyReportWIN()
    jbPolyReportUI()


def jbPolyReportWIN():
    version = 1.01
    if cmds.window("jbPrWin", exists=True):
        cmds.deleteUI("jbPrWin", window=True)

    # if cmds.windowPref("jbPrWin", exists=True):
    #     cmds.windowPref('jbPrWin', remove=True)

    cmds.window("jbPrWin", title="Poly Report  v" + str(version), mnb=False, mxb=False, s=True)

    cmds.columnLayout("mainUI_C", p="jbPrWin")

    cmds.showWindow("jbPrWin")
    cmds.window("jbPrWin", e=True, h=1)


def jbPolyReportUI():
    mainCW = 300
    warningTitleCW = 100
    warningContentCW = 280

    # General Mesh Info
    cmds.rowColumnLayout(nc=1, cw=[(1, mainCW)], p="mainUI_C")
    cmds.separator(h=4, style='none')

    cmds.rowColumnLayout(nc=2, cw=[(1, 100), (2,180)], p="mainUI_C")
    cmds.text(l="Mesh Name:   ", align="right", font="boldLabelFont")
    cmds.text("meshName_TX", l='No Mesh', align="left", font="boldLabelFont")

    cmds.rowColumnLayout(nc=1, cw=[(1, 280)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8)

    cmds.rowColumnLayout(nc=4, cw=[(1, 80),(2,60),(3,75),(4,50)], p="mainUI_C")

    cmds.text(l='Triangles:  ', align="right")
    cmds.text("numTriangles_TX", l='', align="left")

    cmds.text(l='Edges:  ', align="right")
    cmds.text("numEdges_TX", l='', align="left")

    cmds.text(l='Faces:  ', align="right")
    cmds.text("numFaces_TX", l='', align="left")

    cmds.text(l='Vertices:  ', align="right")
    cmds.text("numVerts_TX", l='', align="left")

    cmds.text(l='Mesh Shells:  ', align="right")
    cmds.text("numMeshShells_TX", l='', align="left")

    cmds.text(l='Shapes:  ', align="right")
    cmds.text("numShapes_TX", l='', align="left")

    cmds.text(l='Parents:  ', align="right")
    cmds.text("parents_TX", l='', align="left")

    cmds.text(l='Children:  ', align="right")
    cmds.text("children_TX", l='', align="left")

    cmds.rowColumnLayout(nc=1, cw=[(1, mainCW)], p="mainUI_C")
    cmds.separator(h=4, style='none')

    cmds.rowColumnLayout(nc=4, cw=[(1, 80), (2, 60), (3, 75), (4, 50)], p="mainUI_C")

    cmds.text(l='Materials:  ', align="right")
    cmds.text("materials_TX", l='', align="left")

    cmds.text(l='UV Sets:  ', align="right")
    cmds.text("uvSets_TX", l='', align="left")

    cmds.text(l='UV Points:  ', align="right")
    cmds.text("uvPoints_TX", l='', align="left")

    cmds.text(l='UV Shells:  ', align="right")
    cmds.text("uvShells_TX", l='', align="left")

    cmds.rowColumnLayout(nc=1, cw=[(1, mainCW)], p="mainUI_C")
    cmds.separator(h=4, style='none')

    cmds.rowColumnLayout(nc=4, cw=[(1, 80), (2, 40), (3, 95), (4, 74)], p="mainUI_C")

    cmds.text(l='Has History:  ', align="right")
    cmds.text("hasHistory_TX", l='', align="left")

    cmds.text(l='Transformations:  ', align="right")
    cmds.text("transformations_TX", l='', align="left")

    cmds.rowColumnLayout(nc=1, cw=[(1, 280)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8)

    # Face Info
    cmds.rowColumnLayout(nc=3, cw=[(1, 130), (2, 14), (3, 75)], cs=[(1,0),(2,6),(3,6)], p="mainUI_C")

    cmds.text(l='Quadrilaterals:', align="right")
    cmds.button("quadFaces_BUT", l='', h=14, bgc=defColor)
    cmds.text("quadFaces_TX", l='', align="left")

    cmds.text(l='Defined Triangles:', align="right")
    cmds.button("triangleFaces_BUT", l='', h=14, bgc=defColor)
    cmds.text("triangleFaces_TX", l='', align="left")

    cmds.text(l='N-Gons:', align="right")
    cmds.button("faceFivePlusEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("faceFivePlusEdges_TX", l='', align="left")


    cmds.rowColumnLayout(nc=1, cw=[(1, mainCW)], p="mainUI_C")
    cmds.separator(h=8, style='none')

    # Vertex Info
    cmds.rowColumnLayout(nc=3, cw=[(1, 130), (2, 14), (3, 75)], cs=[(1,0),(2,6),(3,6)], p="mainUI_C")

    cmds.text(l='Vertices w/2 Edges:', align="right")
    cmds.button("vtxTwoEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("vtxTwoEdges_TX", l='', align="left")

    cmds.text(l='Vertices w/3 Edges:', align="right")
    cmds.button("vtxThreeEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("vtxThreeEdges_TX", l='', align="left")

    cmds.text(l='Vertices w/4 Edges:', align="right")
    cmds.button("vtxFourEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("vtxFourEdges_TX", l='', align="left")

    cmds.text(l='Vertices w/5+ Edges:', align="right")
    cmds.button("vtxFivePlusEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("vtxFivePlusEdges_TX", l='', align="left")

    # General Cleanup Info
    cmds.rowColumnLayout(nc=1, cw=[(1, 280)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8)
    # cmds.text(l='Examine / Cleanup', font="boldLabelFont")
    # cmds.separator(h=5, style='none')

    cmds.rowColumnLayout(nc=3, cw=[(1, 130), (2, 14), (3, 75)], cs=[(1, 0), (2, 6), (3, 6)], p="mainUI_C")

    cmds.text(l='Faces w/Zero Area:', align="right")
    cmds.button("faceZeroAreaSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("faceZeroArea_TX", l='', align="left")

    cmds.text(l='Faces w/2 Edges:', align="right")
    cmds.button("faceTwoEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("faceTwoEdges_TX", l='', align="left")

    cmds.text(l='Vertices Sharing Space:', align="right")
    cmds.button("vtxSharingSpaceSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("vtxSharingSpace_TX", l='', align="left")

    cmds.text(l='Nonmanifold Edges:', align="right")
    cmds.button("nonmanifoldEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("nonmanifoldEdges_TX", l='', align="left")

    cmds.text(l='Nonmanifold UV Edges:', align="right")
    cmds.button("nonmanifoldUvEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("nonmanifoldUvEdges_TX", l='', align="left")

    cmds.text(l='Nonmanifold UVs:', align="right")
    cmds.button("nonmanifoldUvsSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("nonmanifoldUvs_TX", l='', align="left")

    cmds.text(l='UV Faces w/Zero Area:', align="right")
    cmds.button("uvZeroAreaFaces_BUT", l='', h=14, bgc=defColor)
    cmds.text("uvZeroAreaFaces_TX", l='', align="left")

    cmds.text(l='Lamina Faces:', align="right")
    cmds.button("laminaFacesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("laminaFaces_TX", l='', align="left")

    cmds.text(l='Invalid Edges:', align="right")
    cmds.button("invalidEdgesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("invalidEdges_TX", l='', align="left")

    cmds.text(l='Invalid Vertices:', align="right")
    cmds.button("invalidVerticesSelect_BUT", l='', h=14, bgc=defColor)
    cmds.text("invalidVertices_TX", l='', align="left")

    cmds.rowColumnLayout(nc=1, cw=[(1, 280)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8)

    # Notice
    cmds.rowColumnLayout(nc=1, cw=[(1, warningTitleCW)], cs=[(1,10)],  p="mainUI_C")
    cmds.text(l="Notice:", font="boldLabelFont", align="left")

    cmds.rowColumnLayout("meshNotice_RCL", nc=1, cw=[(1, warningContentCW)], cs=[(1,20)], p="mainUI_C")

    # Warnings
    cmds.rowColumnLayout(nc=1, cw=[(1, warningTitleCW)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8, style='none')
    cmds.text(l="Warnings:", font="boldLabelFont", align="left")

    cmds.rowColumnLayout("meshWarnings_RCL", nc=1, cw=[(1, warningContentCW)], cs=[(1,15)], p="mainUI_C")

    # Errors
    cmds.rowColumnLayout(nc=1, cw=[(1, warningTitleCW)],cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=8, style='none')
    cmds.text(l="Errors:", font="boldLabelFont", align="left")

    cmds.rowColumnLayout("meshErrors_RCL", nc=1, cw=[(1, warningContentCW)], cs=[(1,15)], p="mainUI_C")

    # Action Button
    cmds.rowColumnLayout(nc=1, cw=[(1, 280)], cs=[(1,10)], p="mainUI_C")
    cmds.separator(h=10, style='none')
    cmds.button(l='Report', h=30, c=lambda args: generatePolyReport())
    cmds.separator(h=8, style='none')



def generatePolyReport():
    sel = cmds.ls(sl=True, o=True)
    if len(sel) != 1:
        cmds.warning("Please select a single object of type: mesh")
        return None
    sel = sel[0]
    shapes = cmds.listRelatives(sel, shapes=True, fullPath=True)
    if shapes is not None:
        for each in shapes:
            if cmds.nodeType(each) != "mesh":
                cmds.warning("Selection type must be of type: mesh")
                return None
    else:
        cmds.warning("Selection has no mesh components. Make sure you are in object mode.")
        return None

    # report list [0] = info, [1] = warnings, [2] = errors
    printReport = [[], [], []]

    # MESH
    meshReport = processMesh(sel)
    if meshReport[0]:
        printReport[0].extend(meshReport[0])
    if meshReport[1]:
        printReport[1].extend(meshReport[1])
    if meshReport[2]:
        printReport[2].extend(meshReport[2])

    # FACES
    facesReport = processFaces(sel)
    if facesReport[0]:
        printReport[0].extend(facesReport[0])
    if facesReport[1]:
        printReport[1].extend(facesReport[1])
    if facesReport[2]:
        printReport[2].extend(facesReport[2])

    # VERTICES
    vertexReport = processVertices(sel)
    if vertexReport[0]:
        printReport[0].extend(vertexReport[0])
    if vertexReport[1]:
        printReport[1].extend(vertexReport[1])
    if vertexReport[2]:
        printReport[2].extend(vertexReport[2])

    # processEdges(sel)

    # CLEANUP / EXAMINE
    cleanupReport = processCleanup(sel)
    if cleanupReport[0]:
        printReport[0].extend(cleanupReport[0])
    if cleanupReport[1]:
        printReport[1].extend(cleanupReport[1])
    if cleanupReport[2]:
        printReport[2].extend(cleanupReport[2])

    # UVs
    uvReport = processUvs(sel)
    if uvReport[0]:
        printReport[0].extend(uvReport[0])
    if uvReport[1]:
        printReport[1].extend(uvReport[1])
    if uvReport[2]:
        printReport[2].extend(uvReport[2])

    # Materials
    materialReport = processMaterials(sel)
    if materialReport[0]:
        printReport[0].extend(materialReport[0])
    if materialReport[1]:
        printReport[1].extend(materialReport[1])
    if materialReport[2]:
        printReport[2].extend(materialReport[2])

    # Write report to UI fields
    clearLayoutChildren("meshNotice_RCL")
    for info in printReport[0]:
        cmds.text(l=info, p="meshNotice_RCL", align="left")
    clearLayoutChildren("meshWarnings_RCL")
    for warning in printReport[1]:
        cmds.text(l=warning, p="meshWarnings_RCL", align="left")
    clearLayoutChildren("meshErrors_RCL")
    for error in printReport[2]:
        cmds.text(l=error, p="meshErrors_RCL", align="left")



def processMesh(sel):

    returnReport = [[], [], []]

    parents = cmds.listRelatives(sel, allParents=True)
    children = cmds.listRelatives(sel, ad=True, type="transform")
    shapes = cmds.listRelatives(sel, shapes=True)
    numVerts = cmds.polyEvaluate(sel, vertex=True)
    numEdges = cmds.polyEvaluate(sel, edge=True)
    numTriangles = cmds.polyEvaluate(sel, triangle=True)
    numFaces = cmds.polyEvaluate(sel, face=True)
    numMeshShells = cmds.polyEvaluate(sel, shell=True)
    cmds.text("meshName_TX", e=True, l=sel)
    cmds.text("numVerts_TX", e=True, l=numVerts)
    cmds.text("numEdges_TX", e=True, l=numEdges)
    cmds.text("numTriangles_TX", e=True, l=numTriangles)
    cmds.text("numFaces_TX", e=True, l=numFaces)
    cmds.text("numMeshShells_TX", e=True, l=numMeshShells)
    cmds.text("numShapes_TX", e=True, l=len(shapes))
    if parents is not None:
        for each in parents:
            s = cmds.listRelatives(each, shapes=True)
            if s is None:
                warning = "Mesh's parent has no shape node"
                if warning not in returnReport[0]:
                    returnReport[0].append(warning)
        cmds.text("parents_TX", e=True, l=len(parents))
    else:
        cmds.text("parents_TX", e=True, l="None")
    if children is not None:
        cmds.text("children_TX", e=True, l=len(children))
    else:
        cmds.text("children_TX", e=True, l="None")

    # Mesh history
    ch = cmds.listHistory(sel, pdo=True, il=2)
    if ch is None or not ch or ch[0] == "initialShadingGroup":
        cmds.text("hasHistory_TX", edit=True, l="No")
    else:
        cmds.text("hasHistory_TX", edit=True, l="Yes")
        warning = "Mesh has input/construction history"
        if warning not in returnReport[0]:
            returnReport[0].append(warning)

    # Multiple Shapes Warning
    if len(shapes) > 1:
        returnReport[1].append("Mesh has more than one shape")

    # Default mesh names warning
    defPolyMeshNames = ["Sphere", "Cube", "Cylinder", "Cone", "Torus", "Plane", "Disc", "Pipe", "Pyramid",
                        "Helix", "Surface"]
    for name in defPolyMeshNames:
        if name in sel and sel.startswith("p"):
            warning="Mesh name may be default"
            if warning not in returnReport[0]:
                returnReport[0].append(warning)

    # Transformations
    transAttrX = cmds.getAttr(sel + ".translateX")
    transAttrY = cmds.getAttr(sel + ".translateY")
    transAttrZ = cmds.getAttr(sel + ".translateZ")
    rotateAttrX = cmds.getAttr(sel + ".rotateX")
    rotateAttrY = cmds.getAttr(sel + ".rotateY")
    rotateAttrZ = cmds.getAttr(sel + ".rotateZ")
    scaleAttrX = cmds.getAttr(sel + ".scaleX")
    scaleAttrY = cmds.getAttr(sel + ".scaleY")
    scaleAttrZ = cmds.getAttr(sel + ".scaleZ")

    transformText = "No"

    if transAttrX != 0.0 or transAttrY != 0.0 or transAttrZ != 0.0:
        transformText = "Trns "
        warning = "Translate attributes are not (0, 0, 0)"
        if warning not in returnReport[0]:
            returnReport[0].append(warning)
    if rotateAttrX != 0.0 or rotateAttrY != 0.0 or rotateAttrZ != 0.0:
        transformText = transformText + "Rot "
        warning = "Rotate attributes are not (0, 0, 0)"
        if warning not in returnReport[0]:
            returnReport[0].append(warning)
    if scaleAttrX != 1.0 or scaleAttrY != 1.0 or scaleAttrZ != 1.0:
        transformText = transformText + "Scl"
        warning = "Scale attributes are not (1, 1, 1)"
        if warning not in returnReport[0]:
            returnReport[0].append(warning)

    cmds.text("transformations_TX", e=True, l=transformText)

    return returnReport



def processVertices(sel):
    returnReport = [[], [], []]
    numVerts = cmds.polyEvaluate(sel, vertex=True)

    twoEdgeVerts = []
    threeEdgeVerts = []
    fourEdgeVerts = []
    moreThanFourEdgeVerts = []
    for x in range(numVerts):
        vtxName = sel + ".vtx[" + str(x) + "]"
        vtxEdges = cmds.polyListComponentConversion(vtxName, te=True)
        vtxEdges = cmds.ls(vtxEdges, flatten=True)
        if len(vtxEdges) == 2:
            twoEdgeVerts.append(vtxName)
            warning = "One or more vertices only has two edges"
            if warning not in returnReport[1]:
                returnReport[1].append(warning)
        elif len(vtxEdges) == 3:
            threeEdgeVerts.append(vtxName)
        elif len(vtxEdges) == 4:
            fourEdgeVerts.append(vtxName)
        elif len(vtxEdges) > 4:
            moreThanFourEdgeVerts.append(vtxName)
            warning = "One or more vertices has more than 4 edges (poles)"
            if warning not in returnReport[0]:
                returnReport[0].append(warning)
        else:
            cmds.warning("Unknown number of edges per vertex")

    # Vertex Positions - Test for vertices in common location
    vertexPositions = []
    sharedVertexSpace = []
    for x in range(numVerts):
        vtxName = sel + ".vtx[" + str(x) + "]"
        vtxPos = cmds.xform(vtxName, q=True, t=True, ws=True)
        pos = [round(vtxPos[0], 5), round(vtxPos[1], 5), round(vtxPos[2], 5)]
        if pos in vertexPositions:
            if pos not in sharedVertexSpace:
                sharedVertexSpace.append(pos)
        vertexPositions.append(pos)
    verticesInSharedSpace = []
    if sharedVertexSpace:
        warning = "One or more vertices share space"
        if warning not in returnReport[1]:
            returnReport[1].append(warning)

        for x in range(numVerts):
            vtxName = sel + ".vtx[" + str(x) + "]"
            vtxPos = cmds.xform(vtxName, q=True, t=True, ws=True)
            pos = [round(vtxPos[0], 5), round(vtxPos[1], 5), round(vtxPos[2], 5)]
            for each in sharedVertexSpace:
                if pos == each:
                    verticesInSharedSpace.append(vtxName)

    if twoEdgeVerts:
        cmds.button("vtxTwoEdgesSelect_BUT", e=True, bgc=warningColor, c=lambda args: selectComponent(sel, twoEdgeVerts, "none"))
    else:
        cmds.button("vtxTwoEdgesSelect_BUT", e=True, bgc=defColor)
    cmds.text("vtxTwoEdges_TX", e=True, l=len(twoEdgeVerts))

    cmds.text("vtxThreeEdges_TX", e=True, l=len(threeEdgeVerts))
    cmds.button("vtxThreeEdgesSelect_BUT", e=True, c=lambda args: selectComponent(sel, threeEdgeVerts, "none"))

    cmds.text("vtxFourEdges_TX", e=True, l=len(fourEdgeVerts))
    cmds.button("vtxFourEdgesSelect_BUT", e=True, c=lambda args: selectComponent(sel, fourEdgeVerts, "none"))

    if moreThanFourEdgeVerts:
        cmds.button("vtxFivePlusEdgesSelect_BUT", e=True, bgc=warningColor,
                    c=lambda args: selectComponent(sel, moreThanFourEdgeVerts, "none"))
    else:
        cmds.button("vtxFivePlusEdgesSelect_BUT", e=True, bgc=defColor)
    cmds.text("vtxFivePlusEdges_TX", e=True, l=len(moreThanFourEdgeVerts))

    if verticesInSharedSpace:
        cmds.text("vtxSharingSpace_TX", e=True, l=len(verticesInSharedSpace))
        cmds.button("vtxSharingSpaceSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, verticesInSharedSpace, "none"))
    else:
        cmds.button("vtxSharingSpaceSelect_BUT", e=True, bgc=passColor)
        cmds.text("vtxSharingSpace_TX", e=True, l="None")

    return returnReport


def processFaces(sel):
    returnReport = [[], [], []]

    numFaces = cmds.polyEvaluate(sel, face=True)

    faceAreas = []
    zeroFaceArea = []
    for x in range(numFaces):
        faceName = sel + ".f[" + str(x) + "]"
        faceArea = cmds.polyEvaluate(faceName, faceArea=True)
        faceArea = float("%.5f" % faceArea[0])
        faceAreas.append(faceArea)
        if faceArea == 0.0:
            warning = "One or more faces has zero area"
            if warning not in returnReport[2]:
                returnReport[2].append(warning)
            zeroFaceArea.append(faceName)

    # Face Connections
    twoEdgeFaces = []
    threeEdgeFaces = []
    fourEdgeFaces = []
    moreThanFourEdgeFaces = []
    for x in range(numFaces):
        faceName = sel + ".f[" + str(x) + "]"
        faceEdges = cmds.polyListComponentConversion(faceName, te=True)
        faceEdges = cmds.ls(faceEdges, flatten=True)
        if len(faceEdges) == 2:
            warning = "One or more faces has only two edges"
            if warning not in returnReport[2]:
                returnReport[2].append(warning)
            twoEdgeFaces.append(faceName)
        elif len(faceEdges) == 3:
            threeEdgeFaces.append(faceName)
        elif len(faceEdges) == 4:
            fourEdgeFaces.append(faceName)
        elif len(faceEdges) > 4:
            warning = "One or more faces has more than 4 edges (n-gons)"
            if warning not in returnReport[0]:
                returnReport[0].append(warning)
            moreThanFourEdgeFaces.append(faceName)
        else:
            cmds.warning("Unknown number of edges per face")

    if twoEdgeFaces:
        cmds.text("faceTwoEdges_TX", e=True, l=len(twoEdgeFaces))
        cmds.button("faceTwoEdgesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, twoEdgeFaces, "none"))
    else:
        cmds.button("faceTwoEdgesSelect_BUT", e=True, bgc=passColor)
        cmds.text("faceTwoEdges_TX", e=True,  l="None")

    cmds.text("triangleFaces_TX", e=True, l=len(threeEdgeFaces))
    cmds.button("triangleFaces_BUT", e=True, c=lambda args: selectComponent(sel, threeEdgeFaces, "none"))

    cmds.text("quadFaces_TX", e=True, l=len(fourEdgeFaces))
    cmds.button("quadFaces_BUT", e=True, c=lambda args: selectComponent(sel, fourEdgeFaces, "none"))

    if moreThanFourEdgeFaces:
        cmds.button("faceFivePlusEdgesSelect_BUT", e=True, bgc=warningColor,
                    c=lambda args: selectComponent(sel, moreThanFourEdgeFaces, "none"))
    else:
        cmds.button("faceFivePlusEdgesSelect_BUT", e=True, bgc=defColor)
    cmds.text("faceFivePlusEdges_TX", e=True, l=len(moreThanFourEdgeFaces))


    if zeroFaceArea:
        cmds.text("faceZeroArea_TX", e=True, l=len(zeroFaceArea))
        cmds.button("faceZeroAreaSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, zeroFaceArea, "faceToVertex"))
    else:
        cmds.button("faceZeroAreaSelect_BUT", e=True, bgc=passColor)
        cmds.text("faceZeroArea_TX", e=True, l="None")

    return returnReport



def processUvs(sel):
    returnReport = [[], [], []]

    uvPoints = cmds.polyEvaluate(sel, uv=True)
    uvShells = cmds.polyEvaluate(sel, us=True)
    uvSets = cmds.polyUVSet(sel, q=True, allUVSets=True)

    numFaces = cmds.polyEvaluate(sel, face=True)
    uvZeroAreaFaces = []
    for x in range(numFaces):
        faceName = sel + ".f[" + str(x) + "]"
        uvFaceArea = cmds.polyEvaluate(faceName, ufa=True)

        if uvFaceArea:
            if uvFaceArea[0] == 0.0:
                uvZeroAreaFaces.append(faceName)
        else:
            warning = "Mesh has no UVs"
            if warning not in returnReport[0]:
                returnReport[0].append(warning)

    cmds.text("uvPoints_TX", e=True, l=uvPoints)
    cmds.text("uvShells_TX", e=True, l=uvShells)
    cmds.text("uvSets_TX", e=True, l=len(uvSets))

    if uvZeroAreaFaces:
        cmds.text("uvZeroAreaFaces_TX", e=True, l=len(uvZeroAreaFaces))
        cmds.button("uvZeroAreaFaces_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, uvZeroAreaFaces, "none"))
        warning = "One or more UV faces has zero area"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
    else:
        cmds.button("uvZeroAreaFaces_BUT", e=True, bgc=passColor)
        cmds.text("uvZeroAreaFaces_TX", e=True, l="None")

    return returnReport


def processMaterials(sel):
    returnReport = [[], [], []]

    shape = cmds.listRelatives(sel, shapes=True, fullPath=True)
    shadingEngine = cmds.listConnections(shape, type="shadingEngine")
    materials = []
    for each in shadingEngine:
        conn = cmds.listConnections(each)
        mat = cmds.ls(conn, materials=True)
        mat = mat[0]
        if mat not in materials:
            materials.append(mat)

    if materials:
        cmds.text("materials_TX", e=True, l=len(materials))
        if len(materials) > 1:
            warning = "Mesh has more than one material"
            if warning not in returnReport[0]:
                returnReport[0].append(warning)
        defMatNames = ["lambert", "phong", "blinn", "Stingray"]
        for each in materials:
            for name in defMatNames:
                if name in each:
                    warning = "One or more materials may have a default name"
                    if warning not in returnReport[0]:
                        returnReport[0].append(warning)

    return returnReport


def processCleanup(sel):
    returnReport = [[], [], []]

    nonManifoldEdges = cmds.polyInfo(sel, nme=True)
    nonManifoldUvEdges = cmds.polyInfo(sel, nue=True)
    nonManifoldUvs = cmds.polyInfo(sel, nuv=True)
    laminaFaces = cmds.polyInfo(sel, lf=True)
    invalidEdges = cmds.polyInfo(sel, ie=True)
    invalidVertices = cmds.polyInfo(sel, iv=True)

    if nonManifoldEdges is not None:
        warning = "One or more edges are nonmanifold"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("nonmanifoldEdges_TX", e=True, l=len(nonManifoldEdges))
        cmds.button("nonmanifoldEdgesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, nonManifoldEdges, "none"))
    else:
        cmds.button("nonmanifoldEdgesSelect_BUT", e=True, bgc=passColor)
        cmds.text("nonmanifoldEdges_TX", e=True, l="None")

    if nonManifoldUvEdges is not None:
        warning = "One or more UV edges are nonmanifold"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("nonmanifoldUvEdges_TX", e=True, l=len(nonManifoldUvEdges))
        cmds.button("nonmanifoldUvEdgesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, nonManifoldUvEdges, "none"))
    else:
        cmds.button("nonmanifoldUvEdgesSelect_BUT", e=True, bgc=passColor)
        cmds.text("nonmanifoldUvEdges_TX", e=True, l="None")

    if nonManifoldUvs is not None:
        warning = "One of more UV points are nonmanifold"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("nonmanifoldUvs_TX", e=True, l=len(nonManifoldUvs))
        cmds.button("nonmanifoldUvsSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, nonManifoldUvs, "none"))
    else:
        cmds.button("nonmanifoldUvsSelect_BUT", e=True, bgc=passColor)
        cmds.text("nonmanifoldUvs_TX", e=True, l="None")

    if laminaFaces is not None:
        warning = "One or more faces share all edges (lamina)"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("laminaFaces_TX", e=True, l=len(laminaFaces))
        cmds.button("laminaFacesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, laminaFaces, "none"))
    else:
        cmds.button("laminaFacesSelect_BUT", e=True, bgc=passColor)
        cmds.text("laminaFaces_TX", e=True, l="None")

    if invalidEdges is not None:
        warning = "One or more edges have no face association (invalid)"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("invalidEdges_TX", e=True, l=len(invalidEdges))
        cmds.button("invalidEdgesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, invalidEdges, "none"))
    else:
        cmds.button("invalidEdgesSelect_BUT", e=True, bgc=passColor)
        cmds.text("invalidEdges_TX", e=True, l="None")

    if invalidVertices is not None:
        warning = "One or more vertices have no face association (invalid)"
        if warning not in returnReport[2]:
            returnReport[2].append(warning)
        cmds.text("invalidVertices_TX", e=True, l=len(invalidVertices))
        cmds.button("invalidVerticesSelect_BUT", e=True, bgc=errorColor, c=lambda args: selectComponent(sel, invalidVertices, "none"))
    else:
        cmds.button("invalidVerticesSelect_BUT", e=True, bgc=passColor)
        cmds.text("invalidVertices_TX", e=True, l="None")

    return returnReport


def clearLayoutChildren(layout):
    children = cmds.layout(layout, q=True, ca=True)
    if children is not None:
        for each in children:
            cmds.deleteUI(each)
        cmds.window("jbPrWin", e=True, h=1)


def selectComponent(sel, comp, convert):
    cmds.select(clear=True)
    if len(comp) == 0:
        cmds.select(sel, r=True)
        return None

    if convert == "none":
        comp = comp
    elif convert == "faceToVertex":
        for each in comp:
            vtxFaces = cmds.polyListComponentConversion(each, tv=True)
            vtxFaces = cmds.ls(vtxFaces, flatten=True)
        comp = vtxFaces

    cmds.select(clear=True)
    cmds.hilite(sel, r=True)
    for each in comp:
        cmds.select(each, add=True)
