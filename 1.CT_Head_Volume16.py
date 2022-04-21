import vtk

dataLocation = './data/headsq/half'

vtkColors = vtk.vtkNamedColors()

vtkColors.SetColor('SkinColor', [240, 184, 160, 255])
vtkColors.SetColor('BackfaceColor', [255, 229, 200, 255])
vtkColors.SetColor('BkgColor', [51, 77, 102, 255])

renderer = vtk.vtkRenderer()
renderingWindow = vtk.vtkRenderWindow()
renderingWindow.AddRenderer(renderer)

renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderingWindow)

####################
# The following v16 is used to read a series of
# 2D slices (images) that make up the volume.
# Set slice size and pixel spacing. The data endian must also be specified.
# v16 Use FilePrefix in conjunction with slice numbering
# to construct filenames in FilePrefix.%d format.
# (In this case, FilePrefix is the root name of the file: quarter/half.)
####################

v16DataReader = vtk.vtkVolume16Reader()
v16DataReader.SetDataDimensions (128, 128)
v16DataReader.SetImageRange (1, 93)
v16DataReader.SetDataByteOrderToLittleEndian()
v16DataReader.SetFilePrefix (dataLocation)
v16DataReader.SetDataSpacing (3.2, 3.2, 2.8)

####################
# A known contour or contour value of 500 corresponds to the patient's skin.
# Triangle stripper is used to create triangle strips from isosurfaces,
# These triangle strips render faster on many systems.
####################

skinExtractor = vtk.vtkFlyingEdges3D()

skinExtractor.SetInputConnection(v16DataReader.GetOutputPort())
skinExtractor.SetValue(0, 500)

skinStripper = vtk.vtkStripper()
skinStripper.SetInputConnection(skinExtractor.GetOutputPort())

skinMapper = vtk.vtkPolyDataMapper()
skinMapper.SetInputConnection(skinStripper.GetOutputPort())
skinMapper.ScalarVisibilityOff()

skinActor = vtk.vtkActor()
skinActor.SetMapper(skinMapper)
skinActor.GetProperty().SetDiffuseColor(vtkColors.GetColor3d('SkinColor'))
skinActor.GetProperty().SetSpecular(0.3)
skinActor.GetProperty().SetSpecularPower(20)
skinActor.GetProperty().SetOpacity(0.1)

backProperty = vtk.vtkProperty()
backProperty.SetDiffuseColor(vtkColors.GetColor3d('BackfaceColor'))
skinActor.SetBackfaceProperty(backProperty)

boneExtractor = vtk.vtkFlyingEdges3D()

boneExtractor.SetInputConnection(v16DataReader.GetOutputPort())
boneExtractor.SetValue(0, 1150)

boneStripper = vtk.vtkStripper()
boneStripper.SetInputConnection(boneExtractor.GetOutputPort())

boneMapper = vtk.vtkPolyDataMapper()
boneMapper.SetInputConnection(boneStripper.GetOutputPort())
boneMapper.ScalarVisibilityOff()

boneActor = vtk.vtkActor()
boneActor.SetMapper(boneMapper)
boneActor.GetProperty().SetDiffuseColor(vtkColors.GetColor3d('Ivory'))
boneActor.GetProperty().SetOpacity(0.1)

outlineDataFilter = vtk.vtkOutlineFilter()
outlineDataFilter.SetInputConnection(v16DataReader.GetOutputPort())

####################
# Now, we create three orthogonal planes that go through the volume.
# Each plane uses a different texture map and therefore has a different color.
####################

# First create a black and white lookup table.
bwLookupTable = vtk.vtkLookupTable()
bwLookupTable.SetTableRange(0, 2000)
bwLookupTable.SetSaturationRange(0, 0)
bwLookupTable.SetHueRange(0, 0)
bwLookupTable.SetValueRange(0, 1)
bwLookupTable.Build() # effect establishment

# Now create a lookup table that contains the full hue circle (from HSV).
hueLookupTable = vtk.vtkLookupTable()
hueLookupTable.SetTableRange(0, 2000)
hueLookupTable.SetHueRange(0, 1)
hueLookupTable.SetSaturationRange(1, 1)
hueLookupTable.SetValueRange(1, 1)
hueLookupTable.Build() # effect establishment

# Finally, create a lookup table hue with a single hue
# but within the saturation range.
satLookupTable = vtk.vtkLookupTable()
satLookupTable.SetTableRange(0, 2000)
satLookupTable.SetHueRange(0.6, 0.6)
satLookupTable.SetSaturationRange(0, 1)
satLookupTable.SetValueRange(1, 1)
satLookupTable.Build() # effect establishment

####################
# Create the first of the three planes.
# The filter vtkImageMapToColors maps the data through
# the corresponding lookup table created above.
####################

vtkImageMapperColors = vtk.vtkImageMapToColors()
vtkImageMapperColors.SetInputConnection(v16DataReader.GetOutputPort())
vtkImageMapperColors.SetLookupTable(bwLookupTable)
vtkImageMapperColors.Update()

sagittal = vtk.vtkImageActor()
sagittal.GetMapper().SetInputConnection(vtkImageMapperColors.GetOutputPort())
sagittal.SetDisplayExtent(64, 64, 0, 128, 0, 92)
sagittal.ForceOpaqueOn()

# Create the third (coronal) plane of the three planes.
# We use the same method as before, except the scope is different.
coronalColors = vtk.vtkImageMapToColors()
coronalColors.SetInputConnection(v16DataReader.GetOutputPort())
coronalColors.SetLookupTable(satLookupTable)
coronalColors.Update()

coronal = vtk.vtkImageActor()
coronal.GetMapper().SetInputConnection(coronalColors.GetOutputPort())
coronal.SetDisplayExtent(0, 128, 64, 64, 0, 92)
coronal.ForceOpaqueOn()

#Set a camera to see in specific direction where we need
vtkCamera = vtk.vtkCamera()
vtkCamera.SetViewUp(0, 0, -1)
vtkCamera.SetPosition(0, -1, 0)
vtkCamera.SetFocalPoint(0, 0, 0)
vtkCamera.ComputeViewPlaneNormal()
vtkCamera.Azimuth(30.0)
vtkCamera.Elevation(30.0)

outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outlineDataFilter.GetOutputPort())

outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(vtkColors.GetColor3d('Black'))

renderer.AddActor(outlineActor)

axialColors = vtk.vtkImageMapToColors()
axialColors.SetInputConnection(v16DataReader.GetOutputPort())
axialColors.SetLookupTable(hueLookupTable)
axialColors.Update()

axialActor = vtk.vtkImageActor()
axialActor.GetMapper().SetInputConnection(axialColors.GetOutputPort())
axialActor.SetDisplayExtent(0, 128, 0, 128, 10, 10)
axialActor.ForceOpaqueOn()
renderer.AddActor(axialActor)
    
renderer.AddActor(skinActor)
renderer.AddActor(boneActor)
renderer.SetActiveCamera(vtkCamera)
renderer.ResetCamera()
vtkCamera.Dolly(1.5)

####################
# Set the background color of the renderer and
# set the size of the render window (in pixels).
####################

renderer.SetBackground(vtkColors.GetColor3d('BkgColor'))
renderingWindow.SetSize(640, 480)
renderingWindow.SetWindowName('Project3-1')

####################
# Note that when there is camera movement (as with the Dolly() method),
# the clipping plane will usually need to be adjusted.
# The clipping plane consists of two planes: near and
# far along the view direction.
# The near plane clips objects in front of the plane,
# and the far plane clips objects behind the plane.
# This way, only what is drawn between the planes is actually rendered.
####################

renderer.ResetCameraClippingRange()
####################
# scroll bar section
####################

def vtkSliderCallback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pos = sliderRepres.GetValue()
    axialActor.SetDisplayExtent(0, 128, 0, 128, int(pos), int(pos))
    SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
    SliderRepres.GetPoint1Coordinate().SetValue(0.1, 0.05)
    SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
    SliderRepres.GetPoint2Coordinate().SetValue(0.9, 0.05)

SliderRepres = vtk.vtkSliderRepresentation3D()

minimumData = 0
maximumData = 92
SliderRepres.SetMinimumValue(minimumData)
SliderRepres.SetMaximumValue(maximumData)
SliderRepres.SetValue((minimumData + maximumData) / 2)
SliderRepres.SetTitleText('Slice')

SliderRepres.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint1Coordinate().SetValue(0.1, 0.05)
SliderRepres.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
SliderRepres.GetPoint2Coordinate().SetValue(0.9, 0.05)

times = 2

SliderRepres.SetSliderLength(0.02 * times)
SliderRepres.SetSliderWidth(0.03 * times)
SliderRepres.SetEndCapLength(0.01 * times)
SliderRepres.SetEndCapWidth(0.03 * times)
SliderRepres.SetTubeWidth(0.005 * times)
SliderRepres.SetLabelFormat('%3.0lf')
SliderRepres.SetTitleHeight(0.02 * times)
SliderRepres.SetLabelHeight(0.02 * times)

SliderWidget = vtk.vtkSliderWidget()
SliderWidget.SetInteractor(renderWindowInteractor)
SliderWidget.SetEnabled(True)
SliderWidget.SetRepresentation(SliderRepres)
SliderWidget.KeyPressActivationOff()
SliderWidget.SetAnimationModeToAnimate()

SliderWidget.AddObserver('InteractionEvent', vtkSliderCallback)

renderWindowInteractor.Initialize()
renderWindowInteractor.Start()